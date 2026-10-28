# -*- coding: utf-8 -*-
"""
Rebuilds System_Design_Tutorial/contentBundle.js from content/*.md
"""
import os, glob, json, tempfile, time

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

fd, temp_path = tempfile.mkstemp(prefix='.contentBundle-', suffix='.tmp', dir=os.path.dirname(OUTPUT_FILE))
try:
    with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
        f.write(js_content)
    for attempt in range(3):
        try:
            os.replace(temp_path, OUTPUT_FILE)
            break
        except OSError:
            if attempt == 2:
                raise
            time.sleep(0.2 * (attempt + 1))
finally:
    if os.path.exists(temp_path):
        os.unlink(temp_path)

print(f"Bundled {len(bundle)} markdown files into {OUTPUT_FILE} ({len(js_content)} bytes)")
