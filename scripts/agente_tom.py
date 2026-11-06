"""Agente de tom do Copom.
Lê cada ata (dados/paragrafos.json), monta o prompt a partir de config/parametros.json
e classifica cada parágrafo: nota, tema, trecho exato e justificativa.

Modos:
  python scripts/agente_tom.py --prompts        # gera prompts/ata_<n>.md (para rodar no Claude Code, sem chave)
  python scripts/agente_tom.py --api            # roda direto na API (precisa ANTHROPIC_API_KEY)
  python scripts/agente_tom.py --conferir       # confere os JSON em dados/tom_agente/ (trechos existem? notas válidas?)
Saída: dados/tom_agente/ata_<n>.json = [{"n":1,"nota":0,"tema":"...","trecho":"...","justificativa":"..."}]"""
import json, re, sys, os
from pathlib import Path
B = Path(__file__).resolve().parents[1]
P = json.load(open(B/"config"/"parametros.json"))
ATAS = json.load(open(B/"dados"/"paragrafos.json"))
SAIDA = B/"dados"/"tom_agente"; SAIDA.mkdir(parents=True, exist_ok=True)
ss = lambda s: re.sub(r"\s+", "", s)

def prompt(r):
    a = ATAS[r]
    regua = "\n".join(f"{k:>3} = {v['nome']}: {v['quando']}" for k, v in P["regua"].items())
    pars = "\n\n".join(f"§{n} [seção {p['secao'][0]}] {p['texto']}" for n, p in a["paragrafos"].items())
    return f"""Você é um economista que analisa a comunicação do Banco Central do Brasil.
Classifique o TOM de política monetária de CADA parágrafo da ata da {r}ª reunião do Copom ({a['data_reuniao']}).

RÉGUA (nota inteira de -2 a +2):
{regua}

Regras:
- Avalie o que o parágrafo SINALIZA sobre juros, não o tema em si. Parágrafo só descritivo = 0.
- Se o parágrafo mistura sinais, dê a nota do sinal dominante e diga isso na justificativa.
- "trecho": copie LITERALMENTE de 6 a 25 palavras do parágrafo que sustentam a nota (sem reticências, sem mudar palavras).
- "tema": um de {P['temas']}.
- "justificativa": até 20 palavras, com suas palavras.

Responda APENAS com um array JSON, um objeto por parágrafo, na ordem:
[{{"n": 1, "nota": 0, "tema": "...", "trecho": "...", "justificativa": "..."}}]

ATA {r}ª:
{pars}
"""

def conferir():
    ok = True
    for r in sorted(ATAS):
        f = SAIDA/f"ata_{r}.json"
        if not f.exists(): print(r, "FALTANDO"); ok = False; continue
        arr = json.load(open(f)); ns = {str(o["n"]) for o in arr}
        faltam = set(ATAS[r]["paragrafos"]) - ns
        ruins = [o["n"] for o in arr if ss(o["trecho"]) not in ss(ATAS[r]["paragrafos"][str(o["n"])]["texto"])]
        notas = [o["nota"] for o in arr if o["nota"] not in (-2, -1, 0, 1, 2)]
        print(f"{r}: {len(arr)} classificados | sem nota: {sorted(faltam, key=int)} | trechos não encontrados: {ruins} | notas inválidas: {notas}")
        ok &= not (faltam or ruins or notas)
    print("TUDO CONFERIDO" if ok else "HÁ PROBLEMAS"); return ok

if __name__ == "__main__":
    if "--prompts" in sys.argv:
        (B/"prompts").mkdir(exist_ok=True)
        for r in ATAS: (B/"prompts"/f"ata_{r}.md").write_text(prompt(r))
        print("prompts gerados em prompts/")
    elif "--api" in sys.argv:
        from anthropic import Anthropic
        cli = Anthropic()
        for r in ATAS:
            txt = cli.messages.create(model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5"), max_tokens=8000,
                                      messages=[{"role": "user", "content": prompt(r)}]).content[0].text
            txt = txt[txt.find("["): txt.rfind("]") + 1]
            (SAIDA/f"ata_{r}.json").write_text(txt); print(r, "ok")
        conferir()
    else:
        conferir()
