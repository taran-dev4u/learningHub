import os
import re

INDEX_PATH = 'DSA_Ultimate_Index.html'

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean curated rows: remove NC, Video, GFG, and Sol links inside div.solutions
# We replace <div class="solutions">...</div> inside <li> with <div class="solutions"></div>
def clean_solutions(match):
    return '<div class="solutions"></div>'

# Regex for curated solutions:
# <div class="solutions">\s*<a class="sol-link[\s\S]*?</div>
content = re.sub(r'<div class="solutions">\s*<a class="sol-link[\s\S]*?</div>', '<div class="solutions"></div>', content)

# 2. Clean Striver rows: replace any <div class="badges">...</div> with <div class="solutions"></div>
content = re.sub(r'<div class="badges">[\s\S]*?</div>', '<div class="solutions"></div>', content)

# Write atomically
tmp_path = INDEX_PATH + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(tmp_path, INDEX_PATH)
print("DSA_Ultimate_Index.html cleaned successfully.")
