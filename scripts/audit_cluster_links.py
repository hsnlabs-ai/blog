import glob
import os
import re
import yaml

CLUSTERS = {
    "why-agents-fail": {
        "hub": "what-is-an-ontology-for-ai-agents",
        "spokes": [
            "the-poc-graveyard",
            "why-rag-breaks-on-erp",
            "integration-drift",
            "llm-as-judge-fallacy",
            "ontology-vs-database-schema",
            "palantir-vs-databricks-agent-architecture"
        ]
    },
    "agent-development-life-cycle": {
        "hub": "how-to-build-an-enterprise-ontology-from-scratch",
        "spokes": [
            "the-operational-ontology",
            "how-to-build-operational-ontology-python-mcp",
            "ontology-vs-knowledge-graph",
            "palantir-aip-bootcamp-operational-ontology",
            "perimeter-isolation-mcp-data-contracts",
            "legacy-core-backing-engine",
            "five-day-architecture-sprint",
            "chatbot-vs-agent"
        ]
    },
    "future-of-work": {
        "hub": "kafka-metamorfose-ia-futuro-do-trabalho",
        "spokes": [
            "collapse-of-legacy-rpa",
            "balance-sheet-guard-bpo-extinction",
            "death-of-tier-1-erp-helpdesk"
        ]
    },
    "agentic-economics": {
        "hub": "bpo-replacement-matrix",
        "spokes": [
            "buy-versus-build-b2b-enterprise-crm",
            "palantir-pricing-tco-and-open-alternatives",
            "c-suite-margin-protection-playbook",
            "protocol-arbitrage-claims-underwriting",
            "cost-legacy-it"
        ]
    },
    "case-studies": {
        "hub": "manifesto",
        "spokes": [
            "cleveland-clinic-case-study-operational-agents",
            "latam-airlines-case-study",
            "unconstrained-agents-finite-state-machines",
            "autonomous-negotiations-collections-contracts"
        ]
    }
}

link_pattern = re.compile(r'href=[\'"](?:\.\./|/blog/post/|post/)([a-zA-Z0-9_-]+)/?[\'"]')

print("=== AUDITORIA DE LINKS INTERNOS POR CLUSTER ===")

for cat, data in CLUSTERS.items():
    hub = data["hub"]
    spokes = data["spokes"]
    print(f"\nCluster: {cat}")
    
    # Hub check
    hub_file = f"docs/post/{hub}.md"
    if os.path.exists(hub_file):
        with open(hub_file, "r", encoding="utf-8") as f:
            content = f.read()
        hub_links = set(link_pattern.findall(content))
        linked_spokes = [s for s in spokes if s in hub_links]
        missing_spokes = [s for s in spokes if s not in hub_links]
        other_links = [l for l in hub_links if l not in spokes]
        print(f"  HUB [{hub}]: {len(linked_spokes)}/{len(spokes)} spokes referenciados | Links fora do cluster: {len(other_links)}")
        if missing_spokes:
            print(f"    Spokes ausentes no Hub: {missing_spokes}")
    else:
        print(f"  HUB [{hub}]: ARQUIVO INEXISTENTE")
        
    # Spokes check
    for sp in spokes:
        sp_file = f"docs/post/{sp}.md"
        if os.path.exists(sp_file):
            with open(sp_file, "r", encoding="utf-8") as f:
                content = f.read()
            sp_links = set(link_pattern.findall(content))
            has_hub = hub in sp_links
            sibling_links = [s for s in spokes if s != sp and s in sp_links]
            out_of_cluster = [l for l in sp_links if l != hub and l not in spokes]
            status = "CONECTADO AO HUB" if has_hub else "SEM LINK P/ HUB"
            print(f"  SPOKE [{sp}]: {status} | Irmaos: {len(sibling_links)}/{len(spokes)-1} | Outros: {len(out_of_cluster)}")
        else:
            print(f"  SPOKE [{sp}]: ARQUIVO INEXISTENTE")
