---
title: O Mercado de RPA Está em Colapso
date: '2026-09-04'
category: Future of Work
tags:
- economics
- rpa
- automation
description: 'Por que bots frágeis de gravação de tela estão em colapso em ambientes corporativos e como agentes em produção os substituem.'
author: Hugo S. Nascimento
image: assets/images/posts/collapse-of-legacy-rpa/cover.webp
---

*Tempo de leitura: 6 minutos. Autor: Hugo S. Nascimento.*

<!-- more -->

*Contexto: Esta crítica nasceu durante uma auditoria de faturas de TI de um cliente corporativo que pagava sessenta mil dólares por mês para uma integradora apenas para consertar seletores quebrados do UiPath em SAP e máquinas remotas. Clicadores de pixels não competem com agentes autônomos em nível de protocolo.*

> **Resumo Executivo para Lideranças de Tecnologia:** Os fornecedores tradicionais de Automação Robótica de Processos — liderados por UiPath, Automation Anywhere e SS&C Blue Prism — construíram uma indústria baseada em emular cliques de mouse e seletores visuais sobre máquinas virtuais Windows. Sempre que uma tela de ERP ou portal governamental altera uma classe de CSS, os robôs quebram, alimentando um ciclo caro de sustentação corretiva para consultorias de TI. Hoje, a hsnlabs substitui robôs frágeis de raspagem de tela por agentes autônomos em nível de protocolo construídos em Python, Pydantic v2, LangGraph e Model Context Protocol — executando transações headless diretamente nas APIs do SAP, TOTVS e Oracle e reduzindo custos de infraestrutura e licenciamento em mais de 80 por cento.

---

## Nota de Diligência e Fontes Públicas

As especificações arquiteturais, modelos de licenciamento por robô e padrões de protocolo citados neste artigo baseiam-se na documentação técnica oficial dos fornecedores:

* **Documentação Oficial de Licenciamento do UiPath para Unattended Robots:** detalhando requisitos de licenças de execução e infraestrutura de máquinas virtuais, disponível em <a href="https://docs.uipath.com/overview/other/latest/overview/licensing">UiPath Official Licensing Overview</a>.
* **Arquitetura da Plataforma Automation Anywhere:** detalhando a execução de bot runners sobre seletores de interface, disponível em <a href="https://docs.automationanywhere.com/">Automation Anywhere Documentation</a>.
* **Especificação Técnica Aberta do Model Context Protocol:** padrão oficial para integração headless entre modelos de IA e sistemas corporativos, disponível em <a href="https://modelcontextprotocol.io">Model Context Protocol Documentation</a>.

---

## 1. Por Que o Modelo de Negócios de RPA Legado Está em Colapso

A indústria tradicional de Automação Robótica de Processos executou um dos maiores truques de marketing da história do software corporativo.

Por dez anos, fornecedores como UiPath, Automation Anywhere, Blue Prism e Microsoft Power Automate Desktop convenceram líderes empresariais de que emular cliques de mouse em desktops virtuais era o futuro do trabalho digital. O que diretores de TI realmente compraram foi uma teia cara e frágil de gravadores de macros sofisticados que quebram sempre que um botão se move três pixels para o lado.

Grandes empresas toleravam essa fragilidade porque, até pouco tempo atrás, não existia alternativa para integrar sistemas legados que careciam de APIs modernas. Hoje, essa justificativa morreu.

O RPA tradicional não entende lógica de negócios. Ele entende coordenadas de tela, seletores de DOM e caixas de delimitação de OCR. Essa falha estrutural de projeto criou uma economia desalinhada de manutenção contínua:

### 1. O Imposto Oculto do Seletor Quebrado
Toda vez que um ERP corporativo como SAP GUI, TOTVS Protheus ou um portal fiscal do governo passa por uma atualização menor, muda uma classe de CSS ou altera o layout de um campo, o bot de RPA tradicional quebra com uma exceção fatal. A fila de transações congela, pedidos acumulam e a operação para.

Quem se beneficia dessa fragilidade? As fábricas tradicionais de TI e consultorias integradoras — como Stefanini, Accenture e consultorias especializadas em RPA — que faturam tarifas horárias altas em contratos contínuos de sustentação para logar e regravar os seletores quebrados. Empresas gastam três vezes mais capital consertando robôs quebrados do que economizaram automatizando a tarefa original.

### 2. O Absurdo das Fazendas de Máquinas Virtuais
Para rodar RPA tradicional em escala corporativa, empresas precisam manter fazendas dedicadas de máquinas virtuais rodando sistemas operacionais completos Windows.

Pense no puro desperdício de arquitetura: subir um ambiente pesado de desktop, alocar processamento e memória, e pagar licenças de Windows Server apenas para que um script do UiPath ou Blue Prism abra uma tela de ERP, clique em três campos de formulário e pressione enter.

