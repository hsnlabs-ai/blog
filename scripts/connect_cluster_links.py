import json
import os
import re

BASE_DIR = "/Users/hugosoares/blog_hsn_labs"
DOCS_EN = os.path.join(BASE_DIR, "docs/post")
DOCS_PT = os.path.join(BASE_DIR, "docs/pt/post")

with open(os.path.join(BASE_DIR, "i18n/routes-map.json"), "r", encoding="utf-8") as f:
    routes = json.load(f)

posts_map = {p["slug_en"]: p for p in routes["blog_posts"]}

CLUSTERS = {
    "Why Agents Fail": {
        "hub": "what-is-an-ontology-for-ai-agents",
        "spokes": [
            "the-poc-graveyard",
            "why-rag-breaks-on-erp",
            "integration-drift",
            "llm-as-judge-fallacy",
            "ontology-vs-database-schema",
            "palantir-vs-databricks-agent-architecture"
        ],
        "spoke_siblings": {
            "the-poc-graveyard": ["why-rag-breaks-on-erp", "integration-drift"],
            "why-rag-breaks-on-erp": ["ontology-vs-database-schema", "the-poc-graveyard"],
            "integration-drift": ["the-poc-graveyard", "llm-as-judge-fallacy"],
            "llm-as-judge-fallacy": ["integration-drift", "palantir-vs-databricks-agent-architecture"],
            "ontology-vs-database-schema": ["why-rag-breaks-on-erp", "palantir-vs-databricks-agent-architecture"],
            "palantir-vs-databricks-agent-architecture": ["ontology-vs-database-schema", "llm-as-judge-fallacy"]
        }
    },
    "Agent Development Life Cycle": {
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
        ],
        "spoke_siblings": {
            "the-operational-ontology": ["ontology-vs-knowledge-graph", "how-to-build-operational-ontology-python-mcp"],
            "how-to-build-operational-ontology-python-mcp": ["the-operational-ontology", "perimeter-isolation-mcp-data-contracts"],
            "ontology-vs-knowledge-graph": ["the-operational-ontology", "palantir-aip-bootcamp-operational-ontology"],
            "palantir-aip-bootcamp-operational-ontology": ["ontology-vs-knowledge-graph", "legacy-core-backing-engine"],
            "perimeter-isolation-mcp-data-contracts": ["how-to-build-operational-ontology-python-mcp", "legacy-core-backing-engine"],
            "legacy-core-backing-engine": ["perimeter-isolation-mcp-data-contracts", "chatbot-vs-agent"],
            "five-day-architecture-sprint": ["the-operational-ontology", "perimeter-isolation-mcp-data-contracts"],
            "chatbot-vs-agent": ["the-operational-ontology", "legacy-core-backing-engine"]
        }
    },
    "Future of Work": {
        "hub": "kafka-metamorfose-ia-futuro-do-trabalho",
        "spokes": [
            "collapse-of-legacy-rpa",
            "balance-sheet-guard-bpo-extinction",
            "death-of-tier-1-erp-helpdesk"
        ],
        "spoke_siblings": {
            "collapse-of-legacy-rpa": ["balance-sheet-guard-bpo-extinction", "death-of-tier-1-erp-helpdesk"],
            "balance-sheet-guard-bpo-extinction": ["collapse-of-legacy-rpa", "death-of-tier-1-erp-helpdesk"],
            "death-of-tier-1-erp-helpdesk": ["collapse-of-legacy-rpa", "balance-sheet-guard-bpo-extinction"]
        }
    },
    "Agentic Economics": {
        "hub": "bpo-replacement-matrix",
        "spokes": [
            "buy-versus-build-b2b-enterprise-crm",
            "palantir-pricing-tco-and-open-alternatives",
            "c-suite-margin-protection-playbook",
            "protocol-arbitrage-claims-underwriting",
            "cost-legacy-it"
        ],
        "spoke_siblings": {
            "buy-versus-build-b2b-enterprise-crm": ["palantir-pricing-tco-and-open-alternatives", "c-suite-margin-protection-playbook"],
            "palantir-pricing-tco-and-open-alternatives": ["buy-versus-build-b2b-enterprise-crm", "cost-legacy-it"],
            "c-suite-margin-protection-playbook": ["buy-versus-build-b2b-enterprise-crm", "protocol-arbitrage-claims-underwriting"],
            "protocol-arbitrage-claims-underwriting": ["c-suite-margin-protection-playbook", "cost-legacy-it"],
            "cost-legacy-it": ["palantir-pricing-tco-and-open-alternatives", "protocol-arbitrage-claims-underwriting"]
        }
    },
    "Case Studies": {
        "hub": "manifesto",
        "spokes": [
            "cleveland-clinic-case-study-operational-agents",
            "latam-airlines-case-study",
            "unconstrained-agents-finite-state-machines",
            "autonomous-negotiations-collections-contracts"
        ],
        "spoke_siblings": {
            "cleveland-clinic-case-study-operational-agents": ["latam-airlines-case-study", "unconstrained-agents-finite-state-machines"],
            "latam-airlines-case-study": ["cleveland-clinic-case-study-operational-agents", "autonomous-negotiations-collections-contracts"],
            "unconstrained-agents-finite-state-machines": ["cleveland-clinic-case-study-operational-agents", "autonomous-negotiations-collections-contracts"],
            "autonomous-negotiations-collections-contracts": ["latam-airlines-case-study", "unconstrained-agents-finite-state-machines"]
        }
    }
}

def clean_title_for_pt(title):
    # Ensure zero parentheses in PT title
    t = title.replace("(", "").replace(")", "").replace("  ", " ").strip()
    return t

