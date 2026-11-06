"""Baixa a Selic meta (SGS 432) e as expectativas do Focus para a Selic direto do Banco Central,
com a biblioteca python-bcb (equivalente ao rbcb do R). Rode no seu computador:

    pip install python-bcb pandas
    python scripts/dados_bcb.py

Gera dados/selic_meta.csv e dados/focus_selic.csv, que o gerar_site.py usa."""
from pathlib import Path
from bcb import sgs, Expectativas

B = Path(__file__).resolve().parents[1] / "dados"
INICIO = "2026-01-01"

selic = sgs.get({"selic_meta": 432}, start=INICIO)
selic.to_csv(B / "selic_meta.csv")
print("Selic meta:", len(selic), "dias; última:", selic.iloc[-1, 0])

em = Expectativas()
ep = em.get_endpoint("ExpectativasMercadoAnuais")
focus = (ep.query()
         .filter(ep.Indicador == "Selic", ep.Data >= INICIO)
         .filter(ep.baseCalculo == 0)
         .select(ep.Data, ep.DataReferencia, ep.Mediana, ep.numeroRespondentes)
         .collect())
focus = focus[focus["DataReferencia"].astype(str).isin(["2026", "2027"])].sort_values("Data")
focus.to_csv(B / "focus_selic.csv", index=False)
print("Focus Selic:", len(focus), "linhas; última data:", focus["Data"].max())
