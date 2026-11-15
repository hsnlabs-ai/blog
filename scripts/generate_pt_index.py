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
                "tags": meta.get("tags", []) or [],
                "description": meta.get("description", ""),
                "image": meta.get("image", "")
            })

# Sort posts by date descending
posts.sort(key=lambda x: x["date"], reverse=True)

CAT_MAP = {
    "Future of Work": "O Futuro do Trabalho",
    "Agentic AI": "Agentic AI",
    "Why Agents Fail": "Por Que Agentes Falham"
}

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
lines.append('<a href="https://hsnlabs.ai/">hsnlabs Boutique</a> &nbsp;&bull;&nbsp; <a href="https://www.linkedin.com/in/hugosoaresnascimento/">LinkedIn</a> &nbsp;&bull;&nbsp; <a href="https://github.com/hsnlabs-ai/blog">GitHub</a> &nbsp;&bull;&nbsp; <a href="/blog/">English Version</a>')
lines.append("")
lines.append("---")
lines.append("")
lines.append('<div class="blog-list" id="component-blog-list" data-posts-per-page="10">')
total_posts = len(posts)
total_pages = max(1, (total_posts - 1) // 10 + 1)
for idx, p in enumerate(posts):
    post_page = (idx // 10) + 1
    hidden_attr = ' style="display: none;"' if post_page > 1 else ''
    tags_str = ",".join(str(t) for t in p.get("tags", []))
    lines.append(f'  <article class="blog-row blog-post-item" data-page="{post_page}" data-category="{p["category"]}" data-tags="{tags_str}"{hidden_attr}>')
    lines.append(f'    <a class="blog-row-card-link" href="/blog/pt/post/{p["slug"]}/">')
    if p.get("image"):
        lines.append('      <div class="blog-row-thumb">')
        lines.append(f'        <img src="../{p["image"]}" alt="{p["title"]}" loading="lazy">')
        lines.append('      </div>')
    lines.append('      <div class="blog-row-body">')
    lines.append(f'        <h2 class="blog-row-title">{p["title"]}</h2>')
    cat_label = CAT_MAP.get(p["category"], p["category"])
    lines.append(f'        <p class="blog-row-meta">{p["date"]} &bull; {cat_label}</p>')
    lines.append(f'        <p class="blog-row-description">{p["description"]}</p>')
    lines.append('      </div>')
    lines.append('    </a>')
    lines.append('  </article>')

if total_pages > 1:
    lines.append(f'  <div id="blog-pagination" class="blog-pagination" data-total-pages="{total_pages}" data-page-size="10">')
    lines.append('    <div class="pagination-info">')
    lines.append(f'      <span id="pagination-status">Mostrando 1–10 de {total_posts} posts</span>')
    lines.append('    </div>')
    lines.append('    <nav class="pagination-controls" aria-label="Paginação do Blog">')
    lines.append('      <button class="pagination-btn pagination-nav" id="pagination-prev" disabled aria-label="Página anterior">')
    lines.append('        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px; margin-right: 4px;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>')
    lines.append('        <span>Anterior</span>')
    lines.append('      </button>')
    lines.append('      <div class="pagination-pages" id="pagination-numbers">')
    for page_i in range(1, total_pages + 1):
        active_cls = "active" if page_i == 1 else ""
        lines.append(f'        <button class="pagination-btn pagination-num {active_cls}" data-target-page="{page_i}" aria-label="Página {page_i}">{page_i}</button>')
    lines.append('      </div>')
    lines.append('      <button class="pagination-btn pagination-nav" id="pagination-next" aria-label="Próxima página">')
    lines.append('        <span>Próxima</span>')
    lines.append('        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px; margin-left: 4px;"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>')
    lines.append('      </button>')
    lines.append('    </nav>')
    lines.append('  </div>')

lines.append('</div>')
lines.append("")

final_text = "\n".join(lines)

# Verify no parentheses
assert "(" not in final_text and ")" not in final_text, "ERRO: Parenteses encontrados em pt/index.md!"

PT_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
PT_INDEX_FILE.write_text(final_text, encoding="utf-8")
print(f"Gerado {PT_INDEX_FILE} com {len(posts)} artigos em portugues.")
