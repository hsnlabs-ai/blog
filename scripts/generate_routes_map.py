import json
import re
from pathlib import Path

routes_data = {
    "site_pages": [
        {
            "id": "site_home",
            "en_path": "/",
            "pt_path": "/pt/",
            "title_en": "HSN Labs — AI Agents That Don't Fail in Production",
            "title_pt": "HSN Labs — Agentes de IA que Nao Falham em Producao",
            "description_en": "Boutique building resilient multi-agent architectures on business ontologies.",
            "description_pt": "Boutique de engenharia construindo arquiteturas multiagente resilientes em ontologias de negocios."
        },
        {
            "id": "site_bootcamp",
            "en_path": "/bootcamp/",
            "pt_path": "/pt/bootcamp/",
            "title_en": "5-Day Enterprise Agent Bootcamp | HSN Labs",
            "title_pt": "Bootcamp de Agentes Enterprise de 5 Dias | HSN Labs",
            "description_en": "Five-day intensive sprint replacing manual BPO workflows with deterministic AI agents.",
            "description_pt": "Sprint intensivo de cinco dias substituindo fluxos manuais de BPO por agentes de IA determinísticos."
        },
        {
            "id": "site_advisory",
            "en_path": "/advisory/",
            "pt_path": "/pt/advisory/",
            "title_en": "Architecture Advisory | Hugo S. Nascimento",
            "title_pt": "Advisory de Arquitetura | Hugo S. Nascimento",
            "description_en": "Strategic architecture advisory for C-level executives on agent transition.",
            "description_pt": "Advisory estrategico de arquitetura para executivos C-level na transicao agentica."
        },
        {
            "id": "site_privacy_policy",
            "en_path": "/privacy-policy/",
            "pt_path": "/pt/privacy-policy/",
            "title_en": "Privacy Policy | HSN Labs",
            "title_pt": "Politica de Privacidade | HSN Labs",
            "description_en": "Privacy policy and data governance terms.",
            "description_pt": "Politica de privacidade e governanca de dados."
        },
        {
            "id": "site_modern_slavery",
            "en_path": "/modern-slavery-statement/",
            "pt_path": "/pt/modern-slavery-statement/",
            "title_en": "Modern Slavery Statement | HSN Labs",
            "title_pt": "Declaracao de Escravidao Moderna | HSN Labs",
            "description_en": "Ethics and compliance statement.",
            "description_pt": "Declaracao de etica e conformidade corporativa."
        },
        {
            "id": "blog_home",
            "en_path": "/blog/",
            "pt_path": "/blog/pt/",
            "title_en": "Hugo S. Nascimento — Enterprise Agent Architecture",
            "title_pt": "Hugo S. Nascimento — Arquitetura de Agentes Enterprise",
            "description_en": "Essays and field notes on enterprise AI architectures and business ontologies.",
            "description_pt": "Ensaios e notas de campo sobre arquiteturas de agentes enterprise e ontologias."
        }
    ],
    "blog_posts": [
        {
            "slug_en": "autonomous-negotiations-collections-contracts",
            "slug_pt": "negociacoes-autonomas-cobranca-contratos",
            "title_en": "High-Velocity Operations: Autonomous Negotiation, Collections, and Contract Execution",
            "title_pt": "Operacoes em Alta Velocidade: Negociacao Autonoma, Cobranca e Contratos",
            "category_en": "Case Studies",
            "category_pt": "Estudos de Caso",
            "target_keyword_pt": "negociacao autonoma agentes de ia cobranca"
        },
        {
            "slug_en": "balance-sheet-guard-bpo-extinction",
            "slug_pt": "guarda-do-balanco-extincao-bpo",
            "title_en": "What I Learned Building HR Tech About Dying BPO Contracts",
            "title_pt": "O Que Aprendi Construindo HR Tech Sobre a Morte do BPO",
            "category_en": "Future of Work",
            "category_pt": "O Futuro do Trabalho",
            "target_keyword_pt": "fim do bpo substituicao por agentes"
        },
        {
            "slug_en": "bpo-replacement-matrix",
            "slug_pt": "matriz-substituicao-bpo",
            "title_en": "The BPO Replacement Matrix: Operational and Financial Metrics",
            "title_pt": "A Matriz de Substituicao de BPO: Metricas Operacionais e Financeiras",
            "category_en": "Agentic Economics",
            "category_pt": "Economia Agentica",
            "target_keyword_pt": "matriz de substituicao bpo calculo roi"
        },
        {
            "slug_en": "c-suite-margin-protection-playbook",
            "slug_pt": "playbook-c-suite-protecao-margem",
            "title_en": "The C-Suite Transition Playbook: Protecting Margins in the Agentic Economy",
            "title_pt": "O Playbook de Transicao da Diretoria: Protegendo Margens na Era Agentica",
            "category_en": "Agentic Economics",
            "category_pt": "Economia Agentica",
            "target_keyword_pt": "playbook protecao de margens agentes ia"
        },
        {
            "slug_en": "chatbot-vs-agent",
            "slug_pt": "chatbot-vs-agente",
            "title_en": "Chatbot vs Agent: Why Replacing BPOs Requires Production Ontologies",
            "title_pt": "Chatbot vs Agente: Por Que Substituir BPOs Exige Ontologias em Producao",
            "category_en": "Agent Development Life Cycle",
            "category_pt": "Ciclo de Vida de Desenvolvimento de Agentes",
            "target_keyword_pt": "diferenca entre chatbot e agente de ia"
        },
        {
            "slug_en": "cleveland-clinic-case-study-operational-agents",
            "slug_pt": "estudo-caso-cleveland-clinic-agentes-operacionais",
            "title_en": "Case Study: How Cleveland Clinic Scaled Patient Flow with Operational Agents",
            "title_pt": "Estudo de Caso: Como a Cleveland Clinic Escalou Fluxo de Pacientes",
            "category_en": "Case Studies",
            "category_pt": "Estudos de Caso",
            "target_keyword_pt": "estudo de caso agentes ia saude operacao"
        },
        {
            "slug_en": "collapse-of-legacy-rpa",
            "slug_pt": "colapso-rpa-legado",
            "title_en": "The RPA Market Is Collapsing",
            "title_pt": "O Mercado de RPA Esta em Colapso",
            "category_en": "Future of Work",
            "category_pt": "O Futuro do Trabalho",
            "target_keyword_pt": "colapso rpa uipath agentes inteligentes"
        },
        {
            "slug_en": "cost-legacy-it",
            "slug_pt": "custo-ia-ilimitada-ti-legada",
            "title_en": "The Cost of Unbounded AI in Legacy IT",
            "title_pt": "O Custo de IA Sem Limites na TI Legada",
            "category_en": "Agentic Economics",
            "category_pt": "Economia Agentica",
            "target_keyword_pt": "custos de falhas de ia ti legada"
        },
        {
            "slug_en": "death-of-tier-1-erp-helpdesk",
            "slug_pt": "morte-suporte-nivel-1-erp",
            "title_en": "The Death of Tier-1 Support: Why ERP Consultancies Lose Billable Hours",
            "title_pt": "A Morte do Suporte Nivel 1: Por Que Consultorias de ERP Perdem Horas Faturaveis",
            "category_en": "Future of Work",
            "category_pt": "O Futuro do Trabalho",
            "target_keyword_pt": "fim do suporte erp nivel 1 agentes"
        },
        {
            "slug_en": "five-day-architecture-sprint",
            "slug_pt": "sprint-arquitetura-cinco-dias",
            "title_en": "Why Big 4 Slide Decks Fail on Agent Projects",
            "title_pt": "Por Que Apresentacoes de Big 4 Falham em Projetos de Agentes",
            "category_en": "Agent Development Life Cycle",
            "category_pt": "Ciclo de Vida de Desenvolvimento de Agentes",
            "target_keyword_pt": "sprint arquitetura agentes enterprise"
        },
        {
            "slug_en": "how-to-build-an-enterprise-ontology-from-scratch",
            "slug_pt": "como-construir-ontologia-enterprise-do-zero",
            "title_en": "How to Build an Enterprise Ontology from Scratch: Step by Step",
            "title_pt": "Como Construir uma Ontologia Enterprise do Zero: Passo a Passo",
            "category_en": "Agent Development Life Cycle",
            "category_pt": "Ciclo de Vida de Desenvolvimento de Agentes",
            "target_keyword_pt": "como construir ontologia de dados empresarial"
        },
        {
            "slug_en": "how-to-build-operational-ontology-python-mcp",
            "slug_pt": "como-construir-ontologia-operacional-python-mcp",
            "title_en": "How to Build an Operational Business Ontology in Python and MCP",
            "title_pt": "Como Construir uma Ontologia Operacional de Negocios em Python e MCP",
            "category_en": "Agent Development Life Cycle",
            "category_pt": "Ciclo de Vida de Desenvolvimento de Agentes",
            "target_keyword_pt": "ontologia operacional python mcp modelo"
        },
        {
            "slug_en": "integration-drift",
            "slug_pt": "deriva-de-integracao",
            "title_en": "The Integration Drift: When Prompts Break Production Agents",
            "title_pt": "A Deriva de Integracao: Quando Prompts Quebram Agentes em Producao",
            "category_en": "Why Agents Fail",
            "category_pt": "Por Que Agentes Falham",
            "target_keyword_pt": "schema drift derivas de integracao agentes"
        },
        {
            "slug_en": "kafka-metamorfose-ia-futuro-do-trabalho",
            "slug_pt": "kafka-metamorfose-ia-futuro-do-trabalho",
            "title_en": "De 1915 a Era da IA: Kafka, utilitarismo e o valor do trabalho",
            "title_pt": "De 1915 a Era da IA: Kafka, utilitarismo e o valor do trabalho",
            "category_en": "Future of Work",
            "category_pt": "O Futuro do Trabalho",
            "target_keyword_pt": "kafka metamorfose ia futuro do trabalho"
        },
        {
            "slug_en": "latam-airlines-case-study",
            "slug_pt": "estudo-caso-latam-airlines",
            "title_en": "LATAM Airlines: Production Agents in a 3 Percent Margin Business",
            "title_pt": "LATAM Airlines: Agentes em Producao com Margem de 3 Por Cento",
            "category_en": "Case Studies",
            "category_pt": "Estudos de Caso",
            "target_keyword_pt": "estudo caso latam airlines agentes automacao"
        },
        {
            "slug_en": "legacy-core-backing-engine",
            "slug_pt": "sistemas-legados-motor-execucao",
            "title_en": "Legacy Core Systems Will Not Die: They Are the Execution Engine",
            "title_pt": "Sistemas Transacionais Legados Nao Vao Morrer: Eles Sao o Motor",
            "category_en": "Agent Development Life Cycle",
            "category_pt": "Ciclo de Vida de Desenvolvimento de Agentes",
            "target_keyword_pt": "integracao sistemas legados agentes ia mainframe"
        },
        {
            "slug_en": "llm-as-judge-fallacy",
            "slug_pt": "falacia-llm-como-juiz",
            "title_en": "Why LLM-as-a-Judge Fails in Banking",
            "title_pt": "Por Que LLM Como Juiz Falha no Setor Bancario",
            "category_en": "Why Agents Fail",
            "category_pt": "Por Que Agentes Falham",
            "target_keyword_pt": "llm as judge falhas avaliacao financeira"
        },
        {
            "slug_en": "manifesto",
            "slug_pt": "manifesto",
            "title_en": "Why I Built HSN Labs",
            "title_pt": "Por Que Criei a HSN Labs",
            "category_en": "Case Studies",
            "category_pt": "Estudos de Caso",
            "target_keyword_pt": "manifesto hsn labs consultoria agentes ia"
        },
        {
            "slug_en": "ontology-vs-database-schema",
            "slug_pt": "ontologia-vs-schema-banco-dados",
            "title_en": "Ontology vs. Database Schema: Why Relational Tables Break Agents",
            "title_pt": "Ontologia vs Schema de Banco de Dados: Por Que Tabelas Relacionais Quebram Agentes",
            "category_en": "Why Agents Fail",
            "category_pt": "Por Que Agentes Falham",
            "target_keyword_pt": "ontologia versus schema banco relacional diferenca"
        },
        {
            "slug_en": "ontology-vs-knowledge-graph",
            "slug_pt": "ontologia-vs-grafo-conhecimento",
            "title_en": "Ontology vs. Knowledge Graph: Key Differences, Architecture, and Agent Reliability",
            "title_pt": "Ontologia vs Grafo de Conhecimento: Diferencas Chave e Arquitetura",
            "category_en": "Agent Development Life Cycle",
            "category_pt": "Ciclo de Vida de Desenvolvimento de Agentes",
            "target_keyword_pt": "diferenca ontologia e grafo de conhecimento"
        },
        {
            "slug_en": "palantir-aip-bootcamp-operational-ontology",
            "slug_pt": "palantir-aip-bootcamp-ontologia-operacional",
            "title_en": "The Architecture of Palantir AIP: Why Enterprise Agents Require an Operational Ontology",
            "title_pt": "A Arquitetura do Palantir AIP: Por Que Agentes Exigem Ontologia Operacional",
            "category_en": "Agent Development Life Cycle",
            "category_pt": "Ciclo de Vida de Desenvolvimento de Agentes",
            "target_keyword_pt": "arquitetura palantir aip ontologia analise"
        },
        {
            "slug_en": "palantir-pricing-tco-and-open-alternatives",
            "slug_pt": "preco-palantir-tco-alternativas-abertas",
            "title_en": "The Real TCO of Palantir: The Dollar Barrier and Modern Open Alternatives",
            "title_pt": "O TCO Real da Palantir: A Barreira em Dolar e Alternativas Abertas",
            "category_en": "Agentic Economics",
            "category_pt": "Economia Agentica",
            "target_keyword_pt": "custo palantir aip alternativas opensource tco"
        },
        {
            "slug_en": "palantir-vs-databricks-agent-architecture",
            "slug_pt": "palantir-vs-databricks-arquitetura-agentes",
            "title_en": "Palantir vs Databricks: Why Data Lakes Fail at Agent Orchestration",
            "title_pt": "Palantir vs Databricks: Por Que Data Lakes Falham na Orquestracao de Agentes",
            "category_en": "Why Agents Fail",
            "category_pt": "Por Que Agentes Falham",
            "target_keyword_pt": "palantir versus databricks arquitetura agentes"
        },
        {
            "slug_en": "perimeter-isolation-mcp-data-contracts",
            "slug_pt": "isolamento-perimetro-mcp-contratos-dados",
            "title_en": "How We Protect Enterprise Databases from AI Agents",
            "title_pt": "Como Protegemos Bancos de Dados Enterprise de Agentes de IA",
            "category_en": "Agent Development Life Cycle",
            "category_pt": "Ciclo de Vida de Desenvolvimento de Agentes",
            "target_keyword_pt": "seguranca bancos de dados mcp isolamento perimetro"
        },
        {
            "slug_en": "protocol-arbitrage-claims-underwriting",
            "slug_pt": "arbitragem-protocolo-sinistros-subscricao",
            "title_en": "Protocol Arbitrage: Autonomous Multimodal Adjudication Across Complex Claims",
            "title_pt": "Arbitragem de Protocolos: Liquidacao Multimodal Autonoma de Sinistros",
            "category_en": "Agentic Economics",
            "category_pt": "Economia Agentica",
            "target_keyword_pt": "liquidacao de sinistros seguros agentes ia"
        },
        {
            "slug_en": "the-operational-ontology",
            "slug_pt": "a-ontologia-operacional",
            "title_en": "The Operational Ontology: How Enterprises Connect LLMs to Proprietary State",
            "title_pt": "A Ontologia Operacional: Como Empresas Conectam LLMs aos Dados Proprietarios",
            "category_en": "Agent Development Life Cycle",
            "category_pt": "Ciclo de Vida de Desenvolvimento de Agentes",
            "target_keyword_pt": "ontologia operacional definicao arquitetura"
        },
        {
            "slug_en": "the-poc-graveyard",
            "slug_pt": "cemiterio-de-pocs",
            "title_en": "Why Agents Fail: The PoC Graveyard",
            "title_pt": "Por Que Agentes Falham: O Cemiterio de PoCs",
            "category_en": "Why Agents Fail",
            "category_pt": "Por Que Agentes Falham",
            "target_keyword_pt": "por que pocs de ia morrem antes de producao"
        },
        {
            "slug_en": "unconstrained-agents-finite-state-machines",
            "slug_pt": "agentes-ilimitados-maquinas-estados-finitos",
            "title_en": "Case Study: 42 Calls in a Loop at 2 AM",
            "title_pt": "Estudo de Caso: 42 Chamadas em Loop as 2 da Manha",
            "category_en": "Case Studies",
            "category_pt": "Estudos de Caso",
            "target_keyword_pt": "loops infinitos agentes ia maquina estados finitos"
        },
        {
            "slug_en": "what-is-an-ontology-for-ai-agents",
            "slug_pt": "o-que-e-uma-ontologia-para-agentes-ia",
            "title_en": "What Is an Ontology for AI Agents? The Definitive Guide",
            "title_pt": "O Que E uma Ontologia para Agentes de IA? O Guia Definitivo",
            "category_en": "Why Agents Fail",
            "category_pt": "Por Que Agentes Falham",
            "target_keyword_pt": "guia definitivo ontologia para agentes de ia"
        },
        {
            "slug_en": "why-rag-breaks-on-erp",
            "slug_pt": "por-que-rag-falha-em-erp",
            "title_en": "Why I Never Use Normal RAG on Financial ERPs",
            "title_pt": "Por Que RAG Tradicional Falha em ERPs Financeiros",
            "category_en": "Why Agents Fail",
            "category_pt": "Por Que Agentes Falham",
            "target_keyword_pt": "falhas de rag em erp contabil busca vetorial"
        }
    ]
}

# Add absolute path fields for blog posts
for item in routes_data["blog_posts"]:
    item["en_path"] = f"/blog/post/{item['slug_en']}/"
    item["pt_path"] = f"/blog/pt/post/{item['slug_pt']}/"

# Verify no parentheses in JSON representation
raw_json = json.dumps(routes_data, indent=2, ensure_ascii=False)
assert "(" not in raw_json and ")" not in raw_json, "ERRO: Parenteses encontrados em routes_data!"

out_path = Path("/Users/hugosoares/blog_hsn_labs/i18n/routes-map.json")
out_path.write_text(raw_json, encoding="utf-8")

site_out_path = Path("/Users/hugosoares/site_hsn_labs/i18n/routes-map.json")
site_out_path.write_text(raw_json, encoding="utf-8")

print(f"Salvo routes-map.json com sucesso em ambos os repositorios. Total posts: {len(routes_data['blog_posts'])}")
