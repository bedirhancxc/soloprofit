"""Verify public SoloProfit directory listing using the launchpad's public read API."""
import json
from urllib.request import Request, urlopen

endpoint = "https://techtools.cz/launchpad-api/tools?sort=recent&per_page=100&page=1"
request = Request(endpoint, headers={"User-Agent":"SoloProfitListingVerifier/1.0","Accept":"application/json"})
with urlopen(request, timeout=30) as response:
    data = json.loads(response.read(1000000))

print("Launchpad public API root structure:", list(data.keys())[:12] if isinstance(data, dict) else type(data).__name__)
if isinstance(data, list):
    tools = data
else:
    tools = data.get("tools") or data.get("results") or data.get("data") or []
    if isinstance(tools, dict):
        tools = tools.get("tools") or tools.get("items") or tools.get("results") or []
if not isinstance(tools, list):
    tools = []

items = [x for x in tools if isinstance(x, dict) and (
    x.get("name","").strip().lower() == "soloprofit" or
    "bedirhancxc.github.io/soloprofit" in x.get("url","").lower()
)]
if not items:
    print("SoloProfit not found on first page of the directory read API. Public listing status unverified.")
else:
    for item in items:
        public_id = item.get("id") or item.get("tool_id") or item.get("slug")
        print("Live listing name:", item.get("name"))
        print("Live listing category:", item.get("category"))
        print("Live listing website:", item.get("url"))
        print("Live listing public ID:", public_id)
        if public_id:
            print("Live directory link: https://techtools.cz/tools/launchpad/?tool="+str(public_id))
    print("PASS: SoloProfit visibly listed by directory's public read API")
