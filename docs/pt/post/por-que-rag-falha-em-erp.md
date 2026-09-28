---
title: Por Que RAG Tradicional Falha em ERPs Financeiros
date: '2026-08-07'
category: Why Agents Fail
tags:
- architecture
- rag
- erp
description: 'Por que a busca vetorial por similaridade corrompe a precisao aritmetica e a integridade de livros contabeis em ERPs.'
author: Hugo S. Nascimento
---

*Tempo de leitura: 4 minutos. Autor: Hugo S. Nascimento.*

<!-- more -->

*Contexto: Este post nasceu de uma auditoria tecnica de emergencia onde uma agencia tentou calcular contas a pagar corporativas usando similaridade de cosseno sobre fragmentos de notas fiscais. As alucinacoes quase corromperam o livro contabilidade do cliente.*

Conectar RAG tradicional a um sistema de gestao empresarial e uma armadilha de arquitetura.

Nos ultimos dois anos, perdi a conta de quantas equipes corporativas me procuraram apos queimarem meses tentando fazer busca vetorial ler dados financeiros. A premissa parece tentadora para um executivo nao tecnico: jogar ordens de compra, faturas de fornecedores, contratos e extratos de banco de dados em um banco vetorial, e deixar um LLM recuperar fragmentos para responder duvidas operacionais.

Em producao, essa abordagem colapsa na aritmetica basica.

## Proximidade Semantica Nao E Verdade Matematica

Embeddings vetoriais medem similaridade semantica em linguagem natural. Eles sabem que palavras como fatura, cobranca e pagamento compartilham proximidade conceitual.

Um banco de dados de ERP como SAP S/4HANA ou Totvs Protheus nao se importa com afinidades semanticas. Ele opera com partidas dobradas imutaveis, restricoes rigidas de chave estrangeira, chaves primarias e periodos fiscais estatutarios.

A distancia de cosseno e matematicamente incapaz de responder consultas relacionais corporativas.

### 1. Busca Vetorial Nao Consegue Unir Tabelas
Imagine um CFO perguntando: Quais pedidos de compra em aberto acima de cinquenta mil dolares do mes passado nao possuem nota fiscal de entrada correspondente?

Para responder a isso com exatidao, um engenheiro precisa executar joins relacionais entre ao menos quatro tabelas normalizadas: pedidos de compra, itens do pedido, comprovantes de entrega e registros fiscais do fornecedor. 

Um banco vetorial busca fragmentos de texto que citam pedidos de compra e valores altos. Ele nao consegue cruzar chaves estrangeiras. Ele nao filtra registros cancelados. Ele puxa cinco trechos de texto que parecem relevantes, joga no prompt, e o modelo inventa uma lista plausivel que omite transacoes criticas.

### 2. Debitos e Creditos Precisam Fechar em Zero
Na contabilidade corporativa, saldos sao invariantes absolutos. Cada debito precisa fechar com um credito de valor identico. 

Quando voce divide uma tabela contabil em embeddings vetoriais, voce fatia linhas relacionais em fragmentos desconectados de texto. O modelo recupera sete de dez itens porque tres fragmentos tiveram pontuacao menor de relevancia semantica. Quando o modelo tenta somar o saldo, ele alucina um valor baseado em informacoes incompletas.

Em financas corporativas, ter noventa e cinco por cento de precisao e rigorosamente identico a estar totalmente quebrado.

### 3. O Pesadelo dos Limites Temporais
Dados corporativos sao estritamente delimitados por calendarios fiscais, taxas de cambio e jurisdicoes tributarias. 

Busca vetorial nao possui nocao inerente de sequencia temporal. A menos que um engenheiro particione manualmente os indices por mes fiscal, uma consulta semantica vai tranquilamente recuperar regras de retencao fiscal de dois anos atras misturadas com faturas atuais, gerando calculos que violam exigencias de autoridades fiscais como SPED no Brasil ou relatorios estatutarios internacionais.

## O Que Construo no Lugar: Ontologias Executaveis

Na HSN Labs, nao deixamos modelos de linguagem chutar comandos SQL nem buscar embeddings soltos para achar verdades financeiras. Esta e a arquitetura exata que aplicamos:

* Ontologias de Negocio Pre-Compiladas: Mapeamos o schema corporativo em um grafo de conhecimento explicito que define relacionamentos verificados, caminhos validos de juncao e regras de negocio antes de qualquer consulta rodar.
* Geracao de Consultas com Tipagem Rigida: O agente nao cria strings livres de SQL. Ele seleciona templates parametrizados e validados contra schemas estritos em Pydantic. Cada parametro e auditado antes de tocar a replica de leitura.
* Camadas de Invariantes em Codigo: Quando o banco retorna registros, camadas de assercoes em nivel de software verificam saldos contabeis, alinhamento de moedas e validade temporal antes que o contexto alcance o usuario ou o sistema seguinte.

Se uma arquitetura nao pode garantir precisao matematica em registros financeiros, ela nao tem lugar na producao corporativa.

## Recursos Estrategicos e Posts Relacionados
- <a href="/blog/pt/post/o-que-e-uma-ontologia-para-agentes-ia/">O Que E uma Ontologia para Agentes de IA? O Guia Definitivo</a>
- <a href="/blog/pt/post/ontologia-vs-schema-banco-dados/">Ontologia vs Schema de Banco de Dados: Por Que Tabelas Relacionais Quebram Agentes</a>
- <a href="/blog/pt/post/cemiterio-de-pocs/">Por Que Agentes Falham: O Cemiterio de PoCs</a>
- <a href="https://hsnlabs.ai/pt/bootcamp/">Aplicar para o Bootcamp de Agentes Enterprise de 5 Dias da HSN Labs</a>