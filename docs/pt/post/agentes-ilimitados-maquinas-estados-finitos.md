---
title: 'Estudo de Caso: 42 Chamadas em Loop às 2 da Manhã'
date: '2026-08-12'
category: Case Studies
tags:
- case-studies
- production
- api-loops
description: 'Auditoria de incidente de emergência e remédio de arquitetura para loops infinitos de chamadas em agentes por máquinas de estados finitos.'
author: Hugo S. Nascimento
---

*Tempo de leitura: 4 minutos. Autor: Hugo S. Nascimento.*

<!-- more -->

*Contexto: Escrevi este post após uma sessão de depuração na madrugada onde um agente em loop aberto executou quarenta e duas chamadas recursivas de ferramentas em um servidor de homologação antes de estourar os limites da API. E por isso que autonomia corporativa exige máquinas de estados matematicamente delimitadas.*

As duas horas da manha em um cluster de homologação, um alerta acordou nossa equipe de plantão.

Um agente autônomo em loop aberto estava preso em uma espiral de execução desgovernada. Por oito minutos consecutivos, o modelo disparou quarenta e duas chamadas sequenciais de ferramentas sem qualquer supervisão humana. Ele encontrou um erro simples de chave estrangeira no banco de dados, entrou em pânico e começou a fabricar identificadores sintéticos de clientes na tentativa de satisfazer a restrição quebrada. No momento em que os limites de requisição da API do provedor cortaram a conexão, o agente havia queimado trinta dólares em custos de tokens para não alcançar absolutamente nada.

Permitir que um modelo de linguagem execute ferramentas dentro de um loop aberto de raciocínio em produção é um desastre anunciado de engenharia.

Se você pesquisar no GitHub ou assistir a tutoriais na internet, verá sempre o mesmo padrão onipresente: o loop ReAct. Você entrega um prompt de sistema para o modelo, passa uma lista com trinta funções em Python e diz para ele pensar passo a passo, chamar a ferramenta que quiser, analisar a resposta e continuar no loop até achar que terminou a tarefa.

Em um tutorial de internet com duas funções de exemplo, isso parece mágico.

Em um ambiente corporativo bancário ou de ERP com dinheiro real e bancos de dados vivos, um loop ReAct sem limites é um risco operacional intolerável.

## O Colapso Matemático da Probabilidade Sem Limites

Modelos de linguagem são preditores estocásticos de próximos tokens. Cada escolha de ferramenta é uma aposta probabilística.

Quando você encadeia apostas probabilísticas dentro de um loop aberto, a matemática joga agressivamente contra a sua operação:

### 1. O Colapso Composto de Probabilidade
Suponha que seu modelo tenha noventa por cento de probabilidade de escolher a ferramenta correta e os parâmetros exatos em cada etapa isolada.

Se um fluxo de trabalho corporativo exige cinco etapas consecutivas, a probabilidade de toda a cadeia executar sem qualquer erro e de apenas cinquenta e nove por cento. Na sétima etapa, ela cai para quarenta e sete por cento. Você está jogando uma moeda para decidir se o seu sistema corporativo vai concluir a tarefa ou quebrar a produção.

### 2. A Espiral Mortal de Correção de Alucinações
O que acontece quando um agente sem limites comete um erro?

Quando um banco de dados retorna um erro ou uma API retorna Bad Request, um agente em loop aberto tenta encontrar uma saída pelo raciocínio. Em vez de parar, ele inventa uma nova consulta. Ele chama outra ferramenta para tentar corrigir o erro que acabou de cometer, empilhando alucinações até que a corrupção de dados aconteça.

### 3. Mutações de Estado Fora de Sequência
Um modelo sem limites não possui noção inerente de causalidade corporativa. Em uma configuração aberta, nada impede o modelo de emitir um reembolso antes que a devolução da mercadoria seja registrada no estoque, ou marcar um contrato como aprovado antes que a validação jurídica termine.

## A Solução: Planejamento Estocástico, Execução Delimitada em Código

Na HSN Labs, nunca permitimos loops abertos de ferramentas em produção. Impomos uma separação estrita entre raciocínio e execução por meio de Máquinas de Estados Finitos:

* Estados Discretos Permitidos: A cada microssegundo, uma transação corporativa existe em um estado explícito: Rascunho, Validado, Aprovado ou Efetivado. O agente só tem visibilidade e permissão para propor ferramentas que pertencem a esse estado específico. E fisicamente impossível para um agente no estado de Rascunho disparar uma ação de Efetivação.
* Funções de Guarda Invariantes: As transições entre estados não são governadas pelo modelo de linguagem. Elas são governadas por funções de guarda em Python em nível de código. Mesmo que o modelo sugira o cancelamento de um pedido, a guarda em software verifica se a mercadoria já saiu do centro de distribuição. Se a guarda avaliar como falso, a transição e rejeitada no nível da arquitetura.
* Propostas em Vez de Escritas Diretas: O modelo de linguagem nunca recebe credenciais diretas de escrita no banco de dados. O modelo e tratado como um motor de propostas não confiável. Ele analisa linguagem natural e propõe uma carga de transição de estado. Validadores estritos de schema como Pydantic processam essa carga, verificam invariantes e efetuam a gravação no banco.

Autonomia não significa ausência de regras. Autonomia corporativa é a capacidade de o software rodar com confiabilidade porque seus limites são matematicamente inquebráveis.

## Recursos Estratégicos e Posts Relacionados
- <a href="/blog/pt/post/manifesto/">Por Que Criei a HSN Labs</a>
- <a href="/blog/pt/post/estudo-caso-cleveland-clinic-agentes-operacionais/">Estudo de Caso: Como a Cleveland Clinic Escalou Fluxo de Pacientes</a>
- <a href="/blog/pt/post/negociacoes-autonomas-cobranca-contratos/">Operações em Alta Velocidade: Negociação Autônoma, Cobrança e Contratos</a>
- <a href="https://hsnlabs.ai/pt/bootcamp/">Aplicar para o Bootcamp de Agentes Enterprise de 5 Dias da HSN Labs</a>