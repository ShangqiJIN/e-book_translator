#!/usr/bin/env python3
import argparse,zipfile
ap=argparse.ArgumentParser();ap.add_argument("epub");a=ap.parse_args()
with zipfile.ZipFile(a.epub) as z:
 assert z.namelist()[0]=="mimetype" and z.read("mimetype")==b"application/epub+zip"
 assert "EPUB/package.opf" in z.namelist()
print("PASS basic_epub_validation")
