import re
import yaml
from pathlib import Path

BASE_DIR = Path("/Users/hugosoares/blog_hsn_labs")
PT_POSTS_DIR = BASE_DIR / "docs" / "pt" / "post"
PT_INDEX_FILE = BASE_DIR / "docs" / "pt" / "index.md"

posts = []
if PT_POSTS_DIR.exists():
    for f in sorted(PT_POSTS_DIR.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        parts = content.split("---")
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1])
            posts.append({
                "slug": f.stem,
                "title": meta.get("title"),
                "date": str(meta.get("date")),
                "category": meta.get("category", ""),
                "description": meta.get("description", "")
            })

# Sort posts by date descending
posts.sort(key=lambda x: x["date"], reverse=True)

lines = []
lines.append("---")
lines.append("title: Hugo S. Nascimento")
lines.append("description: Ensaios e notas de campo sobre arquitetura de agentes enterprise, ontologias de dominio e execucao em producao.")
lines.append("---")
lines.append("")
lines.append("# Hugo S. Nascimento")
lines.append("")
lines.append("Sou CPTO na Eva People e Fundador da HSN Labs. Fundador de 3 startups investidas por venture capital, engenheiro e investidor.")
lines.append("")
lines.append("Meu foco operacional e **Arquitetura de Agentes Enterprise**. Construo arquiteturas multiagente customizadas sobre ontologias de dominio executaveis para operacoes corporativas de missao critica. Substituo operacoes manuais frageis de BPO e gargalos de TI legada por forcas de trabalho digitais autonomas que nao alucinam nem falham em producao.")
lines.append("")
lines.append("Arquiteturas entregues incluem **Deloitte**, **Santander**, **Softplan**, **Unipar Carbocloro**, **LWSA**, **Turbi**, **Caju**, **Cast Group** e **Insi**.")
lines.append("")
lines.append('<a href="https://hsnlabs.ai/pt/">HSN Labs Boutique</a> &nbsp;&bull;&nbsp; <a href="https://www.linkedin.com/in/hugosoaresnascimento/">LinkedIn</a> &nbsp;&bull;&nbsp; <a href="https://github.com/hsnlabs-ai/blog">GitHub</a> &nbsp;&bull;&nbsp; <a href="/blog/">English Version</a>')
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Ensaios de Engenharia e Notas de Campo")
lines.append("")

for p in posts:
    lines.append(f"### <a href=\"/blog/pt/post/{p['slug']}/\">{p['title']}</a>")
    lines.append(f"*Publicado em {p['date']} &bull; Categoria: {p['category']}*")
    lines.append("")
    lines.append(f"{p['description']}")
    lines.append("")
    lines.append(f"<a href=\"/blog/pt/post/{p['slug']}/\">Ler Ensaio &rarr;</a>")
    lines.append("")
    lines.append("---")
    lines.append("")

final_text = "\n".join(lines)

# Verify no parentheses
assert "(" not in final_text and ")" not in final_text, "ERRO: Parenteses encontrados em pt/index.md!"

PT_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
PT_INDEX_FILE.write_text(final_text, encoding="utf-8")
print(f"Gerado {PT_INDEX_FILE} com {len(posts)} artigos em portugues.")
