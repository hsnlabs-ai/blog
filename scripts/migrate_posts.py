import os
import re
import glob
import yaml
from pathlib import Path

BASE_DIR = Path("/Users/hugosoares/blog_hsn_labs")
OLD_POSTS_DIR = BASE_DIR / "docs" / "writing" / "posts"
NEW_POSTS_DIR = BASE_DIR / "docs" / "post"

NEW_POSTS_DIR.mkdir(parents=True, exist_ok=True)

CATEGORY_MAP = {
    # Arquitetura e Sistemas Agênticos
    "chatbot-vs-agent.md": ("Arquitetura e Sistemas Agênticos", ["arquitetura", "guardrails", "state-machines"]),
    "cost-legacy-it.md": ("Arquitetura e Sistemas Agênticos", ["arquitetura", "legacy-it", "confiabilidade"]),
    "integration-drift.md": ("Arquitetura e Sistemas Agênticos", ["arquitetura", "schema-drift", "mcp"]),
    "legacy-core-backing-engine.md": ("Arquitetura e Sistemas Agênticos", ["arquitetura", "legacy-core", "mainframe"]),
    "llm-as-judge-fallacy.md": ("Arquitetura e Sistemas Agênticos", ["arquitetura", "llm-judge", "auditoria"]),
    "perimeter-isolation-mcp-data-contracts.md": ("Arquitetura e Sistemas Agênticos", ["arquitetura", "mcp", "data-contracts"]),
    "why-rag-breaks-on-erp.md": ("Arquitetura e Sistemas Agênticos", ["arquitetura", "rag", "erp"]),

    # Economia Agêntica e Fim do BPO
    "autonomous-negotiations-collections-contracts.md": ("Economia Agêntica e Fim do BPO", ["economia", "cobranca", "bpo"]),
    "balance-sheet-guard-bpo-extinction.md": ("Economia Agêntica e Fim do BPO", ["economia", "bpo", "rh-tech"]),
    "bpo-replacement-matrix.md": ("Economia Agêntica e Fim do BPO", ["economia", "ebitda", "bpo"]),
    "c-suite-margin-protection-playbook.md": ("Economia Agêntica e Fim do BPO", ["economia", "c-suite", "margem"]),
    "collapse-of-legacy-rpa.md": ("Economia Agêntica e Fim do BPO", ["economia", "rpa", "automacao"]),
    "death-of-tier-1-erp-helpdesk.md": ("Economia Agêntica e Fim do BPO", ["economia", "suporte-erp", "helpdesk"]),

    # Linha de Frente e Estudos de Caso
    "five-day-architecture-sprint.md": ("Linha de Frente e Estudos de Caso", ["estudos-de-caso", "consultoria", "sprint"]),
    "latam-airlines-case-study.md": ("Linha de Frente e Estudos de Caso", ["estudos-de-caso", "latam-airlines", "producao"]),
    "manifesto.md": ("Linha de Frente e Estudos de Caso", ["estudos-de-caso", "hsn-labs", "manifesto"]),
    "protocol-arbitrage-claims-underwriting.md": ("Linha de Frente e Estudos de Caso", ["estudos-de-caso", "seguros", "arbitragem"]),
    "the-poc-graveyard.md": ("Linha de Frente e Estudos de Caso", ["estudos-de-caso", "poc", "falhas-de-ia"]),
    "unconstrained-agents-finite-state-machines.md": ("Linha de Frente e Estudos de Caso", ["estudos-de-caso", "producao", "loop-api"]),
}

