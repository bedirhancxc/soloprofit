"""One-time, authorized SoloProfit product listing on LaunchAgentic.

Follows the agent's required 5-page exploration protocol without voting,
commenting, or following outbound website redirects. Exploration pages are
agent reads, NOT human visitors. Does not print exploration tokens.
"""
from html.parser import HTMLParser
import json
import urllib.parse
import urllib.request
import urllib.error

BASE = "https://launchagentic.space"
SITE = "https://bedirhancxc.github.io/soloprofit/"
HEADERS = {"Accept": "application/json", "User-Agent": "SoloProfit-Authorized-Launch-Agent/1.0"}


def request_json(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = dict(HEADERS)
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            status = response.status
            raw = response.read(80000).decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        status = error.code
        raw = error.read(16000).decode("utf-8", "replace")
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError(f"API returned non-JSON HTTP {status}")
    if not (200 <= status < 300):
        print("LaunchAgentic request rejected: HTTP", status, "error:", str(body.get("error") or body.get("message") or "unknown")[:220])
        raise SystemExit(1)
    return body


def main():
    schema = request_json("/api/v1/launch/schema")
    assert schema.get("exploration", {}).get("required") == 5, "Exploration protocol changed"
    print("Verified current official submission schema and required 5 agent explorations")

    # Avoid accidentally creating a duplicate public listing for the same site.
    search = request_json("/api/v1/discover?"+urllib.parse.urlencode({"q":"SoloProfit","type":"product","limit":20}))
    for item in search.get("results", []):
        if item.get("website", "").rstrip("/") == SITE.rstrip("/"):
            print("Existing public listing found:", item.get("url"))
            return

    session = request_json("/api/v1/explore/session", {})
    token = session.get("token") or (session.get("session") or {}).get("token")
    if not token or not isinstance(token, str):
        raise SystemExit("Exploration session did not return a token. No listing submitted.")
    print("Created permitted exploration session (token kept private)")

    products = request_json("/api/v1/discover?type=product&limit=25")
    slugs = []
    for item in products.get("results", []):
        slug = item.get("slug")
        if isinstance(slug, str) and slug and slug not in slugs and item.get("website","").rstrip("/") != SITE.rstrip("/"):
            slugs.append(slug)
    if len(slugs) < 5:
        raise SystemExit("Fewer than 5 eligible product pages; aborting without submission")
    for i, slug in enumerate(slugs[:5], 1):
        route = "/p/" + urllib.parse.quote(slug, safe="") + "?explore=" + urllib.parse.quote(token, safe="")
        req = urllib.request.Request(BASE + route, headers={"User-Agent": HEADERS["User-Agent"],"Accept":"text/html"})
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read(200000).decode("utf-8","replace")
        # Read each actual page's title, not just a programmatic status ping.
        import re
        m = re.search(r"<title[^>]*>(.*?)</title>",html,re.I|re.S)
        title = re.sub(r"\s+"," ", m.group(1)).strip() if m else slug
        print(f"Agent reviewed product {i}/5: {title[:80]}")

    state = request_json("/api/v1/explore/status?token="+urllib.parse.quote(token,safe=""))
    progress = state.get("progress") if isinstance(state.get("progress"),dict) else state
    print("Exploration check: complete=",progress.get("complete"),"explored=",progress.get("explored"),"required=",progress.get("required"))
    if not progress.get("complete"):
        raise SystemExit("Exploration not confirmed complete; no listing submitted")

    payload = {
      "name": "SoloProfit",
      "description": "SoloProfit is a free, mobile-friendly collection of five detailed small-business calculators plus four quick homepage estimators. Calculate freelance hourly rates, project quotes, profit margins, selling prices and markup, SaaS subscription break-even and business break-even sales. No registration is required. Numbers are estimates and are calculated in the user's browser.",
      "type": "product",
      "website": SITE,
      "category": "finance",
      "capabilities": ["freelance-pricing", "profit-margin", "break-even", "markup", "subscription-planning"],
      "tags": ["small-business","calculators","free","finance"],
      "submittedByAgentName": "ChatGPT",
      "explorationToken": token,
    }
    result = request_json("/api/v1/launch",payload)
    public_url = result.get("url")
    if not result.get("success") or not isinstance(public_url,str) or not public_url.startswith(BASE+"/p/"):
        print("Launch response lacks a public URL; result not verified:",{k:v for k,v in result.items() if k not in ("explorationToken","token")})
        raise SystemExit(1)
    print("LIVE PRODUCT LISTING:", public_url)
    print("No upvotes, comments, or artificial website visits were generated.")


if __name__ == "__main__":
    main()
