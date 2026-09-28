---
title: 'Estudo de Caso: 42 Chamadas em Loop as 2 da Manha'
date: '2026-08-12'
category: Case Studies
tags:
- case-studies
- production
- api-loops
description: 'Auditoria de incidente de emergencia e remedio de arquitetura para loops infinitos de chamadas em agentes por maquinas de estados finitos.'
author: Hugo S. Nascimento
---

*Tempo de leitura: 4 minutos. Autor: Hugo S. Nascimento.*

<!-- more -->

*Contexto: Escrevi este ensaio apos uma sessao de depuracao na madrugada onde um agente em loop aberto executou quarenta e duas chamadas recursivas de ferramentas em um servidor de homologacao antes de estourar os limites da API. E por isso que autonomia corporativa exige maquinas de estados matematicamente delimitadas.*

As duas horas da manha em um cluster de homologacao, um alerta acordou nossa equipe de plantao.

Um agente autonomo em loop aberto estava preso em uma espiral de execucao desgovernada. Por oito minutos consecutivos, o modelo disparou quarenta e duas chamadas sequenciais de ferramentas sem qualquer supervisao humana. Ele encontrou um erro simples de chave estrangeira no banco de dados, entrou em panico e comecou a fabricar identificadores sinteticos de clientes na tentativa de satisfazer a restricao quebrada. No momento em que os limites de requisicao da API do provedor cortaram a conexao, o agente havia queimado trinta dolares em custos de tokens para nao alcancar absolutamente nada.

Permitir que um modelo de linguagem execute ferramentas dentro de um loop aberto de raciocinio em producao e um desastre anunciado de engenharia.

Se voce pesquisar no GitHub ou assistir a tutoriais na internet, vera sempre o mesmo padrao onipresente: o loop ReAct. Voce entrega um prompt de sistema para o modelo, passa uma lista com trinta funcoes em Python e diz para ele pensar passo a passo, chamar a ferramenta que quiser, analisar a resposta e continuar no loop ate achar que terminou a tarefa.

Em um tutorial de internet com duas funcoes de exemplo, isso parece magico.

Em um ambiente corporativo bancario ou de ERP com dinheiro real e bancos de dados vivos, um loop ReAct sem limites e um risco operacional intoleravel.

## O Colapso Matematico da Probabilidade Sem Limites

Modelos de linguagem sao preditores estocasticos de proximos tokens. Cada escolha de ferramenta e uma aposta probabilistica.

Quando voce encadeia apostas probabilisticas dentro de um loop aberto, a matematica joga agressivamente contra a sua operacao:

### 1. O Colapso Composto de Probabilidade
Suponha que seu modelo tenha noventa por cento de probabilidade de escolher a ferramenta correta e os parametros exatos em cada etapa isolada.

Se um fluxo de trabalho corporativo exige cinco etapas consecutivas, a probabilidade de toda a cadeia executar sem qualquer erro e de apenas cinquenta e nove por cento. Na setima etapa, ela cai para quarenta e sete por cento. Voce esta jogando uma moeda para decidir se o seu sistema corporativo vai concluir a tarefa ou quebrar a producao.

### 2. A Espiral Mortal de Correcao de Alucinacoes
O que acontece quando um agente sem limites comete um erro?

Quando um banco de dados retorna um erro ou uma API retorna Bad Request, um agente em loop aberto tenta encontrar uma saida pelo raciocinio. Em vez de parar, ele inventa uma nova consulta. Ele chama outra ferramenta para tentar corrigir o erro que acabou de cometer, empilhando alucinacoes ate que a corrupcao de dados aconteca.

### 3. Mutacoes de Estado Fora de Sequencia
Um modelo sem limites nao possui nocao inerente de causalidade corporativa. Em uma configuracao aberta, nada impede o modelo de emitir um reembolso antes que a devolucao da mercadoria seja registrada no estoque, ou marcar um contrato como aprovado antes que a validacao juridica termine.

## A Solucao: Planejamento Estocastico, Execucao Delimitada em Codigo

Na HSN Labs, nunca permitimos loops abertos de ferramentas em producao. Impomos uma separacao estrita entre raciocinio e execucao por meio de Maquinas de Estados Finitos:

* Estados Discretos Permitidos: A cada microssegundo, uma transacao corporativa existe em um estado explicito: Rascunho, Validado, Aprovado ou Efetivado. O agente so tem visibilidade e permissao para propor ferramentas que pertencem a esse estado especifico. E fisicamente impossivel para um agente no estado de Rascunho disparar uma acao de Efetivacao.
* Funcoes de Guarda Invariantes: As transicoes entre estados nao sao governadas pelo modelo de linguagem. Elas sao governadas por funcoes de guarda em Python em nivel de codigo. Mesmo que o modelo sugira o cancelamento de um pedido, a guarda em software verifica se a mercadoria ja saiu do centro de distribuicao. Se a guarda avaliar como falso, a transicao e rejeitada no nivel da arquitetura.
* Propostas em Vez de Escritas Diretas: O modelo de linguagem nunca recebe credenciais diretas de escrita no banco de dados. O modelo e tratado como um motor de propostas nao confiavel. Ele analisa linguagem natural e propoe uma carga de transicao de estado. Validadores estritos de schema como Pydantic processam essa carga, verificam invariantes e efetuam a gravacao no banco.

Autonomia nao significa ausencia de regras. Autonomia corporativa e a capacidade de o software rodar com confiabilidade porque seus limites sao matematicamente inquebraveis.

## Recursos Estrategicos e Ensaios Relacionados
- <a href="/blog/pt/post/chatbot-vs-agente/">Chatbot vs Agente: Por Que Substituir BPOs Exige Ontologias em Producao</a>
- <a href="/blog/pt/post/cemiterio-de-pocs/">Por Que Agentes Falham: O Cemiterio de PoCs</a>
- <a href="/blog/pt/post/custo-ia-ilimitada-ti-legada/">O Custo de IA Sem Limites na TI Legada</a>
- <a href="https://hsnlabs.ai/pt/bootcamp/">Aplicar para o Bootcamp de Agentes Enterprise de 5 Dias da HSN Labs</a>
