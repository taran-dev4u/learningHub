import re
import json
import os
import shutil

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

with open('system_design.html', 'r', encoding='utf-8') as f:
    html = f.read()

sections_raw = re.split(r'(<h2[^>]*>.*?</h2>)', html)[1:]
topics_json = []
all_pages = []

current_section_idx = 0
while current_section_idx < len(sections_raw):
    h2_tag = sections_raw[current_section_idx]
    section_content = sections_raw[current_section_idx + 1] if current_section_idx + 1 < len(sections_raw) else ""
    
    m = re.search(r'<h2[^>]*>(.*?)</h2>', h2_tag)
    if m:
        section_title = m.group(1).strip()
        section_title = re.sub(r'<[^>]+>', '', section_title)
        
        if 'subsection' in section_content:
            group = {
                "group": section_title,
                "topics": []
            }
            
            # Split by <div class="subsection">
            subsections_raw = section_content.split('<div class="subsection">')[1:]
            
            for sub_content in subsections_raw:
                # Extract h3 title
                h3_m = re.search(r'<h3[^>]*>(.*?)</h3>', sub_content)
                if h3_m:
                    sub_title = h3_m.group(1).strip()
                    sub_title = re.sub(r'<[^>]+>', '', sub_title)
                    slug = slugify(sub_title)
                    filename = f"{slug}.md"
                    
                    # Extract concepts inside this subsection
                    concepts = re.findall(r'<div class="cname">(.*?)</div>', sub_content)
                    clean_concepts = [re.sub(r'<[^>]+>', '', c).strip() for c in concepts]
                    
                    group['topics'].append({
                        "id": slug,
                        "title": sub_title,
                        "file": filename
                    })
                    
                    all_pages.append({
                        "title": sub_title,
                        "file": filename,
                        "concepts": clean_concepts
                    })
            
            if group['topics']:
                topics_json.append(group)
                
    current_section_idx += 2

# Save new topics.json
with open(r'System_Design_Tutorial\topics.json', 'w', encoding='utf-8') as f:
    json.dump(topics_json, f, indent=2)

content_dir = r'System_Design_Tutorial\content'
if os.path.exists(content_dir):
    shutil.rmtree(content_dir)
os.makedirs(content_dir)

# Generate new grouped pages
for page in all_pages:
    filepath = os.path.join(content_dir, page['file'])
    with open(filepath, 'w', encoding='utf-8') as out:
        out.write(f"# {page['title']}\n\n")
        out.write("## Overview\n")
        out.write(f"Welcome to the module on **{page['title']}**. This page covers the following related subtopics:\n\n")
        for c in page['concepts']:
            out.write(f"- {c}\n")
            
        out.write("\n---\n\n")
        
        # Create a stub section for each concept
        for c in page['concepts']:
            out.write(f"## {c}\n\n")
            out.write(f"Detailed content for **{c}** is currently being formulated. Check back soon!\n\n")
            
        out.write("> [!NOTE]\n> **Teacher's Note:** This is the *Light-Depth Baseline Version* of this tutorial. We will upgrade this page with deep-dives shortly!\n")

print(f"Generated new topics.json with {sum(len(g['topics']) for g in topics_json)} pages across {len(topics_json)} groups.")
