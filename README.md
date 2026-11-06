# Tradutor do Copom — Case 2

> Claude Lab · Economia & Finanças · PUC-Rio · 06/11/2026

**🎬 Vídeo (2 min):** https://www.youtube.com/watch?v=PN4bFBtdx5Y
**🔗 Artefato público:** https://claude.ai/artifact/AXfdFGVa6h5voQmWovGHnr

## Equipe

| Nome | Curso / período | Papel no projeto | LinkedIn / GitHub |
|---|---|---|---|
| Beatriz Menezes | Economia / 4º | Sugestões de funções e design | www.linkedin.com/in/beatriz-rangel-de-menezes-87a1b738a github: beatrizrmenezes|
| Antônio Varejão | Engenharia de Produção / 3º | Sugestões de funções e organização | https://www.linkedin.com/in/ant%C3%B4nio-varej%C3%A3o-734a68421/ github: antoniovarejao |
| Rafael Sanches | Engenharia de computação / 3º | Desenvolvimento do site e organização | https://www.linkedin.com/in/rafael-sanches-05536a436/ github: rafasanches10 |
| Luiz José Vieira da Cruz | Inteligência Artificial / 3º | Programação com Claude Code e Design | https://www.linkedin.com/in/luiz-jos%C3%A9-vieira-da-cruz/ / https://github.com/Luix-2007 |

## O problema

No dia em que sai uma ata do Copom, o economista-chefe precisa saber em poucos minutos três coisas: se o Banco Central ficou mais "hawkish" ou mais "dovish", o que mudou em relação à ata anterior e o que isso pode significar para os juros. As atas são longas, técnicas e muito parecidas entre si. A mudança que importa costuma ser uma única palavra. E ninguém aceita resumo sem fonte.

## A solução

Um site que **traduz as atas do Copom para quem decide**. Cada nota, cada mudança e cada resposta vem com **o nº do parágrafo e o trecho exato da ata**.

| Aba | O que mostra |
|---|---|
| **Panorama** | Termômetro do tom da última ata, o índice nas 6 reuniões ao lado da Selic meta e da mediana do Focus, e o principal impacto |
| **Ata por ata** | Os parágrafos de cada ata, coloridos pela nota (−2 a +2), com o trecho que justifica cada nota e a média por seção |
| **O que mudou** | As 3 mudanças mais relevantes da 281ª em relação à 280ª, mais um contraponto e os parágrafos que ficaram idênticos |
| **Pergunte às atas** | Chat com o Claude que responde só com base nas atas. Cada citação passa por uma conferência automática (✓ trecho conferido / ⚠ não literal). O usuário também pode **subir uma ata nova em PDF**, como a 282ª, e medir o tom dela com a mesma régua |
| **Como medimos** | A régua, os pesos (que o usuário pode alterar para ver o índice recalcular) e as checagens feitas |

[PREENCHER: prints do site]

### Resultado: índice de tom (−2 brando · +2 duro)

| Reunião | Data | Decisão | Selic | Índice | Média simples |
|---|---|---|---|---|---|
| 276ª | 28/01/2026 | manteve | 15,00% | **−0,47** | −0,16 |
| 277ª | 18/03/2026 | −0,25 | 14,75% | **+0,24** | +0,28 |
| 278ª | 29/04/2026 | −0,25 | 14,50% | **+0,27** | +0,28 |
| 279ª | 17/06/2026 | −0,25 | 14,25% | **+0,32** | +0,32 |
| 280ª | 05/08/2026 | −0,25 | 14,00% | **+0,63** | +0,47 |
| 281ª | 16/09/2026 | −0,25 | 13,75% | **+0,45** | +0,30 |

**A leitura:**
- O Copom cortou a Selic 5 vezes seguidas e, mesmo assim, 5 das 6 atas tiveram tom duro: o BC cortava os juros sem deixar de avisar que vigiava a inflação. Mudança de tom não é mudança de juros.
- A 276ª é a única ata branda. Foi ela que sinalizou o início do ciclo de cortes.
- A 281ª suavizou em relação à 280ª (de +0,63 para +0,45), mas continua dura.

