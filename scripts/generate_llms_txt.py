#!/usr/bin/env python3
import json
import yaml
from pathlib import Path

BASE_DIR = Path("/Users/hugosoares/blog_hsn_labs")
DOCS_DIR = BASE_DIR / "docs"
ROUTES_FILE = BASE_DIR / "i18n" / "routes-map.json"
LLMS_FILE = DOCS_DIR / "llms.txt"


def load_post_meta(md_path: Path) -> dict:
    parts = md_path.read_text(encoding="utf-8").split("---")
    if len(parts) >= 3:
        return yaml.safe_load(parts[1]) or {}
    return {}


def main():
    routes = json.loads(ROUTES_FILE.read_text(encoding="utf-8")).get("blog_posts", [])
    en_entries = []
    pt_entries = []

    for item in routes:
        slug_en = item["slug_en"]
        slug_pt = item["slug_pt"]
        en_meta = load_post_meta(DOCS_DIR / "post" / f"{slug_en}.md")
        pt_meta = load_post_meta(DOCS_DIR / "pt" / "post" / f"{slug_pt}.md")
        en_entries.append({
            "date": str(en_meta.get("date", "")),
            "title": str(en_meta.get("title", item.get("title_en", slug_en))),
            "desc": str(en_meta.get("description", "")).strip(),
            "cat": str(en_meta.get("category", "")),
            "url": f"https://hsnlabs.ai/blog/post/{slug_en}/",
        })
        pt_entries.append({
            "date": str(pt_meta.get("date", "")),
            "title": str(pt_meta.get("title", item.get("title_pt", slug_pt))),
            "desc": str(pt_meta.get("description", "")).strip(),
            "cat": str(pt_meta.get("category", "")),
            "url": f"https://hsnlabs.ai/blog/pt/post/{slug_pt}/",
        })

    en_entries.sort(key=lambda x: x["date"], reverse=True)
    pt_entries.sort(key=lambda x: x["date"], reverse=True)

    header = """# hsnlabs

> AI architecture consulting boutique solving why AI agents fail in production. We handle the complete lifecycle: ontology design, infrastructure, orchestration, and continuous evaluation in production.

## Canonical Positioning & Value Proposition
- Overview: https://hsnlabs.ai/
hsnlabs is an AI architecture consulting boutique. We build production-grade deep agents tailored to the real business ontology of your enterprise.
- Why AI Agents Fail in Production: https://hsnlabs.ai/#services
Over ninety percent of enterprise agent proofs of concept fail when transitioning to production because stochastic models hit legacy systems, unmanaged drift, and rigid business rules. We solve runtime failure through hybrid engineering.
- Consulting Over Staffing: https://hsnlabs.ai/#services
Specialized architectural guidance and hands-on implementation rather than body shopping or hourly junior IT outsourcing.

## Why Agents Fail & Core Failure Modes
- Why Agents Fail: https://hsnlabs.ai/#services
Most enterprise AI agents break when exposed to messy company data, complex compliance, and strict business rules.
- SaaS Billing Reduction: https://hsnlabs.ai/#services
Enterprises spend heavily on recurring software subscriptions and the operators required to use them. Our agents connect directly to company data, automating manual workflows and cutting annual software bills.
- Failed Pilots: https://hsnlabs.ai/#services
Enterprises spend significant capital on chatbot demos that dazzle in boardrooms but never reach production when facing messy production data and edge cases.
- Operational Errors: https://hsnlabs.ai/#services
Probabilistic models cannot guarantee transactional integrity without strict execution boundaries, risking regulatory fines and bad ledger writes.
- Agent Development Life Cycle Stack: https://hsnlabs.ai/#services
Governing the complete Agent Development Lifecycle using market standards like LangGraph and LangSmith for rigorous evaluation, tracing, and production observability.

## Strategic Advisory: The Disruption Gap
- Agentic AI Advisory: https://hsnlabs.ai/advisory/
Guiding C-levels through the structural transformation required to protect market share, defend unit margins, and deploy autonomous workflows safely. Core pillars: Operating Models, Margin Defense, Progressive Migration, and Executive Governance.

## Entry Engagement: Agentic Bootcamp™
- Bootcamp Deployment Protocol: https://hsnlabs.ai/bootcamp/
An intensive 1-to-5-day Forward Deployed Engineering sprint inside client infrastructure. We validate data access, connect tools, and deliver a working sandbox prototype and executive business case with verified operational ROI. Qualifying enterprise accounts unlock fully sponsored terms or a 100% Performance Rebate credited toward production rollout.

## Regulated Enterprise Verticals
- Banking and Capital Markets: https://hsnlabs.ai/#verticals
Eliminating hallucinations on financial ledgers through code-level transaction validation and immutable audit trails.
- Healthcare Operations: https://hsnlabs.ai/#verticals
Verifiable protocol adherence and zero-exfiltration architectures across healthcare billing and medical workflows.
- Legacy ERP and BPO: https://hsnlabs.ai/#verticals
Anchoring agentic workflows to validated state machines across legacy ERPs to replace fragile BPO operations.

## Open Architecture Frameworks
- The Agentic Canvas™: https://hsnlabs.ai/en/canvas/
10-block architecture framework by hsnlabs for structuring and certifying enterprise agentic systems across two tracks — Agentic Products and Agentic Employees — covering legacy data ontologies, deterministic guardrails, evaluation harnesses, and human-in-the-loop governance.

## Knowledge Engine & Research
- hsnlabs Blog: https://hsnlabs.ai/blog/
Technical posts, case studies, and post-mortems on enterprise agent architectures and runtime observability.
- RSS Feed EN: https://hsnlabs.ai/blog/feed_rss_created.xml
- JSON Feed EN: https://hsnlabs.ai/blog/feed_json_created.json
"""

    en_lines = []
    for e in en_entries:
        en_lines.append(f"- {e['title']}: {e['url']}")
        if e["desc"]:
            en_lines.append(f"  {e['desc']}")

    pt_header = """
## Documentação e Recursos em Português
- Visão Geral em Português: https://hsnlabs.ai/
- The Agentic Canvas™: https://hsnlabs.ai/canvas/
- Bootcamp de Agentes: https://hsnlabs.ai/bootcamp/
- Advisory de Arquitetura: https://hsnlabs.ai/advisory/
- Servidores MCP Enterprise: https://hsnlabs.ai/mcp/
- Blog hsnlabs em Português: https://hsnlabs.ai/blog/pt/
- Feed RSS em Português: https://hsnlabs.ai/blog/feed_rss_pt.xml
- Feed JSON em Português: https://hsnlabs.ai/blog/feed_json_pt.json
"""

    pt_lines = []
    for p in pt_entries:
        pt_lines.append(f"- {p['title']}: {p['url']}")
        if p["desc"]:
            pt_lines.append(f"  {p['desc']}")

    footer = """
## Open Source Ecosystem
- hsnlabs GitHub: https://github.com/hsnlabs-ai
Open-source repositories and engineering tools for enterprise agents.

## Contact & Channels
- Contact Form: https://hsnlabs.ai/#contact
- GitHub: https://github.com/hsnlabs-ai
"""

    full_text = header + "\n".join(en_lines) + "\n" + pt_header + "\n".join(pt_lines) + "\n" + footer
    LLMS_FILE.write_text(full_text, encoding="utf-8")
    print(f"Generated {LLMS_FILE} with {len(en_entries)} EN and {len(pt_entries)} PT entries.")


if __name__ == "__main__":
    main()
