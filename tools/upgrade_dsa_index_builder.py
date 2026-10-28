import os
import re
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, 'DSA_Ultimate_Index.html')

def atomic_write(filepath, content):
    tmp = filepath + '.atomic.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(content)
    for attempt in range(5):
        try:
            if os.path.exists(filepath):
                os.replace(tmp, filepath)
            else:
                os.rename(tmp, filepath)
            break
        except Exception as e:
            if attempt == 4:
                raise
            time.sleep(0.2)

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Original file length: {len(html)} chars, {len(html.splitlines())} lines")

# 1. Parse all 47 patterns
pattern_matches = list(re.finditer(r'<(?:section|div)\s+class="pattern"\s+id="([^"]+)"[^>]*>', html))
print(f"Pattern tags found: {len(pattern_matches)}")

sidebar_items = []
for i, m in enumerate(pattern_matches):
    pid = m.group(1)
    sub = html[m.start():m.start() + 2000]
    h2_m = re.search(r'<h2>([^<]+)</h2>', sub)
    title = h2_m.group(1).strip() if h2_m else pid
    next_start = pattern_matches[i+1].start() if i + 1 < len(pattern_matches) else len(html)
    pat_body = html[m.start():next_start]
    lcs = set(re.findall(r'<li [^>]*data-lc="([^"]+)"', pat_body))
    sidebar_items.append({
        'id': pid,
        'title': title,
        'count': len(lcs),
        'index': i + 1
    })

