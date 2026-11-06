"""Extrai as atas do Copom em parágrafos com a NUMERAÇÃO OFICIAL da ata (1., 2., ...),
removendo cabeçalhos de página, notas de rodapé e a Tabela 1.
Saída: dados/paragrafos.json  {reuniao: {data, secoes, paragrafos: {n: texto}}}"""
import json, re, sys
from pathlib import Path
from pypdf import PdfReader

BASE = Path(__file__).resolve().parents[1]
ATAS = BASE / "dados" / "atas"

def limpar_pagina(t):
    # cabeçalho repetido: "281ª Reunião\nCOPOM\n15 e 16 de setembro\n4 bcb.gov.br"
    t = re.sub(r"^.*?\d+\s+bcb\.gov\.br\s*\n", "", t, count=1, flags=re.S)
    # nota de rodapé: linha em branco seguida de "1 A menos..." até o fim da página
    t = re.sub(r"\n\s*\n\d \S.*$", "", t, flags=re.S)
    return t

def extrair(pdf):
    paginas = [limpar_pagina(p.extract_text() or "") for p in PdfReader(pdf).pages]
    texto = "\n".join(paginas)
    ini = re.search(r"A\)\s*Atualiza", texto)
    fim = re.search(r"\n\s*Tabela 1", texto)
    texto = texto[ini.start(): fim.start() if fim else None]
    texto = re.sub(r"(Copom)\d\b", r"\1", texto)            # marca de nota de rodapé
    secoes, pars, sec_atual = {}, {}, None
    for bloco in re.split(r"\n(?=\s*(?:[A-E]\)\s|\d{1,2}\.\s))", texto):
        b = bloco.strip()
        m = re.match(r"([A-E])\)\s*([^\n]+)\n?(.*)", b, flags=re.S)
        if m:
            sec_atual = f"{m.group(1)}) {m.group(2).strip()}"
            b = m.group(3).strip()
            if not b: continue
        m = re.match(r"(\d{1,2})\.\s+(.*)", b, flags=re.S)
        if not m: continue
        n = int(m.group(1)); corpo = re.sub(r"\s+", " ", m.group(2)).strip()
        corpo = re.sub(r"(\w) -(se|lo|la|los|las)\b", r"\1-\2", corpo)
        pars[n] = corpo; secoes[n] = sec_atual
    return pars, secoes

if __name__ == "__main__":
    saida = {}
    for pdf in sorted(ATAS.glob("ata_*.pdf")):
        r, d = re.match(r"ata_(\d+)_(\d{4}-\d{2}-\d{2})", pdf.stem).groups()
        pars, secs = extrair(pdf)
        ns = sorted(pars)
        assert ns == list(range(1, len(ns)+1)), (pdf.name, ns)
        saida[r] = {"data_reuniao": d, "arquivo": pdf.name,
                    "paragrafos": {str(n): {"secao": secs[n], "texto": pars[n]} for n in ns}}
        print(pdf.name, len(ns), "parágrafos")
    (BASE / "dados" / "paragrafos.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1))
