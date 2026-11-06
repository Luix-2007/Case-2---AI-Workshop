"""Junta índice, mudanças, impacto, Selic e Focus num JSON único que alimenta o site.
Confere: todo trecho citado nas mudanças existe na ata; seções C/D 280 vs 281 iguais."""
import json, re, difflib
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
T = json.load(open(BASE / "dados" / "tom.json")); tom = T["atas"]
ss = lambda s: re.sub(r"\s+", "", s)
def tem(r, n, t):
    assert ss(t) in ss(tom[str(r)]["paragrafos"][str(n)]["texto"]), (r, n, t); return t

mudancas = [
 {"titulo": "Expectativas: a desancoragem deixou de ser “adicional”", "efeito": "suavizou",
  "antes": {"reuniao": 280, "par": 9, "trecho": tem(280, 9, "monitora com atenção a desancoragem adicional das expectativas de inflação para prazos mais longos")},
  "depois": {"reuniao": 281, "par": 10, "trecho": tem(281, 10, "monitora com atenção a desancoragem das expectativas de inflação para prazos mais longos")},
  "nota": None, "ref": [(280, 9), (281, 10)],
  "leitura": "O BC tirou uma palavra que vinha desde abril (278ª). Continua vendo expectativas acima da meta, mas parou de dizer que a piora está aumentando."},
 {"titulo": "Inflação ao consumidor voltou para baixo do teto", "efeito": "suavizou",
  "antes": {"reuniao": 280, "par": 2, "trecho": tem(280, 2, "a inflação cheia desacelerou, porém ainda acima do limite superior da meta")},
  "depois": {"reuniao": 281, "par": 2, "trecho": tem(281, 2, "situando-se abaixo do limite superior do intervalo de tolerância, porém ainda acima da meta")},
  "nota": None, "ref": [(280, 2), (281, 2)],
  "leitura": "Em agosto só os núcleos estavam abaixo do teto de 4,5%. Em setembro o índice cheio também está. A inflação segue acima do centro da meta de 3%."},
 {"titulo": "Parágrafo novo: o crédito já está esfriando", "efeito": "suavizou",
  "antes": None,
  "depois": {"reuniao": 281, "par": 6, "trecho": tem(281, 6, "consistente com um quadro de desaceleração do crescimento, em meio a uma política monetária restritiva")},
  "nota": None, "ref": [None, (281, 6)],
  "leitura": "O Copom acrescentou evidência de que os juros altos estão chegando ao crédito livre de prazo mais longo, o canal mais sensível à Selic."},
]
contraponto = {"titulo": "Contraponto: preços ao produtor voltaram a subir", "efeito": "endureceu",
  "antes": {"reuniao": 280, "par": 8, "trecho": tem(280, 8, "os preços aos produtores recuaram")},
  "depois": {"reuniao": 281, "par": 9, "trecho": tem(281, 9, "as variações de preços aos produtores aceleraram")},
  "nota": None, "ref": [(280, 8), (281, 9)]}

def nt(rn): return "novo" if rn is None else (lambda v: ("+" if v > 0 else "−" if v < 0 else "") + str(abs(v)))(tom[str(rn[0])]["paragrafos"][str(rn[1])]["nota"])
for m in mudancas + [contraponto]:
    a, b = m.pop("ref"); m["nota"] = f"{nt(a)} → {nt(b)}"
    va = 0 if a is None else tom[str(a[0])]["paragrafos"][str(a[1])]["nota"]; vb = tom[str(b[0])]["paragrafos"][str(b[1])]["nota"]
    if a is not None and va == vb: m["efeito"] += ", nota igual"
    print(m["titulo"][:40], m["nota"])
# seções C e D: quanto mudou?
p80, p81 = tom["280"]["paragrafos"], tom["281"]["paragrafos"]
pares = [(14, 15), (15, 16), (16, 17), (18, 19)]
sim = {f"280 §{a} → 281 §{b}": round(difflib.SequenceMatcher(None, p80[str(a)]["texto"], p81[str(b)]["texto"]).ratio(), 3) for a, b in pares}
print("similaridade orientação:", sim)
inalterado = {"pares": sim, "trecho": tem(281, 17, "a magnitude do ciclo de calibração será ajustada à luz da evolução do cenário")}

selic = [  # meta Selic: decisões das próprias atas (parágrafo de decisão)
 {"reuniao": 276, "data": "2026-01-28", "selic": 15.00, "decisao": "manteve"},
 {"reuniao": 277, "data": "2026-03-18", "selic": 14.75, "decisao": "−0,25"},
 {"reuniao": 278, "data": "2026-04-29", "selic": 14.50, "decisao": "−0,25"},
 {"reuniao": 279, "data": "2026-06-17", "selic": 14.25, "decisao": "−0,25"},
 {"reuniao": 280, "data": "2026-08-05", "selic": 14.00, "decisao": "−0,25"},
 {"reuniao": 281, "data": "2026-09-16", "selic": 13.75, "decisao": "−0,25"}]
for s in selic:
    tem(s["reuniao"], max(int(k) for k in tom[str(s["reuniao"])]["paragrafos"]) - 1 if s["reuniao"] in (277,278) else
        {276:17,279:23,280:17,281:18}[s["reuniao"]], f"{s['selic']:.2f}".replace(".", ",") + "% a.a.") if s["reuniao"] not in (277,278) else None
tem(277, 16, "14,75% a.a."); tem(278, 16, "14,50% a.a.")

