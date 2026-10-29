import os
import sys
import tempfile
import time
import re
import html as html_lib
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def atomic_write(filepath, content):
    d = os.path.dirname(os.path.abspath(filepath))
    with tempfile.NamedTemporaryFile('w', dir=d, delete=False, encoding='utf-8') as tf:
        tf.write(content)
        temp_name = tf.name
    for attempt in range(4):
        try:
            os.replace(temp_name, filepath)
            break
        except OSError:
            if attempt == 3: raise
            time.sleep(0.1 * (attempt + 1))
    if os.path.exists(temp_name):
        try: os.unlink(temp_name)
        except OSError: pass

# 28 Concepts across 6 Subsections
GIT_SUBSECTIONS = [
    {
        "title": "Git Architecture, Object Storage & Internal Mechanics",
        "concepts": [
            ("5.1.1", "Git Object Model: Blobs, Trees, Commits & Annotated Tags in .git/objects",
             "Content-addressable key-value store, SHA-1/SHA-256 cryptographic hashing, immutable zlib blob compression, tree directory snapshots, and commit DAG parent pointers.",
             "https://www.youtube.com/watch?v=fctCbTWsPvg", "00:00", "Computerphile", "ConvertedDocs/Git/beej_guide_to_git.html#the-git-log-and-head"),
            ("5.1.2", "The Three Trees: Working Directory, Staging Area (Index) & Git Repository",
             "The tripartite architecture: untracked and modified files on disk, binary index staging area (.git/index), and committed object snapshots in HEAD.",
             "https://www.youtube.com/watch?v=HVsySz-h9r4", "00:00", "freeCodeCamp.org", "ConvertedDocs/Git/beej_guide_to_git.html#git-basics"),
            ("5.1.3", "Git Diff Internals: Working vs Staging vs Commit Comparisons",
             "Computing unified diffs with Myers and Histogram algorithms; comparing working tree to stage (git diff), stage to HEAD (git diff --staged), and branch comparisons (git diff A..B).",
             "https://www.youtube.com/watch?v=usS9A_E_260", "00:00", "Corey Schafer", "ConvertedDocs/Git/beej_guide_to_git.html#diff"),
            ("5.1.4", "Atomic Commits, git add -p Patch Staging & Commit Hygiene",
             "Single-responsibility commits, interactive hunk-by-hunk staging with git add -p and s (split), and crafting conventional commit messages (feat, fix, chore, refactor).",
             "https://www.youtube.com/watch?v=sPvg_9gQ9jU", "00:00", "Fireship", "ConvertedDocs/Git/beej_guide_to_git.html#patch-mode-applying-partial-changes"),
            ("5.1.5", "File States, Short Status Flags & .gitignore Pattern Syntax",
             "Untracked, unmodified, modified, and staged lifecycle; rapid diagnostics with git status -s; .gitignore globbing rules, negation patterns (!), and cleaning untracked files (git clean -fd).",
             "https://www.youtube.com/watch?v=8JJ101D3KnE", "00:00", "Traversy Media", "ConvertedDocs/Git/beej_guide_to_git.html#file-states")
        ]
    },
    {
        "title": "Branching Strategies, Merging & Interactive Rebasing",
        "concepts": [
            ("5.2.1", "Branching Workflows: Trunk-Based Development vs GitFlow",
             "Fast-moving short-lived feature branches in trunk-based CI/CD vs release-branching in GitFlow; branch pointers as 41-byte ref files in .git/refs/heads/.",
             "https://www.youtube.com/watch?v=e2IbNHi4uCI", "00:00", "freeCodeCamp.org", "ConvertedDocs/Git/beej_guide_to_git.html#branches-and-fast-forward-merges"),
            ("5.2.2", "Merge Mechanics: Fast-Forward Merges vs True 3-Way Merge Commits",
             "Fast-forward pointer updates without new commits, 3-way merges identifying common merge bases, --no-ff merge commits, and recursive vs ort merge strategies.",
             "https://www.youtube.com/watch?v=3a2x1kA_G7U", "00:00", "The Net Ninja", "ConvertedDocs/Git/beej_guide_to_git.html#merge"),
            ("5.2.3", "Merge Conflict Anatomy, Conflict Markers & Resolution Workflows",
             "Dissecting conflict markers (<<<<<<< HEAD, =======, >>>>>>>), resolving overlapping line changes, using git status during conflict states, and git merge --abort.",
             "https://www.youtube.com/watch?v=JtIX3HJKwfo", "00:00", "freeCodeCamp.org", "ConvertedDocs/Git/beej_guide_to_git.html#merge"),
            ("5.2.4", "Interactive Rebasing (git rebase -i): Pick, Squash, Reword & Fixup",
             "Rewriting local commit histories, squashing fix commits, rewording commit messages, dropping unwanted commits, and handling rebase pauses (git rebase --continue / --abort).",
             "https://www.youtube.com/watch?v=Tyd3zp_6b00", "00:00", "Fireship", "ConvertedDocs/Git/beej_guide_to_git.html#rebase"),
            ("5.2.5", "Merge vs Rebase Trade-Offs & Safe Force Pushing (--force-with-lease)",
             "Linear commit history vs preserved historical context; golden rule of rebasing on public branches; preventing collaborator overwrites with git push --force-with-lease.",
             "https://www.youtube.com/watch?v=0chZFIZLR_0", "00:00", "freeCodeCamp.org", "ConvertedDocs/Git/beej_guide_to_git.html#rebase")
        ]
    },
    {
        "title": "Disaster Recovery, History Manipulation & Undos",
        "concepts": [
            ("5.3.1", "Git Reflog: Recovering Lost Commits, Deleted Branches & Broken Rebases",
             "The local reference log tracking every HEAD movement (.git/logs/HEAD), finding orphaned commit hashes, and restoring deleted branches using git branch <name> HEAD@{n}.",
             "https://www.youtube.com/watch?v=339jxX7b9oY", "00:00", "Fireship", "ConvertedDocs/Git/beej_guide_to_git.html#the-reference-log-reflog"),
            ("5.3.2", "Git Reset Modes: --soft, --mixed & --hard Demystified",
             "Moving HEAD pointer: --soft (keeps changes staged in index), --mixed (resets index, keeps changes in working tree), and --hard (discards both index and working tree modifications).",
             "https://www.youtube.com/watch?v=Xh0Y9Z0l75g", "00:00", "Corey Schafer", "ConvertedDocs/Git/beej_guide_to_git.html#reset"),
            ("5.3.3", "Git Revert: Safe Public Undos via Inverse Commits",
             "Generating new commits that invert previous commit diffs without rewriting history; reverting single commits, merge commits with -m 1, and ranges of commits.",
             "https://www.youtube.com/watch?v=mJ-Te3kG1iU", "00:00", "The Net Ninja", "ConvertedDocs/Git/beej_guide_to_git.html#revert"),
            ("5.3.4", "Modern Git Ergonomics: git restore & git switch vs Overloaded Checkout",
             "Disentangling overloaded git checkout: using git switch for branch navigation and creation (-c), and git restore for discarding uncommitted changes (--staged vs working copy).",
             "https://www.youtube.com/watch?v=sPvg_9gQ9jU", "00:00", "Fireship", "ConvertedDocs/Git/beej_guide_to_git.html#file-states"),
            ("5.3.5", "Git Bisect: Binary Searching History to Pinpoint Regressions",
             "Identifying the exact commit introducing a bug in O(log N) steps; git bisect start, git bisect bad, git bisect good, and automated binary searching with git bisect run <script>.",
             "https://www.youtube.com/watch?v=P21Vj0FjIos", "00:00", "Fireship", "ConvertedDocs/Git/beej_guide_to_git.html#appendix-other-references")
        ]
    },
    {
        "title": "Productivity Workflows, Stashing & Power Tools",
        "concepts": [
            ("5.4.1", "Git Stash Mechanics: Stashing Staged, Untracked & Branching Stashes",
             "Temporarily shelving uncommitted work with git stash push -m 'msg', applying vs popping, inspecting with git stash show -p, stashing untracked files (-u), and git stash branch.",
             "https://www.youtube.com/watch?v=KLEDKgMmbBI", "00:00", "Corey Schafer", "ConvertedDocs/Git/beej_guide_to_git.html#stash"),
            ("5.4.2", "Git Cherry-Pick & Git Worktrees for Isolated Multi-Branch Working",
             "Splicing specific commits across divergent branches; utilizing git worktree add to check out and build multiple branches simultaneously in linked separate directories.",
             "https://www.youtube.com/watch?v=2uEqYw-N8u8", "00:00", "Fireship", "ConvertedDocs/Git/beej_guide_to_git.html#worktrees"),
            ("5.4.3", "Git Submodules & Subtrees for Multi-Repository Dependency Management",
             "Embedding foreign Git repositories as submodules at pinned commit hashes; .gitmodules configuration, git submodule update --init --recursive, and git subtree comparisons.",
             "https://www.youtube.com/watch?v=gSlXo2iLFig", "00:00", "freeCodeCamp.org", "ConvertedDocs/Git/beej_guide_to_git.html#submodules"),
            ("5.4.4", "Configuration Architecture, Global vs Local Scopes & Power Aliases",
             "Hierarchical configuration files (system, global ~/.gitconfig, local .git/config); setting core editors, credential helpers, line endings, and custom productivity aliases.",
             "https://www.youtube.com/watch?v=hwP7mwU4ycQ", "00:00", "Corey Schafer", "ConvertedDocs/Git/beej_guide_to_git.html#configuration"),
            ("5.4.5", "Git Blame, Commit Attribution & Ignoring Whitespace Noise",
             "Line-by-line file attribution with git blame -L, tracing origin commits, ignoring whitespace and formatting churn with .git-blame-ignore-revs, and git log -S pickaxe search.",
             "https://www.youtube.com/watch?v=9Z0l75g-1aU", "00:00", "The Net Ninja", "ConvertedDocs/Git/beej_guide_to_git.html#whos-to-blame-for-this-code")
        ]
    },
    {
        "title": "GitHub Enterprise Collaboration & CI/CD Actions",
        "concepts": [
            ("5.5.1", "Remotes Architecture: Origin, Upstream & Remote-Tracking Branches",
             "Managing distributed remotes (git remote add), anatomy of origin/main remote-tracking references, git fetch vs git pull --rebase, and upstream tracking flags (-u).",
             "https://www.youtube.com/watch?v=Gg4bLk8cGNo", "00:00", "freeCodeCamp.org", "ConvertedDocs/Git/beej_guide_to_git.html#remotes-repos-in-other-places"),
            ("5.5.2", "Enterprise Pull Requests: Branch Protection Rules, Checks & CODEOWNERS",
             "Modern pull request lifecycle, linear commit history enforcement, mandatory status checks, review approvals, code owner routing via .github/CODEOWNERS, and auto-merge.",
             "https://www.youtube.com/watch?v=8lGpZkjnkt4", "00:00", "freeCodeCamp.org", "ConvertedDocs/Git/beej_guide_to_git.html#github-forking-and-pull-requests"),
            ("5.5.3", "GitHub Actions Core: Workflows, Jobs, Steps, Matrix Builds & Runners",
             "Declarative YAML workflow topologies triggered on push/PR events; runner isolation, parallel matrix builds across OS/Python versions, and conditional job execution dependencies.",
             "https://www.youtube.com/watch?v=R8_veQiYBjI", "00:00", "freeCodeCamp.org", "https://docs.github.com/en/actions"),
            ("5.5.4", "CI/CD Secrets Security, Environment Gates & Dependency Caching",
             "Managing repository and environment secrets, OpenID Connect (OIDC) keyless cloud authentication (AWS/Azure/GCP), and build acceleration via actions/cache.",
             "https://www.youtube.com/watch?v=mFFXuXjVgkU", "00:00", "freeCodeCamp.org", "https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows")
        ]
    },
    {
        "title": "Emergency Survival: Demystifying Scary Git Errors",
        "concepts": [
            ("5.6.1", "Error Survival: [rejected] non-fast-forward (fetch first)",
             "Why Git rejects pushes when the remote branch has new commits; why blind force pushing is dangerous; resolving smoothly with git pull --rebase and pushing cleanly.",
             "https://www.youtube.com/watch?v=vV_X1j_B13Y", "00:00", "Corey Schafer", "ConvertedDocs/Git/beej_guide_to_git.html#appendix-errors-and-scary-messages"),
            ("5.6.2", "Error Survival: You are in 'detached HEAD' state",
             "What a detached HEAD actually means (HEAD points directly to a commit hash rather than a named branch); how to inspect code safely, save experiments to a new branch, and get back to main.",
             "https://www.youtube.com/watch?v=2ReR1YJnNUM", "00:00", "Fireship", "ConvertedDocs/Git/beej_guide_to_git.html#the-git-log-and-head"),
            ("5.6.3", "Error Survival: fatal: refusing to merge unrelated histories",
             "Diagnosing why this occurs when combining independently initialized Git repositories; utilizing --allow-unrelated-histories safely and stitching root commit histories.",
             "https://www.youtube.com/watch?v=fctCbTWsPvg", "00:00", "Computerphile", "ConvertedDocs/Git/beej_guide_to_git.html#appendix-errors-and-scary-messages"),
            ("5.6.4", "Emergency Exit: Escaping Vim/Nano & Aborting Hazardous Git Operations",
             "Beej's essential guide to escaping the default terminal editor when trapped in a commit message (:wq, :q!, ZZ); safely aborting runaway merges (git merge --abort) and rebases (git rebase --abort).",
             "https://www.youtube.com/watch?v=ggSyF1SVFr4", "00:00", "Fireship", "ConvertedDocs/Git/beej_guide_to_git.html#editor-get-out")
        ]
    }
]