# 2. Modern Amazon SDE Prep CSS
modern_css = '''
  :root {
    --bg: #f7f8fb;
    --surface: #ffffff;
    --surface-2: #eef2f7;
    --surface-3: #e4eaf2;
    --text: #172033;
    --muted: #5b6578;
    --faint: #7a8599;
    --border: #dbe2ec;
    --navy: #172554;
    --navy-2: #1e3a8a;
    --blue: #2563eb;
    --amber: #f59e0b;
    --green: #0f9f6e;
    --red: #dc4c64;
    --violet: #7c3aed;
    --shadow: 0 4px 16px rgba(23, 32, 51, 0.06);
    --shadow-lift: 0 12px 32px rgba(23, 32, 51, 0.12);
    --sidebar-w: 290px;
    --hub-nav-h: 53px;

    /* Theme compatibility aliases */
    --bg-elev: var(--surface-2);
    --bg-card: var(--surface);
    --bg-row-alt: var(--surface-2);
    --text-dim: var(--muted);
    --text-faint: var(--faint);
    --border-strong: var(--border);
    --accent: var(--blue);
    --accent-dim: rgba(37, 99, 235, 0.1);
    --link: var(--blue);
    --quote-bg: rgba(37, 99, 235, 0.05);
    --easy: var(--green);
    --medium: var(--amber);
    --hard: var(--red);
    --blind75: #dc2626;
    --neetcode: #059669;
    --grind: #d97706;
    --striver: #7c3aed;
    --shadow-card: var(--shadow);
    --shadow-banner: var(--shadow-lift);
    --done: var(--green);
    --done-bg: rgba(15, 159, 110, 0.12);
  }

  html.dark:root, [data-theme="dark"] {
    --bg: #0b1120;
    --surface: #111827;
    --surface-2: #182235;
    --surface-3: #223047;
    --text: #eef3fb;
    --muted: #a6b0c2;
    --faint: #7f8ba0;
    --border: #29364b;
    --navy: #dce7ff;
    --navy-2: #7da2ff;
    --blue: #76a0ff;
    --amber: #fbbf24;
    --green: #35d3a0;
    --red: #ff8098;
    --violet: #b69cff;
    --shadow: 0 8px 24px rgba(0, 0, 0, 0.32);
    --shadow-lift: 0 16px 40px rgba(0, 0, 0, 0.45);
    --accent-dim: rgba(118, 160, 255, 0.14);
    --quote-bg: rgba(118, 160, 255, 0.06);
    --done-bg: rgba(53, 211, 160, 0.12);
    color-scheme: dark;
  }

  html.black:root, [data-theme="black"] {
    --bg: #000000;
    --surface: #090909;
    --surface-2: #101010;
    --surface-3: #181818;
    --text: #f5f5f5;
    --muted: #b8b8b8;
    --faint: #858585;
    --border: #292929;
    --navy: #f3f4f6;
    --navy-2: #9db8ff;
    --blue: #7aa2ff;
    --amber: #fbbf24;
    --green: #42d6a4;
    --red: #ff7b91;
    --violet: #bc9cff;
    --shadow: 0 8px 24px rgba(0, 0, 0, 0.65);
    --shadow-lift: 0 18px 48px rgba(0, 0, 0, 0.85);
    --accent-dim: rgba(122, 162, 255, 0.14);
    --quote-bg: rgba(122, 162, 255, 0.05);
    --done-bg: rgba(66, 214, 164, 0.12);
    color-scheme: dark;
  }

  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0; line-height: 1.55;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: var(--bg); color: var(--text);
    -webkit-font-smoothing: antialiased;
    transition: background 0.2s ease, color 0.2s ease;
  }

  /* ===== APP LAYOUT & SIDEBAR (Amazon Prep Style) ===== */
  .app-layout {
    display: flex;
    min-height: calc(100vh - var(--hub-nav-h, 53px));
    position: relative;
    width: 100%;
  }

  .sidebar {
    position: fixed;
    left: 0;
    top: var(--hub-nav-h, 53px);
    bottom: 0;
    width: var(--sidebar-w, 290px);
    overflow-y: auto;
    background: var(--surface-2);
    border-right: 1px solid var(--border);
    transition: transform .24s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1000;
  }

  .sidebar-inner {
    padding: 18px 14px 48px;
  }

  .sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding: 0 6px;
  }

  .sidebar-label {
    margin: 0;
    color: var(--faint);
    font-size: 11px;
    font-weight: 900;
    letter-spacing: .08em;
    text-transform: uppercase;
  }

  .sidebar-stat {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 11px;
    font-weight: 800;
    color: var(--blue);
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 2px 7px;
    border-radius: 999px;
  }

  #side-nav {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  #side-nav a {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 8px 10px;
    border-radius: 8px;
    color: var(--muted);
    text-decoration: none;
    font-size: 12.5px;
    font-weight: 600;
    transition: all .14s ease;
    line-height: 1.3;
  }

  #side-nav a:hover {
    color: var(--text);
    background: var(--surface);
  }

  #side-nav a.active {
    color: var(--blue);
    background: var(--surface);
    font-weight: 750;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    border-left: 3px solid var(--blue);
  }

  #side-nav a .p-title {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  #side-nav small {
    color: var(--faint);
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 10px;
    font-weight: 750;
    background: var(--surface-3);
    padding: 1px 6px;
    border-radius: 4px;
    flex-shrink: 0;
  }

  #side-nav a:hover small,
  #side-nav a.active small {
    background: var(--surface-2);
    color: var(--text);
  }

  .sidebar-toggle {
    position: fixed;
    z-index: 1120;
    top: calc(var(--hub-nav-h, 53px) + 14px);
    left: calc(var(--sidebar-w, 290px) - 15px);
    width: 30px;
    height: 30px;
    padding: 0;
    border: 1px solid var(--border);
    border-radius: 999px;
    background: var(--surface);
    color: var(--muted);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 800;
    line-height: 1;
    transition: left .24s cubic-bezier(0.4, 0, 0.2, 1), color .18s ease, border-color .18s ease, transform .18s ease;
  }

  .sidebar-toggle:hover {
    color: var(--blue);
    border-color: var(--blue);
    transform: scale(1.08);
  }

  body.sidebar-collapsed .sidebar {
    transform: translateX(-100%);
    pointer-events: none;
  }

  body.sidebar-collapsed .content-area {
    width: 100%;
    margin-left: 0;
  }

  body.sidebar-collapsed .sidebar-toggle {
    left: 12px;
  }

  .content-area {
    min-width: 0;
    width: calc(100% - var(--sidebar-w, 290px));
    margin-left: var(--sidebar-w, 290px);
    padding: 20px 24px 80px;
    transition: width .24s cubic-bezier(0.4, 0, 0.2, 1), margin-left .24s cubic-bezier(0.4, 0, 0.2, 1);
  }

  html:root .content-area .wrap {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 auto !important;
    padding: 0 !important;
  }

  .home-strip { display: flex; justify-content: flex-start; margin-bottom: 12px; }
  .home-strip a {
    display: inline-flex; align-items: center; min-height: 34px;
    padding: 6px 12px; border-radius: 8px;
    background: var(--surface); border: 1px solid var(--border);
    color: var(--muted); text-decoration: none; font-size: 12px; font-weight: 750;
    box-shadow: var(--shadow);
    transition: all .15s ease;
  }
  .home-strip a:hover { color: var(--blue); border-color: var(--blue); }

  /* ===== HERO & STAT CARDS ===== */
  .hero {
    text-align: left;
    padding: 24px 28px;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: linear-gradient(145deg, color-mix(in srgb, var(--blue) 8%, transparent), transparent 60%), var(--surface);
    margin-bottom: 20px;
    box-shadow: var(--shadow);
  }
  .hero h1 {
    font-size: clamp(26px, 3.5vw, 36px);
    margin: 8px 0 6px;
    letter-spacing: -0.03em;
    color: var(--navy);
    font-weight: 850;
    line-height: 1.15;
  }
  .hero .subtitle {
    color: var(--muted);
    margin: 0;
    font-size: 14px;
    line-height: 1.5;
  }
  .hero .edition {
    display: inline-block;
    color: var(--blue);
    font-weight: 800;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    background: var(--accent-dim);
    padding: 3px 9px;
    border-radius: 6px;
    border: 1px solid rgba(37, 99, 235, 0.2);
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px;
    margin-top: 20px;
  }
  .stat {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 4px solid var(--stat-accent, var(--blue));
    border-radius: 10px;
    padding: 12px 14px;
    min-width: 80px;
    box-shadow: var(--shadow);
    transition: transform .14s ease, box-shadow .14s ease;
  }
  .stat:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lift);
  }
  .stat.easy { --stat-accent: var(--green); }
  .stat.medium { --stat-accent: var(--amber); }
  .stat.hard { --stat-accent: var(--red); }
  .stat .n {
    font-size: 24px;
    font-weight: 850;
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
    color: var(--navy);
  }
  .stat.easy .n { color: var(--green); }
  .stat.medium .n { color: var(--amber); }
  .stat.hard .n { color: var(--red); }
  .stat .l {
    font-size: 10.5px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
    font-weight: 800;
  }

  /* ===== OVERALL PROGRESS ===== */
  .overall-progress {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 20px;
    margin: 16px 0 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: var(--shadow);
  }
  .overall-progress .lbl {
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 800;
    white-space: nowrap;
  }
  .overall-progress .bar-track {
    flex: 1;
    height: 9px;
    background: var(--surface-2);
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid var(--border);
  }
  .overall-progress .bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--blue), var(--green));
    transition: width 0.3s ease;
    width: 0%;
    border-radius: 999px;
  }
  .overall-progress .pct {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-weight: 800;
    font-variant-numeric: tabular-nums;
    font-size: 13px;
    min-width: 90px;
    text-align: right;
    color: var(--navy);
  }

  /* ===== STICKY CONTROL BAR (Amazon Prep Style Toolbar) ===== */
  .controls {
    position: sticky;
    top: calc(var(--hub-nav-h, 53px) + 8px);
    z-index: 900;
    background: color-mix(in srgb, var(--surface) 94%, transparent);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: var(--shadow);
    padding: 10px 14px;
    margin: 0 0 22px;
  }
  .controls-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }
  .controls-row .label {
    font-size: 10.5px;
    color: var(--faint);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 850;
    margin-right: 2px;
  }
  .filter-btn {
    padding: 5px 10px;
    font-size: 11.5px;
    font-weight: 750;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    border-radius: 7px;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.14s ease;
  }
  .filter-btn:hover {
    background: var(--surface-2);
    color: var(--text);
    border-color: var(--blue);
  }
  .filter-btn.active {
    background: var(--blue);
    color: white;
    border-color: var(--blue);
  }
  .filter-btn.easy.active { background: var(--green); border-color: var(--green); color: white; }
  .filter-btn.medium.active { background: var(--amber); border-color: var(--amber); color: #172033; }
  .filter-btn.hard.active { background: var(--red); border-color: var(--red); color: white; }
  .filter-btn.blind75.active { background: var(--blind75); border-color: var(--blind75); color: white; }
  .filter-btn.neetcode.active { background: var(--neetcode); border-color: var(--neetcode); color: white; }
  .filter-btn.grind.active { background: var(--grind); border-color: var(--grind); color: white; }
  .filter-btn.striver.active { background: var(--striver); border-color: var(--striver); color: white; }
  .filter-btn.status-solved.active { background: var(--done); border-color: var(--done); color: white; }
  .filter-btn.status-unsolved.active { background: var(--muted); border-color: var(--muted); color: white; }

  .search { flex: 1; min-width: 200px; }
  .search input {
    width: 100%;
    padding: 7px 12px;
    font-size: 13px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 7px;
    font-family: inherit;
    outline: none;
    transition: border-color .15s ease, background .15s ease;
  }
  .search input:focus {
    background: var(--surface);
    border-color: var(--blue);
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
  }

  select.company-select, select.sort-select {
    padding: 6px 10px;
    font-size: 11.5px;
    font-weight: 750;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 7px;
    cursor: pointer;
    font-family: inherit;
    outline: none;
  }
  select.company-select.active {
    background: var(--blue);
    color: white;
    border-color: var(--blue);
  }

  .icon-btn {
    padding: 6px 10px;
    font-size: 13px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    border-radius: 7px;
    cursor: pointer;
    transition: all 0.14s ease;
  }
  .icon-btn:hover {
    border-color: var(--blue);
    color: var(--blue);
    background: var(--surface-2);
  }

  .sep { width: 1px; height: 20px; background: var(--border); margin: 0 3px; }

  .result-count {
    font-size: 11.5px;
    color: var(--faint);
    font-weight: 800;
    white-space: nowrap;
    margin-left: auto;
  }

  /* ===== TOC ===== */
  .toc {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 28px;
    box-shadow: var(--shadow);
  }
  .toc h2 {
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--faint);
    margin: 0 0 12px;
    font-weight: 850;
  }
  .toc-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 4px 10px;
  }
  .toc a {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 10px;
    border-radius: 7px;
    color: var(--text);
    text-decoration: none;
    font-size: 12.5px;
    font-weight: 600;
    transition: all 0.12s ease;
  }
  .toc a:hover {
    background: var(--surface-2);
    color: var(--blue);
  }
  .toc .roman {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 10.5px;
    color: var(--faint);
    min-width: 34px;
    font-weight: 700;
  }
  .toc .name { flex: 1; }
  .toc .cnt {
    font-size: 10px;
    color: var(--faint);
    font-variant-numeric: tabular-nums;
    background: var(--surface-2);
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 750;
  }

  /* ===== PATTERN CONTAINER & BANNER ===== */
  .pattern, .subpattern, section[id] { scroll-margin-top: calc(var(--hub-nav-h, 53px) + 70px); }
  .pattern { margin: 44px 0 0; }
  .pattern-banner {
    border-radius: 12px;
    padding: 18px 22px;
    color: white;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: var(--shadow-banner);
    position: relative;
    background: linear-gradient(135deg, var(--pattern-color, #1e3a8a), color-mix(in srgb, var(--pattern-color, #1e3a8a) 65%, #000));
  }
  .pattern-banner .num {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 20px;
    font-weight: 850;
    min-width: 52px;
    text-align: center;
    padding: 6px 10px;
    background: rgba(255,255,255,0.2);
    border-radius: 8px;
    backdrop-filter: blur(4px);
  }
  .pattern-banner .info { flex: 1; min-width: 0; }
  .pattern-banner .label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    opacity: 0.88;
    margin-bottom: 2px;
    font-weight: 800;
  }
  .pattern-banner h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 850;
    letter-spacing: -0.015em;
  }
  .pattern-banner .meta {
    font-size: 12px;
    opacity: 0.9;
    margin-top: 3px;
  }
  .pattern-banner .ppg {
    min-width: 140px;
    text-align: right;
  }
  .pattern-banner .ppg .pct-text {
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 4px;
    font-variant-numeric: tabular-nums;
  }
  .pattern-banner .ppg .pp-track {
    height: 6px;
    background: rgba(255,255,255,0.25);
    border-radius: 3px;
    overflow: hidden;
  }
  .pattern-banner .ppg .pp-fill {
    height: 100%;
    background: white;
    border-radius: 3px;
    width: 0%;
    transition: width 0.3s;
  }

  .pattern-desc {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--pattern-color, var(--blue));
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 12px 0 8px 0;
    font-size: 13.5px;
    box-shadow: var(--shadow);
  }
  .pattern-desc .tagline {
    font-size: 14.5px;
    font-weight: 750;
    color: var(--text);
    margin: 0 0 6px;
  }
  .pattern-desc .row { margin: 4px 0; color: var(--muted); }
  .pattern-desc .row b { color: var(--text); }

  /* ===== RESOURCE SECTIONS (collapsible) ===== */
  .resources-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    margin: 10px 0 8px 0;
    box-shadow: var(--shadow);
  }
  .resources-section .head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    user-select: none;
  }
  .resources-section .head h4 {
    margin: 0;
    font-size: 11px;
    color: var(--faint);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 850;
  }
  .resources-section .head .count {
    font-size: 10.5px;
    color: var(--faint);
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-weight: 750;
  }
  .resources-section .head .chevron {
    color: var(--faint);
    font-size: 11px;
    margin-left: 8px;
    transition: transform 0.18s ease;
    display: inline-block;
  }
  .resources-section.open .chevron { transform: rotate(90deg); }
  .resources-body { display: none; margin-top: 10px; }
  .resources-section.open .resources-body { display: block; }
  .res-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 6px 8px;
  }
  .res-link {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 11px;
    border-radius: 7px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    text-decoration: none;
    color: var(--text);
    font-size: 12.5px;
    font-weight: 600;
    transition: all 0.14s ease;
  }
  .res-link:hover {
    background: var(--blue);
    color: white;
    border-color: var(--blue);
  }
  .res-link:hover .res-source { color: rgba(255,255,255,0.85); }
  .res-icon { font-size: 13px; flex-shrink: 0; }
  .res-title { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .res-source {
    font-size: 9.5px;
    color: var(--faint);
    margin-left: auto;
    padding-left: 6px;
    white-space: nowrap;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  /* ===== SUBPATTERN ===== */
  .subpattern {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--pattern-color, var(--blue));
    border-radius: 10px;
    margin: 16px 0 0 0;
    padding: 16px 18px 18px;
    box-shadow: var(--shadow);
  }
  .subpattern-head {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 6px;
    flex-wrap: wrap;
  }
  .subpattern-tag {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 10px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--muted);
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 800;
    letter-spacing: 0.04em;
  }
  .subpattern h3 {
    margin: 0;
    font-size: 15px;
    font-weight: 800;
    flex: 1;
    min-width: 0;
    color: var(--navy);
  }
  .subpattern .scount {
    font-size: 11px;
    color: var(--faint);
    font-variant-numeric: tabular-nums;
    font-weight: 750;
  }
  .subpattern-desc {
    font-size: 12.5px;
    color: var(--muted);
    margin: 4px 0 8px;
    padding: 7px 11px;
    background: var(--surface-2);
    border-radius: 6px;
    font-style: italic;
    line-height: 1.5;
  }

  .sub-resources {
    margin: 4px 0 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    font-size: 11.5px;
    align-items: center;
  }
  .sub-resources .label {
    color: var(--faint);
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 800;
    margin-right: 4px;
  }
  .sub-res-link {
    padding: 3px 8px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 5px;
    color: var(--muted);
    text-decoration: none;
    font-size: 11px;
    font-weight: 650;
    transition: all 0.12s ease;
  }
  .sub-res-link:hover {
    background: var(--blue);
    color: white;
    border-color: var(--blue);
  }
  .sub-res-link .src { opacity: 0.75; font-size: 9.5px; margin-left: 4px; }

  /* ===== PROBLEMS TABLE (Amazon Prep Card Grid Style) ===== */
  ol.problems {
    list-style: none;
    padding: 0;
    margin: 10px 0 0;
    border-radius: 10px;
    overflow-x: auto;
    overflow-y: hidden;
    border: 1px solid var(--border);
    background: var(--surface);
    box-shadow: var(--shadow);
    -webkit-overflow-scrolling: touch;
    container-type: inline-size;
  }
  ol.problems li {
    display: grid;
    grid-template-columns: 28px 22px 56px 34px minmax(180px, 1fr) auto auto auto;
    gap: 8px;
    align-items: center;
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
    transition: background 0.14s ease, border-left 0.14s ease;
    min-width: 0;
  }
  ol.problems li:last-child { border-bottom: none; }
  ol.problems li:nth-child(even) { background: color-mix(in srgb, var(--surface-2) 40%, var(--surface)); }
  ol.problems li:hover { background: color-mix(in srgb, var(--surface-2) 80%, var(--surface)); }
  ol.problems li.hidden { display: none; }
  ol.problems li.solved {
    background: var(--done-bg);
    border-left: 4px solid var(--green);
  }
  ol.problems li.solved .pname {
    color: var(--muted);
  }

  /* Status checkbox */
  .solve-check {
    width: 22px;
    height: 22px;
    cursor: pointer;
    border: 2px solid var(--border);
    border-radius: 6px;
    background: var(--surface-2);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
    flex-shrink: 0;
    color: transparent;
  }
  .solve-check:hover { border-color: var(--green); }
  .solve-check.checked {
    background: var(--green);
    border-color: var(--green);
    color: white;
  }
  .solve-check.checked::after {
    content: '✓';
    font-weight: 800;
    font-size: 13px;
    line-height: 1;
  }

  .lc {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 11px;
    background: var(--surface-2);
    color: var(--muted);
    padding: 2px 6px;
    border-radius: 4px;
    border: 1px solid var(--border);
    text-align: center;
    font-weight: 750;
  }

  .diff-pill {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 10px;
    font-weight: 850;
    padding: 2px 6px;
    border-radius: 4px;
    text-align: center;
    letter-spacing: 0.02em;
  }
  .diff-pill.E {
    background: rgba(15, 159, 110, 0.12);
    color: var(--green);
    border: 1px solid rgba(15, 159, 110, 0.25);
  }
  .diff-pill.M {
    background: rgba(245, 158, 11, 0.12);
    color: var(--amber);
    border: 1px solid rgba(245, 158, 11, 0.25);
  }
  .diff-pill.H {
    background: rgba(220, 76, 100, 0.12);
    color: var(--red);
    border: 1px solid rgba(220, 76, 100, 0.25);
  }

  .pname-wrap { display: flex; align-items: center; gap: 8px; min-width: 0; }
  .pname {
    color: var(--text);
    text-decoration: none;
    font-size: 13.5px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-weight: 600;
    transition: color .12s ease;
  }
  .pname:hover {
    color: var(--blue);
    text-decoration: underline;
  }

  .badges-inline { display: flex; gap: 3px; flex-wrap: nowrap; align-items: center; flex-shrink: 0; }
  .list-badge {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 8.5px;
    font-weight: 800;
    letter-spacing: 0.04em;
    padding: 2px 5px;
    border-radius: 4px;
    color: white;
    flex-shrink: 0;
  }
  .list-badge.blind75 { background: var(--blind75); }
  .list-badge.neetcode { background: var(--neetcode); }
  .list-badge.grind { background: var(--grind); }
  .list-badge.striver { background: var(--striver); }

  .company-row { display: flex; gap: 3px; flex-wrap: nowrap; align-items: center; }
  .company-chip {
    font-size: 9px;
    font-weight: 750;
    letter-spacing: 0.02em;
    padding: 2px 5px;
    border-radius: 4px;
    color: var(--muted);
    background: var(--surface-2);
    border: 1px solid var(--border);
    white-space: nowrap;
  }
  .company-chip.more { background: var(--surface-2); color: var(--faint); border: 1px solid var(--border); }

  .solutions { display: flex; gap: 3px; flex-shrink: 0; }
  .sol-link {
    font-size: 10.5px;
    padding: 3px 7px;
    border-radius: 5px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    text-decoration: none;
    white-space: nowrap;
    font-weight: 650;
    transition: all 0.12s ease;
  }
  .sol-link:hover { background: var(--blue); color: white; border-color: var(--blue); }
  .sol-link.video:hover { background: #ff0000; border-color: #ff0000; color: white; }
  .sol-link.gfg:hover { background: #2f8d46; border-color: #2f8d46; color: white; }
  .sol-link.verified {
    background: linear-gradient(135deg, #ff0000, #cc0000);
    border-color: #cc0000;
    color: white;
  }
  .sol-link.verified:hover { background: linear-gradient(135deg, #cc0000, #aa0000); }

  /* ===== BOOKMARK STAR ===== */
  .bookmark-star {
    cursor: pointer;
    font-size: 16px;
    color: var(--faint);
    user-select: none;
    transition: color 0.15s ease, transform 0.15s ease;
    flex-shrink: 0;
  }
  .bookmark-star:hover { color: var(--amber); transform: scale(1.18); }
  .bookmark-star.active { color: var(--amber); }

  /* ===== NOTES ===== */
  .note-btn {
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 5px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    cursor: pointer;
    font-weight: 700;
    white-space: nowrap;
    transition: all 0.12s ease;
  }
  .note-btn:hover { border-color: var(--blue); color: var(--blue); }
  .note-btn.has-note { background: rgba(245, 158, 11, 0.15); color: var(--amber); border-color: var(--amber); }

  .note-editor,
  li.note-editor:not(.open) {
    display: none !important;
    grid-column: 1 / -1;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    margin: 6px 0;
  }
  .note-editor.open,
  li.note-editor.open { display: block !important; width: 100% !important; }
  .note-editor textarea {
    width: 100%;
    min-height: 80px;
    padding: 8px 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 6px;
    font-family: inherit;
    font-size: 13px;
    line-height: 1.5;
    resize: vertical;
  }
  .note-editor textarea:focus { outline: none; border-color: var(--blue); }
  .note-editor-actions { display: flex; gap: 6px; margin-top: 8px; justify-content: flex-end; }
  .note-editor-actions button {
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 650;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 6px;
    cursor: pointer;
  }
  .note-editor-actions button.save {
    background: var(--blue);
    color: white;
    border-color: var(--blue);
  }

  /* ===== LEARNING AID SECTIONS ===== */
  .learning-aid {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
  }
  .learning-aid .head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    user-select: none;
  }
  .learning-aid h3 {
    margin: 0;
    font-size: 14.5px;
    color: var(--navy);
    font-weight: 800;
  }
  .learning-aid h3 .ic { margin-right: 8px; }
  .learning-aid .head .chevron {
    color: var(--faint);
    font-size: 14px;
    transition: transform 0.18s ease;
  }
  .learning-aid.open .chevron { transform: rotate(90deg); }
  .learning-aid .body { display: none; margin-top: 14px; }
  .learning-aid.open .body { display: block; }

  /* Pattern recognition table */
  .pr-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .pr-table thead { background: var(--surface-2); }
  .pr-table th, .pr-table td {
    padding: 9px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
  }
  .pr-table th {
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--faint);
    font-weight: 800;
  }
  .pr-table tr:hover { background: var(--surface-2); }
  .pr-table .if-col { color: var(--text); font-weight: 500; }
  .pr-table .then-col { font-weight: 750; color: var(--blue); }
  .pr-table .pat-link {
    color: var(--faint);
    text-decoration: none;
    font-size: 11px;
    font-family: ui-monospace, monospace;
    font-weight: 650;
  }
  .pr-table .pat-link:hover { color: var(--blue); text-decoration: underline; }

  /* Big-O reference tables */
  .bigo-section { margin-top: 14px; }
  .bigo-section h4 {
    margin: 0 0 8px;
    font-size: 13px;
    color: var(--navy);
    font-weight: 800;
    padding-bottom: 4px;
    border-bottom: 1px solid var(--border);
  }
  .bigo-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
    font-family: ui-monospace, monospace;
    margin-bottom: 16px;
  }
  .bigo-table th, .bigo-table td {
    padding: 7px 10px;
    text-align: center;
    border-bottom: 1px solid var(--border);
  }
  .bigo-table th {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--faint);
    font-weight: 800;
  }
  .bigo-table td:first-child {
    text-align: left;
    color: var(--text);
    font-weight: 600;
    font-family: inherit;
  }
  .bigo-table tr:hover { background: var(--surface-2); }

  /* Study plan */
  .study-plan { display: grid; gap: 10px; }
  .sp-week {
    display: grid;
    grid-template-columns: 80px 1fr;
    gap: 14px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--blue);
    border-radius: 8px;
    padding: 12px 16px;
  }
  .sp-week .wk-num {
    font-family: ui-monospace, monospace;
    font-size: 11px;
    color: var(--faint);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  .sp-week .wk-title {
    font-size: 14px;
    font-weight: 800;
    color: var(--navy);
    margin-bottom: 4px;
  }
  .sp-week .wk-meta {
    font-size: 11px;
    color: var(--faint);
    margin-bottom: 6px;
    font-family: ui-monospace, monospace;
  }
  .sp-week .wk-meta b { color: var(--blue); }
  .sp-week .wk-focus { font-size: 12.5px; color: var(--muted); line-height: 1.5; }
  .sp-week .pat-pills { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }
  .sp-week .pat-pill {
    font-size: 10px;
    padding: 2px 7px;
    border-radius: 4px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--muted);
    text-decoration: none;
    font-family: ui-monospace, monospace;
    font-weight: 700;
  }
  .sp-week .pat-pill:hover { background: var(--blue); color: white; border-color: var(--blue); }

  /* Code template box */
  .code-template {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin: 12px 0 6px 0;
    overflow: hidden;
    box-shadow: var(--shadow);
  }
  .code-template .ct-head {
    background: var(--surface-2);
    padding: 8px 14px;
    font-size: 11px;
    color: var(--faint);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 800;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    user-select: none;
  }
  .code-template .ct-head .chev {
    transition: transform 0.18s ease;
    font-size: 13px;
  }
  .code-template.open .ct-head .chev { transform: rotate(90deg); }
  .code-template .ct-body { display: none; }
  .code-template.open .ct-body { display: block; }
  .code-template pre {
    margin: 0;
    padding: 12px 16px;
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 12.5px;
    line-height: 1.55;
    color: var(--text);
    overflow-x: auto;
    white-space: pre;
    background: var(--surface);
  }
  .ct-copy-btn {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--muted);
    padding: 3px 8px;
    font-size: 10.5px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 700;
  }
  .ct-copy-btn:hover { background: var(--blue); color: white; border-color: var(--blue); }

  /* ===== XREF + SOURCES ===== */
  .xref, .sources {
    margin-top: 40px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: var(--shadow);
  }
  .xref h2, .sources h2 { margin: 0 0 8px; font-size: 18px; color: var(--navy); }
  .xref p, .sources p { color: var(--muted); font-size: 13px; margin: 0 0 12px; }
  .xref table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
  .xref th, .xref td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }
  .xref th { font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--faint); font-weight: 800; }
  .xref td.locs span {
    display: inline-block;
    background: var(--surface-2);
    border: 1px solid var(--border);
    padding: 2px 7px;
    border-radius: 4px;
    margin: 2px 4px 2px 0;
    font-size: 10.5px;
    color: var(--muted);
  }
  .sources ul { color: var(--muted); font-size: 13px; padding-left: 20px; }
  .sources a { color: var(--blue); text-decoration: none; }
  .sources a:hover { text-decoration: underline; }

  .top {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: var(--blue);
    color: white;
    padding: 10px 14px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 13px;
    font-weight: 700;
    box-shadow: var(--shadow-lift);
    z-index: 100;
    transition: transform .15s ease;
  }
  .top:hover { transform: translateY(-2px); }

  /* ===== RESPONSIVE ===== */
  @media (max-width: 1024px) {
    .sidebar { transform: translateX(-100%); }
    body.sidebar-open .sidebar { transform: translateX(0); box-shadow: var(--shadow-lift); }
    .sidebar-toggle { left: 12px; }
    body.sidebar-open .sidebar-toggle { left: calc(var(--sidebar-w, 290px) - 15px); }
    .content-area { width: 100% !important; margin-left: 0 !important; padding: 14px 10px 60px !important; }
  }
  @media (max-width: 900px) {
    .pattern-banner { flex-direction: column; align-items: flex-start; }
    .pattern-banner .ppg { min-width: 100%; text-align: left; }
    .hero h1 { font-size: 24px; }
    ol.problems li:not(.note-editor) {
      display: grid !important;
      grid-template-columns: 26px 22px 50px 28px 1fr auto !important;
      grid-template-rows: auto auto !important;
      row-gap: 6px !important;
      column-gap: 6px !important;
      padding: 8px 10px !important;
      align-items: center !important;
    }
    ol.problems li:not(.note-editor) .solve-check { grid-column: 1 !important; grid-row: 1 !important; }
    ol.problems li:not(.note-editor) .bookmark-star { grid-column: 2 !important; grid-row: 1 !important; }
    ol.problems li:not(.note-editor) .lc { grid-column: 3 !important; grid-row: 1 !important; }
    ol.problems li:not(.note-editor) .diff-pill { grid-column: 4 !important; grid-row: 1 !important; }
    ol.problems li:not(.note-editor) .pname-wrap { grid-column: 5 / -1 !important; grid-row: 1 !important; min-width: 0 !important; }
    ol.problems li:not(.note-editor) .problem-name { grid-column: 3 / -1 !important; grid-row: 1 !important; min-width: 0 !important; }
    ol.problems li:not(.note-editor) .pname,
    ol.problems li:not(.note-editor) .problem-name {
      white-space: normal !important;
      line-height: 1.35 !important;
      font-weight: 600 !important;
      word-break: break-word !important;
    }
    ol.problems li:not(.note-editor) .solutions {
      grid-column: 1 / -2 !important; grid-row: 2 !important;
      display: flex !important; gap: 4px !important; flex-wrap: wrap !important; align-items: center !important;
      justify-self: start !important; min-width: 0 !important;
    }
    ol.problems li:not(.note-editor) .note-btn {
      grid-column: -2 / -1 !important; grid-row: 2 !important;
      justify-self: end !important; align-self: center !important;
    }
    ol.problems li:not(.note-editor) .company-row {
      grid-column: 1 / -1 !important; grid-row: 3 !important;
      justify-self: start !important; align-self: center !important;
      display: flex !important; flex-wrap: wrap !important; gap: 3px !important;
    }
    ol.problems li:not(.note-editor) .company-row:empty { display: none !important; }
    ol.problems li:not(.note-editor) .company-row .company-chip:nth-child(n+3):not(.more) { display: none !important; }
    ol.problems li.note-editor:not(.open) { display: none !important; }
    ol.problems li.note-editor.open { display: block !important; width: 100% !important; }
    .filter-btn { padding: 4px 8px; font-size: 10.5px; }
  }
  @media (max-width: 760px) {
    ol.problems li:not(.note-editor) {
      grid-template-columns: 26px 22px auto auto 1fr auto !important;
      grid-template-rows: auto auto auto !important;
    }
    ol.problems li:not(.note-editor) .note-btn {
      grid-column: -2 / -1 !important; grid-row: 1 !important;
      justify-self: end !important; align-self: center !important;
    }
    ol.problems li:not(.note-editor) .pname-wrap {
      grid-column: 1 / -1 !important; grid-row: 2 !important;
      display: flex !important; align-items: center !important;
      flex-wrap: wrap !important; gap: 4px 6px !important;
    }
    ol.problems li:not(.note-editor) .problem-name {
      grid-column: 1 / -1 !important; grid-row: 2 !important;
    }
    ol.problems li:not(.note-editor) .solutions {
      grid-column: 1 / -1 !important; grid-row: 3 !important;
      gap: 5px !important;
    }
    ol.problems li:not(.note-editor) .company-row {
      grid-column: 1 / -1 !important; grid-row: 4 !important;
    }
  }

  /* ===== PRINT ===== */
  @media print {
    body { background: white; color: black; }
    .sidebar, .sidebar-toggle, .controls, .top, .filter-btn, .icon-btn, .resources-section .head { display: none !important; }
    .content-area { width: 100% !important; margin: 0 !important; padding: 0 !important; }
    .resources-section .resources-body { display: block !important; }
    .pattern { page-break-inside: avoid; }
    .pattern-banner { background: #2563eb !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    a { color: black; text-decoration: underline; }
    ol.problems li { page-break-inside: avoid; background: white !important; }
    ol.problems li { grid-template-columns: 56px 32px 1fr auto !important; }
    .solve-check, .bookmark-star, .note-btn { display: none !important; }
  }
'''

