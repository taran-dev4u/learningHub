/* ==========================================================================
   Shared tutorial engine (AlgoMaster-style) for Taran's Learning Hub
   Used by System_Design_Tutorial and LLD_Tutorial.

   Expects, before this script:
     window.TUTORIAL_CONFIG = { title, subtitle, icon, storageKey, navHtml }
     window.topicsData      = [{ section, priority?, subsections:[{id,title,file,concepts:[{title,anchor}]}] }]
     window.contentBundle   = { "file.md": "markdown" }
   Renders into #am-root. No counters, no percentages — ticks only.
   ========================================================================== */
(function () {
  'use strict';

  var CFG = window.TUTORIAL_CONFIG || {};
  var DONE_KEY = CFG.storageKey || 'hub_done_tutorial';
  var root, topics = [], flat = [], loadedFile = null;

  /* ---------------- storage ---------------- */
  function readSet(key) {
    if (window.LearningHubShared) return window.LearningHubShared.readSet(key);
    try { return new Set(JSON.parse(localStorage.getItem(key) || '[]')); } catch (e) { return new Set(); }
  }
  function writeSet(key, set) {
    if (window.LearningHubShared) window.LearningHubShared.writeSet(key, set);
    else { try { localStorage.setItem(key, JSON.stringify(Array.from(set))); } catch (e) {} }
  }
  var studied = readSet(DONE_KEY);
  var titleToCid = new Map();

  function normalizeTitle(v) {
    if (window.LearningHubShared) return window.LearningHubShared.normalizeTitle(v);
    return String(v || '').toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, ' ').replace(/\s+/g, ' ').trim();
  }

  // Keeps ticks in sync with the main hub pages when a domain is configured.
  function loadHubProgressMap() {
    if (!CFG.progressDomain) return Promise.resolve();
    return fetch('../learning-hub-data.json', { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data) return;
        (data.items || []).forEach(function (item) {
          if (item.domain === CFG.progressDomain) titleToCid.set(normalizeTitle(item.title), item.key);
        });
      })
      .catch(function () { titleToCid = new Map(); });
  }

  function conceptKey(c) {
    var matched = titleToCid.get(normalizeTitle(c && c.conceptTitle));
    return matched || ('tutorial:' + c.pageId + '/' + c.conceptId);
  }
  function isDone(c) { return studied.has(conceptKey(c)); }
  function toggleDone(c) {
    studied = readSet(DONE_KEY);
    var k = conceptKey(c);
    if (studied.has(k)) studied.delete(k); else studied.add(k);
    writeSet(DONE_KEY, studied);
  }

  /* ---------------- helpers ---------------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function chipClass(p) {
    var x = String(p || '').toLowerCase();
    if (x.indexOf('must') === 0) return 'must';
    if (x.indexOf('high') === 0) return 'high';
    if (x.indexOf('start') === 0) return 'start';
    if (x.indexOf('adv') === 0) return 'adv';
    return 'plain';
  }
  function firstLine(md, anchor) {
    if (!md) return '';
    var re = new RegExp('^##\\s+.*$', 'gm'), m, idx = -1, next = md.length;
    var heads = [];
    while ((m = re.exec(md))) heads.push({ i: m.index, t: m[0] });
    for (var j = 0; j < heads.length; j++) {
      var slug = heads[j].t.replace(/^##\s+/, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
      if (slug === anchor) { idx = heads[j].i; next = heads[j + 1] ? heads[j + 1].i : md.length; break; }
    }
    if (idx < 0) return '';
    var body = md.slice(idx, next);
    var why = body.match(/\*\*(?:Why it matters|Requirements to clarify):\*\*\s*([^\n]+)/);
    if (why) return why[1].replace(/[*`\[\]]/g, '').slice(0, 130);
    var para = body.split('\n').slice(1).find(function (l) { return l.trim() && !l.startsWith('>') && !l.startsWith('#'); });
    return para ? para.replace(/[*`\[\]]/g, '').slice(0, 130) : '';
  }

  /* ---------------- markdown ---------------- */
  function setupMarked() {
    if (!window.marked) return;
    var renderer = new marked.Renderer();
    renderer.heading = function () {
      var a = arguments, text = '', level = 1;
      if (a.length === 1 && typeof a[0] === 'object') { text = a[0].text || a[0].raw; level = a[0].depth; }
      else { text = a[0]; level = a[1]; }
      var id = String(text).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
      return '<h' + level + ' id="' + id + '">' + text + '</h' + level + '>';
    };
    marked.setOptions({
      renderer: renderer,
      highlight: function (code, lang) {
        if (!window.hljs) return code;
        var language = hljs.getLanguage(lang) ? lang : 'plaintext';
        try { return hljs.highlight(code, { language: language }).value; } catch (e) { return code; }
      },
      langPrefix: 'hljs language-'
    });
  }

  function renderMarkdown(md) {
    var processed = md.replace(/([A-Za-z0-9_]+)\^([A-Za-z0-9_]+)/g, '$1<sup>$2</sup>');
    var html = window.marked ? marked.parse(processed) : esc(processed);
    html = html.replace(/<blockquote>\s*<p>\[!(TIP|NOTE|WARNING|IMPORTANT|CAUTION)\]([\s\S]*?)<\/p>\s*<\/blockquote>/gi,
      function (match, type, content) {
        var t = type.toLowerCase();
        var icon = t === 'note' ? 'ℹ️' : t === 'warning' ? '⚠️' : t === 'important' ? '🔥' : t === 'caution' ? '🛑' : '💡';
        var clean = content.replace(/^(?:<br\s*\/?>|\n|\s)+/, '');
        return '<div class="alert alert-' + t + '"><div class="alert-header"><span>' + icon + '</span><span>' + t.toUpperCase() +
          '</span></div><div class="alert-content">' + clean + '</div></div>';
      });
    return window.DOMPurify ? DOMPurify.sanitize(html, { ADD_ATTR: ['id', 'target', 'rel'] }) : html;
  }

  function enhanceArticle(article) {
    article.querySelectorAll('a[href^="http"]').forEach(function (a) {
      a.target = '_blank'; a.rel = 'noopener noreferrer';
    });
    article.querySelectorAll('pre').forEach(function (pre) {
      if (pre.querySelector('.am-copy')) return;
      var b = document.createElement('button');
      b.className = 'am-copy'; b.type = 'button'; b.textContent = 'Copy';
      b.addEventListener('click', function () {
        var code = pre.querySelector('code');
        navigator.clipboard.writeText(code ? code.innerText : pre.innerText).then(function () {
          b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1400);
        }).catch(function () {});
      });
      pre.appendChild(b);
    });
    try {
      if (window.mermaid) {
        var blocks = article.querySelectorAll('code.language-mermaid');
        if (blocks.length) {
          blocks.forEach(function (el) {
            var pre = el.parentElement;
            if (pre && pre.tagName === 'PRE') {
              var div = document.createElement('div');
              div.className = 'mermaid';
              div.style.textAlign = 'center';
              div.style.margin = '1.6rem 0';
              div.textContent = el.textContent;
              pre.replaceWith(div);
            }
          });
          mermaid.run();
        }
      }
    } catch (e) { /* diagrams are optional */ }
  }

  /* ---------------- data ---------------- */
  function buildFlat() {
    flat = [];
    topics.forEach(function (section) {
      section.subsections.forEach(function (sub) {
        sub.concepts.forEach(function (concept) {
          flat.push({
            sectionTitle: section.section,
            priority: section.priority || '',
            pageId: sub.id, pageTitle: sub.title, file: sub.file,
            conceptId: concept.anchor, conceptTitle: concept.title
          });
        });
      });
    });
  }

  /* ---------------- home view ---------------- */
  var filters = { q: '', status: 'all' };

  function homeView() {
    var q = filters.q.toLowerCase();
    var html = '<div class="am-hero"><h1>' + esc(CFG.title || 'Curriculum') + '</h1><p>' + esc(CFG.subtitle || '') + '</p></div>' +
      '<div class="am-filters">' +
        '<div class="am-field"><label for="am-q">Search</label>' +
          '<input id="am-q" type="search" placeholder="Search topics…" value="' + esc(filters.q) + '"></div>' +
        '<div class="am-field"><label for="am-status">Status</label><select id="am-status">' +
          ['all', 'todo', 'done'].map(function (v) {
            var label = v === 'all' ? 'All' : v === 'todo' ? 'Not started' : 'Completed';
            return '<option value="' + v + '"' + (filters.status === v ? ' selected' : '') + '>' + label + '</option>';
          }).join('') +
        '</select></div>' +
        '<div class="am-spacer"></div>' +
        '<button class="am-btn" type="button" id="am-expand">Expand all</button>' +
        '<button class="am-btn" type="button" id="am-collapse">Collapse all</button>' +
      '</div>';

    var any = false;
    topics.forEach(function (section) {
      var rows = [];
      section.subsections.forEach(function (sub) {
        var md = (window.contentBundle || {})[sub.file] || '';
        sub.concepts.forEach(function (concept) {
          var item = flat.find(function (f) { return f.pageId === sub.id && f.conceptId === concept.anchor; });
          var done = item ? isDone(item) : false;
          if (filters.status === 'todo' && done) return;
          if (filters.status === 'done' && !done) return;
          if (q && (concept.title + ' ' + section.section + ' ' + sub.title).toLowerCase().indexOf(q) === -1) return;
          rows.push('<a class="am-row' + (done ? ' done' : '') + '" href="#' + sub.id + '/' + concept.anchor + '">' +
            '<button class="am-check' + (done ? ' on' : '') + '" type="button" data-done="' + esc(sub.id + '/' + concept.anchor) + '" ' +
              'title="Mark as completed" aria-label="Mark ' + esc(concept.title) + ' as completed">✓</button>' +
            '<span class="am-title">' + esc(concept.title) + '</span>' +
            '<span class="am-sub">' + esc(firstLine(md, concept.anchor)) + '</span></a>');
        });
      });
      if (!rows.length) return;
      any = true;
      html += '<details class="am-section" open><summary><h2>' + esc(section.section) + '</h2>' +
        (section.priority ? '<span class="am-chip ' + chipClass(section.priority) + '">' + esc(section.priority) + '</span>' : '') +
        '</summary><div class="am-rows">' + rows.join('') + '</div></details>';
    });
    if (!any) html += '<div class="am-section"><div class="am-empty">No topics match that search.</div></div>';
    root.innerHTML = html;

    var qi = document.getElementById('am-q');
    qi.addEventListener('input', function () {
      filters.q = qi.value;
      var pos = qi.selectionStart;
      homeView();
      var ni = document.getElementById('am-q');
      ni.focus(); try { ni.setSelectionRange(pos, pos); } catch (e) {}
    });
    document.getElementById('am-status').addEventListener('change', function (e) {
      filters.status = e.target.value; homeView();
    });
    document.getElementById('am-expand').addEventListener('click', function () {
      root.querySelectorAll('details.am-section').forEach(function (d) { d.open = true; });
    });
    document.getElementById('am-collapse').addEventListener('click', function () {
      root.querySelectorAll('details.am-section').forEach(function (d) { d.open = false; });
    });
    root.querySelectorAll('[data-done]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        var parts = btn.dataset.done.split('/');
        var item = flat.find(function (f) { return f.pageId === parts[0] && f.conceptId === parts[1]; });
        if (!item) return;
        toggleDone(item);
        btn.classList.toggle('on');
        btn.closest('.am-row').classList.toggle('done');
      });
    });
    window.scrollTo({ top: 0 });
  }

  /* ---------------- chapter view ---------------- */
  function sidebarHtml(current) {
    return topics.map(function (section) {
      var links = [];
      section.subsections.forEach(function (sub) {
        sub.concepts.forEach(function (concept) {
          var item = flat.find(function (f) { return f.pageId === sub.id && f.conceptId === concept.anchor; });
          var cls = 'am-side-link' + (item && isDone(item) ? ' studied' : '') +
            (current && current.pageId === sub.id && current.conceptId === concept.anchor ? ' active' : '');
          links.push('<a class="' + cls + '" href="#' + sub.id + '/' + concept.anchor + '">' + esc(concept.title) + '</a>');
        });
      });
      var open = section.subsections.some(function (sub) { return current && sub.id === current.pageId; });
      return '<details' + (open ? ' open' : '') + '><summary>' + esc(section.section) + '</summary>' + links.join('') + '</details>';
    }).join('');
  }

  function chapterView(item) {
    var idx = flat.indexOf(item);
    var prev = flat[idx - 1], next = flat[idx + 1];
    var done = isDone(item);
    root.innerHTML =
      '<div class="am-layout">' +
        '<aside class="am-side" id="am-side">' +
          '<div class="am-side-head"><b>Curriculum</b><a href="#" class="am-btn" style="padding:5px 9px;font-size:.76rem">All topics</a></div>' +
          sidebarHtml(item) +
        '</aside>' +
        '<div class="am-main">' +
          '<div class="am-chapter-head">' +
            '<button class="am-btn am-icon-btn am-side-toggle" type="button" id="am-side-btn" aria-label="Open curriculum">☰</button>' +
            '<span class="am-crumb">' + esc(item.sectionTitle) + ' &rsaquo; <b>' + esc(item.conceptTitle) + '</b></span>' +
            '<span class="am-spacer"></span>' +
            '<button class="am-btn' + (done ? ' is-done' : '') + '" type="button" id="am-done">' + (done ? '✓ Completed' : 'Mark completed') + '</button>' +
          '</div>' +
          '<article class="am-article am-fade" id="am-article"><div class="am-loading">Loading…</div></article>' +
          '<div class="am-pager">' +
            '<button class="am-btn" type="button" id="am-prev"' + (prev ? '' : ' disabled') + '>← ' + esc(prev ? prev.conceptTitle : 'Start') + '</button>' +
            '<button class="am-btn primary" type="button" id="am-next"' + (next ? '' : ' disabled') + '>' + esc(next ? next.conceptTitle : 'End') + ' →</button>' +
          '</div>' +
        '</div>' +
      '</div>';

    var article = document.getElementById('am-article');
    var md = (window.contentBundle || {})[item.file];
    if (!md) {
      article.innerHTML = '<div class="am-empty"><h2>Content not found</h2><p>Missing file: <code>' + esc(item.file) + '</code></p></div>';
    } else {
      article.innerHTML = renderMarkdown(md);
      enhanceArticle(article);
      loadedFile = item.file;
    }

    document.getElementById('am-done').addEventListener('click', function (e) {
      toggleDone(item);
      var nowDone = isDone(item);
      e.currentTarget.classList.toggle('is-done', nowDone);
      e.currentTarget.textContent = nowDone ? '✓ Completed' : 'Mark completed';
      document.getElementById('am-side').innerHTML =
        '<div class="am-side-head"><b>Curriculum</b><a href="#" class="am-btn" style="padding:5px 9px;font-size:.76rem">All topics</a></div>' + sidebarHtml(item);
    });
    if (prev) document.getElementById('am-prev').addEventListener('click', function () { location.hash = prev.pageId + '/' + prev.conceptId; });
    if (next) document.getElementById('am-next').addEventListener('click', function () { location.hash = next.pageId + '/' + next.conceptId; });
    var sideBtn = document.getElementById('am-side-btn');
    if (sideBtn) sideBtn.addEventListener('click', function () { document.getElementById('am-side').classList.toggle('open'); });
    root.querySelectorAll('.am-side-link').forEach(function (a) {
      a.addEventListener('click', function () {
        if (window.innerWidth <= 1000) document.getElementById('am-side').classList.remove('open');
      });
    });

    scrollToConcept(item.conceptId);
    var active = root.querySelector('.am-side-link.active');
    if (active) active.scrollIntoView({ block: 'nearest' });
  }

  function scrollToConcept(anchor) {
    if (!anchor) { window.scrollTo({ top: 0 }); return; }
    var el = document.getElementById(anchor);
    if (!el) {
      var heads = Array.prototype.slice.call(document.querySelectorAll('#am-article h1, #am-article h2, #am-article h3'));
      var clean = anchor.replace(/-/g, '');
      el = heads.find(function (h) {
        var id = h.id.replace(/-/g, '');
        return id.length > 3 && (clean.indexOf(id) !== -1 || id.indexOf(clean) !== -1);
      });
    }
    if (el) el.scrollIntoView({ block: 'start' });
    else window.scrollTo({ top: 0 });
  }

  /* ---------------- routing ---------------- */
  function route() {
    studied = readSet(DONE_KEY);
    var hash = location.hash.replace(/^#/, '');
    if (!hash) { homeView(); return; }
    var parts = hash.split('/');
    var item = flat.find(function (f) { return f.pageId === parts[0] && f.conceptId === parts[1]; }) ||
               flat.find(function (f) { return f.pageId === parts[0]; });
    if (!item) { homeView(); return; }
    chapterView(item);
  }

  /* ---------------- theme ---------------- */
  function initTheme() {
    var saved = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    var btn = document.getElementById('am-theme');
    if (btn) btn.addEventListener('click', function () {
      var cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', cur);
      localStorage.setItem('theme', cur);
    });
  }

  /* ---------------- boot ---------------- */
  document.addEventListener('DOMContentLoaded', function () {
    root = document.getElementById('am-root');
    if (!root) return;
    topics = window.topicsData || [];
    setupMarked();
    initTheme();
    buildFlat();
    route();
    loadHubProgressMap().then(function () { if (titleToCid.size) route(); });
    window.addEventListener('hashchange', route);
    window.addEventListener('learning-hub-progress-updated', function (e) {
      if (!e.detail || e.detail.key !== DONE_KEY) return;
      studied = readSet(DONE_KEY);
    });
  });
})();
