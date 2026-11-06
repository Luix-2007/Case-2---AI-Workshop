"""Calcula o índice de tom de cada ata a partir da classificação do agente (dados/tom_agente/)
e das regras de agregação em config/parametros.json. Compara com a leitura do revisor
(scripts/classificacao_revisor.py) para medir concordância."""
import json, re
from pathlib import Path
from classificacao_revisor import C as REV
B = Path(__file__).resolve().parents[1]
P = json.load(open(B/"config"/"parametros.json"))["agregacao"]
atas = json.load(open(B/"dados"/"paragrafos.json"))
ss = lambda s: re.sub(r"\s+", "", s)

def indice(pars):
    num = den = 0
    for p in pars.values():
        if P["ignorar_neutros"] and p["nota"] == 0: continue
        w = P["peso_por_secao"][p["secao"][0]]; num += w * p["nota"]; den += w
    return round(num / den, 2) if den else 0.0

iguais = perto = tot = 0; disc = []
for r, a in atas.items():
    ag = {str(o["n"]): o for o in json.load(open(B/"dados"/"tom_agente"/f"ata_{r}.json"))}
    for n, p in a["paragrafos"].items():
        o = ag[n]; assert ss(o["trecho"]) in ss(p["texto"]), (r, n)
        p.update(nota=int(o["nota"]), tema=o["tema"], trecho=o["trecho"], justificativa=o.get("justificativa", ""))
        rv = REV[(int(r), int(n))][0]; p["nota_revisor"] = rv
        tot += 1; iguais += rv == p["nota"]; perto += abs(rv - p["nota"]) <= 1
        if abs(rv - p["nota"]) >= 1: disc.append((r, n, p["nota"], rv))
    notas = [p["nota"] for p in a["paragrafos"].values()]
    a["indice"] = indice(a["paragrafos"])
    a["indice_revisor"] = indice({k: {**v, "nota": v["nota_revisor"]} for k, v in a["paragrafos"].items()})
    a["media_simples"] = round(sum(notas) / len(notas), 2)
    a["n_duros"] = sum(x > 0 for x in notas); a["n_brandos"] = sum(x < 0 for x in notas)
    print(f"{r}: agente {a['indice']:+.2f} | revisor {a['indice_revisor']:+.2f} | média simples {a['media_simples']:+.2f}")
conc = {"total": tot, "iguais": iguais, "ate_1_ponto": perto, "discordancias": disc}
print(f"concordância exata {iguais}/{tot} = {iguais/tot:.0%} | até 1 ponto {perto}/{tot} = {perto/tot:.0%}")
json.dump({"atas": atas, "concordancia": conc, "agregacao": P}, open(B/"dados"/"tom.json", "w"), ensure_ascii=False, indent=1)