# Replace the first <style> tag
new_html = re.sub(r'<style>[\s\S]*?</style>', f'<style>{modern_css}\n</style>', html, count=1)

# Remove the second obsolete style tag <style id="site-nav-style">...</style> if present
new_html = re.sub(r'<style id="site-nav-style">[\s\S]*?</style>', '', new_html)

# 3. Generate Sidebar HTML
side_links_html = []
for item in sidebar_items:
    pid = item['id']
    title = item['title']
    cnt = item['count']
    idx = item['index']
    side_links_html.append(
        f'<a href="#{pid}" class="side-link" data-pid="{pid}">'
        f'<span class="p-title">{idx}. {title}</span>'
        f'<small id="pstat-{pid}">0 / {cnt}</small>'
        f'</a>'
    )
side_nav_content = '\n'.join(side_links_html)

sidebar_markup = f'''<div class="app-layout">
<aside class="sidebar" id="sidebar">
  <div class="sidebar-inner">
    <div class="sidebar-header">
      <p class="sidebar-label">Patterns (47)</p>
      <span class="sidebar-stat" id="side-stat-total">0 / 940</span>
    </div>
    <nav id="side-nav">
{side_nav_content}
    </nav>
  </div>
</aside>
<button class="sidebar-toggle" id="sidebar-toggle" aria-label="Toggle Pattern Sidebar" title="Toggle Sidebar">‹</button>
<main class="content-area">
<div class="wrap">'''