### As 3 mudanças da 281ª em relação à 280ª

| # | Mudança | Antes (280ª) | Depois (281ª) | Efeito |
|---|---|---|---|---|
| 1 | A desancoragem das expectativas deixou de ser "adicional" | §9 "monitora com atenção a desancoragem **adicional** das expectativas de inflação para prazos mais longos" | §10 "monitora com atenção a desancoragem das expectativas de inflação para prazos mais longos" | suavizou (nota igual, +2) |
| 2 | A inflação cheia voltou para baixo do teto da meta | §2 "a inflação cheia desacelerou, porém ainda acima do limite superior da meta" | §2 "situando-se abaixo do limite superior do intervalo de tolerância, porém ainda acima da meta" | suavizou (+1 → −1) |
| 3 | Parágrafo novo: o crédito está esfriando | (não existia) | §6 "consistente com um quadro de desaceleração do crescimento, em meio a uma política monetária restritiva" | suavizou (novo, −1) |
| contraponto | Os preços ao produtor voltaram a subir | §8 "os preços aos produtores recuaram" | §9 "as variações de preços aos produtores aceleraram" | endureceu (nota igual, −1) |

### Principal impacto

O diagnóstico da 281ª ficou mais brando, mas as seções de discussão e decisão (C e D) ficaram praticamente iguais às da 280ª. Isso **sinalizava** continuidade dos cortes de 0,25 ponto, sem aceleração. O Focus já ia nessa direção: a mediana da Selic no fim de 2026 caiu de 13,75% para 13,50% em 18/09, logo depois da reunião e antes da publicação da ata (22/09), e chegou a 13,25% em 09/10. O risco estava escrito na própria ata: um câmbio "persistentemente mais depreciado" (281ª §13) é um dos riscos de alta para a inflação. Com o dólar subindo, o Focus voltou a 13,50% em 30/10, e na 282ª reunião (04/11) o Copom **manteve a Selic em 13,75%**, interrompendo os cortes. *Interpretação, não previsão.*

## Como funciona

```
PDFs das atas ──► extrair e numerar parágrafos ──► Claude classifica cada parágrafo (−2 a +2 + trecho literal)
                                                   │
                                                   ├──► 2ª leitura independente (revisor) → concordância
                                                   ▼
                    índice por ata (regra de agregação) + diff 281ª × 280ª + Selic (SGS 432) + Focus (Olinda)
                                                   ▼
                            dados/resultados.json ──► site (artefato do claude.ai com IA)
                                                   ▼
                            verificacao/verificar.py confere tudo contra as fontes
```

1. **Extração:** o texto de cada ata é dividido nos parágrafos numerados do próprio PDF (§1, §2, …) e cada parágrafo recebe a seção dele (A, B, C ou D).
2. **Classificação:** o Claude dá uma nota a cada parágrafo e copia literalmente o trecho que a justifica.
3. **Segunda leitura:** uma classificação independente, feita do zero, mede a consistência.
4. **Agregação:** a média ponderada vira o índice de cada ata.
5. **Diff:** a comparação entre a 281ª e a 280ª mostra parágrafos novos, alterados e idênticos.
6. **Cruzamento com o mercado:** o índice é comparado com a Selic meta e com o Focus.
7. **Site gerado a partir do JSON:** uma ata nova entra pelo próprio site, que extrai o PDF no navegador e aplica a mesma régua.

### A régua (nota por parágrafo)

| Nota | Significado | Exemplo real nas atas |
|---|---|---|
| +2 | muito duro | "desancoragem adicional"; "maior e por mais tempo" |
| +1 | duro | "assimetria altista"; "serenidade e cautela" |
| 0 | neutro | premissas, números, procedimento, votação |
| −1 | brando | inflação cedendo; atividade desacelerando; corte de 0,25 |
| −2 | muito brando | "sinalizar o início de um ciclo de redução" (276ª) |

