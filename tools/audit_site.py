#!/usr/bin/env python3
"""
Static auditor for the whole learning hub (every .html under the repo root).

    python3 tools/audit_site.py            # summary
    python3 tools/audit_site.py --all      # every hit, not just the first few
    python3 tools/audit_site.py --json out.json

Run it after ANY bulk edit. It is the cheapest way to catch the class of
regression that bulk edits produce: a count that no longer matches the rows
under it, a section whose rows were all removed, an anchor pointing at an id
that was renamed, a page that lost the shared nav.

READ THIS BEFORE BELIEVING A REPORT
-----------------------------------
Two earlier versions of this script produced large numbers of false positives
because their idea of "a container" did not match the markup:

  * `.stats` was closed at the first `</div></div>`, so 9 of the 10 header
    chips looked like orphans.  -> containers are now matched by div depth.
  * a section was assumed to end at `<div class="subsection">`, but the DSA
    index groups rows in `<div class="subpattern">` and the Striver blocks in
    `<div class="pattern">`, so one subpattern's stated count was compared
    against a whole pattern's rows ("12 vs 37").  -> every boundary is in BOUND.

If you add markup with a new grouping element, add it to BOUND or this script
will start lying to you. Verify a surprising hit by hand before "fixing" it.
"""
import os, re, sys, json, html, collections, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {".git", ".venv", "node_modules", "__pycache__"}

# every element that can start a new counted group
BOUND = (r'<div class="subpattern">|<div class="subsection">'
         r'|<section class="|<div class="pattern"|<div class="group"|</body>')

issues = collections.defaultdict(list)
def add(kind, page, detail=""): issues[kind].append((page, detail))

def close_div(s, start):
    """Index just past the </div> that closes the <div> opening at `start`."""
    i = s.find(">", start)
    if i < 0: return -1
    depth, i = 1, i + 1
    for m in re.finditer(r"<div\b|</div>", s[i:]):
        depth += -1 if m.group(0) == "</div>" else 1
        if depth == 0: return i + m.end()
    return -1

def strip_scripts(t):
    return re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", t)

pages = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in SKIP]
    pages += [os.path.join(dp, f) for f in fn if f.endswith(".html")]
pages.sort()

_anchors = {}
def anchors_of(p):
    if p not in _anchors:
        try: s = open(p, encoding="utf-8", errors="ignore").read()
        except Exception: s = ""
        _anchors[p] = set(re.findall(r'\bid="([^"]+)"', s)) | set(re.findall(r'\bname="([^"]+)"', s))
    return _anchors[p]

