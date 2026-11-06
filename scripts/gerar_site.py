"""Gera site/index.html a partir de dados/site_data.json (rodar de novo quando chegar ata nova)."""
import json
from pathlib import Path
B = Path(__file__).resolve().parents[1]
d = json.dumps(json.load(open(B/"dados"/"site_data.json")), ensure_ascii=False).replace("</", "<\\/")
html = (B/"site"/"template.html").read_text().replace("/*DATA*/null", d)
(B/"site"/"index.html").write_text(html); print("site/index.html", len(html)//1024, "KB")
