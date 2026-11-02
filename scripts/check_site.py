from pathlib import Path
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

class Parser(HTMLParser):
    def error(self, message):
        raise AssertionError(message)

pages = ["index.html", "freelance-hourly-rate/index.html", "profit-margin/index.html", "subscription-break-even/index.html"]
for page in pages:
    p = Path(page)
    assert p.is_file(), f"Missing {page}"
    html = p.read_text(encoding="utf-8")
    Parser().feed(html)
    assert "<title>" in html and 'name="description"' in html, f"Missing metadata in {page}"
    assert 'type="number"' in html, f"Missing numeric inputs in {page}"
    assert "aria-live" in html, f"Missing accessible result in {page}"
assert Path("robots.txt").is_file()
root = ET.parse("sitemap.xml").getroot()
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [node.text for node in root.findall(".//s:loc", ns)]
assert len(urls) == len(pages)
assert all(u.startswith("https://bedirhancxc.github.io/soloprofit/") for u in urls)
print(f"PASS: {len(pages)} calculator pages, metadata, and sitemap")
