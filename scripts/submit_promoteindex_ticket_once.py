"""One-off PromoteIndex listing submission following its explicit wait-ticket rules.

Never log private queue tickets, edit keys, owner information or provider
responses in full. Submit a single legitimate SoloProfit project.
"""
import json
import time
import datetime as dt
import urllib.error
import urllib.request

ENDPOINT = "https://promoteindex.com/api/v1/projects"
PAYLOAD = {
    "name": "SoloProfit",
    "url": "https://bedirhancxc.github.io/soloprofit/",
    "tagline": "Free calculators for freelance rates, product markup and business break-even.",
    "description": (
        "SoloProfit provides no-signup business calculators to estimate billable "
        "hourly rates, project prices, profit margins, product markup, "
        "subscriber break-even and required sales. Numbers update as you type, "
        "using clear examples and simplified assumptions. Free for anyone."
    ),
    "category": "saas",
    "pricing": "free",
    "tags": ["business", "calculators", "finance"],
    "builtWith": ["chatgpt"],
    "repoUrl": "https://github.com/bedirhancxc/soloprofit",
    "heardAbout": {"source": "not-sure"},
    "submittedBy": {"kind": "agent", "agent": "chatgpt", "agentName": "SoloProfit assistant"},
}
MAX_WAIT_SECONDS = 22 * 60


def submit(ticket=None):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "SoloProfit/1.0 (authorized one-time directory listing)",
        "X-Agent-Name": "SoloProfit assistant",
    }
    if ticket:
        headers["X-Submission-Ticket"] = ticket
    req = urllib.request.Request(
        ENDPOINT, method="POST", data=json.dumps(PAYLOAD).encode("utf-8"),
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            status = response.status
            body = response.read(50000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        status = error.code
        body = error.read(50000).decode("utf-8", errors="replace")
    return status, json.loads(body)


def public_error_code(body):
    error = body.get("error")
    return (error.get("code") if isinstance(error, dict) else str(error))[:100]


def wait_interval(details):
    try:
        seconds = max(0, int(details.get("retryAfter", 0)))
    except (TypeError, ValueError):
        seconds = 0
    queue = details.get("queue") or {}
    scheduled_at = queue.get("scheduledAt")
    if isinstance(scheduled_at, str):
        try:
            when = dt.datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
            until = (when - dt.datetime.now(dt.timezone.utc)).total_seconds()
            seconds = max(seconds, int(until) + 2)
        except ValueError:
            pass
    return max(seconds, 10)


def main():
    started = time.monotonic()
    ticket = None
    for attempt in range(3):
        status, body = submit(ticket)
        if status in (200, 201, 202) and body.get("ok") is not False:
            project = body.get("project") or {}
            slug = project.get("slug") or body.get("slug")
            print(f"PromoteIndex accepted SoloProfit: HTTP {status}, public slug {slug}.")
            print("Any editKey returned by the provider remains private and is not printed.")
            print("This is a listing, not evidence of a human site visitor.")
            return
        if status in (400, 409, 422):
            print(f"PromoteIndex refused this submission, HTTP {status}: {public_error_code(body)}")
            raise SystemExit(1)
        error = body.get("error") or {}
        code = error.get("code") if isinstance(error, dict) else str(error)
        details = error.get("details") or {} if isinstance(error, dict) else {}
        if status == 429 and code == "submission_queue":
            queue = details.get("queue") or {}
            fresh_ticket = queue.get("ticketId")
            if not isinstance(fresh_ticket, str) or not fresh_ticket:
                raise SystemExit("Queued without usable return ticket; not retrying.")
            wait_seconds = wait_interval(details)
            if time.monotonic() - started + wait_seconds >= MAX_WAIT_SECONDS:
                print("Queue wait exceeds one-time job budget; no repeated polling.")
                raise SystemExit(1)
            ticket = fresh_ticket
            print(f"Queued by directory (HTTP 429). Returning once after the provider's required {wait_seconds}s wait.", flush=True)
            time.sleep(wait_seconds)
            continue
        print(f"PromoteIndex submission status HTTP {status}; reason {code}.")
        raise SystemExit(1)
    raise SystemExit("PromoteIndex did not accept within two permitted wait-ticket returns.")


if __name__ == "__main__":
    main()
