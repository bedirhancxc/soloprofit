"""Read-only public traffic counts for SoloProfit, without generating a visit.

Counts come from an independent cookieless analytics provider. They begin
only when the client-side script is installed and successfully loads.
Provider estimates are not conclusive proof of a human visitor.
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

SITE_ID = "bedirhancxc.github.io"
API = "https://icount.kr/api.php?id=" + urllib.parse.quote(SITE_ID)


def main():
    request = urllib.request.Request(
        API, headers={"User-Agent": "SoloProfitTrafficReporter/1.0", "Accept": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    results = {}
    for scope in ("today", "yesterday", "total"):
        period = data.get(scope)
        if not isinstance(period, dict):
            raise RuntimeError("Traffic response missing " + scope)
        counts = []
        for key in ("pv", "uv"):
            count = period.get(key)
            if not isinstance(count, int) or count < 0:
                raise RuntimeError("Missing non-negative count: " + scope + "/" + key)
            counts.append(count)
        results[scope] = counts
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print("SoloProfit website-visitor estimate, UTC", now)
    for scope in ("today", "yesterday", "total"):
        pv, uv = results[scope]
        print(f"{scope}: pageviews={pv}; estimated_unique_visitors={uv}")
    print("Note: bot filtering and unique visitor definition are provided by iCount.")
    print("GitHub Actions and search engine fetches without running JS are not visits.")
    if results["today"][1] >= 1:
        print("FIRST_VISITOR_SIGNAL: Today at least one estimated unique client-side visitor.")
    else:
        print("NO_CLIENT_SIDE_VISITS_REPORTED_TODAY")


if __name__ == "__main__":
    main()
