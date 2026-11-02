from pathlib import Path
import re
p=Path("index.html")
assert p.exists(), "Missing index.html"
html=p.read_text(encoding="utf-8")
for item in ["SoloProfit","Freelance Rate","Project Quote","Subscription Revenue","Profit Target","models=","aria-live"]:
    assert item in html, f"Missing feature: {item}"
assert html.count("<script>")==1
assert "<meta name=\"description\"" in html
assert Path("robots.txt").exists()
assert Path("sitemap.xml").exists()
print("PASS: site files and key calculator components present")
