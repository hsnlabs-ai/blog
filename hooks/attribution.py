import json
import re
from datetime import datetime
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

def insert_newsletter_interstitial(markdown, is_pt=False):
    if ("Agentes [×] Gente" in markdown or "[Agentes] x [a Gente]" in markdown) and "newsletter-follow" in markdown:
        return markdown

    if is_pt:
        note = """
> **[Agentes] x [a Gente]** — Fora do hype, discutimos como Agentic AI multiplica e alavanca a capacidade laboral humana. Análises quinzenais publicadas na newsletter de Hugo S. Nascimento no LinkedIn com mais de 1.600 assinantes. [Acompanhar no LinkedIn ↗](https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=7397999984089935872)
"""
    else:
        note = """
> **[Agentes] x [a Gente]** — Beyond the hype: how Agentic AI multiplies and leverages human labor capacity. Bi-weekly field notes published in Hugo S. Nascimento's LinkedIn newsletter with over 1,600 subscribers. [Follow on LinkedIn ↗](https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=7397999984089935872)
"""

    h2_matches = list(re.finditer(r'^##\s+', markdown, re.MULTILINE))
    if len(h2_matches) >= 2:
        idx = max(1, len(h2_matches) // 2)
        pos = h2_matches[idx].start()
        return markdown[:pos] + note + "\n\n" + markdown[pos:]
    else:
        paragraphs = re.split(r'\n\s*\n', markdown)
        if len(paragraphs) > 3:
            paragraphs.insert(3, note)
            return "\n\n".join(paragraphs)
        else:
            return markdown + "\n\n" + note

def on_page_markdown(markdown, page, config, files):
    src_uri = page.file.src_uri
    dest = page.file.dest_uri
    if dest.endswith("index.html"):
        dest = dest[:-10]
    canonical_url = f"https://hsnlabs.ai/blog/{dest}"
    if not canonical_url.endswith("/"):
        canonical_url += "/"

    if src_uri.startswith("post/"):
        if "originally published on" not in markdown:
            attribution = f"""

---

*Article originally published on [hsnlabs]({canonical_url}). Author: [Hugo S. Nascimento](https://hsnlabs.ai).*
"""
            markdown = markdown + attribution
        return insert_newsletter_interstitial(markdown, is_pt=False)

    if src_uri.startswith("pt/post/"):
        if "publicado originalmente em" not in markdown:
            attribution = f"""

---

*Artigo publicado originalmente em [hsnlabs]({canonical_url}). Autor: [Hugo S. Nascimento](https://hsnlabs.ai).*
"""
            markdown = markdown + attribution
        return insert_newsletter_interstitial(markdown, is_pt=True)

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
                "name": "hsnlabs",
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

def on_env(env, config, files):
    def days_ago(date_val, is_pt=False):
        if not date_val:
            return ""
        try:
            d_str = str(date_val)[:10]
            d = datetime.strptime(d_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            delta = (today - d).days
            if is_pt:
                if delta <= 0:
                    return "postado hoje"
                elif delta == 1:
                    return "há 1 dia"
                else:
                    return f"há {delta} dias"
            else:
                if delta <= 0:
                    return "posted today"
                elif delta == 1:
                    return "1 day ago"
                else:
                    return f"{delta} days ago"
        except Exception:
            return ""
    env.filters["days_ago"] = days_ago
    return env

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

    # 1. Generate clean canonical redirect stubs for legacy /blog/writing/<slug>/ URLs
    writing_dir = site_dir / "writing"
    writing_dir.mkdir(parents=True, exist_ok=True)
    writing_root_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Redirecting... | hsnlabs</title>
  <link rel="canonical" href="https://hsnlabs.ai/blog/">
  <meta http-equiv="refresh" content="0; url=/blog/">
  <script>window.location.replace("/blog/" + window.location.search + window.location.hash);</script>
</head>
<body>
  <p>Redirecting to <a href="/blog/">/blog/</a>...</p>
</body>
</html>"""
    (writing_dir / "index.html").write_text(writing_root_html, encoding="utf-8")

    for post_md in sorted((BASE_DIR / "docs" / "post").glob("*.md")):
        slug = post_md.stem
        stub_dir = writing_dir / slug
        stub_dir.mkdir(parents=True, exist_ok=True)
        target_url = f"https://hsnlabs.ai/blog/post/{slug}/"
        target_rel = f"/blog/post/{slug}/"
        stub_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Redirecting... | hsnlabs</title>
  <link rel="canonical" href="{target_url}">
  <meta http-equiv="refresh" content="0; url={target_rel}">
  <script>window.location.replace("{target_rel}" + window.location.search + window.location.hash);</script>
</head>
<body>
  <p>Redirecting to <a href="{target_rel}">{target_rel}</a>...</p>
</body>
</html>"""
        (stub_dir / "index.html").write_text(stub_html, encoding="utf-8")

    # 2. Clean site/sitemap.xml so only canonical /blog/, /blog/pt/, /blog/post/*, and /blog/pt/post/* are listed
    sitemap_path = site_dir / "sitemap.xml"
    if sitemap_path.exists():
        sm_text = sitemap_path.read_text(encoding="utf-8")
        allowed_pattern = re.compile(
            r"^https://hsnlabs\.ai/blog/(?:pt/|post/[a-z0-9\-]+/|pt/post/[a-z0-9\-]+/)?$"
        )
        url_blocks = re.findall(r"<url>.*?</url>", sm_text, flags=re.DOTALL)
        kept_blocks = []
        for blk in url_blocks:
            m_loc = re.search(r"<loc>(.*?)</loc>", blk)
            if m_loc and allowed_pattern.match(m_loc.group(1).strip()):
                kept_blocks.append("    " + blk.strip())
        clean_sm = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(kept_blocks)
            + "\n</urlset>\n"
        )
        sitemap_path.write_text(clean_sm, encoding="utf-8")
        sitemap_gz = site_dir / "sitemap.xml.gz"
        if sitemap_gz.exists():
            import gzip
            with gzip.open(sitemap_gz, "wb") as gz_f:
                gz_f.write(clean_sm.encode("utf-8"))