DESCRIPTIONS = {
    "chatbot-vs-agent.md": "Diferencas criticas entre chatbots conversacionais e agentes orientados a regras de negócio para substituicao confiavel de processos corporativos.",
    "cost-legacy-it.md": "Analise economica e tecnica dos custos de falhas de IA sem limites de execução integradas a infraestruturas legadas.",
    "integration-drift.md": "Como detectar e blindar agentes em producao contra quebras silenciosas provocadas por desvios de esquemas de dados.",
    "legacy-core-backing-engine.md": "Por que sistemas transacionais legados sao a fundacao de execucao confiavel para operacoes agenticas escalaveis.",
    "llm-as-judge-fallacy.md": "As vulnerabilidades e falhas estruturais de utilizar modelos estocasticos para auditar decisoes financeiras criticas.",
    "perimeter-isolation-mcp-data-contracts.md": "Padroes avancados de isolamento de perimetro e contratos de contexto para blindar bancos corporativos.",
    "why-rag-breaks-on-erp.md": "Por que a busca vetorial por similaridade corrompe a precisao aritmetica exigida por livros contabeis de ERPs.",
    "autonomous-negotiations-collections-contracts.md": "Arquitetura para cobrancas autonomas e execucao de contratos comerciais em alta velocidade operacional.",
    "balance-sheet-guard-bpo-extinction.md": "Licoes operacionais sobre o declinio inevitavel de contratos de outsourcing de processos humanos em RH.",
    "bpo-replacement-matrix.md": "Matriz quantitativa para substituicao de servicos terceirizados por agentes de software autonomos.",
    "c-suite-margin-protection-playbook.md": "Guia estrategico para conselhos de administracao defenderem margens operacionais na era agentica.",
    "collapse-of-legacy-rpa.md": "Por que bots de gravacao de tela estao em colapso e como arquiteturas de agentes os substituem.",
    "death-of-tier-1-erp-helpdesk.md": "O colapso inevitavel do modelo de suporte tecnico faturado por hora em implementacoes de ERP.",
    "five-day-architecture-sprint.md": "Por que apresentacoes genericas de consultorias tradicionais falham em resolver problemas agenticos em producao.",
    "latam-airlines-case-study.md": "Estudo de caso pratico de implementacao de agentes em ambiente de alta volumetria e margem apertada.",
    "manifesto.md": "A tese fundadora da boutique HSN Labs e o compromisso com arquitetura agêntica enterprise para grandes empresas.",
    "protocol-arbitrage-claims-underwriting.md": "Uso de arbitragem multimodais autonoma para liquidacao de sinistros complexos em saude e seguros.",
    "the-poc-graveyard.md": "As razoes estruturais pelas quais prototipos de IA corporativa morrem antes de alcancar a producao real.",
    "unconstrained-agents-finite-state-machines.md": "Auditoria de emergencia detalhando a correcao de loops infinitos de chamadas em agentes de producao.",
}

posts = sorted(glob.glob(str(OLD_POSTS_DIR / "*.md")))

for p_path in posts:
    filename = Path(p_path).name
    with open(p_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    parts = raw_text.split("---")
    body = raw_text
    meta = {}
    if len(parts) >= 3:
        meta = yaml.safe_load(parts[1]) or {}
        body = "---".join(parts[2:]).strip()
        
    h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = meta.get("title")
    if not title:
        if h1_match:
            title = h1_match.group(1).strip()
            # remove icons if present
            title = re.sub(r":[a-z0-9_\-]+:", "", title).strip()
        else:
            title = filename.replace(".md", "").replace("-", " ").title()
            
    # Clean emojis / colons from title
    title = re.sub(r":[a-z0-9_\-]+:", "", title).strip()
    
    date = str(meta.get("date", "2026-08-01"))
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        date = "2026-08-01"
        
    category, tags = CATEGORY_MAP.get(filename, ("Arquitetura e Sistemas Agênticos", ["agentes", "engenharia"]))
    desc = DESCRIPTIONS.get(filename, "Artigo tecnico sobre arquitetura de sistemas agenticos em producao.")
    
    # Ensure <!-- more --> exists in body
    if "<!-- more -->" not in body:
        # Find first paragraph after H1
        lines = body.split("\n")
        new_lines = []
        inserted = False
        saw_h1 = False
        para_lines = 0
        for line in lines:
            new_lines.append(line)
            if line.startswith("# "):
                saw_h1 = True
            elif saw_h1 and line.strip() != "":
                para_lines += 1
            elif saw_h1 and para_lines > 0 and line.strip() == "" and not inserted:
                new_lines.append("<!-- more -->\n")
                inserted = True
        if not inserted:
            new_lines.append("\n<!-- more -->\n")
        body = "\n".join(new_lines)
        
    new_frontmatter = {
        "title": title,
        "date": date,
        "category": category,
        "tags": tags,
        "description": desc,
        "author": "Hugo S. Nascimento"
    }
    
    dest_file = NEW_POSTS_DIR / filename
    with open(dest_file, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(new_frontmatter, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        f.write("---\n\n")
        f.write(body.strip())
        f.write("\n")
        
print(f"Migrados {len(posts)} posts com sucesso para docs/post/")
