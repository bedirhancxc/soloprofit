"""One legitimate, one-time SoloProfit website listing submission.

Uses the public Zearches website submission form, preserves its normal CSRF
and cookie flow, leaves honeypot blank, and never bypasses challenges.
No accounts, fake reviews, votes, clicks, or repeated submissions.
"""
from html.parser import HTMLParser
import http.cookiejar
import time
import urllib.parse
import urllib.request
import urllib.error
import re

HOME = "https://zearches.com/"
TARGET = "https://bedirhancxc.github.io/soloprofit/"
FIELDS = ("csrf_token", "form_started_at", "form_origin")

class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_form = False
        self.in_directory = False
        self.current_option = None
        self.fields = {}
        self.options = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form" and attrs.get("action") == "/submit.php":
            self.in_form = True
        if not self.in_form:
            return
        if tag == "input" and attrs.get("name"):
            self.fields[attrs["name"]] = attrs.get("value", "")
        if tag == "select" and attrs.get("name") == "directory":
            self.in_directory = True
        if tag == "option" and self.in_directory:
            self.current_option = (attrs.get("value", ""), "")

    def handle_data(self, data):
        if self.current_option is not None:
            val, title = self.current_option
            self.current_option = (val, title + data)

    def handle_endtag(self, tag):
        if tag == "option" and self.current_option is not None:
            val, title = self.current_option
            self.options.append((val, title.strip()))
            self.current_option = None
        if tag == "select":
            self.in_directory = False
        if tag == "form" and self.in_form:
            self.in_form = False

def main():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SoloProfitListingAgent/1.0)",
               "Accept": "text/html,application/xhtml+xml"}
    with opener.open(urllib.request.Request(HOME, headers=headers), timeout=30) as response:
        html = response.read(200000).decode("utf-8", "replace")
    parsed = FormParser()
    parsed.feed(html)
    missing = [name for name in FIELDS if not parsed.fields.get(name)]
    if missing:
        raise SystemExit("Submission form lacks normal security or timing fields: " + ",".join(missing))
    print("Public categories:",parsed.options)
    matches = [v for v, label in parsed.options if "software" in label.lower() and v]
    if len(matches) != 1:
        raise SystemExit("Unique appropriate Software category not found. No submission.")
    category=matches[0]
    payload={
        "csrf_token": parsed.fields["csrf_token"],
        "form_started_at": parsed.fields["form_started_at"],
        "form_origin": parsed.fields["form_origin"],
        "url": TARGET,
        "title": "SoloProfit",
        "directory": category,
        "description": "Free business calculators for freelance hourly rates, profit margins, markup, selling prices, subscription costs and break-even sales. No sign-up required.",
        "website": "",  # provider-designated honeypot must stay blank
    }
    print("Prepared genuine submission with secure form fields and Software & SaaS category.")
    # Respect the form's ordinary human completion interval instead of fast-posting.
    time.sleep(14)
    req=urllib.request.Request(
        urllib.parse.urljoin(HOME,"/submit.php"),
        method="POST", data=urllib.parse.urlencode(payload).encode("utf-8"),
        headers={**headers,"Content-Type":"application/x-www-form-urlencoded",
                 "Origin":"https://zearches.com","Referer":HOME},
    )
    try:
        with opener.open(req,timeout=30) as response:
            status=response.status
            final=response.geturl()
            body=response.read(70000).decode("utf-8","replace")
    except urllib.error.HTTPError as err:
        status=err.code
        final=err.geturl()
        body=err.read(50000).decode("utf-8","replace")
    print("Zearches submission response HTTP:",status,"final URL:",final)
    clean=re.sub(r"\s+"," ",re.sub(r"<[^>]*>"," ",body))
    for clue in ("submitted","added successfully","pending review","already exists","duplicate","error","success"):
        if clue in clean.lower():
            i=clean.lower().find(clue)
            print("Public response clue:",clean[max(0,i-70):i+160][:230])
            break
    if status >= 400:
        raise SystemExit(f"Zearches returned unsuccessful HTTP {status}; do not retry automatically")
    print("One submission was sent. Publication and referral visits must be independently verified.")

if __name__ == "__main__":
    main()
