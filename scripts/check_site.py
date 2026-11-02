from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

BASE = "https://bedirhancxc.github.io/soloprofit/"
ROOT = Path(".")
class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.h1_count = 0
        self.robots_noindex = False
        self.canonicals = []
        self.in_title = False
        self.title_text = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots_noindex |= "noindex" in attrs.get("content", "").lower()
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href"))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data

sitemap = ROOT / "sitemap.xml"
assert sitemap.is_file(), "Missing sitemap.xml"
root = ET.parse(sitemap).getroot()
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [n.text for n in root.findall(".//s:loc", ns)]
assert urls and len(urls) == len(set(urls)), "Missing or duplicate sitemap URLs"
assert all(u and u.startswith(BASE) for u in urls), "Invalid sitemap URLs"
pages = []
for url in urls:
    path = unquote(urlparse(url).path)
    relative = path.removeprefix("/soloprofit/").strip("/")
    file = ROOT / relative / "index.html" if relative else ROOT / "index.html"
    assert file.is_file(), f"Sitemap URL has no page: {url}"
    pages.append(file)
    html = file.read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(html)
    assert parser.h1_count == 1, f"Expected one H1: {file}"
    assert parser.title_text.strip(), f"Empty page title: {file}"
    assert not parser.robots_noindex, f"Indexed page marked noindex: {file}"
    assert parser.canonicals == [url], f"Missing or duplicate canonical: {file}"
    assert parser.links, f"No navigation links: {file}"
    for link in parser.links:
        if link.startswith(("mailto:", "tel:", "javascript:")):
            continue
        resolved = urljoin(url, link).split("#", 1)[0]
        if not resolved.startswith(BASE):
            continue
        rel = unquote(urlparse(resolved).path).removeprefix("/soloprofit/").strip("/")
        target = ROOT / rel
        if rel.endswith(".html") or rel.endswith(".xml"):
            assert target.is_file(), f"Broken internal link in {file}: {link}"
        else:
            assert (target / "index.html").is_file(), f"Broken internal link in {file}: {link}"
    assert "<title>" in html and 'name="description"' in html, f"Missing metadata: {file}"
    assert 'type="number"' in html, f"Missing numeric input: {file}"
    assert "aria-live" in html, f"Missing accessible result: {file}"
    assert f'href="{url}"' in html, f"Canonical URL missing or mismatched: {file}"
assert set(urls) == {BASE + ("" if p == ROOT / "index.html" else p.parent.as_posix().strip("/") + "/") for p in pages}, "Sitemap mismatch"
assert (ROOT / "robots.txt").is_file(), "Missing robots.txt"
robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
assert f"Sitemap: {BASE}sitemap.xml" in robots, "robots.txt sitemap mismatch"
print(f"PASS: {len(pages)} indexed pages have valid metadata, calculators and canonical URLs")
