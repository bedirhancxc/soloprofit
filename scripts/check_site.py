from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

BASE = "https://bedirhancxc.github.io/soloprofit/"
ROOT = Path(".")
class Parser(HTMLParser):
    pass

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
    Parser().feed(html)
    assert "<title>" in html and 'name="description"' in html, f"Missing metadata: {file}"
    assert 'type="number"' in html, f"Missing numeric input: {file}"
    assert "aria-live" in html, f"Missing accessible result: {file}"
    assert f'href="{url}"' in html, f"Canonical URL missing or mismatched: {file}"
assert (ROOT / "robots.txt").is_file(), "Missing robots.txt"
robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
assert f"Sitemap: {BASE}sitemap.xml" in robots, "robots.txt sitemap mismatch"
print(f"PASS: {len(pages)} indexed pages have valid metadata, calculators and canonical URLs")
