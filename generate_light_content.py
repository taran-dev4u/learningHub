import json
import os

topics_file = r'System_Design_Tutorial\topics.json'
content_dir = r'System_Design_Tutorial\content'

with open(topics_file, 'r', encoding='utf-8') as f:
    topics_data = json.load(f)

for group in topics_data:
    for topic in group['topics']:
        filepath = os.path.join(content_dir, topic['file'])
        
        # Only rewrite if it's the generic stub or empty
        # Let's read the current content
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f_read:
                content = f_read.read()
                
            # If the content is short (meaning it's just the stub)
            if len(content) < 300 and "currently being generated" in content:
                title = topic['title']
                light_content = f"""# {title}

## Overview
Welcome to the introductory module on **{title}**. This topic is a critical piece of the System Design puzzle, heavily influencing how we build scalable, resilient, and performant architectures.

In modern distributed systems, {title} plays a pivotal role in ensuring that our applications can handle scale without degrading the user experience.

## Key Concepts to Understand
To master this topic, you should focus your research on the following areas:
- **Definition & Purpose:** What exact problem does {title} solve in a massive system?
- **Trade-offs:** What are you sacrificing when you implement {title}? (Remember: everything in System Design is a trade-off between latency, consistency, availability, and cost).
- **Failure Modes:** What happens to the overall system if the {title} component crashes or degrades?

## Next Steps
> [!NOTE]
> **Teacher's Note:** This is the *Light-Depth Baseline Version* of this tutorial, generated to ensure you have a complete overview of the curriculum without broken links. 
> 
> In a future session, we will upgrade this page with a massive deep-dive, including Mermaid.js architecture diagrams, real-world examples (like Netflix and Uber), and specific interview cheat-codes!
"""
                with open(filepath, 'w', encoding='utf-8') as out_f:
                    out_f.write(light_content)

print("Successfully generated light-depth versions for all pending topics.")
