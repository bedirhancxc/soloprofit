"""Submit SoloProfit once to QuestStack's authorized, free agent endpoint.

No spam, fake traffic, payments, or repeated submissions. Do not expose
the management token returned by the provider in public CI logs.
"""
import json
import uuid
import urllib.error
import urllib.parse
import urllib.request

URL = "https://bedirhancxc.github.io/soloprofit/"
CHECK = "https://queststack.io/api/v1/listings/check?url=" + urllib.parse.quote(URL, safe="")
ENDPOINT = "https://queststack.io/api/v1/listings"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "SoloProfit/1.0 (one-time directory listing by authorized assistant)",
}


def request_json(url, method="GET", data=None):
    req = urllib.request.Request(
        url,
        method=method,
        headers=HEADERS,
        data=json.dumps(data).encode("utf-8") if data is not None else None,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.status
            body = resp.read(35000).decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        code = error.code
        body = error.read(35000).decode("utf-8", "replace")
    return code, json.loads(body)


def main():
    code, check = request_json(CHECK)
    print(f"QuestStack preflight: HTTP {code}; available={check.get('available')}")
    if code != 200:
        raise SystemExit("Could not verify whether website is already listed; aborting")
    if check.get("available") is False:
        print("QuestStack: website already listed; no duplicate submission")
        return
    if check.get("available") is not True:
        raise SystemExit("QuestStack availability uncertain; aborting")

    payload = {
        "websiteUrl": URL,
        "name": "SoloProfit",
        "summary": "Free browser-based calculators for freelance rates, profit margins, markup and business break-even points.",
        "category": "finance-payments",
        "tags": ["free", "web"],
        "description": (
            "SoloProfit is a free website for freelancers and small businesses. "
            "Calculate hourly billing rates, selling price, gross profit margin, "
            "subscriber break-even and required unit sales. The tools use "
            "example inputs, update instantly, and require no registration. "
            "They give simplified business estimates, not financial advice."
        ),
        "bestFor": "Freelancers, small businesses, sellers and solo founders.",
        "limitation": "USD examples and simplified estimates; tax, fees and refunds must be entered where applicable.",
        "pricingLabel": "Completely free; no signup.",
        "requestKey": str(uuid.uuid4()),
    }
    status, response = request_json(ENDPOINT, method="POST", data=payload)
    # Be extremely careful: never print the raw response or managementToken.
    listing = response.get("listing") or {}
    public_id = listing.get("id") or response.get("id")
    public_slug = listing.get("slug") or response.get("slug")
    listing_status = listing.get("status") or response.get("status")
    print(f"QuestStack submission: HTTP {status}, public id={public_id}, slug={public_slug}, status={listing_status}")
    if not (200 <= status < 300):
        error = response.get("error")
        if isinstance(error, dict):
            error = error.get("code")
        print("QuestStack rejected request; public reason:", str(error)[:120])
        raise SystemExit("QuestStack listing not accepted")
    print("QuestStack accepted for review; check listing status separately. No visits claimed.")


if __name__ == "__main__":
    main()
