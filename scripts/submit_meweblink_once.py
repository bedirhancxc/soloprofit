"""Submit SoloProfit to MeWebLink once through its public no-account form.

Uses the form's own CSRF token/cookies, leaves anti-spam fields untouched,
does not bypass a challenge, and does not manufacture website visits.
"""
from html.parser import HTMLParser
import http.cookiejar
import re
import urllib.parse
import urllib.request
import urllib.error

URL="https://meweblink.com/submit/"
SITE="https://bedirhancxc.github.io/soloprofit/"

class SubmitForm(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside=False
        self.fields={}
        self.options=[]
        self.select=False
        self.current=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="form" and a.get("action")=="/submit/":self.inside=True
        if not self.inside:return
        if tag=="input" and a.get("name"):
            self.fields[a["name"]]=(a.get("value") or "",a.get("type","text"))
        if tag=="select" and a.get("name")=="category_id":self.select=True
        if tag=="option" and self.select:
            self.current=[a.get("value",""),""]
    def handle_data(self,data):
        if self.current is not None:self.current[1]+=data
    def handle_endtag(self,tag):
        if tag=="option" and self.current is not None:
            self.options.append(self.current)
            self.current=None
        if tag=="select":self.select=False
        if tag=="form" and self.inside:self.inside=False

def main():
    jar=http.cookiejar.CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    headers={"User-Agent":"Mozilla/5.0 (compatible; SoloProfitFreeDirectorySubmission/1.0)","Accept":"text/html"}
    with opener.open(urllib.request.Request(URL,headers=headers),timeout=30) as response:
        html=response.read(150000).decode("utf-8","replace")
    parsed=SubmitForm();parsed.feed(html)
    if not parsed.fields.get("csrf") or not parsed.fields["csrf"][0]:
        raise SystemExit("Missing required CSRF token; aborting")
    cats=[v for v,label in parsed.options if label.strip().lower()=="business" and v]
    print("Available category labels:",[label for v,label in parsed.options],flush=True)
    if len(cats)!=1:raise SystemExit("Cannot find a unique Business category; aborting")
    payload={name:value for name,(value,t) in parsed.fields.items() if t=="hidden"}
    payload.update({
        "url":SITE,
        "title":"SoloProfit",
        "description":"Free, no-signup business calculators for freelancers and small businesses. Estimate hourly rates, project quotes, profit margins, markup and break-even sales with instant results.",
        "category_id":cats[0],
        "language":"English",
        "region":"",
        "company_website":"",  # normal spam-control field stays empty
    })
    request=urllib.request.Request(
        URL,method="POST",data=urllib.parse.urlencode(payload).encode("utf-8"),
        headers={**headers,"Content-Type":"application/x-www-form-urlencoded","Origin":"https://meweblink.com","Referer":URL})
    try:
        with opener.open(request,timeout=40) as resp:
            code=resp.status
            final=resp.url
            body=resp.read(120000).decode("utf-8","replace")
    except urllib.error.HTTPError as ex:
        code=ex.code
        final=ex.geturl()
        body=ex.read(40000).decode("utf-8","replace")
    clean=re.sub(r"\s+"," ",re.sub(r"<[^>]*>"," ",body))
    print("MeWebLink response:",code,"final_url:",final,flush=True)
    for word in ("submitted","accepted","success","added","pending","already listed","duplicate","error","limit"):
        index=clean.lower().find(word)
        if index>=0:
            print("Page response excerpt:",clean[max(0,index-110):index+210],flush=True)
            break
    if code>=400:raise SystemExit("HTTP error. No retry is scheduled.")
    print("One normal form submission completed. Public listing and visits must be checked independently.")

if __name__=="__main__":
    main()
