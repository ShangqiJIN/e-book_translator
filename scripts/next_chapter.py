#!/usr/bin/env python3
from pathlib import Path
import argparse
from common import load
ap=argparse.ArgumentParser();ap.add_argument("--work-dir",required=True);a=ap.parse_args();w=Path(a.work_dir);s=load(w)
done=[c for c in s["chapters"] if c["status"]=="done"];p=[c for c in s["chapters"] if c["status"]!="done"]
if not p:print("DONE");raise SystemExit
if done and not s.get("preview_approved"):print("WAITING_FOR_PREVIEW_APPROVAL");raise SystemExit
c=p[0];f=w/"units"/c["unit"];print(f"NEXT unit={c['unit']} words≈{len(f.read_text(encoding='utf-8').split())} path={f}")
