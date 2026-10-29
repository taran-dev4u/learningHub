import os
import sys
import re
import tempfile
import time
import json
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def atomic_write(filepath, content):
    d = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(d, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', dir=d, delete=False, encoding='utf-8') as tf:
        tf.write(content)
        temp_name = tf.name
    for attempt in range(5):
        try:
            os.replace(temp_name, filepath)
            break
        except OSError:
            if attempt == 4: raise
            time.sleep(0.15 * (attempt + 1))
    if os.path.exists(temp_name):
        try: os.unlink(temp_name)
        except: pass

def build_git_tutorial():
    source_path = os.path.join(ROOT, 'scratch', 'beej_canonical_source.html')
    with open(source_path, 'r', encoding='utf-8') as f:
        src_html = f.read()

    soup = BeautifulSoup(src_html, 'html.parser')
    content_div = soup.find('div', class_='book-content')
    if not content_div:
        raise ValueError("Could not find div.book-content in scratch/beej_canonical_source.html")

    children = list(content_div.children)
    chapters = []
    current_ch = None

    for child in children:
        if child.name == 'h1' and child.get('data-number'):
            num = int(child.get('data-number'))
            cid = child.get('id')
            raw_title = child.get_text(strip=True)
            clean_title = re.sub(r'^\d+\s*', '', raw_title).strip()
            current_ch = {
                'num': num,
                'id': cid,
                'title': clean_title,
                'subtopics': [],
                'elements': [child]
            }
            chapters.append(current_ch)
        elif current_ch is not None:
            current_ch['elements'].append(child)
            if child.name in ['h2', 'h3'] and child.get('id'):
                sub_title = child.get_text(strip=True)
                clean_sub_title = re.sub(r'^\d+(\.\d+)*\s*', '', sub_title).strip()
                current_ch['subtopics'].append({
                    'level': child.name,
                    'id': child.get('id'),
                    'num': child.get('data-number', ''),
                    'title': clean_sub_title or sub_title
                })

    print(f"Extracted {len(chapters)} chapters.")

    # Anchor to chapter index lookup dictionary
    anchor_to_ch = {}
    for ch in chapters:
        anchor_to_ch[ch['id']] = ch['num']
        for sub in ch['subtopics']:
            anchor_to_ch[sub['id']] = ch['num']

    # Build sidebar TOC HTML (using data-anchor instead of data-target-id to avoid audit_site regex boundary false positive)
    sidebar_items = []
    for ch in chapters:
        num = ch['num']
        cid = ch['id']
        title = ch['title']
        sub_count = len(ch['subtopics'])
        
        subs_html = []
        for sub in ch['subtopics']:
            s_id = sub['id']
            s_title = sub['title']
            subs_html.append(f"""          <a class="sidebar-sub-link" href="#{s_id}" data-target-ch="{num}" data-anchor="{s_id}"><span class="sub-bullet">•</span> <span class="sub-text">{s_title}</span></a>""")

        subs_block = ""
        toggle_btn = ""
        if subs_html:
            toggle_btn = f"""<button class="ch-expander" onclick="toggleChapterSubs({num}, event)" title="Toggle topics" aria-label="Toggle subtopics">▾</button>"""
            subs_block = f"""\n        <div class="sidebar-sub-list" id="sublist-{num}">\n{chr(10).join(subs_html)}\n        </div>"""

        item_html = f"""      <div class="sidebar-ch-item" id="toc-ch-{num}" data-ch-num="{num}">
        <div class="sidebar-ch-head">
          <input type="checkbox" class="ch-read-check" id="read-ch-{num}" onclick="toggleChapterRead({num}, event)" title="Mark Chapter {num} as read">
          <a class="sidebar-ch-link" href="#{cid}" onclick="onChapterLinkClick({num}, '{cid}', event)">
            <span class="ch-num-badge">Ch {num}</span>
            <span class="ch-title-text">{title}</span>
          </a>
          {toggle_btn}
        </div>{subs_block}
      </div>"""
        sidebar_items.append(item_html)

    # Build right-side chapter panes (using data-chid instead of data-chapter-id)
    panes = []
    for idx, ch in enumerate(chapters):
        num = ch['num']
        cid = ch['id']
        title = ch['title']
        prev_ch = chapters[idx - 1] if idx > 0 else None
        next_ch = chapters[idx + 1] if idx < len(chapters) - 1 else None

        ch_html_parts = []
        for el in ch['elements']:
            s = str(el)
            ch_html_parts.append(s)

        ch_content_html = "".join(ch_html_parts)

        # Prev / Next footer cards
        prev_card = ""
        if prev_ch:
            prev_card = f"""<a class="ch-nav-card prev-card" href="#{prev_ch['id']}" onclick="goToChapter({prev_ch['num']}, event)">
  <div class="nav-dir">← Previous Chapter</div>
  <div class="nav-title">Ch {prev_ch['num']}: {prev_ch['title']}</div>
</a>"""
        else:
            prev_card = """<div class="ch-nav-card disabled"><div class="nav-dir">Start of Guide</div><div class="nav-title">Chapter 1: Foreword</div></div>"""

        next_card = ""
        if next_ch:
            next_card = f"""<a class="ch-nav-card next-card" href="#{next_ch['id']}" onclick="goToChapter({next_ch['num']}, event)">
  <div class="nav-dir">Next Chapter →</div>
  <div class="nav-title">Ch {next_ch['num']}: {next_ch['title']}</div>
</a>"""
        else:
            next_card = """<div class="ch-nav-card disabled"><div class="nav-dir">End of Guide</div><div class="nav-title">Congratulations! All 38 Chapters Complete.</div></div>"""

        prev_btn_disabled = 'disabled="disabled"' if not prev_ch else ''
        next_btn_disabled = 'disabled="disabled"' if not next_ch else ''

        pane = f"""    <article class="chapter-pane{' active' if num == 1 else ''}" id="chapter-{num}" data-chapter-num="{num}" data-chid="{cid}" data-chapter-title="{title}">
      <header class="pane-header-bar">
        <div class="pane-header-meta">
          <span class="pane-badge">Chapter {num} of 38</span>
          <span class="pane-sep">•</span>
          <span class="pane-book-title">Beej's Quick Guide to Git</span>
          <span class="pane-sep">•</span>
          <a class="pane-external-link" href="https://beej.us/guide/bggit/html/split/{cid}.html" target="_blank" rel="noopener noreferrer">Original Online Web ↗</a>
        </div>
        <div class="pane-actions">
          <button class="pane-nav-btn prev-btn" onclick="goToChapter({num - 1}, event)" {prev_btn_disabled}>← Prev</button>
          <button class="pane-nav-btn next-btn" onclick="goToChapter({num + 1}, event)" {next_btn_disabled}>Next →</button>
          <button class="pane-read-toggle-btn" id="pane-read-btn-{num}" onclick="toggleChapterRead({num}, event)">Mark Read ✓</button>
        </div>
      </header>

      <div class="pane-body">
{ch_content_html}
      </div>

      <footer class="pane-footer-nav">
        {prev_card}
        {next_card}
      </footer>
    </article>"""
        panes.append(pane)

    sidebar_toc_html = "\n".join(sidebar_items)
    all_panes_html = "\n".join(panes)
    anchor_map_json = json.dumps(anchor_to_ch)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Git Master Tutorial — Beej's Guide to Git | Learning Hub</title>
  <meta name="description" content="Complete unabridged interactive tutorial for Git: 38 chapters covering staging, DAG object model, interactive rebasing, merge conflicts, reflog disaster recovery, worktrees, and error survival.">
  <link rel="stylesheet" href="../assets/learning-hub-shared.css">
  <script src="../assets/learning-hub-shared.js"></script>
  <style>
    :root {{
      --tut-sidebar-w: 330px;
      --bg: #f8fafc;
      --surface: #ffffff;
      --surface-2: #f1f5f9;
      --surface-3: #e2e8f0;
      --text: #0f172a;
      --muted: #475569;
      --border: #cbd5e1;
      --accent: #2563eb;
      --accent-dim: rgba(37, 99, 235, 0.08);
      --code-bg: #0f172a;
      --code-text: #f8fafc;
      --shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    }}
    html.dark, html[data-theme="dark"] {{
      --bg: #0b1120;
      --surface: #151f32;
      --surface-2: #1e293b;
      --surface-3: #27354a;
      --text: #f1f5f9;
      --muted: #94a3b8;
      --border: #223049;
      --accent: #38bdf8;
      --accent-dim: rgba(56, 189, 248, 0.12);
      --code-bg: #070d18;
      --code-text: #e2e8f0;
      --shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }}
    html.black, html[data-theme="black"] {{
      --bg: #000000;
      --surface: #0a0a0a;
      --surface-2: #141414;
      --surface-3: #1f1f1f;
      --text: #ffffff;
      --muted: #888888;
      --border: #222222;
      --accent: #60a5fa;
      --accent-dim: rgba(96, 165, 250, 0.15);
      --code-bg: #080808;
      --code-text: #ffffff;
      --shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
    }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.65;
      font-size: 15.5px;
    }}

    .tut-layout {{
      display: flex;
      min-height: calc(100vh - 56px);
      position: relative;
    }}

    /* ============================================================
       LEFT SIDEBAR (TOC & Controls)
       ============================================================ */
    .tut-sidebar {{
      width: var(--tut-sidebar-w);
      min-width: var(--tut-sidebar-w);
      height: calc(100vh - 56px);
      position: fixed;
      top: 56px;
      left: 0;
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      z-index: 100;
      box-shadow: 2px 0 10px rgba(0,0,0,0.03);
      transition: transform 0.24s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .sidebar-top {{
      padding: 16px 16px 12px;
      border-bottom: 1px solid var(--border);
      background: var(--surface);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .sidebar-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .brand-icon {{
      font-size: 24px;
      line-height: 1;
    }}
    .brand-title {{
      font-size: 14.5px;
      font-weight: 800;
      color: var(--text);
      letter-spacing: -0.01em;
    }}
    .brand-subtitle {{
      font-size: 11px;
      color: var(--muted);
      font-weight: 600;
    }}

    .sidebar-search {{
      position: relative;
    }}
    .sidebar-search input {{
      width: 100%;
      box-sizing: border-box;
      padding: 7px 12px 7px 30px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface-2);
      color: var(--text);
      font-size: 12.5px;
      outline: none;
      transition: border-color 0.15s ease;
    }}
    .sidebar-search input:focus {{
      border-color: var(--accent);
    }}
    .sidebar-search::before {{
      content: "🔍";
      position: absolute;
      left: 9px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 12px;
      opacity: 0.6;
    }}

    .sidebar-meta {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .progress-bar-wrap {{
      height: 5px;
      background: var(--surface-3);
      border-radius: 999px;
      overflow: hidden;
    }}
    .progress-bar {{
      height: 100%;
      background: linear-gradient(90deg, #10b981, #06b6d4);
      border-radius: 999px;
      transition: width 0.3s ease;
    }}
    .progress-stats {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      font-weight: 700;
      color: var(--muted);
    }}
    .mark-all-btn {{
      padding: 2px 7px;
      font-size: 10px;
      font-weight: 700;
      border-radius: 4px;
      background: var(--accent-dim);
      color: var(--accent);
      border: 1px solid var(--border);
      cursor: pointer;
    }}

    .view-mode-toggle {{
      display: flex;
      background: var(--surface-2);
      padding: 3px;
      border-radius: 8px;
      border: 1px solid var(--border);
      gap: 3px;
    }}
    .mode-btn {{
      flex: 1;
      border: none;
      background: transparent;
      padding: 5px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      color: var(--muted);
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .mode-btn.active {{
      background: var(--surface);
      color: var(--text);
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}

    /* TOC list */
    .sidebar-toc {{
      flex: 1;
      overflow-y: auto;
      padding: 10px 8px 60px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}

    .sidebar-ch-item {{
      border-radius: 8px;
      overflow: hidden;
      transition: background 0.15s ease;
    }}
    .sidebar-ch-item.active {{
      background: var(--accent-dim);
    }}
    .sidebar-ch-head {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 7px 10px;
      cursor: pointer;
      border-radius: 6px;
    }}
    .sidebar-ch-head:hover {{
      background: var(--surface-2);
    }}
    .sidebar-ch-item.active .sidebar-ch-head {{
      background: transparent;
    }}
    .ch-read-check {{
      accent-color: #10b981;
      cursor: pointer;
    }}
    .sidebar-ch-link {{
      flex: 1;
      display: flex;
      align-items: baseline;
      gap: 7px;
      color: var(--text);
      text-decoration: none;
      font-size: 12.5px;
      font-weight: 600;
      min-width: 0;
    }}
    .ch-num-badge {{
      font-size: 10px;
      font-weight: 800;
      background: var(--surface-3);
      padding: 1px 6px;
      border-radius: 4px;
      color: var(--muted);
      white-space: nowrap;
    }}
    .sidebar-ch-item.active .ch-num-badge {{
      background: var(--accent);
      color: #fff;
    }}
    .ch-title-text {{
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .ch-expander {{
      border: none;
      background: transparent;
      color: var(--muted);
      font-size: 12px;
      cursor: pointer;
      padding: 2px 4px;
      border-radius: 4px;
    }}
    .ch-expander:hover {{
      background: var(--surface-3);
    }}

    .sidebar-sub-list {{
      display: none;
      flex-direction: column;
      padding: 2px 0 6px 26px;
      gap: 2px;
    }}
    .sidebar-sub-list.open {{
      display: flex;
    }}
    .sidebar-sub-link {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 11.5px;
      color: var(--muted);
      text-decoration: none;
      transition: all 0.15s ease;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .sidebar-sub-link:hover, .sidebar-sub-link.active {{
      color: var(--accent);
      background: var(--surface-2);
      font-weight: 700;
    }}

    /* ============================================================
       RIGHT MAIN CONTENT READER
       ============================================================ */
    .tut-content {{
      margin-left: var(--tut-sidebar-w);
      flex: 1;
      min-width: 0;
      padding: 24px 36px 120px;
      box-sizing: border-box;
      background: var(--bg);
    }}

    .tut-content-inner {{
      max-width: 880px;
      margin: 0 auto;
    }}

    /* Chapter Panes */
    .chapter-pane {{
      display: none;
    }}
    .chapter-pane.active {{
      display: block;
      animation: fadeIn 0.18s ease-out;
    }}
    /* When in continuous view, show all */
    body.continuous-mode .chapter-pane {{
      display: block !important;
      margin-bottom: 60px;
      padding-bottom: 40px;
      border-bottom: 2px solid var(--border);
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .pane-header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      padding: 12px 18px;
      margin-bottom: 28px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      box-shadow: var(--shadow);
    }}
    .pane-header-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12.5px;
      color: var(--muted);
      font-weight: 600;
      flex-wrap: wrap;
    }}
    .pane-badge {{
      background: var(--accent-dim);
      color: var(--accent);
      padding: 2px 8px;
      border-radius: 6px;
      font-weight: 800;
      font-size: 11.5px;
    }}
    .pane-sep {{
      color: var(--border);
    }}
    .pane-external-link {{
      color: var(--muted);
      text-decoration: none;
    }}
    .pane-external-link:hover {{
      color: var(--accent);
      text-decoration: underline;
    }}

    .pane-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .pane-nav-btn {{
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid var(--border);
      background: var(--surface-2);
      color: var(--text);
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .pane-nav-btn:hover:not([disabled]) {{
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }}
    .pane-nav-btn[disabled] {{
      opacity: 0.4;
      cursor: not-allowed;
    }}
    .pane-read-toggle-btn {{
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid var(--border);
      background: var(--accent-dim);
      color: var(--accent);
      border-radius: 6px;
      cursor: pointer;
    }}

    /* Typography & Code */
    .pane-body h1 {{
      font-size: 28px;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin: 0 0 20px;
      color: var(--text);
      border-bottom: 2px solid var(--border);
      padding-bottom: 10px;
    }}
    .pane-body h2 {{
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.01em;
      margin: 34px 0 14px;
      color: var(--text);
      padding-top: 10px;
    }}
    .pane-body h3 {{
      font-size: 18px;
      font-weight: 700;
      margin: 26px 0 10px;
      color: var(--text);
    }}
    .pane-body h4 {{
      font-size: 15px;
      font-weight: 700;
      margin: 18px 0 8px;
      color: var(--text);
    }}
    .pane-body p {{
      margin: 14px 0;
      line-height: 1.7;
    }}
    .pane-body pre {{
      background: var(--code-bg);
      color: var(--code-text);
      padding: 14px 18px;
      border-radius: 8px;
      overflow-x: auto;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 13px;
      line-height: 1.55;
      margin: 18px 0;
      box-shadow: 0 2px 10px rgba(0,0,0,0.15);
      border: 1px solid var(--border);
    }}
    .pane-body code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 13.5px;
      background: var(--surface-2);
      color: var(--text);
      padding: 2px 5px;
      border-radius: 4px;
      border: 1px solid var(--border);
    }}
    .pane-body pre code {{
      background: transparent;
      color: inherit;
      padding: 0;
      border: none;
      font-size: 13px;
    }}
    .pane-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 22px 0;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }}
    .pane-body th, .pane-body td {{
      padding: 10px 14px;
      text-align: left;
      border-bottom: 1px solid var(--border);
      font-size: 14px;
    }}
    .pane-body th {{
      background: var(--surface-2);
      font-weight: 700;
    }}
    .pane-body blockquote {{
      margin: 20px 0;
      padding: 12px 18px;
      border-left: 4px solid var(--accent);
      background: var(--surface-2);
      border-radius: 0 8px 8px 0;
      font-style: italic;
    }}
    .pane-body img {{
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      border: 1px solid var(--border);
      margin: 20px 0;
      box-shadow: var(--shadow);
    }}

    /* Footer Prev/Next Cards */
    .pane-footer-nav {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
    }}
    .ch-nav-card {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      padding: 16px 20px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: var(--surface);
      text-decoration: none;
      color: var(--text);
      box-shadow: var(--shadow);
      transition: all 0.15s ease;
    }}
    .ch-nav-card:hover:not(.disabled) {{
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }}
    .ch-nav-card.prev-card {{
      text-align: left;
    }}
    .ch-nav-card.next-card {{
      text-align: right;
    }}
    .ch-nav-card.disabled {{
      opacity: 0.5;
      cursor: not-allowed;
    }}
    .nav-dir {{
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--accent);
    }}
    .nav-title {{
      font-size: 14px;
      font-weight: 700;
    }}

    /* Mobile drawer button */
    .mobile-toc-toggle {{
      display: none;
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 1050;
      background: var(--accent);
      color: #fff;
      border: none;
      padding: 10px 18px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 13.5px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
      cursor: pointer;
      align-items: center;
      gap: 8px;
    }}

    @media (max-width: 1024px) {{
      .tut-sidebar {{
        transform: translateX(-100%);
        width: 300px;
        z-index: 1100;
        box-shadow: 4px 0 25px rgba(0,0,0,0.25);
      }}
      body.drawer-open .tut-sidebar {{
        transform: translateX(0);
      }}
      .tut-content {{
        margin-left: 0;
        padding: 18px 16px 80px;
      }}
      .mobile-toc-toggle {{
        display: inline-flex;
      }}
      .pane-footer-nav {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Announcement Bar / Breadcrumb -->
  <div style="background:var(--surface);border-bottom:1px solid var(--border);padding:8px 16px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;font-size:12.5px;">
    <div style="display:flex;align-items:center;gap:10px;font-weight:600">
      <a href="../index.html" style="color:var(--muted);text-decoration:none">← Hub</a>
      <span style="color:var(--border)">/</span>
      <a href="../all_tech.html" style="color:var(--muted);text-decoration:none">All-Tech Portal</a>
      <span style="color:var(--border)">/</span>
      <a href="../tech_git.html" style="color:var(--muted);text-decoration:none">Git Masterclass</a>
      <span style="color:var(--border)">/</span>
      <span style="color:var(--accent);font-weight:700">Beej's Git Tutorial</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;font-size:12px;color:var(--muted)">
      <span>Keyboard: <kbd style="background:var(--surface-2);border:1px solid var(--border);padding:1px 5px;border-radius:3px;font-family:monospace">[</kbd> Prev &middot; <kbd style="background:var(--surface-2);border:1px solid var(--border);padding:1px 5px;border-radius:3px;font-family:monospace">]</kbd> Next</span>
      <span style="color:var(--border)">|</span>
      <a href="../library.html" style="color:var(--accent);text-decoration:none;font-weight:700">Reading Library ↗</a>
    </div>
  </div>

  <div class="tut-layout">
    <!-- LEFT SIDEBAR -->
    <aside class="tut-sidebar" id="tut-sidebar">
      <div class="sidebar-top">
        <div class="sidebar-brand">
          <span class="brand-icon">📘</span>
          <div>
            <div class="brand-title">Beej's Guide to Git</div>
            <div class="brand-subtitle">Unabridged Interactive Tutorial (38 Ch)</div>
          </div>
        </div>
        <div class="sidebar-search">
          <input type="search" id="sidebar-search" placeholder="Search 38 chapters & topics…" aria-label="Search chapters">
        </div>
        <div class="sidebar-meta">
          <div class="progress-bar-wrap">
            <div class="progress-bar" id="progress-bar" style="width: 0%"></div>
          </div>
          <div class="progress-stats">
            <span id="read-count">0 of 38 chapters read</span>
            <button class="mark-all-btn" onclick="markAllReadToggle()">Mark All ✓</button>
          </div>
          <div class="view-mode-toggle">
            <button class="mode-btn active" id="btn-chapter-mode" onclick="setViewMode('chapter')">📄 Chapter View</button>
            <button class="mode-btn" id="btn-continuous-mode" onclick="setViewMode('continuous')">📜 All Chapters</button>
          </div>
        </div>
      </div>

      <nav class="sidebar-toc" id="sidebar-toc">
{sidebar_toc_html}
      </nav>
    </aside>

    <!-- RIGHT CONTENT AREA -->
    <main class="tut-content" id="tut-content">
      <div class="tut-content-inner">
{all_panes_html}
      </div>
    </main>
  </div>

  <!-- Mobile Floating Drawer Toggle -->
  <button class="mobile-toc-toggle" id="mobile-toc-toggle" onclick="toggleMobileDrawer()" aria-label="Toggle Table of Contents">
    📑 Chapters (38)
  </button>

  <script>
    const ANCHOR_TO_CH = {anchor_map_json};
    const TOTAL_CHAPTERS = 38;
    let currentChapter = 1;
    let viewMode = 'chapter'; // 'chapter' or 'continuous'
    const STORAGE_KEY = 'hub_done_git_beej';

    function getReadSet() {{
      try {{
        return new Set(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'));
      }} catch (e) {{
        return new Set();
      }}
    }}

    function saveReadSet(set) {{
      try {{
        localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(set)));
      }} catch (e) {{}}
      updateProgressUI();
    }}

    function updateProgressUI() {{
      const set = getReadSet();
      const count = set.size;
      const pct = Math.round((count / TOTAL_CHAPTERS) * 100);
      const bar = document.getElementById('progress-bar');
      const lbl = document.getElementById('read-count');
      if (bar) bar.style.width = pct + '%';
      if (lbl) lbl.textContent = `${{count}} of ${{TOTAL_CHAPTERS}} chapters read (${{pct}}%)`;

      for (let i = 1; i <= TOTAL_CHAPTERS; i++) {{
        const isRead = set.has(i);
        const cb = document.getElementById('read-ch-' + i);
        if (cb) cb.checked = isRead;
        const paneBtn = document.getElementById('pane-read-btn-' + i);
        if (paneBtn) {{
          paneBtn.textContent = isRead ? 'Completed ✓' : 'Mark Read ✓';
          paneBtn.style.background = isRead ? 'var(--accent)' : 'var(--accent-dim)';
          paneBtn.style.color = isRead ? '#fff' : 'var(--accent)';
        }}
      }}
    }}

    function toggleChapterRead(num, event) {{
      if (event) event.stopPropagation();
      const set = getReadSet();
      if (set.has(num)) set.delete(num);
      else set.add(num);
      saveReadSet(set);
    }}

    function markAllReadToggle() {{
      const set = getReadSet();
      if (set.size === TOTAL_CHAPTERS) {{
        saveReadSet(new Set());
      }} else {{
        const all = new Set();
        for (let i = 1; i <= TOTAL_CHAPTERS; i++) all.add(i);
        saveReadSet(all);
      }}
    }}

    function setViewMode(mode) {{
      viewMode = mode;
      document.body.classList.toggle('continuous-mode', mode === 'continuous');
      document.getElementById('btn-chapter-mode').classList.toggle('active', mode === 'chapter');
      document.getElementById('btn-continuous-mode').classList.toggle('active', mode === 'continuous');

      if (mode === 'chapter') {{
        showChapter(currentChapter, false);
      }} else {{
        const target = document.getElementById('chapter-' + currentChapter);
        if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}
    }}

    function showChapter(num, scroll = true) {{
      if (num < 1 || num > TOTAL_CHAPTERS) return;
      currentChapter = num;

      document.querySelectorAll('.chapter-pane').forEach(p => p.classList.remove('active'));
      const activePane = document.getElementById('chapter-' + num);
      if (activePane) activePane.classList.add('active');

      document.querySelectorAll('.sidebar-ch-item').forEach(it => it.classList.remove('active'));
      const activeToc = document.getElementById('toc-ch-' + num);
      if (activeToc) {{
        activeToc.classList.add('active');
        activeToc.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
        const subList = document.getElementById('sublist-' + num);
        if (subList) subList.classList.add('open');
      }}

      if (scroll) {{
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
      }}

      if (activePane) {{
        const chId = activePane.dataset.chid;
        history.replaceState(null, null, '#' + chId);
      }}
    }}

    function goToChapter(num, event) {{
      if (event) event.preventDefault();
      if (num < 1 || num > TOTAL_CHAPTERS) return;
      showChapter(num, true);
      document.body.classList.remove('drawer-open');
    }}

    function toggleChapterSubs(num, event) {{
      if (event) event.stopPropagation();
      const subList = document.getElementById('sublist-' + num);
      if (subList) subList.classList.toggle('open');
    }}

    function onChapterLinkClick(num, cid, event) {{
      if (event) event.preventDefault();
      showChapter(num, true);
      document.body.classList.remove('drawer-open');
    }}

    function toggleMobileDrawer() {{
      document.body.classList.toggle('drawer-open');
    }}

    const searchInput = document.getElementById('sidebar-search');
    if (searchInput) {{
      searchInput.addEventListener('input', () => {{
        const q = searchInput.value.trim().toLowerCase();
        document.querySelectorAll('.sidebar-ch-item').forEach(item => {{
          const text = item.textContent.toLowerCase();
          const match = !q || text.includes(q);
          item.style.display = match ? 'block' : 'none';
          if (q && match) {{
            const sub = item.querySelector('.sidebar-sub-list');
            if (sub) sub.classList.add('open');
          }}
        }});
      }});
    }}

    document.querySelectorAll('.sidebar-sub-link').forEach(link => {{
      link.addEventListener('click', (e) => {{
        const targetCh = parseInt(link.dataset.targetCh, 10);
        const targetId = link.dataset.anchor;
        if (targetCh) {{
          if (viewMode === 'chapter' && currentChapter !== targetCh) {{
            showChapter(targetCh, false);
          }}
          setTimeout(() => {{
            const el = document.getElementById(targetId);
            if (el) {{
              el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
              el.style.transition = 'background 0.3s ease';
              const origBg = el.style.background;
              el.style.background = 'var(--accent-dim)';
              setTimeout(() => el.style.background = origBg, 1600);
            }}
          }}, 80);
          document.body.classList.remove('drawer-open');
        }}
      }});
    }});

    document.addEventListener('keydown', (e) => {{
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === '[' || e.key === 'p') {{
        if (currentChapter > 1) goToChapter(currentChapter - 1);
      }} else if (e.key === ']' || e.key === 'n') {{
        if (currentChapter < TOTAL_CHAPTERS) goToChapter(currentChapter + 1);
      }}
    }});

    function handleHash() {{
      const hash = (window.location.hash || '').replace('#', '');
      if (hash) {{
        if (ANCHOR_TO_CH[hash]) {{
          const chNum = ANCHOR_TO_CH[hash];
          showChapter(chNum, false);
          setTimeout(() => {{
            const el = document.getElementById(hash);
            if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
          }}, 150);
        }} else if (hash.startsWith('chapter-')) {{
          const chNum = parseInt(hash.replace('chapter-', ''), 10);
          if (chNum) showChapter(chNum, true);
        }}
      }}
    }}

    window.addEventListener('hashchange', handleHash);
    window.addEventListener('DOMContentLoaded', () => {{
      updateProgressUI();
      if (window.location.hash) {{
        handleHash();
      }} else {{
        showChapter(1, false);
      }}
    }});
  </script>
</body>
</html>"""

    # 1. Write Git_Tutorial/index.html
    tut_path = os.path.join(ROOT, 'Git_Tutorial', 'index.html')
    atomic_write(tut_path, full_html)
    print(f"Wrote Git_Tutorial/index.html ({len(full_html)} bytes).")

    # 2. Write ConvertedDocs/Git/beej_guide_to_git.html with adjusted asset paths (../assets/ -> ../../assets/)
    converted_html = full_html.replace('href="../assets/', 'href="../../assets/').replace('src="../assets/', 'src="../../assets/')
    converted_html = converted_html.replace('href="../index.html"', 'href="../../index.html"')
    converted_html = converted_html.replace('href="../all_tech.html"', 'href="../../all_tech.html"')
    converted_html = converted_html.replace('href="../tech_git.html"', 'href="../../tech_git.html"')
    converted_html = converted_html.replace('href="../library.html"', 'href="../../library.html"')
    
    atomic_write(os.path.join(ROOT, 'ConvertedDocs', 'Git', 'beej_guide_to_git.html'), converted_html)
    print(f"Wrote ConvertedDocs/Git/beej_guide_to_git.html ({len(converted_html)} bytes).")

if __name__ == '__main__':
    build_git_tutorial()