def generate_subsections_html():
    blocks = []
    for s_idx, sub in enumerate(GIT_SUBSECTIONS):
        concepts_html = []
        for c in sub["concepts"]:
            cid, cname, cdesc, yt_url, start_time, channel, doc_url = c
            dur_label = "20:00"
            doc_label = "📖Beej's Guide" if "beej" in doc_url else "🌐Doc"
            # Crucial: Escape HTML characters in name & desc to prevent unclosed <script> or other tags
            safe_cname = html_lib.escape(cname)
            safe_cdesc = html_lib.escape(cdesc)
            clean_name_attr = re.sub(r'[^a-zA-Z0-9\s-]', '', cname).lower()
            clean_name_attr = ' '.join(clean_name_attr.split())

            row = f"""      <li data-cid="{cid}" data-name="{clean_name_attr}">
        <div class="done-check" title="Mark as done"></div>
        <div class="bookmark-star" title="Bookmark">☆</div>
        <div>
          <div class="cname">{safe_cname}</div>
          <div style="font-size:11.5px;color:var(--text-faint);margin-top:2px">{safe_cdesc}</div>
        </div>
        <div class="res-links"><a class="video" href="{yt_url}" data-vtitle="{safe_cname}" data-vchannel="{channel}" data-start="{start_time}" data-vdur="{dur_label}" target="_blank" rel="noopener" title="Watch walkthrough: {safe_cname}">🎬YT</a><a href="{doc_url}" target="_blank" rel="noopener" title="Reference Guide: {safe_cname}">{doc_label}</a></div>
      </li>"""
            concepts_html.append(row)

        sub_block = f"""    <div class="subsection">
      <div class="subsection-head">
        <span class="subsection-tag">5.{s_idx+1}</span>
        <h3>{html_lib.escape(sub['title'])}</h3>
        <span style="font-size:11px;color:var(--text-faint);">{len(sub['concepts'])} concepts</span>
      </div>
      <div class="subsection-desc">Masterclass lessons covering {html_lib.escape(sub['title'])} architecture, operational mechanisms, and failure modes.</div>
      <ol class="concepts">
{chr(10).join(concepts_html)}
      </ol>
    </div>"""
        blocks.append(sub_block)
    return "\n".join(blocks)

