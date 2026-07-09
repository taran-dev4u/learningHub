#!/usr/bin/env python3
"""Integrity checks for the DSA Tutorial site. Run after every build.py."""
import os, re, json, sys

root = os.path.dirname(os.path.abspath(__file__))
ok = True

htmls = []
for d, _, fs in os.walk(root):
    if '.git' in d or '__pycache__' in d:
        continue
    htmls += [os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/')
              for f in fs if f.endswith('.html')]

broken = []
for h in htmls:
    src = open(os.path.join(root, h), encoding='utf-8').read()
    base = os.path.dirname(h)
    for m in re.finditer(r'(?:href|src)="([^"#]+)"', src):
        url = m.group(1)
        if url.startswith(('http', 'mailto')):
            continue
        t = os.path.normpath(os.path.join(base, url)).replace(os.sep, '/')
        if not os.path.exists(os.path.join(root, t)):
            broken.append((h, url))

cur = json.load(open(os.path.join(root, 'data', 'curriculum.json'), encoding='utf-8'))
want = sum(len(s['problems']) for p in cur for s in p['subpatterns'])
probs = [h for h in htmls if h.startswith('problems/')]
no_icon = [p for p in probs
           if 'lc-icon' not in open(os.path.join(root, p), encoding='utf-8').read()]
no_pager = [h for h in htmls
            if 'pager' not in open(os.path.join(root, h), encoding='utf-8').read()]

def check(label, cond, detail=''):
    global ok
    print(('PASS' if cond else 'FAIL'), label, detail if not cond else '')
    ok = ok and cond

check('all internal links resolve', not broken, str(broken[:5]))
check(f'all {want} curriculum problems have pages', len(probs) == want,
      f'{len(probs)} != {want}')
check('every problem page has a LeetCode icon', not no_icon, str(no_icon[:5]))
check('every page has a prev/next pager', not no_pager, str(no_pager[:5]))
check('total page count sane', len(htmls) >= want + 40, str(len(htmls)))

sys.exit(0 if ok else 1)
