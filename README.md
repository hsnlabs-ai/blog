# HSN Labs Personal Hub

Personal engineering and consulting hub for Hugo Nascimento, built with MkDocs and Material for MkDocs.

## Concept
Based on the "Hub and Spoke" strategy. This site is the Hub. The 30 spokes are content pieces (writing/essays) driving inbound traffic from Level 3 Economic Buyers (CFOs, CEOs). 
The goal is to convert technical authority into high-ticket enterprise consulting (Advisory, Audit, 5-Day Agentic Bootcamp).

## Architecture
- **Generator:** MkDocs
- **Theme:** Material for MkDocs (`mkdocs-material`)
- **Hosting:** GitHub Pages (Subdirectory routing via `hsn-labs.github.io/blog` or similar).

## Local Development
```bash
uv venv
source .venv/bin/activate
uv pip install mkdocs mkdocs-material
mkdocs serve
```
