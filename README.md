# Tradutor do Copom — Case 2

> Claude Lab · Economia & Finanças · PUC-Rio · 06/11/2026

**🎬 Vídeo (2 min):** [PREENCHER]
**🔗 Artefato público:** https://claude.ai/artifact/LB7jNVrtXFB8NjuukvTzAq

## Equipe

| Nome | Curso / período | Papel no projeto | LinkedIn / GitHub |
|---|---|---|---|
| [PREENCHER] | | | |
| | | | |
| | | | |
| | | | |

## O problema

No dia em que o Copom publica uma ata, o economista-chefe de um banco precisa saber em poucos minutos três coisas: se o Banco Central ficou mais duro ou mais brando, o que mudou em relação à ata anterior e o que isso pode significar para os juros. As atas são longas e quase iguais entre si. A diferença costuma estar em poucas palavras.

## A solução

Um site que lê as atas do Copom e mostra:

1. **Veredito e termômetro**: o índice de tom da ata mais recente, de −2 (muito brando) a +2 (muito duro), comparado com a ata anterior.
2. **Evolução**: o índice das 6 atas de 2026 (276ª a 281ª), com a Selic meta e a expectativa do Focus para a Selic no fim de 2026.
3. **O que mudou** da 280ª para a 281ª: as 3 mudanças mais relevantes, com o trecho exato antes e depois, e o efeito de cada uma no tom.
4. **Principal impacto**: o que a mudança sinaliza para a Selic, os juros futuros, o câmbio e o crédito, em linguagem condicional.
5. **Evidências**: cada parágrafo de cada ata, com a nota, o tema, o trecho que sustenta a nota e a justificativa.
6. **Pergunte às atas**: um chat único que conhece as 6 atas e responde citando reunião, parágrafo e trecho. O site confere automaticamente se cada trecho citado existe na ata. Também é possível subir uma ata nova (PDF ou texto) e medir o tom dela com a mesma régua.
7. **Como medimos**: a régua, a regra de agregação, a concordância com uma segunda leitura e um painel para testar outros pesos ao vivo.

## Como funciona

```
atas (PDF) ──► extrair.py ──► paragrafos.json   (numeração oficial dos parágrafos, sem cabeçalhos/rodapés)
                                   │
config/parametros.json ──► agente_tom.py ──► dados/tom_agente/ata_<n>.json   (nota, tema, trecho, justificativa)
                                   │                  └─ --conferir: todo trecho existe na ata?
                                   ▼
                              indice.py ──► tom.json   (índice por ata + concordância com o revisor)
                                   ▼
dados_bcb.py (Selic, Focus) ──► montar_dados.py ──► site_data.json ──► gerar_site.py ──► site/index.html
```

- **Agente de tom.** Um agente Claude por ata, rodando em paralelo. Cada um recebe a régua do `config/parametros.json` e classifica todos os parágrafos. Os prompts usados estão em `prompts/`.
- **Parâmetros.** A régua (o que vale cada nota) e a agregação (pesos por seção, ignorar neutros) ficam em `config/parametros.json`. Se a régua mudar, o agente roda de novo. Se só os pesos mudarem, basta recalcular o índice. O site também tem um painel para testar pesos na hora.

### Régua e agregação

| Nota | Significado | Exemplo nas atas |
|---|---|---|
| +2 | muito duro | "desancoragem adicional"; restrição "maior e por mais tempo" com ênfase |
| +1 | duro | riscos com "assimetria altista"; "serenidade e cautela" |
| 0 | neutro | premissas, números, procedimento, votação |
| −1 | brando | inflação cedendo; atividade e crédito desacelerando; corte de 0,25 |
| −2 | muito brando | "sinalizar o início de um ciclo de redução" (276ª) |

**Índice da ata** = média ponderada das notas, **ignorando parágrafos neutros**, com **peso 2 nas seções C (discussão) e D (decisão)** e peso 1 em A e B. Os neutros diluíam o sinal, e é nas seções C e D que o Copom sinaliza os próximos passos.

### Resultado

| Reunião | Data | Selic | Índice (agente) | Índice (revisor) |
|---|---|---|---|---|
| 276ª | 28/01/2026 | 15,00% (manteve) | −0,47 | −1,00 |
| 277ª | 18/03/2026 | 14,75% | +0,24 | +0,07 |
| 278ª | 29/04/2026 | 14,50% | +0,27 | +0,36 |
| 279ª | 17/06/2026 | 14,25% | +0,32 | +0,39 |
| 280ª | 05/08/2026 | 14,00% | +0,63 | +0,44 |
| 281ª | 16/09/2026 | 13,75% | +0,45 | +0,38 |

