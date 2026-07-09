#!/usr/bin/env python3
"""DSA Tutorial site generator.

Reads data/curriculum.json + content_*.py and generates every page with a
connected prev/next chain. Edit content files, then re-run: python3 build.py
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))

import content_python, content_foundations, content_patterns, content_problems, content_statements

CURR = json.load(open(os.path.join(ROOT, 'data', 'curriculum.json'), encoding='utf-8'))
CURR = [p for p in CURR if p['subpatterns']]  # drop empty trailing sections

def slugify(s):
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s[:60]

def esc(s):
    return html.escape(s, quote=False)

BADGE_HTML = {'B75': '<span class="badge b75" title="Blind 75">★75</span>',
              'NC150': '<span class="badge nc" title="NeetCode 150">★NC</span>',
              'G75': '<span class="badge g75" title="Grind 75">★G</span>'}

LC_SVG = ('<a class="lc-icon" href="{url}" target="_blank" rel="noopener" title="Open on LeetCode">'
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
          '<path d="M14.5 3l-8 8a5 5 0 000 7l2 2a5 5 0 007 0l2.5-2.5" stroke="#ffa116" stroke-width="2.4" stroke-linecap="round"/>'
          '<path d="M9 13h10" stroke="#ffa116" stroke-width="2.4" stroke-linecap="round"/></svg>LeetCode</a>')

# ---------------------------------------------------------------- page shell
def shell(title, body, depth, prev_page, next_page, crumb_html, mid_label):
    rel = '../' * depth
    prev_a = (f'<a href="{rel}{prev_page["path"]}">← {esc(prev_page["short"])}</a>' if prev_page else '<span></span>')
    next_a = (f'<a href="{rel}{next_page["path"]}">{esc(next_page["short"])} →</a>' if next_page else '<span></span>')
    pager_prev = (f'<a href="{rel}{prev_page["path"]}"><span class="lbl">← Previous</span>{esc(prev_page["short"])}</a>'
                  if prev_page else '<span></span>')
    pager_next = (f'<a href="{rel}{next_page["path"]}" style="text-align:right"><span class="lbl">Next →</span>{esc(next_page["short"])}</a>'
                  if next_page else '<span></span>')
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} — DSA Tutorial</title>
<link rel="stylesheet" href="{rel}assets/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script defer src="{rel}assets/app.js"></script>
</head>
<body>
<div class="nav-bar">{prev_a}<div class="mid"><a href="{rel}index.html">🏠 DSA Tutorial</a> · {mid_label}</div>
<div style="display:flex;gap:8px;align-items:center">{next_a}<button class="theme-btn" title="Toggle theme">☀️</button></div></div>
<div class="container">
<div class="crumbs">{crumb_html}</div>
{body}
<div class="pager">{pager_prev}{pager_next}</div>
</div>
</body>
</html>'''

# ---------------------------------------------------------------- page list
pages = []  # each: {path, short, title, kind, ...}

pages.append({'path': 'index.html', 'short': 'Home', 'title': 'DSA Tutorial', 'kind': 'hub'})

for pg in content_python.PAGES:
    pages.append({'path': f'python/{pg["id"]}.html', 'short': pg['short'], 'title': pg['title'],
                  'kind': 'content', 'body': pg['body'], 'crumb': 'Python Primer', 'blurb': pg['blurb']})

for pg in content_foundations.PAGES:
    pages.append({'path': f'foundations/{pg["id"]}.html', 'short': pg['short'], 'title': pg['title'],
                  'kind': 'content', 'body': pg['body'], 'crumb': 'Foundations', 'blurb': pg['blurb']})

seq = 0
for pi, pat in enumerate(CURR, 1):
    meta = content_patterns.PATTERNS.get(pat['title'], {})
    pslug = f'p{pi:02d}-{slugify(meta.get("slug", pat["title"]))}'
    ppage = {'path': f'patterns/{pslug}.html', 'short': pat['title'].replace(' Patterns',''),
             'title': pat['title'], 'kind': 'pattern', 'pat': pat, 'meta': meta, 'pi': pi}
    pages.append(ppage)
    pat['_page'] = ppage
    for sub in pat['subpatterns']:
        for prob in sub['problems']:
            seq += 1
            fn = f'problems/{seq:04d}-lc{prob["lc"]}-{slugify(prob["name"])}.html'
            pages.append({'path': fn, 'short': f'#{prob["lc"]} {prob["name"]}', 'title': f'{prob["name"]}',
                          'kind': 'problem', 'prob': prob, 'sub': sub, 'pat': pat, 'pi': pi, 'seq': seq})
            prob['_path'] = fn

TOTAL = seq

# duplicate map: lc -> list of seqs
from collections import defaultdict
occ = defaultdict(list)
for pg in pages:
    if pg['kind'] == 'problem':
        occ[pg['prob']['lc']].append(pg)

# lc -> filename (basename within problems/) for [[nn]] shorthand links in deep content
LC_HREF = {lc: pgs[0]['path'].split('/', 1)[1] for lc, pgs in occ.items()}

def link_lc(m):
    lc = int(m.group(1))
    href = LC_HREF.get(lc)
    return f'<a href="{href}">#{lc}</a>' if href else f'#{lc}'

# ---------------------------------------------------------------- renderers
def render_hub():
    py_cards = ''.join(
        f'<a class="card" href="python/{pg["id"]}.html" data-search="{esc(pg["title"].lower())}">'
        f'<div class="t">{esc(pg["title"])}</div><div class="d">{esc(pg["blurb"])}</div></a>'
        for pg in content_python.PAGES)
    f_cards = ''.join(
        f'<a class="card" href="foundations/{pg["id"]}.html" data-search="{esc(pg["title"].lower())}">'
        f'<div class="t">{esc(pg["title"])}</div><div class="d">{esc(pg["blurb"])}</div></a>'
        for pg in content_foundations.PAGES)
    pat_cards = ''
    for pat in CURR:
        n = sum(len(s['problems']) for s in pat['subpatterns'])
        pp = pat['_page']
        short = esc(pat['title'])
        meta = content_patterns.PATTERNS.get(pat['title'], {})
        pat_cards += (f'<a class="card" href="{pp["path"]}" data-search="{short.lower()} '
                      f'{esc(" ".join(s["name"].lower() for s in pat["subpatterns"]))}">'
                      f'<div class="t">{short}</div><div class="d">{esc(meta.get("short", ""))}</div>'
                      f'<div class="n">{len(pat["subpatterns"])} subpatterns · {n} problems · '
                      f'<span data-count-of="p{pat["_page"]["pi"]:02d}-"></span></div></a>')
    body = f'''
<h1>📘 DSA Tutorial</h1>
<p>A complete, beginner-first Data Structures &amp; Algorithms course. Start with the Python Primer,
build the Foundations, then master all {len(CURR)} patterns and {TOTAL} problems.
Every page teaches — LeetCode is just one click away when you want to practice.</p>
<p class="progress-note">Tip: use <kbd>←</kbd> and <kbd>→</kbd> to move between pages; every page follows the previous one in the curriculum.</p>
<input class="searchbar" id="hub-search" placeholder="🔍 Filter topics… (e.g. sliding window, heap, dp)">

<div class="section-head"><h2>🐍 Python Primer</h2><span class="progress-note">know your tools first</span></div>
<div class="grid">{py_cards}</div>

<div class="section-head"><h2>🧱 Foundations</h2><span class="progress-note">every data structure from zero</span></div>
<div class="grid">{f_cards}</div>

<div class="section-head"><h2>🧩 The {len(CURR)} Patterns</h2><span class="progress-note">every problem, fully taught</span></div>
<div class="grid">{pat_cards}</div>
'''
    return shell('DSA Tutorial', body, 0, None, None, 'Home', 'Beginner → Interview-ready')

def render_pattern(pg):
    pat, meta, pi = pg['pat'], pg['meta'], pg['pi']
    n = sum(len(s['problems']) for s in pat['subpatterns'])
    parts = [f'<h1>🧩 {esc(pat["title"])}</h1>'
             f'<p class="progress-note">{len(pat["subpatterns"])} subpatterns · {n} problems · <span data-count-of="p{pi:02d}-"></span></p>']
    if meta.get('intuition'):
        parts.append(f'<h2>1. Intuition — the mental model</h2>{meta["intuition"]}')
    if meta.get('aha'):
        parts.append(f'<div class="insight"><strong>💡 The “aha” insight</strong><br>{meta["aha"]}</div>')
    if meta.get('signals'):
        sig = ''.join(f'<li>{s}</li>' for s in meta['signals'])
        parts.append(f'<h2>2. Recognition signals</h2><p>Think of this pattern when the problem says:</p><ul>{sig}</ul>')
    if meta.get('template'):
        parts.append(f'<h2>3. Master template</h2><pre><code>{esc(meta["template"])}</code></pre>')
        if meta.get('template_notes'):
            parts.append(f'<p>{meta["template_notes"]}</p>')
    if meta.get('complexity'):
        parts.append(f'<h2>4. Complexity of the template</h2><p>{meta["complexity"]}</p>')
    if meta.get('mistakes'):
        mm = ''.join(f'<li>{m}</li>' for m in meta['mistakes'])
        parts.append(f'<h2>5. Common mistakes</h2><ul>{mm}</ul>')
    parts.append('<h2>6. Subpatterns &amp; problems</h2>')
    for sub in pat['subpatterns']:
        items = ''
        for prob in sub['problems']:
            badges = ''.join(BADGE_HTML[b] for b in prob['badges'])
            items += (f'<li><input type="checkbox" data-id="p{pi:02d}-lc{prob["lc"]}" title="mark solved">'
                      f'<span class="num">#{prob["lc"]}</span><span class="pill {prob["diff"]}">{prob["diff"]}</span>'
                      f'<a href="../{prob["_path"]}">{esc(prob["name"])}</a>{badges}</li>')
        parts.append(f'<h3>{esc(sub["tag"])} — {esc(sub["name"])}</h3>'
                     f'<p class="progress-note">{esc(sub["desc"])}</p><ul class="plist">{items}</ul>')
    crumb = f'<a href="../index.html">Home</a> › Patterns › {esc(pat["title"])}'
    return shell(pat['title'], '\n'.join(parts), 1, pg['_prev'], pg['_next'], crumb, f'Pattern {pi} of {len(CURR)}')

def render_problem(pg):
    prob, sub, pat, pi = pg['prob'], pg['sub'], pg['pat'], pg['pi']
    meta = content_patterns.PATTERNS.get(pat['title'], {})
    badges = ''.join(BADGE_HTML[b] for b in prob['badges'])
    lc_icon = LC_SVG.format(url=prob['url']) if prob['url'] else ''
    comp = ''.join(f'<span class="chip">{esc(c.title())}</span>' for c in prob['companies'])
    video = (f'<a class="chip" href="{prob["video"]}" target="_blank" rel="noopener">🎬 Video walkthrough</a>'
             if prob.get('video') else '')
    dups = [o for o in occ[prob['lc']] if o['seq'] != pg['seq']]
    dup_html = ''
    if dups:
        links = ', '.join(f'<a href="{d["path"].split("/",1)[1]}">{esc(d["pat"]["title"].replace(" Patterns",""))}</a>' for d in dups)
        dup_html = f'<p class="progress-note">This problem also appears under: {links} — same problem, different lens.</p>'

    stmt = content_statements.STATEMENTS.get(prob['lc'], '')
    stmt_html = ''
    if stmt:
        stmt_html = (f'<h2>📋 The problem</h2><p>{esc(stmt)}</p>'
                     '<p class="progress-note">Restated in our own words — the LeetCode icon above opens the '
                     'formal statement with exact constraints and examples.</p>')

    deep = content_problems.DEEP.get((pi, prob['lc'])) or content_problems.DEEP.get(prob['lc'])
    if deep:
        main = re.sub(r'\[\[(\d+)\]\]', link_lc, deep)
    else:
        insight = content_problems.INSIGHTS.get(prob['lc'], '')
        insight_html = (f'<div class="insight"><strong>💡 Key idea</strong><br>{insight}</div>' if insight else '')
        tmpl = (f'<h2>Pattern template to adapt</h2><p>Start from the {esc(pat["title"].replace(" Patterns",""))} '
                f'master template and adapt the marked parts to this problem:</p>'
                f'<pre><code>{esc(meta["template"])}</code></pre>' if meta.get('template') else '')
        sig = ''
        if meta.get('signals'):
            sig = ('<h2>Why this pattern?</h2><ul>' + ''.join(f'<li>{s}</li>' for s in meta['signals'][:4]) + '</ul>')
        main = f'''
<h2>Where this fits</h2>
<p><strong>{esc(sub["name"])}</strong> — {esc(sub["desc"])}</p>
{insight_html}
{sig}
{tmpl}
<h2>How to work on it now</h2>
<ol>
<li>Read the problem on LeetCode (icon above) and restate it in your own words.</li>
<li>Write the brute force first — know what you are improving.</li>
<li>Apply the subpattern idea above; dry-run your code on a 4–5 element example by hand.</li>
<li>Check edge cases: empty input, one element, duplicates, extremes.</li>
</ol>
<div class="status-light">📖 <strong>Deep tutorial status:</strong> guided outline (v1). A full step-by-step walkthrough
(brute force → insight → dry run → commented solution → edge cases → follow-ups) is scheduled for this page in the
deepening sessions — see <code>PROGRESS.md</code>. Nothing will be skipped.</div>'''

    solved_cb = f'<label style="font-size:14px;color:var(--text-dim)"><input type="checkbox" data-id="p{pi:02d}-lc{prob["lc"]}"> mark solved</label>'
    body = f'''
<h1><span class="num" style="color:var(--text-dim)">#{prob['lc']}</span> {esc(prob['name'])}
<span class="pill {prob['diff']}">{ {'E':'Easy','M':'Medium','H':'Hard'}[prob['diff']] }</span>{badges}{lc_icon}</h1>
<p>{comp} {video} &nbsp; {solved_cb}</p>
<p class="progress-note">Pattern: <a href="../{pat['_page']['path'].replace('patterns/','../patterns/')[3:]}">{esc(pat['title'])}</a>
 › Subpattern {esc(sub['tag'])}: {esc(sub['name'])} · Problem {pg['seq']} of {TOTAL}</p>
{dup_html}
{stmt_html}
{main}
'''
    crumb = (f'<a href="../index.html">Home</a> › <a href="../{pat["_page"]["path"]}">{esc(pat["title"])}</a> '
             f'› {esc(sub["name"])} › #{prob["lc"]}')
    return shell(f'#{prob["lc"]} {prob["name"]}', body, 1, pg['_prev'], pg['_next'], crumb,
                 f'Problem {pg["seq"]} / {TOTAL}')

def render_content(pg):
    crumb = f'<a href="../index.html">Home</a> › {pg["crumb"]} › {esc(pg["short"])}'
    body = f'<h1>{esc(pg["title"])}</h1>\n{pg["body"]}'
    return shell(pg['title'], body, 1, pg['_prev'], pg['_next'], crumb, pg['crumb'])

# ---------------------------------------------------------------- link chain + write
for i, pg in enumerate(pages):
    pg['_prev'] = pages[i-1] if i > 0 else None
    pg['_next'] = pages[i+1] if i+1 < len(pages) else None

os.makedirs(os.path.join(ROOT, 'problems'), exist_ok=True)
os.makedirs(os.path.join(ROOT, 'patterns'), exist_ok=True)
os.makedirs(os.path.join(ROOT, 'python'), exist_ok=True)
os.makedirs(os.path.join(ROOT, 'foundations'), exist_ok=True)

for pg in pages:
    if pg['kind'] == 'hub': out = render_hub()
    elif pg['kind'] == 'pattern': out = render_pattern(pg)
    elif pg['kind'] == 'problem': out = render_problem(pg)
    else: out = render_content(pg)
    with open(os.path.join(ROOT, pg['path'].replace('/', os.sep)), 'w', encoding='utf-8') as f:
        f.write(out)

# ---------------------------------------------------------------- PROGRESS.md
lines = ['# DSA Tutorial — Deepening Progress', '',
         'Tick a box when the problem page has its FULL deep tutorial (all 12 steps of the master prompt).',
         'Generated by build.py — safe to edit the checkboxes by hand.', '']
for pat in CURR:
    pi = pat['_page']['pi']
    lines.append('')
    lines.append(f'## {pat["title"]}')
    for sub in pat['subpatterns']:
        lines.append('')
        lines.append(f'### {sub["tag"]} {sub["name"]}')
        for prob in sub['problems']:
            deep = ((pi, prob['lc']) in content_problems.DEEP
                    or prob['lc'] in content_problems.DEEP)
            box = 'x' if deep else ' '
            lines.append(f'- [{box}] #{prob["lc"]} {esc(prob["name"])} ({prob["diff"]}) — '
                         f'`{prob["_path"]}`')
    lines.append('')

with open(os.path.join(ROOT, 'PROGRESS.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

# ---------------------------------------------------------------- build summary
deep_count = sum(1 for pg in pages if pg['kind'] == 'problem'
                 and (content_problems.DEEP.get((pg['pi'], pg['prob']['lc']))
                      or content_problems.DEEP.get(pg['prob']['lc'])))
print(f'Built {len(pages)} pages · {TOTAL} problems · {deep_count} with deep tutorials.')