def update_tech_git():
    path = os.path.join(ROOT, 'tech_git.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    total_subs = len(GIT_SUBSECTIONS)
    total_concepts = sum(len(sub["concepts"]) for sub in GIT_SUBSECTIONS)

    # 1. Update hero edition and stats
    html = re.sub(r'· \d+ Subsections · \d+ Concepts', f'· {total_subs} Subsections · {total_concepts} Concepts', html)
    html = re.sub(r'<div class="stat"><div class="n">\d+</div><div class="l">Subsections</div></div>', f'<div class="stat"><div class="n">{total_subs}</div><div class="l">Subsections</div></div>', html)
    html = re.sub(r'<div class="stat"><div class="n">\d+</div><div class="l">Concepts</div></div>', f'<div class="stat"><div class="n">{total_concepts}</div><div class="l">Concepts</div></div>', html)
    html = re.sub(r'<span class="pct" id="overall-pct">0 / \d+</span>', f'<span class="pct" id="overall-pct">0 / {total_concepts}</span>', html)
    html = re.sub(r'placeholder="Search \d+ concepts…"', f'placeholder="Search {total_concepts} concepts…"', html)

    # 2. Add / update Beej banner
    beej_banner = """  <!-- Beej's Guide Recommended Reading Banner -->
  <div class="beej-banner" style="background:var(--surface);border:1px solid var(--border);border-left:4px solid #f97316;border-radius:10px;padding:14px 18px;margin:20px 0 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;box-shadow:var(--shadow)">
    <div style="display:flex;align-items:center;gap:12px">
      <span style="font-size:24px">📖</span>
      <div>
        <div style="font-weight:700;font-size:14px;color:var(--text)">Primary Recommended Reading: Beej's Guide to Git (Unabridged)</div>
        <div style="font-size:12px;color:var(--muted)">Read Brian "Beej" Hall's legendary practical walkthrough covering staging, fast-forward merges, reflog resurrection, and worktrees.</div>
      </div>
    </div>
    <div style="display:flex;gap:8px">
      <a href="ConvertedDocs/Git/beej_guide_to_git.html" target="_blank" style="padding:6px 14px;font-size:12.5px;font-weight:700;background:var(--accent);color:#fff;border-radius:6px;text-decoration:none">Read Offline Edition ↗</a>
      <a href="https://beej.us/guide/bggit/html/split/index.html" target="_blank" rel="noopener noreferrer" style="padding:6px 14px;font-size:12.5px;font-weight:600;background:var(--surface-2);color:var(--text);border:1px solid var(--border);border-radius:6px;text-decoration:none">Original Web ↗</a>
    </div>
  </div>"""

    # Strip existing banner if present
    html = re.sub(r'\s*<!-- Beej\'s Guide Recommended Reading Banner -->\s*<div class="beej-banner"[\s\S]*?</div>\s*</div>\s*</div>\s*', '\n\n', html)
    # Insert right before <div class="stats">
    html = html.replace('\n  <div class="stats">', f'\n{beej_banner}\n\n  <div class="stats">')

    # 3. Build section-5
    subs_html = generate_subsections_html()
    new_sec = f"""<section class="section domain-section" data-domain="git" id="section-5" style="--section-color:hsl(12, 80%, 50%)">
  <div id="git"></div>
  <div class="domain-focus-bar">
    <div class="focus-bar-left">
      <span class="focus-bar-pill">Domain 5 of 16</span>
      <span class="focus-bar-title">Git &amp; GitHub Architecture</span>
      <span class="focus-bar-stats">{total_concepts} concepts &bull; {total_subs} subsections</span>
    </div>
    <div class="focus-bar-right">
      <button class="focus-btn" onclick="navigateDomain(-1)" type="button">← Prev Domain</button>
      <button class="focus-btn view-all-btn" onclick="switchDomain('all')" type="button">🌐 View All (16)</button>
      <button class="focus-btn" onclick="navigateDomain(1)" type="button">Next Domain →</button>
      <a class="focus-btn masterclass-btn" href="all_tech.html#section-5">Tech Portal View ↗</a>
    </div>
  </div>

  <div class="section-banner" style="background:linear-gradient(135deg, hsl(12, 85%, 45%), hsl(32, 75%, 35%))">
    <div class="num">5</div>
    <div class="info">
      <div class="label">Section 5 of 16</div>
      <h2>5. Git &amp; GitHub Architecture</h2>
      <div class="meta">{total_subs} subsections &middot; {total_concepts} concepts</div>
    </div>
    <div class="ppg">
      <div class="pct-text" data-pp-text="5">0 / {total_concepts}</div>
      <div class="pp-track"><div class="pp-bar" data-pp-bar="5"></div></div>
    </div>
  </div>

  <div class="sec-desc">
    <p><strong>Core Focus:</strong> Git DAG object model (blobs, trees, commits), 3 trees, staging, branching models, interactive rebase, cherry-pick, merge conflicts, reflog disaster recovery, worktrees, and Beej's guide to scary Git errors.</p>
    <p><strong>Track Key:</strong> Object DB, Branching, Rebasing, Emergency Survival &amp; Advanced Workflows</p>
  </div>

{subs_html}
</section>"""

    m5 = re.search(r'<section[^>]*id="section-5"[^>]*>', html)
    ms = re.search(r'<div class="sister-guides-card">', html)
    if not m5 or not ms:
        raise ValueError("Could not find section-5 or sister-guides boundaries in tech_git.html")

    html = html[:m5.start()] + new_sec + "\n\n  " + html[ms.start():]
    atomic_write(path, html)
    print(f"Updated tech_git.html: {total_subs} subs, {total_concepts} concepts.")

def update_all_tech():
    path = os.path.join(ROOT, 'all_tech.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    total_git_subs = len(GIT_SUBSECTIONS)
    total_git_concepts = sum(len(sub["concepts"]) for sub in GIT_SUBSECTIONS)

    subs_html = generate_subsections_html()

    new_sec = f"""<section class="section domain-section" data-domain="git" id="section-5" style="--section-color:hsl(12, 80%, 50%)">
<div id="git"></div>
<div class="domain-focus-bar">
<div class="focus-bar-left">
<span class="focus-bar-pill">Domain 5 of 16</span>
<span class="focus-bar-title">Git &amp; GitHub Architecture</span>
<span class="focus-bar-stats">{total_git_concepts} concepts • {total_git_subs} subsections</span>
</div>
<div class="focus-bar-right">
<button class="focus-btn" onclick="navigateDomain(-1)" type="button">← Prev Domain</button>
<button class="focus-btn view-all-btn" onclick="switchDomain('all')" type="button">🌐 View All (16)</button>
<button class="focus-btn" onclick="navigateDomain(1)" type="button">Next Domain →</button>
<a class="focus-btn masterclass-btn" href="tech_git.html">Dedicated Masterclass ↗</a>
</div>
</div>
<div class="section-banner" style="background:linear-gradient(135deg, hsl(12, 85%, 45%), hsl(32, 75%, 35%))">
<div class="num">5</div>
<div class="info">
<div class="label">Section 5 of 16</div>
<h2>5. Git &amp; GitHub Architecture</h2>
<div class="meta">{total_git_subs} subsections · {total_git_concepts} concepts</div>
</div>
<div class="ppg">
<div class="pct-text" data-pp-text="5">0 / {total_git_concepts}</div>
<div class="pp-track"><div class="pp-bar" data-pp-bar="5"></div></div>
</div>
</div>
<div class="sec-desc">
<p><strong>Core Focus:</strong> Git DAG object model (blobs, trees, commits), 3 trees, staging, branching models, interactive rebase, cherry-pick, merge conflicts, reflog disaster recovery, worktrees, and Beej's guide to scary Git errors.</p>
<p><strong>Track Key:</strong> Object DB, Branching, Rebasing, Emergency Survival &amp; Advanced Workflows</p>
</div>
{subs_html}
</section>
"""

    m5 = re.search(r'<section[^>]*id="section-5"[^>]*>', html)
    m6 = re.search(r'<section[^>]*id="section-6"[^>]*>', html)
    if not m5 or not m6:
        raise ValueError("Could not find section-5 or section-6 boundaries in all_tech.html")

    html = html[:m5.start()] + new_sec + html[m6.start():]

    # Recalculate totals in all_tech.html
    soup = BeautifulSoup(html, 'html.parser')
    all_subs = soup.find_all('div', class_='subsection')
    all_concepts = soup.find_all('li', attrs={'data-cid': True})
    total_subs = len(all_subs)
    total_concepts = len(all_concepts)

    print(f"all_tech.html recalculated totals: {total_subs} subs, {total_concepts} concepts.")

    # Update hero edition and stats in all_tech.html
    html = re.sub(r'· \d+ Subsections · \d+ Concepts', f'· {total_subs} Subsections · {total_concepts} Concepts', html)
    html = re.sub(r'<div class="stat"><div class="n">\d+</div><div class="l">Subsections</div></div>', f'<div class="stat"><div class="n">{total_subs}</div><div class="l">Subsections</div></div>', html)
    html = re.sub(r'<div class="stat"><div class="n">\d+</div><div class="l">Concepts</div></div>', f'<div class="stat"><div class="n">{total_concepts}</div><div class="l">Concepts</div></div>', html)
    html = re.sub(r'<span class="pct" id="overall-pct">0 / \d+</span>', f'<span class="pct" id="overall-pct">0 / {total_concepts}</span>', html)
    html = re.sub(r'placeholder="Search \d+ engineering &amp; infrastructure concepts…"', f'placeholder="Search {total_concepts} engineering &amp; infrastructure concepts…"', html)

    # Update card-git in all_tech.html
    card_git_pattern = r'(<div class="domain-card"[^>]*id="card-git"[^>]*>[\s\S]*?<div class="domain-card-chips">)[\s\S]*?(</div>\s*<div class="domain-card-actions">)'
    new_chips = r"""\1
<span class="domain-card-chip">28 concepts</span>
<span class="domain-card-chip">6 subsections</span>
<span class="domain-card-chip highlight">Beej's Guide Integrated</span>
\2"""
    html = re.sub(card_git_pattern, new_chips, html)

    atomic_write(path, html)
    print("Updated all_tech.html with enriched Git section and updated counts.")

if __name__ == '__main__':
    update_tech_git()
    update_all_tech()