focus_noticias = [  # mediana Focus: Selic no FIM DE 2026 (não é a próxima reunião). Fonte: notícias que citam o boletim.
 {"data": "2026-02-02", "v": 12.25, "fonte": "https://bpmoney.com.br/?p=391870"},
 {"data": "2026-03-02", "v": 12.00, "fonte": "https://economicnewsbrasil.com.br/2026/03/02/boletim-focus-dolar-selic-2026/"},
 {"data": "2026-05-18", "v": 13.25, "fonte": "https://www.infomoney.com.br/economia/boletim-focus-projecoes-18052026/"},
 {"data": "2026-06-08", "v": 13.50, "fonte": "https://www.poder360.com.br/poder-economia/mercado-eleva-projecao-da-selic-para-135-em-2026/"},
 {"data": "2026-06-22", "v": 14.00, "fonte": "https://www.suno.com.br/noticias/expectativa-para-a-selic-no-fim-de-2026-22062026-go/"},
 {"data": "2026-07-20", "v": 14.00, "fonte": "https://www.dgabc.com.br/Noticia/4336199/selic-no-fim-de-2026-segue-em-14-00-pela-quarta-semana-seguida-aponta-focus"},
 {"data": "2026-08-03", "v": 13.75, "fonte": "https://www.opovo.com.br/noticias/economia/2026/08/03/selic-no-fim-de-2026-cai-de-14-para-1375-calcula-focus.html"},
 {"data": "2026-08-24", "v": 13.75, "fonte": "https://diariodocomercio.com.br/economia/selic-focus-projecoes-juros/"},
 {"data": "2026-09-08", "v": 13.75, "fonte": "https://www.jornaldocomercio.com/economia/2026/09/1262567-selic-no-fim-de-2026-continua-em-1375-pela-quinta-semana-seguida-aponta-focus.html"},
 {"data": "2026-09-21", "v": 13.50, "fonte": "https://timesbrasil.com.br/brasil/economia-brasileira/selic-13-50-boletim-focus-2026/"},
 {"data": "2026-10-13", "v": 13.25, "fonte": "https://rankia.com.br/proxima-reuniao-copom/"},
 {"data": "2026-11-03", "v": 13.50, "fonte": "https://www.diariodepernambuco.com.br/economia/2026/11/11728218-expectativa-para-a-selic-no-fim-de-2026-sobe-de-1325-para-1350.html"}]

# Focus oficial (python-bcb) se existir; senão, pontos de notícias que citam o boletim
import csv
fcsv = BASE / "dados" / "focus_selic.csv"
if fcsv.exists():
    rows = [r for r in csv.DictReader(open(fcsv)) if str(r["DataReferencia"]) == "2026"]
    focus = [{"data": r["Data"][:10], "v": float(r["Mediana"]), "fonte": "BCB/Olinda (python-bcb)"} for r in rows]
    focus_origem = "oficial"
else:
    focus, focus_origem = focus_noticias, "noticias"
print("Focus:", focus_origem, len(focus), "pontos")

impacto = {
 "manchete": "Sinal de cortes graduais, sem pressa e sem pausa anunciada",
 "texto": [
  "A 281ª ata suavizou o diagnóstico: inflação ao consumidor abaixo do teto, desaceleração confirmada pelo PIB e pelo crédito, e a desancoragem das expectativas deixou de ser “adicional”. Mas as seções de discussão e decisão (C e D) ficaram praticamente iguais às de agosto. A leitura é de continuidade do ritmo de 0,25 ponto por reunião, sem sinal de aceleração.",
  "Para os juros futuros curtos, isso pode sustentar a aposta em mais cortes. O mercado já ia nessa direção: a mediana do Focus para a Selic no fim de 2026 caiu de 13,75% (08/09) para 13,50% (21/09, um dia antes da ata, após o comunicado) e para 13,25% em 13/10.",
  "O risco está escrito na própria ata: câmbio “persistentemente mais depreciado” é um dos riscos de alta (§13). Depois da alta do dólar pós-eleição, as opções de Copom da B3 passaram a indicar cerca de 63% de chance de pausa em 4/11 (fechamento de 26/10), e o Focus voltou a 13,50% (dados de 30/10). Na 282ª reunião, em 04/11, o Copom de fato manteve a Selic em 13,75%, interrompendo os cortes (comunicado do BC). A ata dessa reunião, esperada para 10/11 (padrão de 6 dias após a reunião), dirá o quanto o tom endureceu."],
 "risco_trecho": tem(281, 13, "por meio de uma taxa de câmbio persistentemente mais depreciada"),
 "fontes": ["https://rankia.com.br/copom-4-novembro-selic-manutencao-63-opcoes-b3/",
            "https://www.bcb.gov.br/publicacoes/comunicadoscopom"]}

saida = {"atas": tom, "concordancia": T["concordancia"], "agregacao": T["agregacao"], "focus_origem": focus_origem, "mudancas": mudancas, "contraponto": contraponto, "inalterado": inalterado,
         "selic": selic, "focus": focus, "impacto": impacto,
         "ata_publicada": {"279": "2026-06-23", "280": "2026-08-11", "281": "2026-09-22", "282": "2026-11-10"}}
json.dump(saida, open(BASE / "dados" / "site_data.json", "w"), ensure_ascii=False)
print("ok", len(json.dumps(saida, ensure_ascii=False)) // 1024, "KB")
