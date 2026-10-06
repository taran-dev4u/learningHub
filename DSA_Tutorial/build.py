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
    root_rel = rel + '../'
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
<link rel="stylesheet" href="{root_rel}assets/learning-hub-shared.css">
<link rel="stylesheet" href="{rel}assets/style.css?v=2">
<script src="{root_rel}assets/learning-hub-shared.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script defer src="{rel}assets/app.js?v=2"></script>
</head>
<body>
<div class="nav-bar">{prev_a}<div class="mid"><a href="{rel}index.html">🏠 DSA Tutorial</a> · {mid_label}</div>
<div style="display:flex;gap:8px;align-items:center"><a href="{root_rel}DSA_Ultimate_Index.html" class="dsa-switch-link" title="Switch to DSA Ultimate Index (940 Problems Sheet)">📊 DSA Index ↗</a>{next_a}</div></div>
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
UNIQUE_PROBLEMS = len({p['prob']['lc'] for p in pages if p['kind'] == 'problem'})

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
def plain_text(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', str(s or ''))).strip()

STOPWORDS = {
    'and', 'the', 'for', 'with', 'from', 'into', 'that', 'this', 'when', 'your',
    'you', 'are', 'but', 'all', 'any', 'each', 'every', 'using', 'use', 'uses',
    'patterns', 'pattern', 'problems', 'problem', 'array', 'arrays'
}

def keyword_list(*parts, limit=10):
    words = []
    seen = set()
    text = ' '.join(plain_text(p).lower() for p in parts)
    for word in re.findall(r'[a-z][a-z0-9+\-]{2,}', text):
        word = word.strip('-')
        if word in STOPWORDS or word in seen:
            continue
        seen.add(word)
        words.append(word)
        if len(words) >= limit:
            break
    return words

PHASES = [
    ('foundation', '0. Language & Foundations'),
    ('arrays', '1. Arrays, Strings & Hashing'),
    ('linear', '2. Linked Lists, Stacks & Heaps'),
    ('trees', '3. Trees, Tries & Hierarchies'),
    ('graphs', '4. Graphs & Traversal'),
    ('search', '5. Search, Sort, Greedy & Intervals'),
    ('dp', '6. Recursion & Dynamic Programming'),
    ('advanced', '7. Advanced Data Structures & Specialized Algorithms'),
]

def phase_for_title(title):
    t = title.lower()
    if any(x in t for x in ('dynamic programming', 'backtracking')):
        return 'dp'
    if any(x in t for x in ('graph', 'bfs', 'multi-source', 'union')):
        return 'graphs'
    if any(x in t for x in ('tree', 'trie')):
        return 'trees'
    if any(x in t for x in ('linked list', 'stack', 'heap', 'iterator', 'data-stream')):
        return 'linear'
    if any(x in t for x in ('binary search', 'greedy', 'interval', 'line sweep', 'sorting')):
        return 'search'
    if any(x in t for x in ('segment tree', 'fenwick', 'randomized', 'bit manipulation', 'math', 'geometry', 'design')):
        return 'advanced'
    return 'arrays'

def diff_summary(problems):
    counts = {'E': 0, 'M': 0, 'H': 0}
    for prob in problems:
        counts[prob['diff']] = counts.get(prob['diff'], 0) + 1
    return ''.join(f'<span class="mini-diff {k}">{k}: {v}</span>' for k, v in counts.items() if v)

def subtopic_anchor(sub):
    return 'subtopic-' + re.sub(r'[^a-z0-9]+', '-', sub['tag'].lower()).strip('-')

def render_hub():
    foundation_rows = []
    for label, prefix, entries in (
        ('Python Primer', 'python', content_python.PAGES),
        ('Foundations', 'foundations', content_foundations.PAGES),
    ):
        for idx, pg in enumerate(entries, 1):
            search = f'{label} {pg["title"]} {pg["blurb"]}'.lower()
            foundation_rows.append(
                f'<a class="sheet-row foundation-row" href="{prefix}/{pg["id"]}.html" data-search="{esc(search)}">'
                f'<span class="sheet-index">{idx:02d}</span><span class="sheet-main">'
                f'<strong>{esc(pg["title"])}</strong><small>{esc(pg["blurb"])}</small></span>'
                f'<span class="sheet-type">{esc(label)}</span></a>')

    phase_nav = ''.join(
        f'<a href="#phase-{key}">{esc(label)}</a>' for key, label in PHASES
    )

    foundation_section = (
        '<section class="sheet-section" id="phase-foundation" data-search="python foundations complexity data structures recursion sorting">'
        '<div class="sheet-section-head"><div><span class="stage-label">0. Language &amp; Foundations</span>'
        '<h2>Build the base before patterns</h2></div>'
        f'<span class="sheet-count">{len(content_python.PAGES) + len(content_foundations.PAGES)} lessons</span></div>'
        '<p class="sheet-section-note">Start here if Python syntax, complexity, recursion, hashing, sorting, or core data structures feel shaky. These pages are the vocabulary used by every pattern below.</p>'
        '<div class="sheet-rows">' + ''.join(foundation_rows) + '</div></section>'
    )

    phase_sections = {'foundation': foundation_section}
    for key, label in PHASES[1:]:
        matching = [pat for pat in CURR if phase_for_title(pat['title']) == key]
        if not matching:
            continue
        pattern_html = []
        total_subs = sum(len(pat['subpatterns']) for pat in matching)
        total_probs = sum(len(sub['problems']) for pat in matching for sub in pat['subpatterns'])
        for pat in matching:
            meta = content_patterns.PATTERNS.get(pat['title'], {})
            pi = pat['_page']['pi']
            pp = pat['_page']
            all_probs = [prob for sub in pat['subpatterns'] for prob in sub['problems']]
            keywords = keyword_list(
                pat['title'], meta.get('short', ''), meta.get('intuition', ''),
                ' '.join(meta.get('signals', [])),
                ' '.join(s['name'] + ' ' + s['desc'] for s in pat['subpatterns']),
                limit=12,
            )
            sub_rows = []
            for sub in pat['subpatterns']:
                row_search = f'{pat["title"]} {sub["tag"]} {sub["name"]} {sub["desc"]} ' + ' '.join(p['name'] for p in sub['problems'])
                samples = ', '.join(f'#{p["lc"]} {p["name"]}' for p in sub['problems'][:4])
                more = f' +{len(sub["problems"]) - 4} more' if len(sub['problems']) > 4 else ''
                sub_rows.append(
                    f'<div class="sheet-subtopic" data-search="{esc(row_search.lower())}">'
                    f'<div class="subtopic-copy"><a href="{pp["path"]}#{subtopic_anchor(sub)}">'
                    f'<b>{esc(sub["tag"])}</b> {esc(sub["name"])}</a>'
                    f'<p>{esc(sub["desc"])}</p>'
                    f'<small>{esc(samples + more)}</small></div>'
                    f'<a class="subtopic-open" href="{pp["path"]}#{subtopic_anchor(sub)}">'
                    f'{len(sub["problems"])} practice pages</a></div>')
            signal_html = ''.join(f'<li>{s}</li>' for s in meta.get('signals', [])[:4])
            search_text = f'{label} {pat["title"]} {meta.get("short", "")} ' + ' '.join(keywords)
            pattern_html.append(
                f'<article class="sheet-topic" id="pattern-{pi:02d}" data-search="{esc(search_text.lower())}">'
                f'<div class="topic-top"><div><span class="sheet-index">P{pi:02d}</span>'
                f'<h3>{esc(pat["title"])}</h3><p>{esc(meta.get("short", ""))}</p></div>'
                f'<a class="learn-btn" href="{pp["path"]}">Open full tutorial</a></div>'
                f'<div class="topic-meta"><span>{len(pat["subpatterns"])} subtopics</span>'
                f'<span>{len(all_probs)} practice pages</span>{diff_summary(all_probs)}'
                f'<span data-count-of="p{pi:02d}-" data-lcs="{",".join(str(p["lc"]) for p in all_probs)}"></span></div>'
                f'<div class="keyword-line">{"".join(f"<span>{esc(k)}</span>" for k in keywords)}</div>'
                f'<div class="signal-box"><strong>Use this when:</strong><ul>{signal_html}</ul></div>'
                f'<div class="sheet-subtopics">{"".join(sub_rows)}</div></article>')
        phase_sections[key] = (
            f'<section class="sheet-section" id="phase-{key}" data-search="{esc(label.lower())}">'
            f'<div class="sheet-section-head"><div><span class="stage-label">{esc(label)}</span>'
            f'<h2>{esc(label.split(". ", 1)[1])}</h2></div>'
            f'<span class="sheet-count">{len(matching)} topics · {total_subs} subtopics · {total_probs} practice pages</span></div>'
            f'<div class="sheet-topic-list">{"".join(pattern_html)}</div></section>'
        )

    ordered_sections = ''.join(phase_sections[key] for key, _ in PHASES if key in phase_sections)
    keyword_cloud = []
    seen_keywords = set()
    for pat in CURR:
        meta = content_patterns.PATTERNS.get(pat['title'], {})
        for key in keyword_list(pat['title'], meta.get('short', ''), ' '.join(s['name'] for s in pat['subpatterns']), limit=8):
            if key not in seen_keywords:
                seen_keywords.add(key)
                keyword_cloud.append(f'<a href="#pattern-{pat["_page"]["pi"]:02d}">{esc(key)}</a>')
            if len(keyword_cloud) >= 72:
                break
        if len(keyword_cloud) >= 72:
            break

    body = f'''
<div class="tutorial-sheet">
<section class="sheet-hero">
  <div>
    <span class="eyebrow">Taran's DSA Tutorial</span>
    <h1>Concept-first DSA learning sheet</h1>
    <p>This page is now the tutorial roadmap: topics, subtopics, keywords, recognition signals, templates, and the existing problem tutorials arranged from fundamentals to advanced interview patterns.</p>
  </div>
  <div class="sheet-stats">
    <span><b>{len(content_python.PAGES) + len(content_foundations.PAGES)}</b> foundation lessons</span>
    <span><b>{len(CURR)}</b> core topics</span>
    <span><b>{sum(len(p["subpatterns"]) for p in CURR)}</b> subtopics</span>
    <span><b>{UNIQUE_PROBLEMS}</b> unique problems</span>
  </div>
</section>

<div class="companion-switch-banner" style="background:var(--bg-card);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:10px;padding:14px 18px;margin:18px 0 22px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;">
  <div>
    <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:var(--accent);margin-bottom:2px;">Comprehensive Problem Sheet &amp; Tracker</div>
    <div style="font-size:15px;font-weight:700;color:var(--text);margin-bottom:2px;">DSA Ultimate Index (940 Problems Sheet)</div>
    <div style="font-size:12.5px;color:var(--text-dim);">Switch to the 47-pattern master sheet with Blind 75, NeetCode 150, Striver A2Z, multi-video side panel, multi-approach reader, and progress tracking.</div>
  </div>
  <a href="../DSA_Ultimate_Index.html" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:7px;background:var(--accent);color:#fff;text-decoration:none;font-size:13px;font-weight:700;white-space:nowrap;">Switch to DSA Ultimate Index (940 Problems) &rarr;</a>
</div>

<div class="sheet-toolbar">
  <input class="searchbar" id="hub-search" placeholder="Filter concepts, subtopics, keywords, or problems...">
  <div class="phase-nav">{phase_nav}</div>
</div>

<section class="keyword-index">
  <div><span class="stage-label">Keyword Index</span><h2>Jump by the word you recognize in a question</h2></div>
  <div class="keyword-cloud">{''.join(keyword_cloud)}</div>
</section>

{ordered_sections}
</div>
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
            items += (f'<li data-lc="{prob["lc"]}" data-lc-url="{esc(prob["url"] or "")}"><input type="checkbox" data-id="p{pi:02d}-lc{prob["lc"]}" title="mark solved">'
                      f'<span class="num">#{prob["lc"]}</span><span class="pill {prob["diff"]}">{prob["diff"]}</span>'
                      f'<a href="../{prob["_path"]}">{esc(prob["name"])}</a>{badges}</li>')
        parts.append(f'<h3 id="{subtopic_anchor(sub)}">{esc(sub["tag"])} — {esc(sub["name"])}</h3>'
                     f'<p class="progress-note">{esc(sub["desc"])}</p><ul class="plist">{items}</ul>')
    crumb = f'<a href="../index.html">Home</a> › Patterns › {esc(pat["title"])}'
    return shell(pat['title'], '\n'.join(parts), 1, pg['_prev'], pg['_next'], crumb, f'Pattern {pi} of {len(CURR)}')

def render_problem(pg):
    prob, sub, pat, pi = pg['prob'], pg['sub'], pg['pat'], pg['pi']
    meta = content_patterns.PATTERNS.get(pat['title'], {})
    badges = ''.join(BADGE_HTML[b] for b in prob['badges'])
    lc_icon = LC_SVG.format(url=prob['url']) if prob['url'] else ''
    comp = ''.join(f'<span class="chip">{esc(c.title())}</span>' for c in prob['companies'])
    video = ''
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
<p>{comp} &nbsp; {solved_cb}</p>
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

def write_page(path, text):
    """Write atomically: overwriting in place can fail with EINVAL on mounted
    filesystems, so write a temp file next to the target and rename it."""
    import time
    last = None
    for _ in range(4):
        try:
            tmp = path + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                f.write(text)
            os.replace(tmp, path)
            return
        except OSError as exc:
            last = exc
            time.sleep(0.2)
    raise last



for pg in pages:
    if pg['kind'] == 'hub': out = render_hub()
    elif pg['kind'] == 'pattern': out = render_pattern(pg)
    elif pg['kind'] == 'problem': out = render_problem(pg)
    else: out = render_content(pg)
    write_page(os.path.join(ROOT, pg['path'].replace('/', os.sep)), out)

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
