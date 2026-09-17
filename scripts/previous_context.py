#!/usr/bin/env python3
from pathlib import Path
import argparse
from common import load
ap=argparse.ArgumentParser();ap.add_argument("--work-dir",required=True);ap.add_argument("--chars",type=int,default=1200);a=ap.parse_args();w=Path(a.work_dir);s=load(w)
d=[c for c in s["chapters"] if c["status"]=="done"]
print((w/"translations"/d[-1]["unit"]).read_text(encoding="utf-8")[-a.chars:] if d else "")
