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
            <span class="ch-num-badge">{num:02d}</span>
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
        ch_content_html = re.sub(r'# vim:[^\n]*\n?', '', ch_content_html)
        ch_content_html = re.sub(r'\\hyphenation\{[^}]*\}\s*', '', ch_content_html)
        ch_content_html = re.sub(r'\bNo hyphenation\b\s*', '', ch_content_html)
        ch_content_html = re.sub(r'\bIndex see alsos\b\s*', '', ch_content_html)

        # Prev / Next footer cards (Atlas Style)
        prev_card = ""
        if prev_ch:
            prev_card = f"""<a class="ch-nav-card prev-card" href="#{prev_ch['id']}" onclick="goToChapter({prev_ch['num']}, event)">
  <div class="nav-dir">← PREVIOUS CHAPTER</div>
  <div class="nav-title">Ch {prev_ch['num']:02d}: {prev_ch['title']}</div>
</a>"""
        else:
            prev_card = """<div class="ch-nav-card prev-card disabled"><div class="nav-dir">← PREVIOUS CHAPTER</div><div class="nav-title">Start of Guide</div></div>"""

        next_card = ""
        if next_ch:
            next_card = f"""<a class="ch-nav-card next-card" href="#{next_ch['id']}" onclick="goToChapter({next_ch['num']}, event)">
  <div class="nav-dir">NEXT CHAPTER →</div>
  <div class="nav-title">Ch {next_ch['num']:02d}: {next_ch['title']}</div>
</a>"""
        else:
            next_card = """<div class="ch-nav-card next-card disabled"><div class="nav-dir">NEXT CHAPTER →</div><div class="nav-title">All 38 Chapters Complete</div></div>"""

        prev_btn_disabled = 'disabled="disabled"' if not prev_ch else ''
        next_btn_disabled = 'disabled="disabled"' if not next_ch else ''

        pane = f"""    <article class="chapter-pane{' active' if num == 1 else ''}" id="chapter-{num}" data-chapter-num="{num}" data-chid="{cid}" data-chapter-title="{title}">
      <header class="pane-header-bar">
        <div class="pane-header-meta">
          <span class="pane-badge">Module {num:02d}</span>
          <span class="pane-crumb">Beej's Guide to Git &rsaquo; <b>{title}</b></span>
          <span class="pane-sep">•</span>
          <a class="pane-external-link" href="https://beej.us/guide/bggit/html/split/{cid}.html" target="_blank" rel="noopener noreferrer">Original Web ↗</a>
        </div>
        <div class="pane-actions">
          <button class="pane-nav-btn prev-btn" onclick="goToChapter({num - 1}, event)" {prev_btn_disabled}>← Prev</button>
          <button class="pane-nav-btn next-btn" onclick="goToChapter({num + 1}, event)" {next_btn_disabled}>Next →</button>
          <button class="pane-read-toggle-btn" id="pane-read-btn-{num}" onclick="toggleChapterRead({num}, event)">Mark Completed ✓</button>
        </div>
      </header>

      <div class="pane-card">
        <div class="pane-body">
{ch_content_html}
        </div>
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
      --tut-sidebar-w: 290px;
      --bg: #F7F8FA;
      --surface: #FFFFFF;
      --surface-2: #F0F2F6;
      --surface-3: #E3E4EB;
      --text: #15171C;
      --muted: #474C5A;
      --faint: #8A92A6;
      --border: #E3E4EB;
      --border-strong: #C9CCD7;
      --separator: #ECEDF2;
      --accent: #5B3CC4;
      --accent-dim: #EFEBFC;
      --accent-strong: #43289E;
      --accent-border: #D9D0F5;
      --success: #2F8F63;
      --success-dim: #E4F3EA;
      --success-border: #BFDECB;
      --success-text: #1F6B47;
      --code-bg: #15171E;
      --code-header: #1D2029;
      --code-border: #2A2E3A;
      --code-text: #E4E6EC;
      --font-heading: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-body: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: 'IBM Plex Mono', SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --shadow: 0 1px 3px rgba(21, 23, 28, 0.05);
      --shadow-md: 0 8px 24px rgba(21, 23, 28, 0.06);
    }}
    html.dark, html[data-theme="dark"] {{
      --bg: #0E1016;
      --surface: #161922;
      --surface-2: #11131A;
      --surface-3: #242938;
      --text: #E9EBF1;
      --muted: #B8BDCB;
      --faint: #6A7182;
      --border: #242938;
      --border-strong: #353B4F;
      --separator: #1E2330;
      --accent: #8F78F2;
      --accent-dim: #211C38;
      --accent-strong: #B7A8FF;
      --accent-border: #3B3268;
      --success: #46B987;
      --success-dim: #11261C;
      --success-border: #24503B;
      --success-text: #7FE0B5;
      --code-bg: #0B0D12;
      --code-header: #12151D;
      --code-border: #1E2330;
      --shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
      --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.45);
    }}
    html.black, html[data-theme="black"] {{
      --bg: #000000;
      --surface: #0A0A0E;
      --surface-2: #060608;
      --surface-3: #1F222B;
      --text: #FFFFFF;
      --muted: #A6ACB9;
      --faint: #5E6472;
      --border: #1F222B;
      --border-strong: #2F3342;
      --separator: #181920;
      --accent: #9D85F7;
      --accent-dim: #1B172E;
      --accent-strong: #C4B7FF;
      --accent-border: #322B57;
      --success: #46B987;
      --success-dim: #0E1F17;
      --success-border: #1C402F;
      --success-text: #7FE0B5;
      --code-bg: #050608;
      --code-header: #0D0F14;
      --code-border: #1A1D24;
      --shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
      --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.75);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      line-height: 1.65;
      font-size: 15.5px;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Announcement / Breadcrumb Bar */
    .tut-top-ribbon {{
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 13px;
    }}
    .tut-top-crumbs {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
    }}
    .tut-top-crumbs a {{
      color: var(--muted);
      text-decoration: none;
      transition: color 0.15s ease;
    }}
    .tut-top-crumbs a:hover {{
      color: var(--accent);
    }}
    .tut-top-crumbs .sep {{
      color: var(--border-strong);
    }}
    .tut-top-crumbs .cur {{
      color: var(--accent);
      font-weight: 700;
    }}
    .tut-top-links {{
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 12.5px;
      color: var(--muted);
    }}
    .tut-top-links a {{
      color: var(--accent);
      text-decoration: none;
      font-weight: 700;
    }}

    /* Outer Wrapper */
    .tut-wrap {{
      max-width: 1300px;
      margin: 0 auto;
      padding: 24px 20px 80px;
    }}

    .tut-layout {{
      display: grid;
      grid-template-columns: var(--tut-sidebar-w) minmax(0, 1fr);
      gap: 28px;
      align-items: start;
    }}

    /* ============================================================
       LEFT SIDEBAR (.course-nav Atlas Style)
       ============================================================ */
    .tut-sidebar {{
      position: sticky;
      top: 76px;
      max-height: calc(100vh - 96px);
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow);
      overflow: hidden;
      z-index: 40;
    }}

    .sidebar-top {{
      padding: 16px 16px 12px;
      border-bottom: 1px solid var(--separator);
      background: var(--surface);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .sidebar-brand {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-bottom: 8px;
      border-bottom: 2px solid var(--accent);
    }}
    .brand-title {{
      font-family: var(--font-heading);
      font-size: 12px;
      font-weight: 800;
      color: var(--accent);
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .brand-subtitle {{
      font-size: 11px;
      color: var(--muted);
      font-weight: 600;
    }}

    .sidebar-search input {{
      width: 100%;
      box-sizing: border-box;
      padding: 8px 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface-2);
      color: var(--text);
      font-size: 12.5px;
      outline: none;
      transition: all 0.15s ease;
    }}
    .sidebar-search input:focus {{
      border-color: var(--accent);
      background: var(--surface);
    }}

    .sidebar-meta {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .progress-bar-wrap {{
      height: 6px;
      background: var(--surface-2);
      border-radius: 999px;
      overflow: hidden;
      border: 1px solid var(--border);
    }}
    .progress-bar {{
      height: 100%;
      background: var(--accent);
      border-radius: 999px;
      transition: width 0.3s ease;
    }}
    .progress-stats {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11.5px;
      font-weight: 650;
      color: var(--muted);
      font-family: var(--font-heading);
    }}
    .mark-all-btn {{
      padding: 3px 8px;
      font-size: 10.5px;
      font-weight: 700;
      border-radius: 6px;
      background: var(--accent-dim);
      color: var(--accent);
      border: 1px solid var(--accent-border);
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .mark-all-btn:hover {{
      background: var(--accent);
      color: #fff;
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
      font-family: var(--font-heading);
      font-size: 11px;
      font-weight: 700;
      color: var(--muted);
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .mode-btn.active {{
      background: var(--surface);
      color: var(--text);
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}

    /* TOC list */
    .sidebar-toc {{
      flex: 1;
      overflow-y: auto;
      overscroll-behavior: contain;
      scrollbar-width: thin;
      padding: 10px 10px 40px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}

    .sidebar-ch-item {{
      border-radius: 8px;
      overflow: hidden;
      transition: background 0.15s ease;
    }}
    .sidebar-ch-head {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 10px;
      cursor: pointer;
      border-radius: 8px;
      transition: background 0.15s ease;
    }}
    .sidebar-ch-head:hover {{
      background: var(--surface-2);
    }}
    .sidebar-ch-item.active .sidebar-ch-head {{
      background: var(--accent-dim);
      border-left: 3px solid var(--accent);
      border-radius: 0 8px 8px 0;
    }}
    .ch-read-check {{
      accent-color: var(--success);
      width: 15px;
      height: 15px;
      cursor: pointer;
      flex-shrink: 0;
    }}
    .sidebar-ch-link {{
      flex: 1;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text);
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      min-width: 0;
    }}
    .ch-num-badge {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      background: var(--accent-dim);
      color: var(--accent);
      padding: 2px 6px;
      border-radius: 6px;
      white-space: nowrap;
      border: 1px solid var(--accent-border);
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
    .sidebar-ch-item.active .ch-title-text {{
      color: var(--accent);
      font-weight: 750;
    }}
    .ch-expander {{
      border: none;
      background: transparent;
      color: var(--faint);
      font-size: 12px;
      cursor: pointer;
      padding: 2px 4px;
      border-radius: 4px;
    }}
    .ch-expander:hover {{
      background: var(--surface-3);
      color: var(--text);
    }}

    .sidebar-sub-list {{
      display: none;
      flex-direction: column;
      padding: 3px 0 6px 20px;
      gap: 2px;
      border-left: 2px solid var(--separator);
      margin-left: 20px;
      margin-top: 2px;
    }}
    .sidebar-sub-list.open {{
      display: flex;
    }}
    .sidebar-sub-link {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 5px 8px;
      border-radius: 6px;
      font-size: 12px;
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
       RIGHT MAIN CONTENT READER (Atlas Style)
       ============================================================ */
    .tut-content {{
      min-width: 0;
    }}

    .tut-content-inner {{
      max-width: 900px;
      margin: 0 auto;
    }}

    /* Chapter Panes */
    .chapter-pane {{
      display: none;
    }}
    .chapter-pane.active {{
      display: block;
      animation: amFade 0.22s ease-out;
    }}
    body.continuous-mode .chapter-pane {{
      display: block !important;
      margin-bottom: 60px;
      padding-bottom: 40px;
      border-bottom: 2px solid var(--border);
    }}

    @keyframes amFade {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: none; }}
    }}

    .pane-header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      padding: 14px 20px;
      margin-bottom: 22px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: var(--shadow);
    }}
    .pane-header-meta {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13px;
      color: var(--muted);
      font-weight: 600;
      flex-wrap: wrap;
    }}
    .pane-badge {{
      background: var(--accent-dim);
      color: var(--accent);
      padding: 3px 9px;
      border-radius: 999px;
      font-family: var(--font-heading);
      font-weight: 800;
      font-size: 11.5px;
      border: 1px solid var(--accent-border);
      letter-spacing: 0.04em;
    }}
    .pane-crumb {{
      color: var(--muted);
      font-size: 13.5px;
    }}
    .pane-crumb b {{
      color: var(--text);
      font-family: var(--font-heading);
    }}
    .pane-sep {{
      color: var(--border-strong);
    }}
    .pane-external-link {{
      color: var(--muted);
      text-decoration: none;
      font-size: 12px;
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
      padding: 7px 13px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid var(--border);
      background: var(--surface-2);
      color: var(--text);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: var(--font-heading);
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
      padding: 7px 14px;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid var(--accent-border);
      background: var(--accent-dim);
      color: var(--accent);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: var(--font-heading);
    }}
    .pane-read-toggle-btn:hover {{
      background: var(--accent);
      color: #fff;
    }}

    /* Pane Enclosing Card (Atlas Article Style) */
    .pane-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: clamp(24px, 3.5vw, 44px);
      box-shadow: var(--shadow);
    }}

    /* Typography & Code */
    .pane-body h1 {{
      font-family: var(--font-heading);
      font-size: clamp(1.8rem, 2.8vw, 2.3rem);
      font-weight: 800;
      letter-spacing: -0.022em;
      margin: 0 0 20px;
      color: var(--text);
      line-height: 1.25;
    }}
    .pane-body h2 {{
      font-family: var(--font-heading);
      font-size: 1.45rem;
      font-weight: 750;
      letter-spacing: -0.015em;
      margin: 2.4rem 0 1rem;
      color: var(--text);
      padding-top: 1.2rem;
      border-top: 1px solid var(--separator);
    }}
    .pane-body h2:first-of-type {{
      border-top: 0;
      padding-top: 0;
    }}
    .pane-body h3 {{
      font-family: var(--font-heading);
      font-size: 1.15rem;
      font-weight: 700;
      margin: 1.8rem 0 0.6rem;
      color: var(--text);
    }}
    .pane-body h4 {{
      font-family: var(--font-heading);
      font-size: 1.02rem;
      font-weight: 650;
      margin: 1.3rem 0 0.5rem;
      color: var(--text);
    }}
    .pane-body p {{
      margin: 0.9rem 0;
      line-height: 1.7;
    }}
    .pane-body pre {{
      background: var(--code-bg);
      color: var(--code-text);
      padding: 18px 20px;
      border-radius: 12px;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 13.5px;
      line-height: 1.65;
      margin: 1.4rem 0;
      box-shadow: 0 4px 18px rgba(0,0,0,0.25);
      border: 1px solid var(--code-border);
    }}
    .pane-body code {{
      font-family: var(--font-mono);
      font-size: 13.5px;
      background: var(--surface-2);
      color: var(--accent);
      padding: 2px 6px;
      border-radius: 6px;
      border: 1px solid var(--border);
    }}
    .pane-body pre code {{
      background: transparent;
      color: inherit;
      padding: 0;
      border: none;
      font-size: 13.5px;
    }}
    .pane-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.4rem 0;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
      font-size: 14px;
    }}
    .pane-body th, .pane-body td {{
      padding: 10px 14px;
      text-align: left;
      border: 1px solid var(--border);
    }}
    .pane-body th {{
      background: var(--surface-2);
      font-weight: 750;
      font-family: var(--font-heading);
      text-transform: uppercase;
      font-size: 12.5px;
      letter-spacing: 0.04em;
    }}
    .pane-body blockquote {{
      margin: 1.4rem 0;
      padding: 14px 18px;
      border-left: 4px solid var(--accent);
      background: var(--accent-dim);
      border-radius: 0 10px 10px 0;
      color: var(--muted);
      font-style: normal;
    }}
    .pane-body img {{
      max-width: 100%;
      height: auto;
      border-radius: 10px;
      border: 1px solid var(--border);
      margin: 20px 0;
      box-shadow: var(--shadow);
    }}

    /* Footer Prev/Next Cards (Atlas Style) */
    .pane-footer-nav {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
      margin-top: 28px;
    }}
    .ch-nav-card {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      padding: 16px 20px;
      border-radius: 14px;
      border: 1px solid var(--border);
      background: var(--surface);
      text-decoration: none;
      color: var(--text);
      box-shadow: var(--shadow);
      transition: all 0.16s ease;
    }}
    .ch-nav-card:hover:not(.disabled) {{
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      text-decoration: none;
    }}
    .ch-nav-card.prev-card {{
      text-align: left;
    }}
    .ch-nav-card.next-card {{
      text-align: right;
    }}
    .ch-nav-card.disabled {{
      opacity: 0.45;
      cursor: not-allowed;
      pointer-events: none;
    }}
    .nav-dir {{
      font-family: var(--font-heading);
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent);
    }}
    .nav-title {{
      font-family: var(--font-heading);
      font-size: 14.5px;
      font-weight: 700;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
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
      font-weight: 750;
      font-size: 13.5px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
      cursor: pointer;
      align-items: center;
      gap: 8px;
      font-family: var(--font-heading);
    }}

    @media (max-width: 1040px) {{
      .tut-layout {{
        grid-template-columns: 1fr;
      }}
      .tut-sidebar {{
        position: fixed;
        top: 56px;
        left: 0;
        bottom: 0;
        max-height: none;
        width: min(340px, 88vw);
        border-radius: 0;
        transform: translateX(-102%);
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
        z-index: 1100;
        box-shadow: var(--shadow-md);
      }}
      body.drawer-open .tut-sidebar {{
        transform: translateX(0);
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
  <div class="tut-top-ribbon">
    <div class="tut-top-crumbs">
      <a href="../index.html">← Hub</a>
      <span class="sep">/</span>
      <a href="../all_tech.html">All-Tech Portal</a>
      <span class="sep">/</span>
      <a href="../tech_git.html">Git Masterclass</a>
      <span class="sep">/</span>
      <span class="cur">Beej's Git Tutorial</span>
    </div>
    <div class="tut-top-links">
      <span>Keyboard: <kbd style="background:var(--surface-2);border:1px solid var(--border);padding:1px 5px;border-radius:4px;font-family:monospace">[</kbd> Prev · <kbd style="background:var(--surface-2);border:1px solid var(--border);padding:1px 5px;border-radius:4px;font-family:monospace">]</kbd> Next</span>
      <span class="sep">|</span>
      <a href="../library.html">Reading Library ↗</a>
    </div>
  </div>

  <div class="tut-wrap">
    <div class="tut-layout">
      <!-- LEFT SIDEBAR -->
      <aside class="tut-sidebar" id="tut-sidebar">
        <div class="sidebar-top">
          <div class="sidebar-brand">
            <span class="brand-title">📘 Beej's Git Track</span>
            <span class="brand-subtitle">38 Modules</span>
          </div>
          <div class="sidebar-search">
            <input type="search" id="sidebar-search" placeholder="Search 38 chapters & topics…" aria-label="Search chapters">
          </div>
          <div class="sidebar-meta">
            <div class="progress-bar-wrap">
              <div class="progress-bar" id="progress-bar" style="width: 0%"></div>
            </div>
            <div class="progress-stats">
              <span id="read-count">0 of 38 chapters completed</span>
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
    if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

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

      window.scrollTo({{ top: 0, behavior: 'instant' }});

      if (activePane) {{
        const chId = activePane.dataset.chid;
        history.replaceState(null, null, '#' + chId);
        window.scrollTo({{ top: 0, behavior: 'instant' }});
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
          const activePane = document.getElementById('chapter-' + chNum);
          const isChId = activePane && activePane.dataset.chid === hash;
          showChapter(chNum, false);
          if (!isChId) {{
            setTimeout(() => {{
              const el = document.getElementById(hash);
              if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}, 150);
          }} else {{
            window.scrollTo(0, 0);
            setTimeout(() => window.scrollTo(0, 0), 60);
          }}
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
