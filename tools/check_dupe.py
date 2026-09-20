import re
html = open('DSA_Ultimate_Index.html', 'r', encoding='utf-8').read()
matches = re.findall(r'<li[^>]*data-lc="151"[^>]*>', html)
for m in matches:
    print(m)
