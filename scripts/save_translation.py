#!/usr/bin/env python3
from pathlib import Path
import argparse,shutil
from common import load,save,segs
ap=argparse.ArgumentParser();ap.add_argument("--work-dir",required=True);ap.add_argument("--unit",required=True);ap.add_argument("--translation",required=True);a=ap.parse_args()
w=Path(a.work_dir);src=w/"units"/a.unit;tr=Path(a.translation);dest=w/"translations"/a.unit
if segs(src.read_text(encoding="utf-8"))!=segs(tr.read_text(encoding="utf-8")):raise SystemExit("FAIL SEG_MISMATCH")
if tr.resolve()!=dest.resolve():shutil.copyfile(tr,dest)
s=load(w)
for c in s["chapters"]:
 if c["unit"]==a.unit:c["status"]="done"
save(w,s);print("PASS saved="+a.unit)
