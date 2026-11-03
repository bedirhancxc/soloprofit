"""One authorized free editorial tool submission, not a visit generator.

Uses current WordPress nonce and session cookie, requests free listing only.
Does not bypass captchas, fake ratings, or retry/re-submit on errors.
"""
from html.parser import HTMLParser
import http.cookiejar
import re
import urllib.parse
import urllib.request
import urllib.error

HOME="https://thetooldirectory.com/submit-a-tool/"
SITE="https://bedirhancxc.github.io/soloprofit/"
EMAIL="bedirhancimen@outlook.com"

class Form(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active=False
        self.hidden={}
        self.options={}
        self.select=None
        self.current=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="form" and (a.get("method") or "").lower()=="post":
            self.active=True
        if not self.active:return
        if tag=="input" and a.get("name") and a.get("type")=="hidden":
            self.hidden[a["name"]]=a.get("value","")
        if tag=="select" and a.get("name") in ("tool_category","tool_pricing"):
            self.select=a["name"]
            self.options.setdefault(self.select,[])
        if tag=="option" and self.select:
            self.current=[a.get("value",""),""]
    def handle_data(self,data):
        if self.current is not None:self.current[1]+=data
    def handle_endtag(self,tag):
        if tag=="option" and self.current:
            self.options[self.select].append(tuple(self.current))
            self.current=None
        if tag=="select":self.select=None
        if tag=="form":self.active=False

def choose(form,key,need):
    matches=[v for v,label in form.options.get(key,[]) if label.strip().casefold()==need.casefold()]
    if len(matches)!=1:raise SystemExit("Cannot uniquely select "+need+"; available: "+str(form.options.get(key,[])))
    return matches[0]

def main():
    jar=http.cookiejar.CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    headers={"User-Agent":"Mozilla/5.0 (compatible; SoloProfitEditorialSubmission/1.0)","Accept":"text/html"}
    with opener.open(urllib.request.Request(HOME,headers=headers),timeout=30) as res:
        page=res.read(150000).decode("utf-8","replace")
    form=Form();form.feed(page)
    print("Public category options:",form.options.get("tool_category"),flush=True)
    print("Public pricing options:",form.options.get("tool_pricing"),flush=True)
    if not form.hidden.get("ttd_submit_nonce"):
        raise SystemExit("No standard WordPress submit nonce; abort")
    if "captcha" in page.lower() and "recaptcha" in page.lower():
        raise SystemExit("Captcha challenge present; submit through the site instead of bypassing")
    # Safe exact editorial fit. Do not post when categories are ambiguous.
    category=choose(form,"tool_category","Business & Finance")
    pricing=choose(form,"tool_pricing","Free")
    payload=dict(form.hidden)
    payload.update({
      "tool_name":"SoloProfit",
      "tool_url":SITE,
      "tool_tagline":"Free business calculators for pricing, profit margins and break-even.",
      "tool_pricing":pricing,
      "tool_category":category,
      "tool_description":(
        "SoloProfit is a free, no-signup website for freelancers, e-commerce sellers and "
        "small businesses. Visitors can calculate freelance hourly rates, project quotes, "
        "profit margins, product markups, selling prices, subscription break-even and "
        "business break-even sales. All calculators have example inputs, update as you "
        "type, and include formulas with practical worked examples. The calculations "
        "run in the browser and are simplified estimates, not financial advice."
      ),
      "tool_platforms":"Web browser, mobile and desktop",
      "tool_audiences":"Freelancers, independent makers, small business owners, online sellers",
      "tool_use_cases":"Estimate a freelance rate, set a selling price, find break-even sales",
      "submitter_email":EMAIL,
      "tool_logo":"",
      "tool_screenshots":"",
      "tool_alternatives":"",
      "growth_challenge":"visitors",
    })
    req=urllib.request.Request(HOME,method="POST",
       data=urllib.parse.urlencode(payload).encode("utf-8"),
       headers={**headers,"Content-Type":"application/x-www-form-urlencoded","Referer":HOME})
    try:
        with opener.open(req,timeout=35) as res:
            code=res.status;final=res.url;raw=res.read(200000).decode("utf-8","replace")
    except urllib.error.HTTPError as e:
        code=e.code;final=e.geturl();raw=e.read(120000).decode("utf-8","replace")
    text=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",raw))
    print("Directory form response: HTTP",code,"url",final,flush=True)
    for needle in ("successfully submitted","submission received","pending review","thank you for submitting","submission failed","invalid nonce","already submitted","error"):
        index=text.lower().find(needle)
        if index>=0:print("Result excerpt:",text[max(0,index-110):index+200][:315],flush=True)
    if code>=400:raise SystemExit("Submission not accepted (HTTP status); no retry scheduled")
    print("One editorial submission request sent, subject to publication review. No visitors claimed.")

if __name__=="__main__":
    main()
