import os
import json

content_dir = r'System_Design_Tutorial\content'
bundle_file = r'System_Design_Tutorial\contentBundle.js'

bundle = {}

if os.path.exists(content_dir):
    for filename in os.listdir(content_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(content_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                bundle[filename] = f.read()

with open(bundle_file, 'w', encoding='utf-8') as out:
    out.write("window.contentBundle = " + json.dumps(bundle, indent=2) + ";\n")

print(f"Bundled {len(bundle)} markdown files into contentBundle.js")
