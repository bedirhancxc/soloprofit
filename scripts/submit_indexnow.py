"""Notify IndexNow-compatible search engines about existing SoloProfit pages.

Run once after the key file is publicly accessible. This is URL notification,
not a visit, crawl, indexation guarantee, or Google Search Console submission.
"""
import json
from pathlib import Path
import urllib.error
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

SITE_ROOT = "https://bedirhancxc.github.io/soloprofit/"
HOST = "bedirhancxc.github.io"
KEY = "2148619bda0c75df72d69909f542441e"
KEY_LOCATION = SITE_ROOT + KEY + ".txt"
API = "https://api.indexnow.org/indexnow"


def prepare_submission():
    local_key = Path(KEY + ".txt").read_text(encoding="utf-8").strip()
    assert local_key == KEY, "IndexNow key file has changed"
    tree = ET.parse("sitemap.xml").getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [n.text for n in tree.findall(".//s:loc", ns)]
    assert 1 <= len(urls) <= 10000 and len(set(urls)) == len(urls), "Invalid URL list"
    assert all(url and url.startswith(SITE_ROOT) and
               urllib.parse.urlsplit(url).hostname == HOST for url in urls), "Invalid URL host"
    return {"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": urls}


def submit():
    payload = prepare_submission()
    with urllib.request.urlopen(
        urllib.request.Request(
            KEY_LOCATION, headers={"User-Agent": "SoloProfit-IndexNow/1.0"}
        ), timeout=25
    ) as response:
        assert response.read().decode("utf-8").strip() == KEY, "Public key file does not match"
    print("Public key file verified", flush=True)

    req = urllib.request.Request(
        API, data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "SoloProfit-IndexNow/1.0",
        }, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            status = response.status
            message = response.read().decode("utf-8", errors="replace")[:500]
    except urllib.error.HTTPError as error:
        status = error.code
        message = error.read().decode("utf-8", errors="replace")[:500]

    print(f"IndexNow response HTTP {status}; URLs submitted: {len(payload['urlList'])}.", flush=True)
    if message:
        print("Response details:", message, flush=True)
    if status not in (200, 202):
        raise RuntimeError(f"IndexNow did not accept URL notification (HTTP {status})")
    print("IndexNow accepted the URL notification; indexation and visits are not guaranteed.", flush=True)


if __name__ == "__main__":
    submit()
