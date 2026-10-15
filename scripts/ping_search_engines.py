import urllib.request
import urllib.parse
import json
import glob
import os

INDEXNOW_KEY = "fb6d944d28fc4484bd669f6d9c4d3292"
HOST = "hsnlabs.ai"
KEY_LOCATION = f"https://{HOST}/{INDEXNOW_KEY}.txt"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def build_url_list():
    urls = [
        "https://hsnlabs.ai/",
        "https://hsnlabs.ai/pt/",
        "https://hsnlabs.ai/bootcamp/",
        "https://hsnlabs.ai/pt/bootcamp/",
        "https://hsnlabs.ai/advisory/",
        "https://hsnlabs.ai/pt/advisory/",
        "https://hsnlabs.ai/mcp/",
        "https://hsnlabs.ai/pt/mcp/",
        "https://hsnlabs.ai/canvas/",
        "https://hsnlabs.ai/pt/canvas/",
        "https://hsnlabs.ai/llms.txt",
        "https://hsnlabs.ai/sitemap.xml",
        "https://hsnlabs.ai/blog/",
        "https://hsnlabs.ai/blog/pt/",
        "https://hsnlabs.ai/blog/feed_rss_created.xml",
        "https://hsnlabs.ai/blog/feed_json_created.json",
        "https://hsnlabs.ai/blog/sitemap.xml",
        "https://hsnlabs.ai/blog/llms.txt"
    ]
    for f in sorted(glob.glob(os.path.join(BASE_DIR, "docs", "post", "*.md"))):
        slug = os.path.basename(f)[:-3]
        urls.append(f"https://hsnlabs.ai/blog/post/{slug}/")
    for f in sorted(glob.glob(os.path.join(BASE_DIR, "docs", "pt", "post", "*.md"))):
        slug = os.path.basename(f)[:-3]
        urls.append(f"https://hsnlabs.ai/blog/pt/post/{slug}/")
    return urls

def ping_indexnow(endpoint, urls):
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"[IndexNow] {endpoint} ({len(urls)} URLs) -> HTTP {resp.status}")
    except Exception as e:
        print(f"[IndexNow Warning] {endpoint} -> {e}")

def ping_websub():
    hub_url = "https://pubsubhubbub.appspot.com/"
    for feed_url in [
        "https://hsnlabs.ai/blog/feed_rss_created.xml",
        "https://hsnlabs.ai/blog/feed_rss_updated.xml"
    ]:
        params = urllib.parse.urlencode({
            "hub.mode": "publish",
            "hub.url": feed_url
        }).encode("utf-8")
        req = urllib.request.Request(hub_url, data=params, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"[WebSub Hub] {feed_url} -> HTTP {resp.status}")
        except Exception as e:
            print(f"[WebSub Warning] {feed_url} -> {e}")

if __name__ == "__main__":
    urls = build_url_list()
    print(f"=== Submitting {len(urls)} URLs to IndexNow & WebSub ===")
    ping_indexnow("https://api.indexnow.org/indexnow", urls)
    ping_indexnow("https://www.bing.com/indexnow", urls)
    ping_indexnow("https://yandex.com/indexnow", urls)
    ping_websub()
    print("=== Submission complete ===")