O tom ficou mais duro enquanto a Selic caía. O Copom cortou em todas as reuniões a partir de março, mas falando como quem quer manter os juros restritivos. A 276ª, com a Selic parada, foi a mais branda porque anunciou o início dos cortes. Mudança de tom não é mudança de juros.

## Dados usados

- **Atas do Copom** 276ª a 281ª (PDF), do repositório do workshop. Fonte: [Banco Central do Brasil](https://www.bcb.gov.br/publicacoes/atascopom). A data da reunião é diferente da data de publicação da ata (por exemplo, a 281ª reunião foi em 16/09 e a ata saiu em 22/09).
- **Selic meta**: o valor do parágrafo de decisão de cada ata (conferido por script). `scripts/dados_bcb.py` baixa a série 432 do SGS.
- **Focus**: mediana da Selic esperada para o **fim de 2026**, que não é a expectativa para a próxima reunião. `scripts/dados_bcb.py` baixa os dados oficiais com `python-bcb`. Enquanto o CSV oficial não for gerado, o site usa 12 pontos de notícias que citam o boletim (fontes listadas em `scripts/montar_dados.py` e no rodapé do site).

## Como verificamos os resultados

1. **Trechos existem?** `agente_tom.py --conferir` procura cada um dos 119 trechos citados no texto do parágrafo, ignorando espaços quebrados pelo PDF. Resultado: 119 de 119 encontrados. O chat faz a mesma conferência em cada resposta (✓ ou ⚠).
2. **Segunda leitura independente.** Um revisor classificou os 119 parágrafos sem ver as notas do agente (`scripts/classificacao_revisor.py`). As notas foram idênticas em 91 (76%) e diferiram em no máximo 1 ponto em 115 (97%). Os índices seguem a mesma tendência. As discordâncias se concentram em parágrafos mistos (por exemplo, "inflação cedendo, mas acima da meta").
3. **Selic conferida na fonte.** O valor da Selic de cada reunião foi conferido contra o parágrafo de decisão da própria ata.
4. **"Nada mudou" medido, não suposto.** Os parágrafos de orientação da 281ª (§15–§19) foram comparados com os da 280ª (§14–§18) por similaridade de texto: 100%.
5. **Ajuste feito.** O agente manteve nota +2 no parágrafo de expectativas da 281ª, mesmo sem a palavra "adicional". Por isso o site descreve essa mudança como "palavra mais branda, mesma nota", e não como queda de nota.
6. **Validação manual (time):** [PREENCHER — 10 parágrafos classificados às cegas pelo time e comparados].

## Como reproduzir

```bash
pip install -r requirements.txt
python scripts/extrair.py              # PDFs -> dados/paragrafos.json
python scripts/dados_bcb.py            # Selic e Focus oficiais (python-bcb)
python scripts/agente_tom.py --prompts # gera os prompts do agente (prompts/ata_<n>.md)
#   rodar cada prompt no Claude Code, salvando em dados/tom_agente/ata_<n>.json
#   ou, com chave de API: python scripts/agente_tom.py --api
python scripts/agente_tom.py --conferir
cd scripts && python indice.py && python montar_dados.py && python gerar_site.py
```

**Ata nova** (ex.: 282ª, publicada em 10/11/2026): salvar o PDF como `dados/atas/ata_282_2026-11-04.pdf` e rodar o fluxo de novo, ou subir o PDF direto no chat do site.

## Limitações e próximos passos

- A nota de tom é um julgamento, mesmo com uma régua fixa. A concordância de 76% mostra onde a régua ainda é ambígua, principalmente em parágrafos com sinais mistos.
- O Focus é anual (fim de 2026). Uma próxima versão pode usar as expectativas por reunião (`ExpectativasMercadoSelic`) e os juros futuros (DI) para medir a reação do mercado no dia da ata.
- Automatizar: rodar o fluxo sozinho quando sair uma ata nova e mandar o resumo por e-mail.

## Aviso

Projeto acadêmico desenvolvido em workshop. Não constitui recomendação de investimento.

**Feito com:** Claude (Claude Code e agentes), Python (pypdf, python-bcb, pandas), HTML/JS.
