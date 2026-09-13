---
type: blog_post
title: "LATAM Airlines: Deterministic Agents in a 3% Margin Business"
date: 2026-09-13
tags:
  - blog
  - agentic-engineering
  - roi
  - case-study
status: active
---

# Resumo do Transcript (Outline)

1. **O Contexto de Margem Baixa:** A LATAM opera com margens de 3% a 5%. Combustível de aviação consome 31% do custo. Não há margem para ineficiência de software. Cada chamada de IA precisa justificar o custo contra infraestrutura física.
2. **O Erro de Arquitetura Inicial:** O agente original delegava para especialistas, e cada especialista era forçado a gerar outputs estruturados de ponta a ponta. Isso gerava 15% de overhead em tokens e latência.
3. **A Correção Determinística (Supervisor Pattern):** Eles mudaram para uma arquitetura onde especialistas usam ferramentas de forma bruta, e apenas o Supervisor (roteador principal) formata a resposta final. Resultado: -15% no custo sem perda de qualidade.
4. **UX Baseada em Dados (Falso Out-of-Scope):** O sistema descartava 13% das conversas como "fora de escopo". A observabilidade (LangSmith) mostrou que 95% eram dúvidas reais sobre bagagem e check-in, não tentativas de quebrar o prompt. A adição de um agente de Customer Care reduziu a rejeição para 1%.
5. **A Verdadeira Tese (O Chat não é o Produto):** O chatbot ao consumidor final é apenas a interface de coleta. O verdadeiro produto é o **Compass**, um motor que lê interações não-estruturadas, aplica ontologias semânticas rígidas e joga os dados estruturados em um Knowledge Graph no BigQuery. Isso é Business Intelligence em escala.

---

# Draft do Blog Post (Hugo Nascimento)

A maioria dos projetos de IA enterprise falha porque os líderes tratam LLMs como mágica livre de restrições. Eles constroem chatbots de texto livre e oram por engajamento.

Eu acabo de analisar o case de agentes autônomos da LATAM Airlines. Eles operam com uma margem de lucro de 3% a 5%. Combustível representa 31% do custo operacional. Em um negócio onde cada centavo compete com querosene de aviação, não existe orçamento para chamadas de API ineficientes. 

Aqui estão as lições reais de como a engenharia agentiva determinística salvou o projeto de falhar na produção.

## 1. Descentralização semântica custa caro
No começo, a LATAM usava um modelo de triagem que passava o controle para agentes especialistas (voos, hotéis, seguros). O erro: exigir que cada especialista também fizesse a formatação estruturada da resposta final. 

Forçar estruturação de linguagem natural em todas as etapas intermediárias gerou **15% de overhead em latência e consumo de tokens**. 

Eles corrigiram a arquitetura utilizando um padrão estrito de Supervisor. Os agentes especialistas operam como executores cegos de ferramentas. Apenas o nó supervisor consolida os dados e gera a resposta final. Mesma qualidade, 15% a menos de custo imediato.

## 2. Usuários não querem hackear seu prompt, eles querem resolver problemas
Em produção, a telemetria acusou que 13% das interações do agente "Concierge" caiam na regra de erro de "fora de escopo". 

A reação amadora seria aumentar a penalização no prompt. A observabilidade revelou que 95% dessas requisições eram clientes com problemas reais de bagagem e check-in. O modelo não falhou. A arquitetura não falhou. Eles apenas não haviam previsto o problema real da operação. Eles acoplaram um novo nó especialista no Supervisor. O erro despencou para 1%.

## 3. O Chatbot não é o produto. O Grafo é.
Aqui está a tese central da HSN Labs aplicada na prática. A LATAM percebeu que um cliente perguntando sobre "restaurantes italianos perto do hotel" não está apenas pedindo recomendação. Ele está alimentando um perfil semântico de preferências.

Para capturar isso, a interface B2C deixou de ser o objetivo final. Eles construíram o **Compass**.

O Compass pega todas as conversas desestruturadas, transcripts de call center e entrevistas de UX, aplica ontologias semânticas estritas e consolida tudo em um *Knowledge Graph* no BigQuery (GraphRAG).

Isso é Engenharia Agentiva Determinística. Você usa a IA não para conversar com o usuário, mas como um parser implacável que transforma ruído em uma tabela rígida no seu banco de dados de produção. 

É assim que você corta o BPO legado. É assim que você prova ROI para um CFO.