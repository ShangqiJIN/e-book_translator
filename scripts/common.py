from pathlib import Path
import json,re
SEG_RE=re.compile(r"<!--SEG:([^>]+)-->")
def load(w): return json.loads((Path(w)/"state.json").read_text(encoding="utf-8"))
def save(w,s): (Path(w)/"state.json").write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding="utf-8")
def segs(t): return SEG_RE.findall(t)