body_wrap_match = re.search(r'<body>\s*<div class="wrap">', new_html)
if body_wrap_match:
    new_html = new_html[:body_wrap_match.start()] + '<body>\n' + sidebar_markup + new_html[body_wrap_match.end():]
    print("Replaced body wrap with app-layout, sidebar, and content-area")
else:
    print("WARNING: Could not find <body>\\s*<div class=\"wrap\">")

if 'id="result-count"' not in new_html:
    new_html = new_html.replace(
        '<button class="filter-btn" id="clear-filters">Clear</button>',
        '<button class="filter-btn" id="clear-filters">Clear</button>\n<span class="result-count" id="result-count">940 problems</span>'
    )
    print("Added #result-count to controls")

new_html = new_html.replace(
    'placeholder="Search problems by name or LC#…"',
    'placeholder="Search problems by name or LC# (press / to focus)…"'
)

new_html = re.sub(
    r'</script>\s*</div>\s*</body>\s*</html>',
    '</script>\n</div>\n</main>\n</div>\n</body></html>',
    new_html
)

modern_script = '''<script>
(function() {
  const STORAGE_SOLVED = 'dsa_index_solved_v1';
  const STORAGE_BOOKMARK = 'dsa_index_bookmark_v1';
  const STORAGE_NOTES = 'dsa_index_notes_v1';
  const THEME_KEY = 'learning_hub_theme';

  // ===== Theme synchronization with Hub Navbar 3-Theme Switch =====
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const sharedBtn = document.querySelector('[data-hub-theme]');
      if (sharedBtn) {
        sharedBtn.click();
      } else {
        const root = document.documentElement;
        const current = root.getAttribute('data-theme') || (root.classList.contains('light') ? 'light' : 'dark');
        const next = current === 'light' ? 'dark' : (current === 'dark' ? 'black' : 'light');
        root.classList.remove('light', 'dark', 'black');
        root.classList.add(next);
        root.setAttribute('data-theme', next);
        localStorage.setItem(THEME_KEY, next);
      }
    });
  }

  // ===== Solved & Bookmarks & Notes =====
  function getSet(k) { try { return new Set(JSON.parse(localStorage.getItem(k) || '[]')); } catch(e) { return new Set(); } }
  function saveSet(k, s) { localStorage.setItem(k, JSON.stringify([...s])); }
  function getObj(k) { try { return JSON.parse(localStorage.getItem(k) || '{}'); } catch(e) { return {}; } }
  function saveObj(k, o) { localStorage.setItem(k, JSON.stringify(o)); }

  let solved = getSet(STORAGE_SOLVED);
  let bookmarks = getSet(STORAGE_BOOKMARK);
  let notes = getObj(STORAGE_NOTES);

  function renderState() {
    document.querySelectorAll('ol.problems li[data-lc]').forEach(li => {
      const lc = li.dataset.lc;
      const isSolved = solved.has(lc);
      const isBM = bookmarks.has(lc);
      const hasNote = notes[lc] && notes[lc].trim().length > 0;
      li.classList.toggle('solved', isSolved);
      const cb = li.querySelector('.solve-check');
      if (cb) cb.classList.toggle('checked', isSolved);
      const star = li.querySelector('.bookmark-star');
      if (star) { star.classList.toggle('active', isBM); star.textContent = isBM ? '★' : '☆'; }
      const nb = li.querySelector('.note-btn');
      if (nb) nb.classList.toggle('has-note', hasNote);
    });
    updateProgress();
  }

  function updateProgress() {
    const allLcs = new Set();
    document.querySelectorAll('ol.problems li[data-lc]').forEach(li => allLcs.add(li.dataset.lc));
    const solvedTotal = [...solved].filter(lc => allLcs.has(lc)).length;
    const pct = allLcs.size ? Math.round(100 * solvedTotal / allLcs.size) : 0;
    
    const bar = document.getElementById('overall-bar');
    if (bar) bar.style.width = pct + '%';
    const pctEl = document.getElementById('overall-pct');
    if (pctEl) pctEl.textContent = `${solvedTotal} / ${allLcs.size} (${pct}%)`;

    // Sidebar total stat
    const sideTotal = document.getElementById('side-stat-total');
    if (sideTotal) sideTotal.textContent = `${solvedTotal} / ${allLcs.size}`;

    // Update per-pattern progress and sidebar counters
    document.querySelectorAll('.pattern').forEach(p => {
      const lcs = (p.dataset.patternLcs || '').split(',').filter(Boolean);
      const uniq = new Set(lcs);
      const totalP = uniq.size;
      const solvedP = [...uniq].filter(lc => solved.has(lc)).length;
      const pnum = p.id.replace('pattern-', '');
      const fill = p.querySelector(`[data-pp-fill="${pnum}"]`);
      const txt = p.querySelector(`[data-pp-text="${pnum}"]`) || p.querySelector(`[data-pp-count="${pnum}"]`);
      if (fill) fill.style.width = (totalP ? (100 * solvedP / totalP) : 0) + '%';
      if (txt) txt.textContent = `${solvedP} / ${totalP}`;

      // Update sidebar counter for this pattern
      const pstat = document.getElementById(`pstat-${p.id}`);
      if (pstat) pstat.textContent = `${solvedP} / ${totalP}`;
    });
  }

  // Solve checkbox
  document.querySelectorAll('.solve-check').forEach(cb => {
    cb.addEventListener('click', (e) => {
      e.stopPropagation();
      const lc = cb.dataset.lc;
      if (solved.has(lc)) solved.delete(lc); else solved.add(lc);
      saveSet(STORAGE_SOLVED, solved);
      renderState();
    });
  });

  // Bookmark star
  document.querySelectorAll('.bookmark-star').forEach(star => {
    star.addEventListener('click', (e) => {
      e.stopPropagation();
      const lc = star.dataset.lc;
      if (bookmarks.has(lc)) bookmarks.delete(lc); else bookmarks.add(lc);
      saveSet(STORAGE_BOOKMARK, bookmarks);
      renderState();
      applyFilters();
    });
  });

  // Note button
  function noteEditorFor(li, lc) {
    const list = li.parentElement;
    let ed = list ? list.querySelector(`.note-editor[data-note-lc="${CSS.escape(lc)}"]`) : null;
    if (ed) return ed;
    ed = document.createElement('li');
    ed.className = 'note-editor';
    ed.setAttribute('data-note-lc', lc);
    ed.style.display = 'none';
    ed.style.gridTemplateColumns = '1fr';
    ed.innerHTML = '<textarea placeholder="Write your notes, edge cases, time/space complexity notes..."></textarea>' +
      '<div class="note-editor-actions">' +
        '<button type="button" class="cancel">Cancel</button>' +
        '<button type="button" class="save">Save Note</button>' +
      '</div>';
    li.insertAdjacentElement('afterend', ed);
    ed.querySelector('.cancel').addEventListener('click', () => { ed.classList.remove('open'); });
    ed.querySelector('.save').addEventListener('click', () => {
      const val = ed.querySelector('textarea').value.trim();
      if (val) notes[lc] = val; else delete notes[lc];
      saveObj(STORAGE_NOTES, notes);
      ed.classList.remove('open');
      renderState();
    });
    return ed;
  }

  document.querySelectorAll('.note-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const li = btn.closest('li[data-lc]');
      if (!li) return;
      const lc = li.dataset.lc;
      const ed = noteEditorFor(li, lc);
      const isOpen = ed.classList.toggle('open');
      if (isOpen) {
        const ta = ed.querySelector('textarea');
        ta.value = notes[lc] || '';
        ta.focus();
      }
    });
  });

  // Filters
  const filters = {
    diff: new Set(),
    list: new Set(),
    status: null,
    company: '',
    search: ''
  };

  function applyFilters() {
    let visibleCount = 0;
    document.querySelectorAll('ol.problems li[data-lc]').forEach(li => {
      let show = true;
      if (filters.diff.size > 0 && !filters.diff.has(li.dataset.diff)) show = false;
      if (filters.list.size > 0) {
        let hasList = false;
        if (filters.list.has('blind75') && li.dataset.blind75) hasList = true;
        if (filters.list.has('neetcode') && li.dataset.neetcode) hasList = true;
        if (filters.list.has('grind') && li.dataset.grind) hasList = true;
        if (filters.list.has('striver') && li.dataset.striver) hasList = true;
        if (!hasList) show = false;
      }
      if (filters.status === 'solved' && !solved.has(li.dataset.lc)) show = false;
      if (filters.status === 'unsolved' && solved.has(li.dataset.lc)) show = false;
      if (filters.status === 'bookmarked' && !bookmarks.has(li.dataset.lc)) show = false;
      if (filters.company) {
        const comps = (li.dataset.companies || '').split(',');
        if (!comps.includes(filters.company)) show = false;
      }
      if (filters.search) {
        const hay = (li.dataset.name + ' ' + li.dataset.lc).toLowerCase();
        if (!hay.includes(filters.search)) show = false;
      }
      li.classList.toggle('hidden', !show);
      if (show) visibleCount++;
    });
    const resCountEl = document.getElementById('result-count');
    if (resCountEl) resCountEl.textContent = `${visibleCount} problems`;
  }

  document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      const f = btn.dataset.filter, v = btn.dataset.val;
      if (f === 'diff' || f === 'list') {
        if (filters[f].has(v)) {
          filters[f].delete(v);
          btn.classList.remove('active');
        } else {
          filters[f].add(v);
          btn.classList.add('active');
        }
      } else {
        const same = filters[f] === v;
        document.querySelectorAll(`.filter-btn[data-filter="${f}"]`).forEach(b => b.classList.remove('active'));
        filters[f] = same ? null : v;
        if (!same) btn.classList.add('active');
      }
      applyFilters();
    });
  });

  document.getElementById('clear-filters').addEventListener('click', () => {
    filters.diff.clear(); filters.list.clear(); filters.status = null; filters.search = ''; filters.company = '';
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('search-input').value = '';
    document.getElementById('company-select').value = '';
    document.getElementById('company-select').classList.remove('active');
    applyFilters();
  });

  document.getElementById('search-input').addEventListener('input', e => {
    filters.search = e.target.value.toLowerCase().trim();
    applyFilters();
  });

  document.getElementById('company-select').addEventListener('change', e => {
    filters.company = e.target.value;
    e.target.classList.toggle('active', !!filters.company);
    applyFilters();
  });

  // Sort
  function diffRank(d) { return { 'E': 0, 'M': 1, 'H': 2 }[d] ?? 99; }
  function sortBy(mode) {
    document.querySelectorAll('ol.problems').forEach(ol => {
      const all = Array.from(ol.children);
      const problems = all.filter(el => el.dataset.lc);
      const editors = all.filter(el => el.dataset.noteLc);
      const editorMap = {};
      editors.forEach(ed => editorMap[ed.dataset.noteLc] = ed);
      problems.sort((a, b) => {
        if (mode === 'lc') return parseInt(a.dataset.lc) - parseInt(b.dataset.lc);
        if (mode === 'name') return a.dataset.name.localeCompare(b.dataset.name);
        if (mode === 'diff') return diffRank(a.dataset.diff) - diffRank(b.dataset.diff) || parseInt(a.dataset.lc) - parseInt(b.dataset.lc);
        if (mode === 'diff-rev') return diffRank(b.dataset.diff) - diffRank(a.dataset.diff) || parseInt(a.dataset.lc) - parseInt(b.dataset.lc);
        return 0;
      });
      problems.forEach(p => {
        ol.appendChild(p);
        if (editorMap[p.dataset.lc]) ol.appendChild(editorMap[p.dataset.lc]);
      });
    });
  }
  document.getElementById('sort-select').addEventListener('change', e => sortBy(e.target.value));

  // Random picker
  document.getElementById('random-btn').addEventListener('click', () => {
    const visible = Array.from(document.querySelectorAll('ol.problems li[data-lc]:not(.hidden)'));
    if (!visible.length) { alert('No problems match current filters.'); return; }
    const pick = visible[Math.floor(Math.random() * visible.length)];
    pick.scrollIntoView({ behavior: 'smooth', block: 'center' });
    pick.style.transition = 'box-shadow 0.4s, transform 0.4s';
    pick.style.boxShadow = '0 0 0 3px var(--blue), 0 6px 20px rgba(37, 99, 235, 0.4)';
    pick.style.transform = 'scale(1.02)';
    setTimeout(() => { pick.style.boxShadow = ''; pick.style.transform = ''; }, 2500);
  });

  // Sidebar toggle
  const sidebarToggle = document.getElementById('sidebar-toggle');
  if (sidebarToggle) {
    if (localStorage.getItem('dsa_sidebar_collapsed') === '1') {
      document.body.classList.add('sidebar-collapsed');
      sidebarToggle.textContent = '›';
    }
    sidebarToggle.addEventListener('click', () => {
      if (window.innerWidth <= 1024) {
        document.body.classList.toggle('sidebar-open');
      } else {
        const isCollapsed = document.body.classList.toggle('sidebar-collapsed');
        sidebarToggle.textContent = isCollapsed ? '›' : '‹';
        localStorage.setItem('dsa_sidebar_collapsed', isCollapsed ? '1' : '0');
      }
    });
  }

  // Close sidebar drawer on link click in mobile
  document.querySelectorAll('#side-nav a').forEach(a => {
    a.addEventListener('click', () => {
      if (window.innerWidth <= 1024) {
        document.body.classList.remove('sidebar-open');
      }
    });
  });

  // Active scrollspy for sidebar links
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          document.querySelectorAll('#side-nav a').forEach(a => {
            a.classList.toggle('active', a.dataset.pid === id);
          });
        }
      });
    }, { rootMargin: '-10% 0px -75% 0px' });

    document.querySelectorAll('.pattern').forEach(p => observer.observe(p));
  }

  // Keyboard shortcut '/' to search
  window.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      const input = document.getElementById('search-input');
      if (input) { input.focus(); input.select(); }
    }
  });

  // Initial render
  renderState();
})();
</script>'''

# Replace the original script block
new_html = re.sub(r'<script>\s*\(function\(\)\s*\{[\s\S]*?\}\)\(\);\s*</script>', modern_script, new_html)

# Atomic write to DSA_Ultimate_Index.html
atomic_write(INDEX_PATH, new_html)

print("Atomically wrote upgraded DSA_Ultimate_Index.html")
print(f"New file size: {len(new_html)} chars, {len(new_html.splitlines())} lines")
