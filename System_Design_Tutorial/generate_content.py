import json
import os

topics_file = 'topics.json'
content_dir = 'content'

with open(topics_file, 'r') as f:
    topics_data = json.load(f)

for group in topics_data:
    for topic in group['topics']:
        filepath = os.path.join(content_dir, topic['file'])
        # Only create if it doesn't already exist
        if not os.path.exists(filepath):
            with open(filepath, 'w') as out_f:
                out_f.write(f"# {topic['title']}\n\n")
                out_f.write(f"The tutorial for **{topic['title']}** is currently being formulated by your teacher.\n\n")
                out_f.write("> [!NOTE]\n> Check back soon for deep dives, visual diagrams, and interview strategies for this topic!\n")