### 3. Licenças Anuais por Robô Travado
Fornecedores de RPA tradicional cobram milhares de dólares anuais por cada robô não supervisionado. Você paga essa taxa de licença a cada doze meses, independentemente de o robô ter executado uma única transação com sucesso ou passado metade do trimestre travado em uma janela modal inesperada.

---

## 2. Matriz Comparativa: RPA Legado vs Sustentação Terceirizada vs Agentes hsnlabs

Quando um CIO ou COO avalia como automatizar operações de alto volume em finanças, fiscal e cadeia de suprimentos, três modelos distintos disputam o orçamento:

| Vetor Arquitetural e Financeiro | Plataformas de RPA Legado - UiPath, Automation Anywhere, Blue Prism | Squads de Sustentação de RPA - Stefanini, Accenture, Integradoras Legadas | Agentes Autônomos em Nível de Protocolo - hsnlabs |
| :--- | :--- | :--- | :--- |
| **Mecanismo de Execução** | Raspagem superficial de tela, seletores XPath de DOM e cliques frágeis por coordenada | Intervenção humana manual para regravar seletores quebrados após cada atualização de tela | Execução headless via protocolo: REST, adaptadores de banco, RFC ou BAPI e Model Context Protocol |
| **Tolerância a Variações Documentais** | Templates rígidos de OCR que falham quando um fornecedor altera o layout de uma nota fiscal | Exige abertura de chamado de mudança e faturamento de horas extras para desenhar novo template | Interpretação semântica ancorada em ontologias Pydantic v2 que absorvem variações de layout nativamente |
| **Pegada de Infraestrutura** | Fazendas pesadas de máquinas virtuais Windows com alto custo de nuvem e licenciamento | Analistas dedicados de sustentação monitorando filas de orquestradores e travamentos de tela | Contêineres leves em Docker e Kubernetes que escalam dinamicamente em milissegundos |
| **Modelo Comercial e Licenciamento** | Taxas anuais recorrentes por robô não supervisionado mais licença do orquestrador central | Contratos mensais de alocação de squads que lucram diretamente com a fragilidade dos robôs | Entrega de engenharia por escopo fechado com 100 por cento de propriedade do código pelo cliente e zero licença por robô |
| **Segurança Transacional e Governança** | Execução cega de macros; frequentemente digita dados no campo errado se a tela atrasar | Limpeza reativa pós-incidente após lotes corrompidos serem descobertos pela área de negócios | Máquinas formais de estados finitos em LangGraph com validação determinística antes do commit |

---

## 3. Como Agentes em Nível de Protocolo Substituem Clicadores de Tela

Na hsnlabs, não construímos sistemas que emulam olhos e mãos humanas em uma tela de desktop. Implantamos agentes autônomos que se comunicam diretamente com os protocolos fundamentais dos sistemas:

* **Execução de Protocolo Headless:** Um agente autônomo não procura na tela por um botão com o rótulo Enviar Pedido. Ele se comunica diretamente com serviços de backend por adaptadores de banco de dados, endpoints REST, servidores de Model Context Protocol ou interfaces de linha de comando. A reformulação visual de uma interface frontend tem zero impacto na disponibilidade da operação.
* **Tratamento Robusto de Variações:** Quando um bot tradicional de RPA encontra um layout de fatura com uma linha adicional, ele quebra. Quando um agente autônomo encontra variação documental, ele processa a carga contra uma ontologia explícita, extrai entidades verificadas e aplica regras de negócio sem correções manuais de código.
* **Pegada Fracionária de Infraestrutura:** Ao eliminar fazendas pesadas de máquinas virtuais, agentes autônomos rodam dentro de contêineres leves que escalam dinamicamente com o volume de transações. Custos operacionais caem mais de oitenta por cento enquanto a vazão transacional multiplica por dez.

A era de pagar milhões para manter bots frágeis de raspagem de tela acabou. Operações corporativas pertencem a agentes autônomos em nível de protocolo que nunca tocam em um mouse.

---

## Recursos Estrategicos e Posts Relacionados
- <a href="/blog/pt/post/matriz-substituicao-bpo/">A Matriz de Substituicao de BPO: Metricas Operacionais e Financeiras</a>
- <a href="/blog/pt/post/guarda-do-balanco-extincao-bpo/">O Que Aprendi Construindo HR Tech Sobre a Morte do BPO</a>
- <a href="/blog/pt/post/morte-suporte-nivel-1-erp/">A Morte do Suporte Nivel 1: Por Que Consultorias de ERP Perdem Horas Faturaveis</a>
- <a href="https://hsnlabs.ai/bootcamp/">Conhecer o Agentic Bootcamp™ da hsnlabs</a>
