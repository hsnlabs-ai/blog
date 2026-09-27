import glob
import re

SLUG_TO_POST_DIR = {
    "why-agents-fail-the-poc-graveyard": "../the-poc-graveyard/",
    "chatbot-vs-agent-why-replacing-bpos-requires-deterministic-guardrails": "../chatbot-vs-agent/",
    "the-rpa-market-is-collapsing": "../collapse-of-legacy-rpa/",
    "what-i-learned-building-hr-tech-about-dying-bpo-contracts": "../balance-sheet-guard-bpo-extinction/",
    "protocol-arbitrage-autonomous-multimodal-adjudication-in-healthcare-and-underwriting": "../protocol-arbitrage-claims-underwriting/",
    "the-death-of-tier-1-support-why-erp-consultancies-and-it-helpdesks-cannot-defend-the-billable-hour": "../death-of-tier-1-erp-helpdesk/",
    "high-velocity-operations-autonomous-negotiation-collections-and-contract-execution": "../autonomous-negotiations-collections-contracts/",
    "legacy-core-systems-will-not-die-they-are-the-engine-behind-autonomous-agents": "../legacy-core-backing-engine/",
    "how-we-protect-enterprise-databases-from-ai-agents": "../perimeter-isolation-mcp-data-contracts/",
    "the-bpo-replacement-matrix-operational-and-financial-impact-of-deterministic-agents": "../bpo-replacement-matrix/",
    "case-study-42-calls-in-a-loop-at-2-am": "../unconstrained-agents-finite-state-machines/",
    "the-cost-of-non-deterministic-ai-in-legacy-it": "../cost-legacy-it/",
    "the-c-suite-transition-playbook-protecting-margins-in-the-agentic-economy": "../c-suite-margin-protection-playbook/",
    "why-big-4-slide-decks-fail-on-agent-projects": "../five-day-architecture-sprint/",
    "the-integration-drift-when-prompts-break-production": "../integration-drift/",
    "why-i-never-use-normal-rag-on-financial-erps": "../why-rag-breaks-on-erp/",
    "why-llm-as-a-judge-fails-in-banking": "../llm-as-judge-fallacy/",
    "latam-airlines-deterministic-agents-in-a-3-percent-margin-business": "../latam-airlines-case-study/",
    "latam-airlines-case-study": "../latam-airlines-case-study/",
    "why-i-built-hsn-labs": "../manifesto/",
}

posts = glob.glob("/Users/hugosoares/blog_hsn_labs/docs/post/*.md")

count = 0
for p in posts:
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace href="filename.md"
    for slug, dest in SLUG_TO_POST_DIR.items():
        stem = dest.replace("../", "").replace("/", "")
        md_file = f"{stem}.md"
        content = content.replace(f'href="{md_file}"', f'href="{dest}"')
        content = content.replace(f'href="../post/{md_file}"', f'href="{dest}"')

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1

print(f"Links entre posts ajustados para relative directory em {count} posts.")
