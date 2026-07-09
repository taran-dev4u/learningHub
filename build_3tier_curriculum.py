import re
import json
import os
import shutil
import html

def slugify(text):
    text = html.unescape(text) # Fix &amp; issue
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

with open('system_design.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

sections_raw = re.split(r'(<h2[^>]*>.*?</h2>)', html_content)[1:]
topics_json = []

current_section_idx = 0
while current_section_idx < len(sections_raw):
    h2_tag = sections_raw[current_section_idx]
    section_content = sections_raw[current_section_idx + 1] if current_section_idx + 1 < len(sections_raw) else ""
    
    m = re.search(r'<h2[^>]*>(.*?)</h2>', h2_tag)
    if m:
        section_title = m.group(1).strip()
        section_title = html.unescape(re.sub(r'<[^>]+>', '', section_title))
        
        if 'subsection' in section_content:
            group = {
                "section": section_title,
                "subsections": []
            }
            
            subsections_raw = section_content.split('<div class="subsection">')[1:]
            
            for sub_content in subsections_raw:
                h3_m = re.search(r'<h3[^>]*>(.*?)</h3>', sub_content)
                if h3_m:
                    sub_title = h3_m.group(1).strip()
                    sub_title = html.unescape(re.sub(r'<[^>]+>', '', sub_title))
                    slug = slugify(sub_title)
                    filename = f"{slug}.md"
                    
                    concepts = re.findall(r'<div class="cname">(.*?)</div>', sub_content)
                    clean_concepts = [html.unescape(re.sub(r'<[^>]+>', '', c).strip()) for c in concepts]
                    
                    sub_obj = {
                        "id": slug,
                        "title": sub_title,
                        "file": filename,
                        "concepts": [
                            {
                                "title": c,
                                "anchor": slugify(c)
                            } for c in clean_concepts
                        ]
                    }
                    
                    group['subsections'].append(sub_obj)
            
            if group['subsections']:
                topics_json.append(group)
                
    current_section_idx += 2

# Save as topics.js to bypass CORS issues for local file execution
with open(r'System_Design_Tutorial\topics.js', 'w', encoding='utf-8') as f:
    f.write("window.topicsData = " + json.dumps(topics_json, indent=2) + ";\n")

# To fix the already generated markdown files, we just rename them.
# If they don't exist, we don't care because Phase 1 already created them.
# Let's just create a quick shell script logic to recreate any missing files
content_dir = r'System_Design_Tutorial\content'
if not os.path.exists(content_dir):
    os.makedirs(content_dir)

# Ensure all 62 markdown stubs exist
for g in topics_json:
    for s in g['subsections']:
        filepath = os.path.join(content_dir, s['file'])
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as out:
                out.write(f"# {s['title']}\n\n")
                out.write("## Overview\n")
                out.write(f"Welcome to the module on **{s['title']}**.\n\n")
                for c in s['concepts']:
                    out.write(f"## {c['title']}\n\n")
                    out.write(f"Detailed content for **{c['title']}** is currently being formulated.\n\n")

print("Generated 3-tier topics.js successfully.")