def update_spoke_en(slug, hub_slug, siblings):
    filepath = os.path.join(DOCS_EN, f"{slug}.md")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    hub_info = posts_map[hub_slug]
    sib1_info = posts_map[siblings[0]]
    sib2_info = posts_map[siblings[1]]
    
    # Target replacement block
    new_section = (
        "## Strategic Resources and Related Essays\n"
        f'- <a href="../{hub_slug}/">{hub_info["title_en"]}</a>\n'
        f'- <a href="../{siblings[0]}/">{sib1_info["title_en"]}</a>\n'
        f'- <a href="../{siblings[1]}/">{sib2_info["title_en"]}</a>\n'
        '- <a href="https://hsnlabs.ai/bootcamp">Apply for the HSN Labs Five-Day Architecture Bootcamp</a>'
    )
    
    pattern = r"## Strategic Resources and Related (?:Essays|Posts)[\s\S]*?(?=\n## |\Z)"
    if re.search(pattern, content):
        content = re.sub(pattern, new_section, content)
    else:
        # Check if there is ## Sources
        if "## Sources" in content:
            # Place it before ## Sources or at the very end
            content = content.strip() + "\n\n" + new_section + "\n"
        else:
            content = content.strip() + "\n\n" + new_section + "\n"
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def update_spoke_pt(slug, hub_slug, siblings):
    spoke_info = posts_map[slug]
    pt_slug = spoke_info["slug_pt"]
    filepath = os.path.join(DOCS_PT, f"{pt_slug}.md")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    hub_info = posts_map[hub_slug]
    sib1_info = posts_map[siblings[0]]
    sib2_info = posts_map[siblings[1]]
    
    hub_title = clean_title_for_pt(hub_info["title_pt"])
    sib1_title = clean_title_for_pt(sib1_info["title_pt"])
    sib2_title = clean_title_for_pt(sib2_info["title_pt"])
    
    new_section = (
        "## Recursos Estrategicos e Posts Relacionados\n"
        f'- <a href="/blog/pt/post/{hub_info["slug_pt"]}/">{hub_title}</a>\n'
        f'- <a href="/blog/pt/post/{sib1_info["slug_pt"]}/">{sib1_title}</a>\n'
        f'- <a href="/blog/pt/post/{sib2_info["slug_pt"]}/">{sib2_title}</a>\n'
        '- <a href="https://hsnlabs.ai/pt/bootcamp/">Aplicar para o Bootcamp de Agentes Enterprise de 5 Dias da HSN Labs</a>'
    )
    
    pattern = r"## Recursos Estrat[eé]gicos e Posts Relacionados[\s\S]*?(?=\n## |\Z)"
    if re.search(pattern, content):
        content = re.sub(pattern, new_section, content)
    else:
        content = content.strip() + "\n\n" + new_section + "\n"
        
    assert "(" not in content and ")" not in content, f"ERRO: Parenteses gerados em {filepath}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def update_hub_en(hub_slug, spokes):
    filepath = os.path.join(DOCS_EN, f"{hub_slug}.md")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = ["## Related Field Notes and Technical Spokes"]
    for sp in spokes:
        sp_info = posts_map[sp]
        lines.append(f'- <a href="../{sp}/">{sp_info["title_en"]}</a>')
    lines.append('- <a href="https://hsnlabs.ai/bootcamp">Apply for the HSN Labs Five-Day Architecture Bootcamp</a>')
    new_section = "\n".join(lines)
    
    pattern = r"## (?:Related Field Notes and Technical Spokes|Strategic Resources and Related Essays)[\s\S]*?(?=\n## |\Z)"
    if re.search(pattern, content):
        content = re.sub(pattern, new_section, content)
    else:
        content = content.strip() + "\n\n" + new_section + "\n"
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def update_hub_pt(hub_slug, spokes):
    hub_info = posts_map[hub_slug]
    pt_slug = hub_info["slug_pt"]
    filepath = os.path.join(DOCS_PT, f"{pt_slug}.md")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = ["## Notas de Campo e Artigos Relacionados"]
    for sp in spokes:
        sp_info = posts_map[sp]
        sp_title = clean_title_for_pt(sp_info["title_pt"])
        lines.append(f'- <a href="/blog/pt/post/{sp_info["slug_pt"]}/">{sp_title}</a>')
    lines.append('- <a href="https://hsnlabs.ai/pt/bootcamp/">Aplicar para o Bootcamp de Agentes Enterprise de 5 Dias da HSN Labs</a>')
    new_section = "\n".join(lines)
    
    pattern = r"## (?:Notas de Campo e Artigos Relacionados|Recursos Estrat[eé]gicos e Posts Relacionados)[\s\S]*?(?=\n## |\Z)"
    if re.search(pattern, content):
        content = re.sub(pattern, new_section, content)
    else:
        content = content.strip() + "\n\n" + new_section + "\n"
        
    assert "(" not in content and ")" not in content, f"ERRO: Parenteses gerados no Hub PT {filepath}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

# Run process across all clusters
for cat, data in CLUSTERS.items():
    hub_slug = data["hub"]
    spokes = data["spokes"]
    spoke_siblings = data["spoke_siblings"]
    
    print(f"Atualizando Hub: {hub_slug}")
    update_hub_en(hub_slug, spokes)
    update_hub_pt(hub_slug, spokes)
    
    for sp in spokes:
        sibs = spoke_siblings[sp]
        print(f"  Atualizando Spoke: {sp} (irmaos: {sibs})")
        update_spoke_en(sp, hub_slug, sibs)
        update_spoke_pt(sp, hub_slug, sibs)

print("\nProcessamento concluido com sucesso!")
