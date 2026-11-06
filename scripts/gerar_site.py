"""Gera o site a partir de dados/site_data.json (rodar de novo quando chegar ata nova).

site/index.html     página completa, para abrir no navegador ou hospedar em qualquer lugar
site/artifact.html  mesma página sem <html>/<head>/<body>, no formato que o artefato do claude.ai espera
                    (o claude.ai acrescenta o esqueleto do documento ao publicar)"""
import json, re
from pathlib import Path
B = Path(__file__).resolve().parents[1]
d = json.dumps(json.load(open(B/"dados"/"site_data.json")), ensure_ascii=False).replace("</", "<\\/")
html = (B/"site"/"template.html").read_text().replace("/*DATA*/null", d)
(B/"site"/"index.html").write_text(html); print("site/index.html", len(html)//1024, "KB")

art = re.sub(r"<!DOCTYPE html>\s*|<html[^>]*>\s*|</?head>\s*|</?body>\s*|</html>\s*", "", html)
art = re.sub(r'<meta charset="utf-8">\s*|<meta name="viewport"[^>]*>\s*', "", art)
(B/"site"/"artifact.html").write_text(art); print("site/artifact.html", len(art)//1024, "KB")
