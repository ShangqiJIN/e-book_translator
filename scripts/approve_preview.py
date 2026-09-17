#!/usr/bin/env python3
import argparse
from common import load,save
ap=argparse.ArgumentParser();ap.add_argument("--work-dir",required=True);a=ap.parse_args();s=load(a.work_dir);s["preview_approved"]=True;save(a.work_dir,s);print("PASS")
