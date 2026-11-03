"""One-time, truthful product listings on two agent-friendly directories.

Only submit the SoloProfit homepage; never generate votes, visits, or repeat
a submission. CI prints no private edit keys from provider responses.
"""
import json
import urllib.request
import urllib.error
from urllib.parse import quote

URL = "https://bedirhancxc.github.io/soloprofit/"
NAME = "SoloProfit"
AGENT = "SoloProfit ChatGPT assistant"
DESCRIPTION = (
    "SoloProfit provides free, no-signup calculators for freelancers and small "
    "businesses. Calculate freelance hourly rates, project quotes, profit "
    "margins, product markup, and the sales or paying subscribers needed to "
    "break even. Edit example values and see results instantly in your browser. "
    "The calculators are educational estimates, not financial advice."
)
REQUESTS = [
    (
        "TechTools Launchpad",
        "https://techtools.cz/launchpad-api/tools",
        {
            "name": NAME,
            "url": URL,
            "tagline": "Free business calculators for pricing, margins, and break-even.",
            "description": DESCRIPTION,
            "category": "business",
            "submitted_by": AGENT,
        },
        {},
    ),
    (
        "PromoteIndex",
        "https://promoteindex.com/api/v1/projects",
        {
            "name": NAME,
            "url": URL,
            "tagline": "Free calculators for freelance pricing, profit margins and break-even sales.",
            "description": DESCRIPTION,
            "category": "saas",
            "pricing": "free",
            "tags": ["business", "finance", "calculators"],
            "builtWith": ["chatgpt"],
            "repoUrl": "https://github.com/bedirhancxc/soloprofit",
            "heardAbout": {"source": "not-sure"},
            "submittedBy": {
                "kind": "agent",
                "agent": "chatgpt",
                "agentName": AGENT,
            },
        },
        {"X-Agent-Name": AGENT},
    ),
]

def submit(name, endpoint, fields, headers):
    request = urllib.request.Request(
        endpoint,
        method="POST",
        data=json.dumps(fields).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "SoloProfit/1.0 (one-time legitimate listing submission)",
            **headers,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            code = response.status
            raw = response.read(40000).decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        code = error.code
        raw = error.read(10000).decode("utf-8", "replace")
    except Exception as error:
        print(f"{name}: network error ({type(error).__name__}); not confirmed.")
        return False

    try:
        data = json.loads(raw)
    except Exception:
        data = {}

    if code in (200, 201, 202) and data.get("ok") is not False:
        result = data.get("project") or data.get("tool") or data.get("listing") or {}
        public_id = result.get("slug") or result.get("id") or data.get("id")
        print(f"{name}: submission accepted, HTTP {code}. Public listing ID/slug: {str(public_id)[:70]}.")
        print(f"{name}: provider response recorded without private edit keys.")
        return True

    if code == 409:
        print(f"{name}: existing listing / duplicate URL (HTTP 409), no repeat submission.")
        return True

    # Do not print provider responses wholesale: they may contain private tokens.
    detail = data.get("error")
    if isinstance(detail, dict):
        detail = detail.get("code") or detail.get("message")
    if not isinstance(detail, str):
        detail = data.get("message") if isinstance(data.get("message"), str) else "unavailable"
    print(f"{name}: submission not accepted, HTTP {code}; reason: {detail[:130]}")
    return False


def main():
    results = [submit(*args) for args in REQUESTS]
    if not any(results):
        raise SystemExit("No directory accepted the listing.")
    print(f"Finished one-time submissions: {sum(results)}/{len(results)} successful or duplicate.")
    print("Public listing does not imply real visits or search indexing.")


if __name__ == "__main__":
    main()
