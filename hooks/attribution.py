import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROUTES_MAP_FILE = BASE_DIR / "i18n" / "routes-map.json"

ROUTES_MAP = {}
if ROUTES_MAP_FILE.exists():
    try:
        with open(ROUTES_MAP_FILE, "r", encoding="utf-8") as f:
            ROUTES_MAP = json.load(f)
    except Exception:
        ROUTES_MAP = {}

EN_TO_PT_MAP = {}
PT_TO_EN_MAP = {}
for post in ROUTES_MAP.get("blog_posts", []):
    s_en = post.get("slug_en")
    s_pt = post.get("slug_pt")
    if s_en and s_pt:
        EN_TO_PT_MAP[s_en] = s_pt
        PT_TO_EN_MAP[s_pt] = s_en

def on_page_markdown(markdown, page, config, files):
    src_uri = page.file.src_uri
    dest = page.file.dest_uri
    if dest.endswith("index.html"):
        dest = dest[:-10]
    canonical_url = f"https://hsnlabs.ai/blog/{dest}"
    if not canonical_url.endswith("/"):
        canonical_url += "/"

    if src_uri.startswith("post/"):
        if "originally published on" in markdown:
            return markdown
        attribution = f"""

---

*Article originally published on [HSN Labs]({canonical_url}). Author: [Hugo S. Nascimento](https://hsnlabs.ai).*
"""
        return markdown + attribution

    if src_uri.startswith("pt/post/"):
        if "publicado originalmente em" in markdown:
            return markdown
        attribution = f"""

---

*Artigo publicado originalmente em [HSN Labs]({canonical_url}). Autor: [Hugo S. Nascimento](https://hsnlabs.ai).*
"""
        return markdown + attribution

    return markdown

def on_page_content(html, page, config, files):
    src_uri = page.file.src_uri
    dest = page.file.dest_uri
    if dest.endswith("index.html"):
        dest = dest[:-10]
    canonical_url = f"https://hsnlabs.ai/blog/{dest}"
    if not canonical_url.endswith("/"):
        canonical_url += "/"

    hreflang_tags = []
    lang = "en"

    if src_uri.startswith("post/"):
        slug = Path(src_uri).stem
        slug_pt = EN_TO_PT_MAP.get(slug)
        hreflang_tags.append(f'<link rel="alternate" hreflang="en" href="{canonical_url}">')
        if slug_pt:
            pt_url = f"https://hsnlabs.ai/blog/pt/post/{slug_pt}/"
            hreflang_tags.append(f'<link rel="alternate" hreflang="pt-BR" href="{pt_url}">')
        hreflang_tags.append(f'<link rel="alternate" hreflang="x-default" href="{canonical_url}">')

    elif src_uri.startswith("pt/post/"):
        lang = "pt-BR"
        slug_pt = Path(src_uri).stem
        slug_en = PT_TO_EN_MAP.get(slug_pt)
        if slug_en:
            en_url = f"https://hsnlabs.ai/blog/post/{slug_en}/"
            hreflang_tags.append(f'<link rel="alternate" hreflang="en" href="{en_url}">')
            hreflang_tags.append(f'<link rel="alternate" hreflang="x-default" href="{en_url}">')
        hreflang_tags.append(f'<link rel="alternate" hreflang="pt-BR" href="{canonical_url}">')

    elif src_uri == "index.md":
        hreflang_tags.append('<link rel="alternate" hreflang="en" href="https://hsnlabs.ai/blog/">')
        hreflang_tags.append('<link rel="alternate" hreflang="pt-BR" href="https://hsnlabs.ai/blog/pt/">')
        hreflang_tags.append('<link rel="alternate" hreflang="x-default" href="https://hsnlabs.ai/blog/">')

    elif src_uri == "pt/index.md":
        lang = "pt-BR"
        hreflang_tags.append('<link rel="alternate" hreflang="en" href="https://hsnlabs.ai/blog/">')
        hreflang_tags.append('<link rel="alternate" hreflang="pt-BR" href="https://hsnlabs.ai/blog/pt/">')
        hreflang_tags.append('<link rel="alternate" hreflang="x-default" href="https://hsnlabs.ai/blog/">')

    injected_meta = ""
    if hreflang_tags:
        injected_meta = "\n" + "\n".join(hreflang_tags) + "\n"

    if src_uri.startswith("post/") or src_uri.startswith("pt/post/"):
        schema_data = {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": page.title,
            "url": canonical_url,
            "description": page.meta.get("description", page.title),
            "inLanguage": lang,
            "author": {
                "@type": "Person",
                "name": "Hugo S. Nascimento",
                "url": "https://hsnlabs.ai"
            },
            "publisher": {
                "@type": "Organization",
                "name": "HSN Labs",
                "url": "https://hsnlabs.ai",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://hsnlabs.ai/assets/brand/lockups/hsnlabs-lockup-horizontal-light.png"
                }
            }
        }
        if page.meta.get("date"):
            schema_data["datePublished"] = str(page.meta["date"])

        json_ld = f'\n<script type="application/ld+json">\n{json.dumps(schema_data, indent=2)}\n</script>\n'
        return html + injected_meta + json_ld

    return html + injected_meta

def on_post_build(config):
    site_dir = Path(config.site_dir)
    hub_tag = '<atom:link href="https://pubsubhubbub.appspot.com/" rel="hub" type="application/rss+xml"/>'

    for rss_name in ["feed_rss_created.xml", "feed_rss_updated.xml"]:
        rss_path = site_dir / rss_name
        if rss_path.exists():
            content = rss_path.read_text(encoding="utf-8")
            content = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', content)
            content = content.replace("<url>None</url>", "<url>https://hsnlabs.ai/blog/assets/brand/symbol/symbol-square-pure-cyan.png</url>")
            if 'rel="hub"' not in content:
                content = re.sub(
                    r'(<atom:link [^>]*rel="self"[^>]*/>)',
                    r'\1 ' + hub_tag,
                    content
                )
            rss_path.write_text(content, encoding="utf-8")