### Regra de agregação

**Índice = média ponderada das notas, ignorando os parágrafos neutros (0).** As seções têm pesos diferentes:

| Seção | Peso |
|---|---|
| A) Conjuntura | 1 |
| B) Cenários e riscos | 1 |
| C) Discussão da política monetária | 2 |
| D) Decisão | 2 |

**Por quê:**
- Os parágrafos neutros (dados, votação) diluem o sinal.
- As seções C e D são onde o Copom sinaliza os próximos passos.

A média simples continua sendo mostrada, para comparação. No site, o usuário pode mudar os pesos e ver o índice recalcular.

## Dados usados

| Dado | Fonte | Data dos dados |
|---|---|---|
| Atas 276ª a 281ª (PDF) | Banco Central do Brasil, [Atas do Copom](https://www.bcb.gov.br/publicacoes/atascopom), arquivos em `data/case2_copom/atas/` do repositório do workshop | reuniões de 28/01 a 16/09/2026 |
| Selic meta | BCB, SGS série 432 | até 06/11/2026 |
| Mediana da Selic esperada para o fim de 2026 | BCB, Relatório Focus (API Olinda, `ExpectativasMercadoAnuais`, base de cálculo 0) | 02/01 a 30/10/2026 (208 dias úteis) |
| Decisão da 282ª reunião | BCB, [Comunicados do Copom](https://www.bcb.gov.br/publicacoes/comunicadoscopom) | 04/11/2026 |
| Probabilidade de pausa nas opções de Copom da B3 (~63%) | [Rankia](https://rankia.com.br/copom-4-novembro-selic-manutencao-63-opcoes-b3/) | fechamento de 26/10/2026 (**dado de terceiros, não conferido**) |

### Como tratamos os cuidados do case

1. **Data da reunião ≠ data da ata.** Guardamos as duas. As atas foram publicadas 6 dias depois de cada reunião (ex.: reunião em 16/09, ata em 22/09), e o impacto separa o que aconteceu depois da reunião do que aconteceu depois da ata. A ata da 282ª é esperada para 10/11.
2. **Tom ≠ juros.** O site mostra lado a lado "o que decidiram" (Selic) e "como falaram" (índice): 5 cortes com tom duro.
3. **Sem trecho, não vale.** Toda nota, mudança e resposta do chat cita o nº do parágrafo e um trecho literal. O site confere automaticamente as citações do chat.
4. **Trechos curtos.** Citamos só o necessário e linkamos a ata original do BCB.
5. **Focus = Selic esperada para o fim do ano**, não para a próxima reunião. É assim que o site e este README a descrevem.
6. **Impacto é interpretação.** O texto usa linguagem condicional e o site traz o aviso de que não é recomendação de investimento.

## Como verificamos os resultados

Escrevemos um verificador independente ([`verificacao/verificar.py`](verificacao/verificar.py)). Ele relê os PDFs originais e consulta as APIs do Banco Central. O resultado completo está em [`verificacao/relatorio.md`](verificacao/relatorio.md).

| O que conferimos | Contra o quê | Resultado |
|---|---|---|
| Os 119 parágrafos do site (texto e numeração §) | PDFs das 6 atas | ✅ 119/119; o nº de parágrafos bate nas 6 atas |
| Os 119 trechos que justificam as notas | PDFs | ✅ 119/119 existem literalmente |
| As 8 citações das mudanças, do contraponto e do risco | PDFs + nº do parágrafo | ✅ 8/8 no parágrafo indicado |
| Os 6 índices, a 2ª leitura e a média simples | Recálculo com a regra de agregação | ✅ todos idênticos |
| A Selic de cada reunião | Parágrafo da decisão no PDF + SGS 432 | ✅ 6/6 |
| A série do Focus no gráfico | API Olinda do BCB | ✅ 208/208 pontos |
| As datas de publicação das atas | API de atas do BCB | ✅ 6/6 |
| A decisão da 282ª (manteve 13,75%) | Comunicado oficial do BCB | ✅ |

**Exemplos concretos:**
- **Trecho que parecia não existir:** em 15 parágrafos o texto do site não batia de primeira com o PDF. Investigamos e a causa era o próprio PDF: notas de rodapé e cabeçalhos de página caem no meio do parágrafo. O texto do site estava correto. O verificador passou a tolerar esse ruído, mas continua exigindo pelo menos 99% do texto em sequência.
- **Frase imprecisa corrigida:** a primeira versão do impacto dizia que o Focus foi a 13,50% "em 21/09". A série oficial mostra que a mudança aconteceu em **18/09**, e que os 13,25% apareceram em **09/10**, não em 13/10. Corrigimos o texto neste README. [PREENCHER: confirmar que a frase também foi corrigida no site.]
- **Consistência da classificação:** duas leituras independentes do Claude deram notas idênticas em **91 de 119 parágrafos (76%)** e diferiram em no máximo 1 ponto em **115 de 119 (97%)**. As 4 divergências grandes (276ª §3, 277ª §3, 279ª §20, 280ª §2) estão todas em parágrafos com sinais mistos ("desacelerou, **porém** ainda acima da meta"). Isso mede **coerência**, não acerto, por isso fizemos a validação humana abaixo.
- **Validação humana:** [PREENCHER: o time classificou 10 parágrafos à mão sem olhar as notas do Claude. Concordância: X de 10. Onde discordamos e o que ajustamos.]

| Ata § | Nota do time | Nota do Claude | Comentário |
|---|---|---|---|
| [PREENCHER] | | | |

## Como reproduzir

```bash
git clone https://github.com/jplucas29/claude-lab-financas-puc2026   # atas em data/case2_copom/atas
pip install pypdf
python verificacao/verificar.py --atas claude-lab-financas-puc2026/data/case2_copom/atas
```

O script regera `verificacao/relatorio.md`. Para rodar sem internet (só a parte dos PDFs e o recálculo), use `--offline`.

- Os dados que alimentam o site estão em [`dados/resultados.json`](dados/resultados.json).
- Os prompts estão em [`prompts.md`](prompts.md).

[PREENCHER: se tiverem os scripts de extração e classificação, coloquem em `codigo/` e citem aqui.]

## Limitações e próximos passos

- **A classificação é do Claude.** A 2ª leitura mede consistência, e a validação humana foi feita numa amostra de 10 parágrafos, não nas 6 atas inteiras.
- **Os pesos por seção (C e D valem 2) são uma escolha nossa.** Com média simples a 276ª continua a mais branda e a 280ª a mais dura, mas o nível e a ordem das atas intermediárias mudam. Por isso o site deixa o usuário testar outros pesos.
- **O mapa de calor por seção** faz a média de todos os parágrafos, incluindo os neutros, enquanto o índice ignora os neutros. Por isso os dois números não são diretamente comparáveis.
- **Dados de terceiros:** a probabilidade das opções de Copom da B3 e o movimento do dólar vêm de notícias, não de fonte primária.
- **Texto do PDF:** em alguns parágrafos, ao ler a ata inteira no site, aparecem palavras partidas pela extração (ex.: "ju ros"). Os trechos citados estão limpos.
- **Com mais um dia:**
  - medir a reação dos juros futuros (DI) no dia da publicação de cada ata;
  - ampliar o histórico para antes de 2026, para testar se o índice antecipa a Selic;
  - rodar a 282ª assim que for publicada, prevista para 10/11.

## Aviso

Projeto acadêmico desenvolvido em workshop. **Não constitui recomendação de investimento.** Fonte dos dados: Banco Central do Brasil (atas e comunicados do Copom, SGS e Relatório Focus).

**Feito com:** Claude (claude.ai e Claude Code) · Python · pypdf · pdf.js · API de dados abertos do Banco Central
