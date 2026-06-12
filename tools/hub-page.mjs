// Hub landing page (index.html / hub.html).
// Six page cards + global search, bookmark review queue, and progress export/import.

function escHtml(value = "") {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function personalPurpose(source) {
  const purposes = {
    dsa: "My primary coding-interview practice map: patterns first, problems second, repeat weak spots until they feel automatic.",
    sd: "My system design control room: concepts, trade-offs, classic designs, and interview structure in one place.",
    cs: "My fundamentals refresh layer: OS, networking, databases, concurrency, security, and architecture for deeper reasoning.",
    bh: "My story bank and leadership prep space: STAR answers, principles, conflict, ownership, and mock practice.",
    ai: "My AI engineering track: LLM apps, RAG, agents, evals, MLOps, and production quality constraints.",
    cloud: "My AWS and Azure comparison desk: services, Q&A, architecture pillars, security, reliability, and cost thinking.",
  };
  return purposes[source.key] || source.summary;
}

export function simpleHubHtml(data) {
  const json = JSON.stringify({
    sources: data.sources.map((s) => ({
      key: s.key,
      title: s.title,
      file: s.file,
      label: s.label,
      color: s.color,
      storage: s.storage,
      itemCount: s.itemCount,
      progressLabel: s.progressLabel,
    })),
  }).replace(/</g, "\\u003c");

  const totals = {
    items: data.sources.reduce((sum, s) => sum + s.itemCount, 0),
    sections: data.sources.reduce((sum, s) => sum + s.sections.length, 0),
    resources: data.sources.reduce((sum, s) => sum + s.resourceCount, 0),
  };

  const cards = data.sources.map((source, index) => `
    <article class="page-card" data-page-card="${escHtml(source.key)}" style="--card-color:${escHtml(source.color)}">
      <div class="card-index">${String(index + 1).padStart(2, "0")}</div>
      <div class="card-body">
        <p class="card-kicker">${escHtml(source.label)} / ${escHtml(source.progressLabel)}</p>
        <h2>${escHtml(source.title)}</h2>
        <p>${escHtml(personalPurpose(source))}</p>
        <div class="card-stats">
          <span>${source.sections.length} sections</span>
          <span>${source.itemCount} ${escHtml(source.progressLabel)}</span>
          <span>${source.resourceCount} resources</span>
        </div>
        <div class="card-progress" aria-label="Progress for ${escHtml(source.title)}">
          <span data-page-progress-fill="${escHtml(source.key)}"></span>
        </div>
        <div class="card-footer">
          <span data-page-progress-text="${escHtml(source.key)}">0 / ${source.itemCount} complete</span>
          <a href="${escHtml(source.file)}">Open</a>
        </div>
      </div>
    </article>`).join("");

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Taran's personal learning hub for DSA, system design, CS fundamentals, behavioral interviews, AI engineering, and cloud.">
<title>Taran's Learning Hub</title>
<style>
:root {
  --bg: #f4f6f8;
  --surface: #ffffff;
  --surface-2: #edf1f5;
  --text: #151922;
  --muted: #586173;
  --faint: #818b9d;
  --border: #dce3ec;
  --strong: #202a3a;
  --accent: #2459d6;
  --shadow: 0 14px 36px rgba(31, 42, 63, .1);
  --shadow-lift: 0 22px 48px rgba(31, 42, 63, .16);
}
html.dark {
  --bg: #101319;
  --surface: #181d27;
  --surface-2: #232a37;
  --text: #edf1f7;
  --muted: #a2acbc;
  --faint: #737d90;
  --border: #303849;
  --strong: #f7f9fc;
  --accent: #7ca2ff;
  --shadow: 0 16px 42px rgba(0, 0, 0, .32);
  --shadow-lift: 0 24px 56px rgba(0, 0, 0, .44);
}
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  line-height: 1.5;
}
a { color: inherit; }
.wrap {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 28px 0 54px;
}
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 18px;
}
.brand h1 {
  margin: 0;
  font-size: clamp(28px, 5vw, 54px);
  letter-spacing: -0.02em;
  line-height: 1.02;
}
.brand p {
  margin: 8px 0 0;
  max-width: 760px;
  color: var(--muted);
  font-size: 15px;
}
.actions { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
.hub-btn {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  min-height: 40px;
  padding: 0 14px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 800;
  font-size: 13px;
  box-shadow: var(--shadow);
  transition: border-color .15s ease, transform .15s ease;
}
.hub-btn:hover { border-color: var(--accent); transform: translateY(-1px); }
.stats-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 0 0 16px;
}
.stat-chip {
  display: flex;
  flex-direction: column;
  min-width: 130px;
  flex: 1;
  padding: 12px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  box-shadow: var(--shadow);
}
.stat-chip b { font-size: 22px; font-variant-numeric: tabular-nums; }
.stat-chip span { color: var(--muted); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .07em; }
.overall-progress { height: 8px; border-radius: 999px; background: var(--surface-2); border: 1px solid var(--border); overflow: hidden; margin-top: 8px; }
.overall-progress i { display: block; height: 100%; width: 0; background: linear-gradient(90deg, #2f6fdd, #7b61d8, #d84f86); transition: width .4s ease; }
.search-block { position: relative; margin: 0 0 18px; }
.search-input {
  width: 100%;
  min-height: 48px;
  padding: 0 16px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--surface);
  color: var(--text);
  font-size: 15px;
  font-family: inherit;
  box-shadow: var(--shadow);
  outline: none;
}
.search-input:focus { border-color: var(--accent); }
.search-results {
  display: none;
  margin-top: 8px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--surface);
  box-shadow: var(--shadow-lift);
  max-height: 420px;
  overflow: auto;
}
.search-results.open { display: block; }
.search-results a {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 10px 14px;
  text-decoration: none;
  border-bottom: 1px solid var(--border);
  font-size: 14px;
}
.search-results a:last-child { border-bottom: none; }
.search-results a:hover { background: var(--surface-2); }
.sr-page {
  flex-shrink: 0;
  font-size: 10.5px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: .07em;
  color: #fff;
  background: var(--pill, var(--accent));
  border-radius: 999px;
  padding: 2px 8px;
}
.sr-section { margin-left: auto; color: var(--faint); font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 38%; }
.search-note { padding: 12px 14px; color: var(--muted); font-size: 13px; }
.review-panel {
  margin: 0 0 18px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  box-shadow: var(--shadow);
  overflow: hidden;
}
.review-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  cursor: pointer;
  user-select: none;
}
.review-head h2 { margin: 0; font-size: 16px; }
.review-head .count { color: var(--muted); font-size: 13px; font-weight: 800; }
.review-body { display: none; padding: 0 16px 14px; }
.review-panel.open .review-body { display: block; }
.review-group { margin-top: 10px; }
.review-group h3 { margin: 0 0 6px; font-size: 13px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }
.review-group a {
  display: inline-block;
  margin: 0 6px 6px 0;
  padding: 4px 10px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface-2);
  font-size: 12.5px;
  text-decoration: none;
}
.review-group a:hover { border-color: var(--accent); }
.review-empty { color: var(--muted); font-size: 13px; margin: 8px 0 0; }
.page-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.page-card {
  display: grid;
  grid-template-columns: 58px minmax(0, 1fr);
  min-height: 250px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 5px solid var(--card-color);
  border-radius: 10px;
  box-shadow: var(--shadow);
  overflow: hidden;
  transition: transform .18s ease, box-shadow .18s ease;
}
.page-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lift); }
.card-index {
  display: grid;
  place-items: start center;
  padding-top: 18px;
  background: color-mix(in srgb, var(--card-color) 13%, var(--surface-2));
  color: var(--card-color);
  font-weight: 900;
  font-size: 16px;
  font-variant-numeric: tabular-nums;
}
.card-body { padding: 18px 18px 16px; display: flex; flex-direction: column; min-width: 0; }
.card-kicker {
  margin: 0 0 8px;
  color: var(--card-color);
  text-transform: uppercase;
  letter-spacing: .1em;
  font-size: 11px;
  font-weight: 900;
}
.page-card h2 {
  margin: 0;
  font-size: clamp(20px, 3vw, 28px);
  line-height: 1.12;
  letter-spacing: -0.01em;
}
.page-card p {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 14px;
}
.card-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 14px;
}
.card-stats span {
  display: inline-flex;
  align-items: center;
  min-height: 25px;
  padding: 3px 8px;
  border-radius: 999px;
  background: var(--surface-2);
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
}
.card-progress {
  height: 9px;
  border: 1px solid var(--border);
  border-radius: 999px;
  overflow: hidden;
  margin-top: auto;
  background: var(--surface-2);
}
.card-progress span { display: block; width: 0; height: 100%; background: var(--card-color); transition: width .4s ease; }
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-top: 12px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
}
.card-footer a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 36px;
  padding: 0 14px;
  border-radius: 8px;
  background: var(--strong);
  color: var(--bg);
  text-decoration: none;
  white-space: nowrap;
  transition: opacity .15s ease, transform .15s ease;
}
.card-footer a:hover { opacity: .88; transform: translateY(-1px); }
@media (max-width: 820px) {
  .topbar { align-items: flex-start; }
  .page-grid { grid-template-columns: 1fr; }
  .page-card { grid-template-columns: 46px minmax(0, 1fr); min-height: 230px; }
}
@media (max-width: 520px) {
  .wrap { width: min(100% - 24px, 1180px); padding-top: 18px; }
  .topbar { flex-direction: column; }
  .actions { width: 100%; justify-content: stretch; }
  .hub-btn { flex: 1; }
  .card-footer { align-items: stretch; flex-direction: column; }
  .card-footer a { width: 100%; }
}
</style>
</head>
<body>
<script id="hub-data" type="application/json">${json}</script>
<main class="wrap">
  <div class="topbar">
    <section class="brand">
      <h1>Taran's Learning Hub</h1>
      <p>Six connected study spaces for my interview prep and engineering growth. Pick a page, follow the content inside it, and let progress/bookmarks stay local in this browser.</p>
    </section>
    <div class="actions">
      <button class="hub-btn" id="theme">Theme</button>
      <button class="hub-btn" id="export-progress" title="Download progress and bookmarks as JSON">Backup</button>
      <button class="hub-btn" id="import-progress" title="Restore progress from a backup file">Restore</button>
      <input type="file" id="import-file" accept="application/json" hidden>
    </div>
  </div>
  <section class="stats-strip" aria-label="Overall stats">
    <div class="stat-chip"><b id="total-done">0 / ${totals.items}</b><span>items complete</span><div class="overall-progress"><i id="total-fill"></i></div></div>
    <div class="stat-chip"><b>${data.sources.length}</b><span>study spaces</span></div>
    <div class="stat-chip"><b>${totals.sections}</b><span>sections</span></div>
    <div class="stat-chip"><b>${totals.resources}</b><span>resources</span></div>
  </section>
  <section class="search-block" aria-label="Global search">
    <input class="search-input" id="global-search" type="search" placeholder="Search all ${totals.items} topics and problems across every page…" autocomplete="off">
    <div class="search-results" id="search-results"></div>
  </section>
  <section class="review-panel" id="review-panel" aria-label="Bookmarked items">
    <div class="review-head" id="review-head">
      <h2>★ Review queue</h2>
      <span class="count" id="review-count">0 bookmarked</span>
    </div>
    <div class="review-body" id="review-body"></div>
  </section>
  <section class="page-grid" aria-label="Learning pages">
    ${cards}
  </section>
