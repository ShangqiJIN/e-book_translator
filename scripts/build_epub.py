#!/usr/bin/env python3
from pathlib import Path
import argparse,zipfile,re,html,datetime
from common import load,SEG_RE
def inline(x):
 x=html.escape(x);return re.sub(r"\*([^*\n]+)\*",r"<em>\1</em>",x)
def page(t,title):
 t=SEG_RE.sub("",t);bs=[x.strip() for x in re.split(r"\n\s*\n",t) if x.strip()];o=[]
 for b in bs:
  if b.startswith("# "):o.append("<h1>"+inline(b[2:])+"</h1>")
  elif b.startswith("## "):o.append("<h2>"+inline(b[3:])+"</h2>")
  else:o.append("<p>"+inline(" ".join(b.splitlines()))+"</p>")
 return '<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>'+html.escape(title)+'</title><link rel="stylesheet" href="style.css"/></head><body>'+''.join(o)+"</body></html>"
ap=argparse.ArgumentParser();ap.add_argument("--work-dir",required=True);ap.add_argument("--output",required=True);ap.add_argument("--preview",action="store_true");a=ap.parse_args();w=Path(a.work_dir);s=load(w)
cs=[c for c in s["chapters"] if c["status"]=="done"]
if not a.preview and len(cs)!=len(s["chapters"]):raise SystemExit("FAIL incomplete")
docs=[(f"c{c['index']:02d}.xhtml",f"Chapter {c['index']}",page((w/"translations"/c["unit"]).read_text(encoding="utf-8"),f"Chapter {c['index']}")) for c in cs]
items=''.join(f'<item id="c{i}" href="{n}" media-type="application/xhtml+xml"/>' for i,(n,_,_) in enumerate(docs,1));sp=''.join(f'<itemref idref="c{i}"/>' for i in range(1,len(docs)+1));nav=''.join(f'<li><a href="{n}">{t}</a></li>' for n,t,_ in docs)
opf=f'<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="id">urn:v6</dc:identifier><dc:title>{html.escape(Path(s["source"]).stem)}</dc:title><dc:language>zh-CN</dc:language><meta property="dcterms:modified">{datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}</meta></metadata><manifest>{items}<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="css" href="style.css" media-type="text/css"/></manifest><spine>{sp}</spine></package>'
navx=f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>目录</title></head><body><nav epub:type="toc"><ol>{nav}</ol></nav></body></html>'
with zipfile.ZipFile(a.output,"w") as z:
 z.writestr("mimetype","application/epub+zip",compress_type=zipfile.ZIP_STORED);z.writestr("META-INF/container.xml",'<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>');z.writestr("EPUB/package.opf",opf);z.writestr("EPUB/nav.xhtml",navx);z.writestr("EPUB/style.css","body{font-family:serif;line-height:1.8;margin:5%}p{margin:0 0 .8em}")
 for n,_,x in docs:z.writestr("EPUB/"+n,x)
print(f"PASS chapters={len(docs)} output={a.output}")
