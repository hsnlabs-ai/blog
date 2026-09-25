import json
import re
from pathlib import Path

def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri.startswith("writing/posts/") or (page.file.src_uri.startswith("writing/") and page.file.src_uri != "writing/index.md"):
        dest = page.file.dest_uri
        if dest.endswith("index.html"):
            dest = dest[:-10]
        canonical_url = f"https://hsnlabs.ai/blog/{dest}"
        if not canonical_url.endswith("/"):
            canonical_url += "/"

        if "originally published on" in markdown:
            return markdown

        attribution = f"""

---

*Article originally published on [HSN Labs]({canonical_url}). Author: [Hugo Nascimento](https://hsnlabs.ai).*
"""
        return markdown + attribution
    return markdown

def on_page_content(html, page, config, files):
    if page.file.src_uri.startswith("writing/posts/") or (page.file.src_uri.startswith("writing/") and page.file.src_uri != "writing/index.md"):
        dest = page.file.dest_uri
        if dest.endswith("index.html"):
            dest = dest[:-10]
        canonical_url = f"https://hsnlabs.ai/blog/{dest}"
        if not canonical_url.endswith("/"):
            canonical_url += "/"

        schema_data = {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": page.title,
            "url": canonical_url,
            "description": page.meta.get("description", page.title),
            "inLanguage": "en",
            "author": {
                "@type": "Person",
                "name": "Hugo Nascimento",
                "url": "https://hsnlabs.ai"
            },
            "publisher": {
                "@type": "Organization",
                "name": "HSN Labs",
                "url": "https://hsnlabs.ai",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://hsnlabs.ai/assets/brand/lockups/hsn-labs-lockup-horizontal-light.png"
                }
            }
        }
        if page.meta.get("date"):
            schema_data["datePublished"] = str(page.meta["date"])

        json_ld = f'\n<script type="application/ld+json">\n{json.dumps(schema_data, indent=2)}\n</script>\n'
        return html + json_ld
    return html

def on_post_build(config):
    site_dir = Path(config.site_dir)
    hub_tag = '<atom:link href="https://pubsubhubbub.appspot.com/" rel="hub" type="application/rss+xml"/>'

    for rss_name in ["feed_rss_created.xml", "feed_rss_updated.xml"]:
        rss_path = site_dir / rss_name
        if rss_path.exists():
            content = rss_path.read_text(encoding="utf-8")
            if 'rel="hub"' not in content:
                content = re.sub(
                    r'(<atom:link [^>]*rel="self"[^>]*/>)',
                    r'\1 ' + hub_tag,
                    content
                )
                rss_path.write_text(content, encoding="utf-8")
