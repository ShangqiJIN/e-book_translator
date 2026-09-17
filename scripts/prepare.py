#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import argparse,re,zipfile,json
class P(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True);self.b=[];self.tag=None;self.buf=[]
 def handle_starttag(self,t,a):
  if t in ("h1","h2","h3","p","blockquote","li") and self.tag is None:self.tag=t;self.buf=[]
  elif self.tag and t in ("em","i"):self.buf.append("*")
  elif self.tag and t=="br":self.buf.append("\n")
 def handle_endtag(self,t):
  if self.tag and t in ("em","i"):self.buf.append("*")
  if t==self.tag:
   x="".join(self.buf).strip()
   if x:self.b.append((t,x))
   self.tag=None;self.buf=[]
 def handle_data(self,d):
  if self.tag:self.buf.append(d)
def blocks(x):p=P();p.feed(x);return p.b
def groups(b):
 starts=[i for i,(t,x) in enumerate(b) if t in ("h1","h2") and re.search(r"chapter|part|第.{0,8}章",x,re.I)]
 if not starts:return [b]
 out=[]
 if starts[0]:out.append(b[:starts[0]])
 for n,s in enumerate(starts):out.append(b[s:starts[n+1] if n+1<len(starts) else len(b)])
 return [x for x in out if x]
ap=argparse.ArgumentParser();ap.add_argument("source");ap.add_argument("--work-dir",required=True);a=ap.parse_args()
src=Path(a.source);w=Path(a.work_dir);(w/"units").mkdir(parents=True,exist_ok=True);(w/"translations").mkdir(exist_ok=True)
suf=src.suffix.lower()
if suf in (".html",".htm"): gs=groups(blocks(src.read_text(encoding="utf-8",errors="ignore")))
elif suf==".epub":
 gs=[]
 with zipfile.ZipFile(src) as z:
  for n in z.namelist():
   if n.lower().endswith((".xhtml",".html",".htm")) and "nav" not in n.lower():
    b=blocks(z.read(n).decode("utf-8","ignore"))
    if b:gs.append(b)
elif suf in (".txt",".md"):
 raw=src.read_text(encoding="utf-8",errors="ignore")
 pat=r"(?mi)^(?=(?:#{1,3}\s*)?(?:chapter|part)\s+\S+|第.{0,8}章\s*$)"
 chunks=[x.strip() for x in re.split(pat,raw) if x.strip()] or [raw]
 gs=[[("p",p) for p in re.split(r"\n\s*\n",x) if p.strip()] for x in chunks]
elif suf==".pdf": raise SystemExit("PDF_TEXT_EXTRACTION_REQUIRED: no OCR by default; extract text layer to TXT/MD first.")
else: raise SystemExit("UNSUPPORTED_INPUT "+suf)
chs=[]
for i,g in enumerate(gs,1):
 name=f"chapter{i:02d}.md";out=[]
 for j,(tag,x) in enumerate(g,1):
  out += [f"<!--SEG:c{i:02d}-p{j:04d}-->",({"h1":"# ","h2":"## ","h3":"### "}.get(tag,""))+x,""]
 (w/"units"/name).write_text("\n".join(out),encoding="utf-8");chs.append({"index":i,"unit":name,"status":"pending"})
state={"version":"6.0","pipeline":"chapter-first-lite","source":src.name,"preview_approved":False,"chapters":chs}
(w/"state.json").write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
tpl=Path(__file__).parent.parent/"references/translation_profile.template.md"
if not (w/"translation_profile.md").exists():(w/"translation_profile.md").write_text(tpl.read_text(encoding="utf-8"),encoding="utf-8")
if not (w/"terminology.json").exists():(w/"terminology.json").write_text("{}\n",encoding="utf-8")
print(f"PASS chapters={len(chs)} next={chs[0]['unit'] if chs else 'NONE'}")