for path in pages:
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    t = open(path, encoding="utf-8", errors="ignore").read()
    body = strip_scripts(t)

    # ---- page skeleton ----
    if not re.search(r"<title>\s*\S", t): add("no-title", rel)
    if not re.search(r"<h1[ >]", t) and rel != "hub.html" and "ConvertedDocs" not in rel: add("no-h1", rel)
    if 'name="viewport"' not in t: add("no-viewport", rel)
    if rel != "hub.html":
        if "learning-hub-shared.js" not in t: add("missing-shared-js", rel)
        if "learning-hub-shared.css" not in t: add("missing-shared-css", rel)
    if re.search(r'class="(site-nav|global-learning-nav)"', t): add("legacy-nav", rel)
    if len(re.findall(r"<title>", t)) > 1: add("multiple-title", rel)

    # ---- ids / headings / anchors ----
    ids = re.findall(r'\bid="([^"]+)"', body)
    dup = [i for i, c in collections.Counter(ids).items() if c > 1]
    if dup: add("duplicate-id", rel, ", ".join(sorted(dup)[:5]))
    for m in re.finditer(r"<h([1-4])[^>]*>\s*</h\1>", body): add("empty-heading", rel, "h" + m.group(1))
    for _ in re.finditer(r"<a\b[^>]*>\s*</a>", body): add("empty-anchor", rel)

    # ---- content smells ----
    for pat, kind in ((r"\$\{[^}]{1,40}\}", "template-leak"),
                      (r"\b(TODO|TBD|FIXME|lorem ipsum|coming soon)\b", "placeholder"),
                      (r"(?<![\w-])(undefined|NaN|\[object Object\])(?=[<\s.,])", "js-artifact")):
        hits = re.findall(pat, body, re.I)
        if hits: add(kind, rel, ", ".join(sorted({h if isinstance(h, str) else h[0] for h in hits})[:4]))
    if re.search(r"Ã[©¨¢‚]|â€[™œ“]", body): add("mojibake", rel)
    for m in re.finditer(r"(?:[A-Z]:\\\\?[\w\\ .-]{4,}|file:///)", body): add("local-path", rel, m.group(0)[:50])
    if re.search(r"\b(?:password|passcode|pin)\s*[:=]\s*['\"]?\d{4,}", t, re.I): add("inline-secret", rel)
    if re.search(r"console\.(log|debug)\(", t): add("console-log", rel)

    # ---- links ----
    for m in re.finditer(r'href="([^"]+)"', body):
        href = html.unescape(m.group(1))
        if "${" in href or "' +" in href: continue
        if href.startswith("http://"): add("insecure-link", rel, href[:60])
        if href.startswith(("http", "mailto:", "data:", "javascript:", "//")): continue
        if href.strip() == "#": continue          # back-to-top / current-page markers are fine
        if href.startswith("#"): continue
        p = urllib.parse.unquote(href.split("#")[0].split("?")[0])
        if not p: continue
        tgt = os.path.normpath(os.path.join(os.path.dirname(path), p))
        if not os.path.exists(tgt): add("broken-link", rel, href[:60])
        elif "#" in href and tgt.endswith(".html"):
            frag = href.split("#", 1)[1]
            if frag and frag not in anchors_of(tgt): add("dead-anchor", rel, href[:60])

    # ---- header stat chips must live inside a .stats container ----
    spans = []
    for m in re.finditer(r'<div class="stats"', t):
        e = close_div(t, m.start())
        if e > 0: spans.append((m.start(), e))
    for m in re.finditer(r'<div class="stat[ "]', t):
        if not any(a <= m.start() < b for a, b in spans): add("orphan-stat-chip", rel, str(m.start()))

    # ---- stated counts vs actual rows ----
    for m in re.finditer(r'<span class="scount">(\d+) problems?</span>([\s\S]*?)(?=' + BOUND + ")", t):
        actual = len(re.findall(r"<li [^>]*data-lc=", m.group(2)))
        if int(m.group(1)) != actual:
            h = re.search(r"<h3>([^<]*)</h3>", t[max(0, m.start() - 400):m.start()])
            add("count-mismatch", rel, f'{(h.group(1) if h else "?")[:34]}: says {m.group(1)}, has {actual}')
    for m in re.finditer(r">(\d+) concepts?<([\s\S]*?)(?=" + BOUND + ")", t):
        actual = len(re.findall(r"<li [^>]*data-cid=", m.group(2)))
        if actual and int(m.group(1)) != actual: add("count-mismatch", rel, f"{m.group(1)} vs {actual} concepts")

    # ---- empty / duplicated groups ----
    for m in re.finditer(r'<div class="subpattern">', t):
        blk = t[m.start():close_div(t, m.start())]
        if "data-lc=" not in blk:
            h = re.search(r"<h3>([^<]*)</h3>", blk)
            add("empty-subpattern", rel, (h.group(1) if h else "?")[:40])
    for m in re.finditer(r'<ol class="(?:problems|concepts)">([\s\S]*?)</ol>', t):
        inner = m.group(1)
        if "data-lc=" not in inner and "data-cid=" not in inner: add("empty-list", rel)
        row_ids = re.findall(r'<li [^>]*data-(?:lc|cid)="([^"]*)"', inner)
        d = [i for i, c in collections.Counter(row_ids).items() if c > 1]
        if d: add("dup-row-in-list", rel, ",".join(d[:5]))

    # ---- SUBPATTERN n.m numbering must be 1..k inside each pattern ----
    grp = collections.defaultdict(list)
    for s in re.findall(r'<span class="subpattern-tag">SUBPATTERN ([\d.]+)</span>', t):
        a, _, b = s.partition(".")
        try: grp[int(a)].append(int(b))
        except ValueError: add("bad-subpattern-tag", rel, s)
    for p, v in grp.items():
        if v != list(range(1, len(v) + 1)): add("subpattern-numbering", rel, f"pattern {p}: {v}")

    # ---- data-pattern-lcs must list exactly the rows inside that pattern ----
    marks = [(m.start(), m.group(0)) for m in re.finditer(r'<(?:section|div) class="pattern" id="[^"]*"[^>]*>', t)]
    for i, (s, tag) in enumerate(marks):
        e = marks[i + 1][0] if i + 1 < len(marks) else len(t)
        dm = re.search(r'data-pattern-lcs="([^"]*)"', tag)
        if not dm: continue
        declared = set(filter(None, dm.group(1).split(",")))
        actual = set(re.findall(r'<li [^>]*data-lc="([^"]*)"', t[s:e]))
        if declared != actual:
            pid = re.search(r'id="([^"]*)"', tag)
            add("pattern-lcs-drift", rel,
                f'{pid.group(1) if pid else "?"}: '
                f'missing={sorted(actual - declared)[:4]} stale={sorted(declared - actual)[:4]}')

ORDER = ["broken-link", "dead-anchor", "duplicate-id", "count-mismatch", "orphan-stat-chip",
         "empty-subpattern", "empty-list", "dup-row-in-list", "subpattern-numbering",
         "bad-subpattern-tag", "pattern-lcs-drift", "template-leak", "js-artifact", "placeholder",
         "mojibake", "local-path", "inline-secret", "console-log", "legacy-nav", "missing-shared-js",
         "missing-shared-css", "multiple-title", "no-title", "no-h1", "no-viewport",
         "empty-heading", "empty-anchor", "insecure-link"]

show_all = "--all" in sys.argv
print("pages scanned:", len(pages), "\n")
total = 0
for k in ORDER + [k for k in issues if k not in ORDER]:
    v = issues.get(k)
    if not v: continue
    total += len(v)
    print(f"=== {k}: {len(v)} ===")
    for p, d in (v if show_all else v[:8]): print("   ", p, "|", d)
    if not show_all and len(v) > 8: print(f"    ... +{len(v) - 8} (use --all)")
print("\ntotal:", total)
if "--json" in sys.argv:
    out = sys.argv[sys.argv.index("--json") + 1]
    json.dump({k: v for k, v in issues.items()}, open(out, "w"), indent=1)
    print("written:", out)
sys.exit(1 if total else 0)
