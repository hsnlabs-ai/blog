import os
import re
from pathlib import Path

POSTS_DIR = Path("/Users/hugosoares/blog_hsn_labs/docs/post")

CATEGORY_MAP = {
    "Economia Agêntica e Fim do BPO": "Agentic Economy & BPO Collapse",
    "Linha de Frente e Estudos de Caso": "Frontline & Case Studies",
    "Arquitetura e Sistemas Agênticos": "Deterministic Architecture & Systems",
    "Arquitetura e Engenharia Determinística": "Deterministic Architecture & Systems"
}

TAG_MAP = {
    "economia": "economics",
    "cobranca": "collections",
    "rh-tech": "hr-tech",
    "margem": "margins",
    "estudos-de-caso": "case-studies",
    "consultoria": "consulting",
    "sprint": "sprint",
    "seguros": "insurance",
    "arbitragem": "arbitrage",
    "suporte-erp": "erp-support",
    "helpdesk": "helpdesk",
    "rpa": "rpa",
    "automacao": "automation",
    "poc": "poc",
    "falhas-de-ia": "ai-failures",
    "arquitetura": "architecture",
    "producao": "production",
    "auditoria": "audit",
    "loop-api": "api-loops",
    "confiabilidade": "reliability",
    "legados": "legacy-systems",
    "substituicao": "replacement",
    "ebitda": "ebitda",
    "c-suite": "c-suite",
    "bpo": "bpo",
    "mcp": "mcp",
    "data-contracts": "data-contracts",
    "latam-airlines": "latam-airlines",
    "llm-judge": "llm-judge",
    "rag": "rag",
    "erp": "erp",
    "legacy-core": "legacy-core",
    "mainframe": "mainframe",
    "schema-drift": "schema-drift",
    "guardrails": "guardrails",
    "state-machines": "state-machines",
    "legacy-it": "legacy-it",
    "hsn-labs": "hsn-labs",
    "manifesto": "manifesto"
}

DESCRIPTION_MAP = {
    "autonomous-negotiations-collections-contracts.md": "Production architecture for autonomous collections, contract negotiation, and high-velocity commercial execution.",
    "balance-sheet-guard-bpo-extinction.md": "Operational field lessons on the structural collapse of enterprise HR outsourcing contracts and manual workflows.",
    "bpo-replacement-matrix.md": "Quantitative framework analyzing unit economics, operational metrics, and margin impact of replacing legacy BPO contracts with autonomous software agents.",
    "c-suite-margin-protection-playbook.md": "Executive blueprint for boardrooms and CFOs defending operational margins against legacy IT cost structures in the agentic economy.",
    "chatbot-vs-agent.md": "Critical architectural differences between conversational chatbots and deterministic enterprise agents mutating live ERP state.",
    "collapse-of-legacy-rpa.md": "Why brittle screen-recording bots are collapsing in enterprise environments and how deterministic agent architectures replace them.",
    "cost-legacy-it.md": "Economic and technical audit of runaway costs and execution risks caused by unbounded stochastic AI on legacy enterprise infrastructure.",
    "death-of-tier-1-erp-helpdesk.md": "The structural collapse of hourly billable support models across enterprise ERP consultancies and IT helpdesks.",
    "five-day-architecture-sprint.md": "Why traditional Big 4 strategy slide decks fail to deliver working agentic software in complex enterprise production environments.",
    "integration-drift.md": "How to detect and guard production agent workflows against silent runtime breaks caused by upstream schema and API drift.",
    "latam-airlines-case-study.md": "Field post-mortem on deploying deterministic enterprise agents in low-margin, high-throughput commercial aviation operations.",
    "legacy-core-backing-engine.md": "Why legacy core transaction systems remain the indispensable deterministic foundation powering autonomous enterprise agents.",
    "llm-as-judge-fallacy.md": "Structural vulnerabilities and compliance liabilities of relying on stochastic LLM evaluators to audit critical financial decisions.",
    "manifesto.md": "Foundational thesis of HSN Labs: building production-grade enterprise agent architectures on executable domain ontologies.",
    "perimeter-isolation-mcp-data-contracts.md": "Architectural patterns for perimeter isolation, context contracts, and cryptographic access boundaries shielding enterprise data from AI agents.",
    "protocol-arbitrage-claims-underwriting.md": "Autonomous multimodal adjudication and real-time protocol arbitrage across complex insurance claims and healthcare underwriting.",
    "the-poc-graveyard.md": "Root cause post-mortem on why ninety percent of enterprise AI proofs of concept fail before reaching live production.",
    "unconstrained-agents-finite-state-machines.md": "Emergency incident audit and architectural remedy for unbounded agent API loops through deterministic finite state machines.",
    "why-rag-breaks-on-erp.md": "Why vector similarity retrieval corrupts arithmetic precision and ledger integrity in enterprise financial ERPs."
}

def migrate_post(file_path: Path):
    text = file_path.read_text(encoding="utf-8")
    
    # Split frontmatter
    match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        print(f"Skipping {file_path.name}: no frontmatter found")
        return
    
    fm_text, body = match.group(1), match.group(2)
    filename = file_path.name
    
    # 1. Update Category
    for pt_cat, en_cat in CATEGORY_MAP.items():
        fm_text = re.sub(r"^category:\s*" + re.escape(pt_cat) + r"$", f"category: {en_cat}", fm_text, flags=re.MULTILINE)
    
    # 2. Update Tags
    for pt_tag, en_tag in TAG_MAP.items():
        fm_text = re.sub(r"(\s*-\s*)" + re.escape(pt_tag) + r"$", r"\1" + en_tag, fm_text, flags=re.MULTILINE)
    
    # 3. Update Description
    new_desc = DESCRIPTION_MAP.get(filename)
    if new_desc:
        # Escape any double quotes in description
        escaped_desc = new_desc.replace('"', '\\"')
        fm_text = re.sub(r"description:.*?(?=\n\w|\n---|\Z)", f'description: "{escaped_desc}"', fm_text, flags=re.DOTALL)
    
    new_content = f"---\n{fm_text.strip()}\n---\n{body}"
    file_path.write_text(new_content, encoding="utf-8")
    print(f"Migrated {filename} successfully")

def main():
    files = sorted(POSTS_DIR.glob("*.md"))
    print(f"Migrating {len(files)} posts...")
    for f in files:
        migrate_post(f)
    print("All posts migrated.")

if __name__ == "__main__":
    main()
