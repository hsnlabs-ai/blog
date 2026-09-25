import re

def on_page_markdown(markdown, page, config, files):
    # Only append attribution to blog post articles
    if page.file.src_uri.startswith("writing/posts/") or (page.file.src_uri.startswith("writing/") and page.file.src_uri != "writing/index.md"):
        # Determine exact canonical url
        dest = page.file.dest_uri
        if dest.endswith("index.html"):
            dest = dest[:-10]
        canonical_url = f"https://hsnlabs.ai/blog/{dest}"
        if not canonical_url.endswith("/"):
            canonical_url += "/"

        # Avoid duplicating if already present
        if "originally published on" in markdown:
            return markdown

        attribution = f"""

---

*Article originally published on [HSN Labs]({canonical_url}). Author: [Hugo Nascimento](https://hsnlabs.ai).*
"""
        return markdown + attribution
    return markdown
