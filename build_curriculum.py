import re
import json
import os

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

with open('system_design.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We need to extract the hierarchy.
# Sections are <h2>...</h2>
# Subsections are <h3>...</h3> inside a <div class="subsection">
# Items are <div class="cname">...</div> inside <li ...>

sections_raw = re.split(r'(<h2[^>]*>.*?</h2>)', html)[1:]
topics = []

current_section_idx = 0
while current_section_idx < len(sections_raw):
    h2_tag = sections_raw[current_section_idx]
    section_content = sections_raw[current_section_idx + 1] if current_section_idx + 1 < len(sections_raw) else ""
    
    # Extract h2 title
    m = re.search(r'<h2[^>]*>(.*?)</h2>', h2_tag)
    if m:
        section_title = m.group(1).strip()
        # Clean HTML from title if any
        section_title = re.sub(r'<[^>]+>', '', section_title)
        
        # We only care about actual system design sections, they have subsections
        if 'subsection' in section_content:
            group = {
                "group": section_title,
                "topics": []
            }
            
            # Extract items
            # The items have <div class="cname">Item Name</div>
            items = re.findall(r'<div class="cname">(.*?)</div>', section_content)
            
            for item in items:
                title = re.sub(r'<[^>]+>', '', item).strip()
                slug = slugify(title)
                filename = f"{slug}.md"
                
                group['topics'].append({
                    "id": slug,
                    "title": title,
                    "file": filename
                })
            
            if group['topics']:
                topics.append(group)
                
    current_section_idx += 2

print(f"Extracted {len(topics)} sections.")
for g in topics:
    print(f" - {g['group']}: {len(g['topics'])} topics")

# Save to topics.json
with open(r'System_Design_Tutorial\topics.json', 'w', encoding='utf-8') as f:
    json.dump(topics, f, indent=2)

# Generate stubs
content_dir = r'System_Design_Tutorial\content'
if not os.path.exists(content_dir):
    os.makedirs(content_dir)

for g in topics:
    for t in g['topics']:
        filepath = os.path.join(content_dir, t['file'])
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as out:
                out.write(f"# {t['title']}\n\n")
                out.write(f"The detailed tutorial for **{t['title']}** is currently being generated. Check back soon for an in-depth breakdown!\n")
