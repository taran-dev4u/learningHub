# -*- coding: utf-8 -*-
"""
Rebuilds System_Design_Tutorial/contentBundle.js from content/*.md
"""
import os, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, 'System_Design_Tutorial', 'content')
OUTPUT_FILE = os.path.join(ROOT, 'System_Design_Tutorial', 'contentBundle.js')

bundle = {}
md_files = sorted(glob.glob(os.path.join(CONTENT_DIR, '*.md')))
for fpath in md_files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        bundle[fname] = f.read()

js_content = "window.contentBundle = " + json.dumps(bundle, ensure_ascii=False, indent=2) + ";\n"

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Bundled {len(bundle)} markdown files into {OUTPUT_FILE} ({len(js_content)} bytes)")
