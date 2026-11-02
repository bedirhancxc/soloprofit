#!/usr/bin/env bash
# Daily, real-network audit of publicly served Google discovery files.
set -euo pipefail
base="https://bedirhancxc.github.io/soloprofit"
workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

download() {
  local url="$1" dest="$2"
  echo "Checking $url"
  curl --fail --location --silent --show-error \
    --retry 3 --retry-delay 5 --max-time 30 \
    --user-agent 'SoloProfitSiteMonitor/1.0' \
    --output "$dest" "$url"
}

download "$base/sitemap.xml" "$workdir/sitemap.xml"
download "$base/robots.txt" "$workdir/robots.txt"

python3 - "$workdir/sitemap.xml" "$workdir/robots.txt" <<'PY'
import sys
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

sitemap = Path(sys.argv[1])
robots = Path(sys.argv[2]).read_text(encoding="utf-8")
base = "https://bedirhancxc.github.io/soloprofit/"
root = ET.parse(sitemap).getroot()
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
assert root.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset", "Invalid XML sitemap root"
urls = [n.text for n in root.findall(".//s:loc", ns)]
assert urls and len(urls) == len(set(urls)), "Missing or repeated sitemap URLs"
assert all(u and u.startswith(base) and urlparse(u).query == "" for u in urls), "Unexpected sitemap URL"
assert f"Sitemap: {base}sitemap.xml" in robots, "Live robots.txt does not reference sitemap.xml"
assert not any(line.strip().lower() == "disallow: /" for line in robots.splitlines()), "Live robots.txt blocks all crawlers"
print(f"PASS: Public sitemap XML valid, contains {len(urls)} URLs, robots.txt references it")
PY

for path in / /freelance-hourly-rate/ /profit-margin/ /subscription-break-even/ /markup-calculator/ /break-even-calculator/; do
  download "$base$path" "$workdir/page.html"
  if ! grep -qi '<html' "$workdir/page.html"; then
    echo "FAIL: $base$path did not return HTML" >&2
    exit 1
  fi
done
echo "PASS: All 6 public calculator pages can be fetched."
