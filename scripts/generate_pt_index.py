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
                "description": meta.get("description", ""),
                "image": meta.get("image", "")
            })

# Sort posts by date descending
posts.sort(key=lambda x: x["date"], reverse=True)

lines = []
lines.append("---")
lines.append("title: Hugo S. Nascimento")
lines.append("description: Posts e notas de campo sobre arquitetura de agentes enterprise, ontologias de domínio e execução em produção.")
lines.append("---")
lines.append("")
lines.append("# Hugo S. Nascimento")
lines.append("")
lines.append('<img src="../assets/images/author/hugo-nascimento.jpg" alt="Hugo S. Nascimento" class="author-photo" width="200" height="250" loading="eager" />')
lines.append("")
lines.append("Empresário, consultor e diretor de tecnologia e produto como CPTO. Pioneiro na implementação de sistemas agênticos em produção para grandes contas e referência na aplicação dessas arquiteturas desde 2022.")
lines.append("")
lines.append("Meu foco operacional é **Arquitetura de Agentes Enterprise**. Construo arquiteturas multiagente customizadas sobre ontologias de domínio executáveis para operações corporativas de missão crítica. Substituo operações manuais frágeis de BPO e gargalos de TI legada por forças de trabalho digitais autônomas que não alucinam nem falham em produção.")
lines.append("")
lines.append("Arquiteturas entregues incluem **Deloitte**, **Santander**, **Softplan**, **Unipar Carbocloro**, **LWSA**, **Turbi**, **Caju**, **Cast Group** e **Insi**.")
lines.append("")
lines.append('<a href="https://hsnlabs.ai/pt/">HSN Labs Boutique</a> &nbsp;&bull;&nbsp; <a href="https://www.linkedin.com/in/hugosoaresnascimento/">LinkedIn</a> &nbsp;&bull;&nbsp; <a href="https://github.com/hsnlabs-ai/blog">GitHub</a> &nbsp;&bull;&nbsp; <a href="/blog/">English Version</a>')
lines.append("")
lines.append("---")
lines.append("")
lines.append('<div class="blog-list" id="component-blog-list">')
for p in posts:
    lines.append('  <article class="blog-row blog-post-item">')
    if p.get("image"):
        lines.append(f'    <a class="blog-row-thumb" href="/blog/pt/post/{p["slug"]}/">')
        lines.append(f'      <img src="../{p["image"]}" alt="{p["title"]}" loading="lazy">')
        lines.append('    </a>')
    lines.append('    <div class="blog-row-body">')
    lines.append('      <div class="blog-row-byline">')
    lines.append('        <img class="blog-row-avatar" src="../assets/images/author/hugo-nascimento.jpg" alt="Hugo S. Nascimento" loading="lazy">')
    lines.append('        <h2 class="blog-row-title">')
    lines.append(f'          <a href="/blog/pt/post/{p["slug"]}/">{p["title"]}</a>')
    lines.append('        </h2>')
    lines.append('      </div>')
    lines.append(f'      <p class="blog-row-meta">{p["date"]} &bull; {p["category"]} &bull; Hugo S. Nascimento</p>')
    lines.append(f'      <p class="blog-row-description">{p["description"]}</p>')
    lines.append(f'      <a class="blog-row-cta" href="/blog/pt/post/{p["slug"]}/">Ler Post &rarr;</a>')
    lines.append('    </div>')
    lines.append('  </article>')
lines.append('</div>')
lines.append("")

final_text = "\n".join(lines)

# Verify no parentheses
assert "(" not in final_text and ")" not in final_text, "ERRO: Parenteses encontrados em pt/index.md!"

PT_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
PT_INDEX_FILE.write_text(final_text, encoding="utf-8")
print(f"Gerado {PT_INDEX_FILE} com {len(posts)} artigos em portugues.")
