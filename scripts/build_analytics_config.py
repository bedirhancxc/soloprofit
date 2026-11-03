"""Generate a PUBLIC browser analytics config from deployment environment.

The repository never contains a real PostHog project token. A public phc_
token is suitable for a website browser client; NEVER use a personal phx_ key.
"""
import json
import os
import pathlib
import re

token = os.environ.get("POSTHOG_PROJECT_TOKEN", "").strip()
host = os.environ.get("POSTHOG_API_HOST", "").strip()
valid_token = bool(re.fullmatch(r"phc_[A-Za-z0-9]+", token))
valid_host = host in {"https://us.i.posthog.com", "https://eu.i.posthog.com"}

if token or host:
    if not (valid_token and valid_host):
        raise SystemExit("PostHog project token or ingestion host invalid; refusing deployment")
    print("Private analytics config: project token and region validated")
else:
    print("Private analytics config: no project configured; pageviews remain disabled")

payload = {"token": token if valid_token and valid_host else "",
           "host": host if valid_token and valid_host else ""}
text = (
    "/* Generated during GitHub Pages deploy; public client config, no personal keys. */\n"
    "window.SOLOPROFIT_ANALYTICS_CONFIG = "
    + json.dumps(payload, separators=(",", ":")) + ";\n"
)
path = pathlib.Path("assets/analytics-config.js")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(text, encoding="utf-8")
print("Wrote runtime config; analytics enabled:", bool(payload["token"]))
