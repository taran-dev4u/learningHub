import json

with open('learning-hub-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find first item that belongs to system design
for k, v in data['items'].items():
    if 'sd' in k or '14.' in k:
        print("Item:", v)
        break

# Also let's just see how many items there are in total
print("Total items:", len(data['items']))

# Are there subsection IDs? 
# The HTML grep earlier showed: <li data-cid="14.2.1" data-name="functional requirements checklist">
# So the items key is probably "14.2.1"
if '14.2.1' in data['items']:
    print("Found 14.2.1:", data['items']['14.2.1'])
