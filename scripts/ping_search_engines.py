import urllib.request
import urllib.parse
import json
import sys

INDEXNOW_KEY = "fb6d944d28fc4484bd669f6d9c4d3292"
HOST = "hsnlabs.ai"
KEY_LOCATION = f"https://{HOST}/blog/{INDEXNOW_KEY}.txt"

URLS = [
    "https://hsnlabs.ai/blog/",
    "https://hsnlabs.ai/blog/feed_rss_created.xml",
    "https://hsnlabs.ai/blog/feed_json_created.json",
    "https://hsnlabs.ai/blog/sitemap.xml",
    "https://hsnlabs.ai/blog/llms.txt"
]

def ping_indexnow(endpoint):
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": URLS
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[IndexNow] {endpoint} -> HTTP {resp.status}")
    except Exception as e:
        print(f"[IndexNow Warning] {endpoint} -> {e}")

def ping_websub():
    hub_url = "https://pubsubhubbub.appspot.com/"
    params = urllib.parse.urlencode({
        "hub.mode": "publish",
        "hub.url": "https://hsnlabs.ai/blog/feed_rss_created.xml"
    }).encode("utf-8")
    req = urllib.request.Request(hub_url, data=params, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[WebSub Hub] -> HTTP {resp.status}")
    except Exception as e:
        print(f"[WebSub Warning] -> {e}")

def ping_sitemaps():
    sitemap_url = "https://hsnlabs.ai/blog/sitemap.xml"
    endpoints = [
        f"https://www.google.com/ping?sitemap={urllib.parse.quote(sitemap_url)}",
        f"https://www.bing.com/ping?sitemap={urllib.parse.quote(sitemap_url)}"
    ]
    for url in endpoints:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"[Sitemap Ping] {url.split('?')[0]} -> HTTP {resp.status}")
        except Exception as e:
            print(f"[Sitemap Ping Warning] {url.split('?')[0]} -> {e}")

if __name__ == "__main__":
    print("=== Submitting to Search Engines and IndexNow ===")
    ping_indexnow("https://api.indexnow.org/indexnow")
    ping_indexnow("https://www.bing.com/indexnow")
    ping_websub()
    ping_sitemaps()
    print("=== Ping complete ===")