</main>
<script>
(function () {
  const data = JSON.parse(document.getElementById("hub-data").textContent);
  const themeKey = "learning_hub_theme_v2";
  function readSet(key) {
    try { return new Set(JSON.parse(localStorage.getItem(key) || "[]")); }
    catch (_e) { return new Set(); }
  }
  function applyTheme(theme) {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }
  applyTheme(localStorage.getItem(themeKey) || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
  document.getElementById("theme").addEventListener("click", function () {
    const next = document.documentElement.classList.contains("dark") ? "light" : "dark";
    localStorage.setItem(themeKey, next);
    applyTheme(next);
  });

  // Per-card progress + overall totals
  let doneTotal = 0;
  data.sources.forEach(function (source) {
    const done = readSet(source.storage.done).size;
    const safeDone = Math.min(done, source.itemCount);
    doneTotal += safeDone;
    const pct = source.itemCount ? Math.round((safeDone / source.itemCount) * 100) : 0;
    const fill = document.querySelector('[data-page-progress-fill="' + source.key + '"]');
    const text = document.querySelector('[data-page-progress-text="' + source.key + '"]');
    if (fill) fill.style.width = pct + "%";
    if (text) text.textContent = safeDone + " / " + source.itemCount + " complete";
  });
  const itemsTotal = data.sources.reduce(function (sum, s) { return sum + s.itemCount; }, 0);
  document.getElementById("total-done").textContent = doneTotal + " / " + itemsTotal;
  document.getElementById("total-fill").style.width = (itemsTotal ? Math.round(100 * doneTotal / itemsTotal) : 0) + "%";

  // Search index (lazy-loaded, shared by search + review queue)
  let indexPromise = null;
  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch("search-index.json").then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      });
    }
    return indexPromise;
  }
  const byKey = {};
  data.sources.forEach(function (s) { byKey[s.key] = s; });

  // Global search
  const input = document.getElementById("global-search");
  const results = document.getElementById("search-results");
  let searchToken = 0;
  function renderResults(list, query) {
    if (!list.length) {
      results.innerHTML = '<div class="search-note">No matches for "' + query.replace(/[<>&]/g, "") + '".</div>';
      results.classList.add("open");
      return;
    }
    results.innerHTML = list.slice(0, 40).map(function (item) {
      const src = byKey[item.k] || {};
      return '<a href="' + item.a + '" style="--pill:' + (src.color || "#888") + '">'
        + '<span class="sr-page">' + (src.label || item.k) + '</span>'
        + '<span>' + item.t.replace(/[<>&]/g, "") + '</span>'
        + '<span class="sr-section">' + (item.s || "").replace(/[<>&]/g, "") + '</span>'
        + '</a>';
    }).join("");
    results.classList.add("open");
  }
  input.addEventListener("input", function () {
    const q = input.value.trim().toLowerCase();
    const token = ++searchToken;
    if (q.length < 2) { results.classList.remove("open"); return; }
    loadIndex().then(function (index) {
      if (token !== searchToken) return;
      const hits = index.filter(function (item) {
        return item.t.toLowerCase().includes(q) || (item.s || "").toLowerCase().includes(q);
      });
      renderResults(hits, q);
    }).catch(function () {
      if (token !== searchToken) return;
      results.innerHTML = '<div class="search-note">Search needs the site to be served over HTTP (works on the live GitHub Pages site).</div>';
      results.classList.add("open");
    });
  });
  document.addEventListener("click", function (event) {
    if (!event.target.closest(".search-block")) results.classList.remove("open");
  });

  // Review queue (bookmarked items across all pages)
  const reviewPanel = document.getElementById("review-panel");
  const reviewBody = document.getElementById("review-body");
  const reviewCount = document.getElementById("review-count");
  const bookmarkSets = {};
  let bookmarkTotal = 0;
  data.sources.forEach(function (s) {
    const set = readSet(s.storage.bookmark);
    bookmarkSets[s.key] = set;
    bookmarkTotal += set.size;
  });
  reviewCount.textContent = bookmarkTotal + " bookmarked";
  document.getElementById("review-head").addEventListener("click", function () {
    const open = reviewPanel.classList.toggle("open");
    if (!open || reviewBody.dataset.loaded) return;
    if (!bookmarkTotal) {
      reviewBody.innerHTML = '<p class="review-empty">Nothing bookmarked yet. Use the ☆ star on any item to queue it for review.</p>';
      reviewBody.dataset.loaded = "1";
      return;
    }
    reviewBody.innerHTML = '<p class="review-empty">Loading…</p>';
    loadIndex().then(function (index) {
      const groups = data.sources.map(function (s) {
        const set = bookmarkSets[s.key];
        if (!set.size) return "";
        const links = index.filter(function (item) { return item.k === s.key && set.has(item.c); })
          .map(function (item) { return '<a href="' + item.a + '">' + item.t.replace(/[<>&]/g, "") + '</a>'; })
          .join("");
        if (!links) return "";
        return '<div class="review-group"><h3>' + s.title + " (" + set.size + ')</h3>' + links + "</div>";
      }).join("");
      reviewBody.innerHTML = groups || '<p class="review-empty">Bookmarked items could not be matched to the index. Rebuild the site to refresh the index.</p>';
      reviewBody.dataset.loaded = "1";
    }).catch(function () {
      reviewBody.innerHTML = '<p class="review-empty">The review queue needs the site to be served over HTTP (works on the live GitHub Pages site).</p>';
    });
  });

  // Progress backup / restore
  function progressKeys() {
    const keys = [themeKey, "hub_theme"];
    data.sources.forEach(function (s) {
      keys.push(s.storage.done, s.storage.bookmark);
    });
    return keys;
  }
  document.getElementById("export-progress").addEventListener("click", function () {
    const payload = { exportedAt: new Date().toISOString(), site: "taran-learning-hub", data: {} };
    progressKeys().forEach(function (key) {
      const value = localStorage.getItem(key);
      if (value !== null) payload.data[key] = value;
    });
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "learning-hub-progress-" + new Date().toISOString().slice(0, 10) + ".json";
    a.click();
    URL.revokeObjectURL(url);
  });
  const importFile = document.getElementById("import-file");
  document.getElementById("import-progress").addEventListener("click", function () { importFile.click(); });
  importFile.addEventListener("change", function () {
    const file = importFile.files && importFile.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function () {
      try {
        const payload = JSON.parse(String(reader.result));
        const entries = payload && payload.data ? payload.data : payload;
        const allowed = new Set(progressKeys());
        let applied = 0;
        Object.keys(entries || {}).forEach(function (key) {
          if (allowed.has(key) && typeof entries[key] === "string") {
            localStorage.setItem(key, entries[key]);
            applied += 1;
          }
        });
        alert(applied ? "Restored " + applied + " progress entries. Reloading." : "No matching progress entries found in that file.");
        if (applied) location.reload();
      } catch (_e) {
        alert("That file is not a valid progress backup.");
      }
    };
    reader.readAsText(file);
  });
})();
</script>
</body>
</html>
`;
}
