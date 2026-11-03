"""Read-only inspect of three public relevant free-listing forms. No submissions."""
from html.parser import HTMLParser
import re
import urllib.request
from urllib.error import URLError

SITES = [
    "https://meweblink.com/submit/",
    "https://apprater.net/add",
    "https://thetooldirectory.com/submit-a-tool/",
]
class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms=[]
        self.current=None
        self.select=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="form":
            self.current={"action":a.get("action"),"method":a.get("method"),"id":a.get("id"),"fields":[],"options":[]}
            self.forms.append(self.current)
        if self.current is not None:
            if tag in ("input","textarea","select","button"):
                field={k:a.get(k) for k in ("name","type","id","placeholder","required","value") if k in a and not (k=="value" and a.get("type") in ("hidden","password"))}
                self.current["fields"].append((tag,field))
            if tag=="select":self.select=a.get("name") or a.get("id")
            if tag=="option" and self.select is not None:
                self.current["options"].append((self.select,a.get("value"),a.get("label"),a.get("disabled")))
    def handle_endtag(self,tag):
        if tag=="select":self.select=None
        if tag=="form":self.current=None

for site in SITES:
    try:
        req=urllib.request.Request(site,headers={"User-Agent":"Mozilla/5.0 (compatible; SoloProfitPublicFormInspector/1.0)","Accept":"text/html"})
        with urllib.request.urlopen(req,timeout=25) as resp:
            html=resp.read(250000).decode("utf-8","replace")
            print("SITE",site,"HTTP",resp.status,"FINAL",resp.url,"bytes",len(html),flush=True)
        parser=FormParser();parser.feed(html)
        print("FORMS",repr(parser.forms[:6])[:14500],flush=True)
        print("POSSIBLE LINKS",re.findall(r'href=["\']([^"\']*(?:submit|add|list)[^"\']*)',html,re.I)[:18],flush=True)
        print("POSSIBLE ACTIONS",re.findall(r'(?:action|fetch)\(["\']([^"\']{1,140})',html,re.I)[:12],flush=True)
    except Exception as ex:
        print("ERROR",site,type(ex).__name__,str(ex)[:180],flush=True)
