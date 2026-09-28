---
title: Por Que RAG Tradicional Falha em ERPs Financeiros
date: '2026-08-07'
category: Why Agents Fail
tags:
- architecture
- rag
- erp
description: 'Por que a busca vetorial por similaridade corrompe a precisão aritmética e a integridade de livros contábeis em ERPs.'
author: Hugo S. Nascimento
---

*Tempo de leitura: 4 minutos. Autor: Hugo S. Nascimento.*

<!-- more -->

*Contexto: Este post nasceu de uma auditoria técnica de emergência onde uma agência tentou calcular contas a pagar corporativas usando similaridade de cosseno sobre fragmentos de notas fiscais. As alucinações quase corromperam o livro contabilidade do cliente.*

Conectar RAG tradicional a um sistema de gestão empresarial é uma armadilha de arquitetura.

Nos últimos dois anos, perdi a conta de quantas equipes corporativas me procuraram após queimarem meses tentando fazer busca vetorial ler dados financeiros. A premissa parece tentadora para um executivo não técnico: jogar ordens de compra, faturas de fornecedores, contratos e extratos de banco de dados em um banco vetorial, e deixar um LLM recuperar fragmentos para responder dúvidas operacionais.

Em produção, essa abordagem colapsa na aritmética básica.

## Proximidade Semântica Não E Verdade Matemática

Embeddings vetoriais medem similaridade semântica em linguagem natural. Eles sabem que palavras como fatura, cobrança e pagamento compartilham proximidade conceitual.

Um banco de dados de ERP como SAP S/4HANA ou Totvs Protheus não se importa com afinidades semânticas. Ele opera com partidas dobradas imutáveis, restrições rígidas de chave estrangeira, chaves primarias e períodos fiscais estatutários.

A distância de cosseno e matematicamente incapaz de responder consultas relacionais corporativas.

### 1. Busca Vetorial Não Consegue Unir Tabelas
Imagine um CFO perguntando: Quais pedidos de compra em aberto acima de cinquenta mil dólares do mês passado não possuem nota fiscal de entrada correspondente?

Para responder a isso com exatidão, um engenheiro precisa executar joins relacionais entre ao menos quatro tabelas normalizadas: pedidos de compra, ítens do pedido, comprovantes de entrega e registros fiscais do fornecedor. 

Um banco vetorial busca fragmentos de texto que citam pedidos de compra e valores altos. Ele não consegue cruzar chaves estrangeiras. Ele não filtra registros cancelados. Ele puxa cinco trechos de texto que parecem relevantes, joga no prompt, e o modelo inventa uma lista plausível que omite transações críticas.

### 2. Débitos e Créditos Precisam Fechar em Zero
Na contabilidade corporativa, saldos são invariantes absolutos. Cada débito precisa fechar com um crédito de valor idêntico. 

Quando você divide uma tabela contábil em embeddings vetoriais, você fatia linhas relacionais em fragmentos desconectados de texto. O modelo recupera sete de dez ítens porque três fragmentos tiveram pontuação menor de relevância semântica. Quando o modelo tenta somar o saldo, ele alucina um valor baseado em informações incompletas.

Em finanças corporativas, ter noventa e cinco por cento de precisão e rigorosamente idêntico a estar totalmente quebrado.

### 3. O Pesadelo dos Limites Temporais
Dados corporativos são estritamente delimitados por calendários fiscais, taxas de cambio e jurisdições tributárias. 

Busca vetorial não possui noção inerente de sequência temporal. A menos que um engenheiro particione manualmente os índices por mês fiscal, uma consulta semântica vai tranquilamente recuperar regras de retenção fiscal de dois anos atrás misturadas com faturas atuais, gerando cálculos que violam exigências de autoridades fiscais como SPED no Brasil ou relatórios estatutários internacionais.

## O Que Construo no Lugar: Ontologias Executáveis

Na HSN Labs, não deixamos modelos de linguagem chutar comandos SQL nem buscar embeddings soltos para achar verdades financeiras. Esta é a arquitetura exata que aplicamos:

* Ontologias de Negócio Pré-Compiladas: Mapeamos o schema corporativo em um grafo de conhecimento explícito que define relacionamentos verificados, caminhos válidos de junção e regras de negócio antes de qualquer consulta rodar.
* Geração de Consultas com Tipagem Rígida: O agente não cria strings livres de SQL. Ele seleciona templates parametrizados e validados contra schemas estritos em Pydantic. Cada parâmetro e auditado antes de tocar a replica de leitura.
* Camadas de Invariantes em Código: Quando o banco retorna registros, camadas de asserções em nível de software verificam saldos contábeis, alinhamento de moedas e validade temporal antes que o contexto alcance o usuário ou o sistema seguinte.

Se uma arquitetura não pode garantir precisão matemática em registros financeiros, ela não tem lugar na produção corporativa.

## Recursos Estratégicos e Posts Relacionados
- <a href="/blog/pt/post/o-que-e-uma-ontologia-para-agentes-ia/">O Que É uma Ontologia para Agentes de IA? O Guia Definitivo</a>
- <a href="/blog/pt/post/ontologia-vs-schema-banco-dados/">Ontologia vs Schema de Banco de Dados: Por Que Tabelas Relacionais Quebram Agentes</a>
- <a href="/blog/pt/post/cemiterio-de-pocs/">Por Que Agentes Falham: O Cemitério de PoCs</a>
- <a href="https://hsnlabs.ai/pt/bootcamp/">Aplicar para o Bootcamp de Agentes Enterprise de 5 Dias da HSN Labs</a>