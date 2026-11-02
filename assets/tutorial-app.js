/* ==========================================================================
   Engineering Atlas Tutorial Engine for Taran's Learning Hub
   Powers System_Design_Tutorial, LLD_Tutorial, and Cloud_DevOps_Tutorial
   Inspired by https://engineering-atlas.in/

   Expects, before this script:
     window.TUTORIAL_CONFIG = { title, subtitle, icon, storageKey, navHtml, progressDomain, companionLink }
     window.topicsData      = [{ section, priority?, subsections:[{id,title,file,concepts:[{title,anchor}]}] }]
     window.contentBundle   = { "file.md": "markdown" }
   Renders into #am-root.
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
  function pad2(n) {
    return String(n < 10 ? '0' + n : n);
  }
  function chipClass(p) {
    var x = String(p || '').toLowerCase();
    if (x.indexOf('must') === 0) return 'must';
    if (x.indexOf('high') === 0) return 'high';
    if (x.indexOf('start') === 0) return 'start';
    if (x.indexOf('adv') === 0) return 'adv';
    return 'plain';
  }

  function splitTitle(value) {
    var s = String(value == null ? '' : value).trim();
    var m = s.match(/^(.*?)\s+[—–]\s+(.+)$/);
    if (!m) {
      m = s.match(/^([^:]{3,60}):\s+(.+)$/);
    }
    if (!m) return { short: s, detail: '' };
    var short = m[1].trim(), detail = m[2].trim();
    if (!short || short.length > 72) return { short: s, detail: '' };
    return { short: short, detail: detail.charAt(0).toUpperCase() + detail.slice(1) };
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

    // Atlas Special Pedagogical Blocks
    html = html.replace(/<blockquote>\s*<p>\[!(ANSWER30|30S|FASTRECALL)\]([\s\S]*?)<\/blockquote>/gi,
      function (match, type, content) {
        var clean = content.replace(/^(?:<br\s*\/?>|\n|\s)+/, '');
        return '<div class="answer30"><div class="answer30__label">In 30 Seconds (Fast Recall)</div>' + clean + '</div>';
      });

    html = html.replace(/<blockquote>\s*<p>\[!(SCOPE|REQUIREMENTS)\]([\s\S]*?)<\/blockquote>/gi,
      function (match, type, content) {
        var clean = content.replace(/^(?:<br\s*\/?>|\n|\s)+/, '');
        return '<div class="lblock lblock--scope"><div class="lblock__label">📋 System Scope & Requirements Checklist</div>' + clean + '</div>';
      });

    html = html.replace(/<blockquote>\s*<p>\[!(TRADEOFF|DECISION)\]([\s\S]*?)<\/blockquote>/gi,
      function (match, type, content) {
        var clean = content.replace(/^(?:<br\s*\/?>|\n|\s)+/, '');
        return '<div class="lblock lblock--try"><div class="lblock__label">⚖️ Architectural Trade-off & Decision</div>' + clean + '</div>';
      });

    html = html.replace(/<blockquote>\s*<p>\[!(LEARN|OBJECTIVES)\]([\s\S]*?)<\/blockquote>/gi,
      function (match, type, content) {
        var clean = content.replace(/^(?:<br\s*\/?>|\n|\s)+/, '');
        return '<div class="learn"><div class="learn__label">🎯 What You Will Master</div>' + clean + '</div>';
      });

    html = html.replace(/<blockquote>\s*<p>\[!(TIP|NOTE|WARNING|IMPORTANT|CAUTION)\]([\s\S]*?)<\/blockquote>/gi,
      function (match, type, content) {
        var t = type.toLowerCase();
        var icon = t === 'note' ? 'ℹ️' : t === 'warning' ? '⚠️' : t === 'important' ? '🔥' : t === 'caution' ? '🛑' : '💡';
        var clean = content.replace(/^(?:<br\s*\/?>|\n|\s)+/, '');
        return '<div class="alert alert-' + t + '"><div class="alert-header"><span>' + icon + '</span><span>' + t.toUpperCase() +
          '</span></div><div class="alert-content">' + clean + '</div></div>';
      });
    return window.DOMPurify ? DOMPurify.sanitize(html, { ADD_ATTR: ['id', 'target', 'rel', 'class', 'data-video-id', 'data-sr', 'data-done'] }) : html;
  }

  function enhanceArticle(article) {
    article.querySelectorAll('a[href^="http"]').forEach(function (a) {
      a.target = '_blank'; a.rel = 'noopener noreferrer';
    });
    // Wrap tables in .tablewrap for responsive scroll and Atlas styling
    article.querySelectorAll('table').forEach(function (tbl) {
      if (tbl.parentElement && tbl.parentElement.classList.contains('tablewrap')) return;
      var wrap = document.createElement('div');
      wrap.className = 'tablewrap';
      tbl.parentNode.insertBefore(wrap, tbl);
      wrap.appendChild(tbl);
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
          typeof mermaid !== "undefined" && mermaid.run();
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

    // Compute stats
    var totalLessons = flat.length;
    var completedLessons = flat.filter(function (it) { return isDone(it); }).length;
    var pct = Math.round((completedLessons / (totalLessons || 1)) * 100);

    var companionBanner = '';
    if (CFG.companionLink) {
      companionBanner = '<div class="am-companion-card">' +
        '<div>' +
          '<div class="am-companion-tag">' + esc(CFG.companionLink.tag || 'Companion Guide') + '</div>' +
          '<div class="am-companion-title">' + esc(CFG.companionLink.title || '') + '</div>' +
          '<div class="am-companion-desc">' + esc(CFG.companionLink.desc || '') + '</div>' +
        '</div>' +
        '<a href="' + esc(CFG.companionLink.href) + '" class="am-btn primary" style="white-space:nowrap">' +
          esc(CFG.companionLink.label || 'Open Companion →') + '</a>' +
      '</div>';
    }

    var html = '<div class="am-hero">' +
      '<div class="atlas-badge">📚 Atlas Curriculum Track</div>' +
      '<h1>' + esc(CFG.title || 'Curriculum') + '</h1>' +
      '<p>' + esc(CFG.subtitle || '') + '</p>' +
      '<div class="atlas-stats-bar">' +
        '<span class="atlas-stat-pill"><b>' + topics.length + '</b> Modules</span>' +
        '<span class="atlas-stat-pill"><b>' + totalLessons + '</b> Lessons</span>' +
        '<span class="atlas-stat-pill"><b>' + completedLessons + '</b> Completed</span>' +
        '<span class="atlas-stat-pill"><b>' + pct + '%</b> Progress</span>' +
      '</div>' +
    '</div>' +
    companionBanner +
    '<div class="am-filters">' +
      '<div class="am-field"><label for="am-q">Search Topics</label>' +
        '<input id="am-q" type="search" placeholder="Search by topic, keyword, or module…" value="' + esc(filters.q) + '"></div>' +
      '<div class="am-field"><label for="am-status">Status</label><select id="am-status">' +
        ['all', 'todo', 'done'].map(function (v) {
          var label = v === 'all' ? 'All Lessons' : v === 'todo' ? 'Not Started' : 'Completed';
          return '<option value="' + v + '"' + (filters.status === v ? ' selected' : '') + '>' + label + '</option>';
        }).join('') +
      '</select></div>' +
      '<div class="am-spacer"></div>' +
      '<button class="am-btn" type="button" id="am-expand">Expand all</button>' +
      '<button class="am-btn" type="button" id="am-collapse">Collapse all</button>' +
    '</div>';

    var any = false;
    topics.forEach(function (section, secIdx) {
      var rows = [];
      var secTotal = 0;
      var secDone = 0;

      section.subsections.forEach(function (sub) {
        var md = (window.contentBundle || {})[sub.file] || '';
        sub.concepts.forEach(function (concept) {
          secTotal++;
          var item = flat.find(function (f) { return f.pageId === sub.id && f.conceptId === concept.anchor; });
          var done = item ? isDone(item) : false;
          if (done) secDone++;

          if (filters.status === 'todo' && done) return;
          if (filters.status === 'done' && !done) return;
          if (q && (concept.title + ' ' + section.section + ' ' + sub.title).toLowerCase().indexOf(q) === -1) return;

          var parts = splitTitle(concept.title);
          var detail = parts.detail || firstLine(md, concept.anchor);
          rows.push('<a class="am-row' + (done ? ' done' : '') + '" href="#' + sub.id + '/' + concept.anchor + '"' +
            ' data-short-title="' + esc(parts.short) + '">' +
            '<button class="am-check' + (done ? ' on' : '') + '" type="button" data-done="' + esc(sub.id + '/' + concept.anchor) + '" ' +
              'title="Mark as completed" aria-label="Mark ' + esc(parts.short) + ' as completed">✓</button>' +
            '<span class="am-title">' + esc(parts.short) + '</span>' +
            '<span class="am-sub">' + esc(detail) + '</span>' +
            '</a>');
        });
      });

      if (!rows.length) return;
      any = true;

      html += '<details class="am-section" open>' +
        '<summary>' +
          '<span class="cn-module__no">' + pad2(secIdx + 1) + '</span>' +
          '<div class="cn-module__head">' +
            '<h2>' + esc(section.section) + '</h2>' +
          '</div>' +
          '<div class="cn-module__meta">' +
            (section.priority ? '<span class="am-chip ' + chipClass(section.priority) + '">' + esc(section.priority) + '</span>' : '') +
            '<span class="cn-module__count">' + secDone + '/' + secTotal + ' done</span>' +
            '<span class="am-section-chevron">▾</span>' +
          '</div>' +
        '</summary>' +
        '<div class="am-rows">' +
          '<div class="am-topic-guide-rail">' + rows.join('') + '</div>' +
        '</div>' +
      '</details>';
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
  function sidebarHtml(current, filterText) {
    var sq = (filterText || '').toLowerCase().trim();
    return topics.map(function (section, secIdx) {
      var links = [];
      var secTotal = 0;
      var secDone = 0;

      section.subsections.forEach(function (sub) {
        sub.concepts.forEach(function (concept) {
          secTotal++;
          var item = flat.find(function (f) { return f.pageId === sub.id && f.conceptId === concept.anchor; });
          var done = item ? isDone(item) : false;
          if (done) secDone++;

          if (sq && (concept.title + ' ' + section.section).toLowerCase().indexOf(sq) === -1) {
            return;
          }

          var cls = 'am-side-link' + (done ? ' studied' : '') +
            (current && current.pageId === sub.id && current.conceptId === concept.anchor ? ' active' : '');
          var sp = splitTitle(concept.title);
          links.push('<a class="' + cls + '" href="#' + sub.id + '/' + concept.anchor + '" title="' + esc(concept.title) + '">' + esc(sp.short) + '</a>');
        });
      });

      if (sq && !links.length) return '';

      var open = Boolean(sq) || section.subsections.some(function (sub) { return current && sub.id === current.pageId; });
      return '<details class="am-side-mod"' + (open ? ' open' : '') + '>' +
        '<summary>' +
          '<span class="am-side-mod-no">' + pad2(secIdx + 1) + '</span>' +
          '<span class="am-side-mod-t">' + esc(section.section) + '</span>' +
          '<span class="am-side-mod-subcount">' + secDone + '/' + secTotal + '</span>' +
        '</summary>' +
        '<div class="am-side-sublinks">' + links.join('') + '</div>' +
      '</details>';
    }).join('');
  }

  function getLessonResources(item) {
    var out = { videos: [], docs: [] };
    var store = window.sdResources || window.aiResources || window.cloudDevOpsResources || window.roadmapResources;
    var file = item.file;
    var parent = file && store && store.lessons && store.lessons[file];
    var conceptKey = item.pageId + '/' + item.conceptId;
    var hit = store && store.concepts && store.concepts[conceptKey];

    var vids = (hit && hit.videos && hit.videos.length) ? hit.videos.slice() : (parent && parent.videos ? parent.videos.slice() : []);
    var docs = (hit && hit.docs && hit.docs.length) ? hit.docs.slice() : (parent && parent.docs ? parent.docs.slice() : []);

    // Also pull links from markdown content
    var md = (window.contentBundle || {})[file] || "";
    if (md) {
      var start = 0, end = md.length;
      var heads = [], re = /^##\s+.*$/gm, m;
      while ((m = re.exec(md))) heads.push({ i: m.index, t: m[0] });
      for (var j = 0; j < heads.length; j++) {
        var slug = heads[j].t.replace(/^#+\s+/, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
        if (slug === item.conceptId) {
          start = heads[j].i;
          end = heads[j + 1] ? heads[j + 1].i : md.length;
          break;
        }
      }
      var body = start >= 0 ? md.slice(start, end) : md;
      var linkRe = /\[([^\]]*)\]\((https?:\/\/[^\s)]+)\)|(?:^|\s)(https?:\/\/[^\s)<]+)/g, l;
      while ((l = linkRe.exec(body))) {
        var href = l[2] || l[3], label = (l[1] || "").trim() || "Reference Document";
        if (!href || href.indexOf("youtube.com/results") !== -1 || href.indexOf("google.com/search") !== -1) continue;
        var ytMatch = href.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([\w-]{11})/);
        if (ytMatch) {
          var yId = ytMatch[1];
          if (!vids.some(function (v) { return v[0] === yId; })) {
            vids.push([yId, label, "YouTube Walkthrough"]);
          }
        } else {
          if (!docs.some(function (d) { return d[1] === href; })) {
            docs.push([label, href]);
          }
        }
      }
    }
    return { videos: vids, docs: docs };
  }

  function chapterView(item) {
    var idx = flat.indexOf(item);
    var prev = flat[idx - 1], next = flat[idx + 1];
    var done = isDone(item);

    var totalLessons = flat.length;
    var completedLessons = flat.filter(function (it) { return isDone(it); }).length;
    var pct = Math.round((completedLessons / (totalLessons || 1)) * 100);

    var prevShort = prev ? splitTitle(prev.conceptTitle).short : '';
    var nextShort = next ? splitTitle(next.conceptTitle).short : '';
    var parts = splitTitle(item.conceptTitle);

    var res = getLessonResources(item);
    var subj = location.pathname.indexOf('LLD') !== -1 ? 'low level design' : (location.pathname.indexOf('Cloud') !== -1 ? 'cloud devops' : 'system design');
    var q = encodeURIComponent(parts.short + ' ' + subj);
    var ytSearchUrl = 'https://www.youtube.com/results?search_query=' + q;
    var gSearchUrl = 'https://www.google.com/search?q=' + q;

    var resourceBarHtml =
      '<div class="am-lesson-resources">' +
        '<div class="am-res-badge"><span>Course Companion Resources</span></div>' +
        '<div class="am-res-actions">' +
          (res.videos.length ?
            '<button class="study-link youtube" type="button" id="am-watch-btn" title="Watch ' + res.videos.length + ' video(s) in side panel">' +
              'Watch Lecture <span class="sr-count">' + res.videos.length + '</span>' +
            '</button>' :
            '<a class="study-link youtube icon-only yt-search" href="' + ytSearchUrl + '" target="_blank" rel="noopener" title="Search YouTube: ' + esc(parts.short) + '">⌕</a>'
          ) +
          (res.docs.length ?
            '<button class="study-link read" type="button" id="am-read-btn" title="Read ' + res.docs.length + ' article(s) in side panel">' +
              'Read Docs <span class="sr-count">' + res.docs.length + '</span>' +
            '</button>' : ''
          ) +
          '<a class="study-link youtube yt-search" href="' + ytSearchUrl + '" target="_blank" rel="noopener">⌕ Search YouTube</a>' +
          '<a class="study-link google" href="' + gSearchUrl + '" target="_blank" rel="noopener">Google Topic</a>' +
        '</div>' +
      '</div>';

    root.innerHTML =
      '<div class="am-layout">' +
        '<aside class="am-side" id="am-side">' +
          '<div class="am-side-head">' +
            '<b>' + esc(CFG.title ? CFG.title.split(' ')[0] + ' Track' : 'Curriculum') + '</b>' +
            '<a href="#" class="am-btn" style="padding:4px 9px;font-size:.74rem">Overview</a>' +
          '</div>' +
          '<div class="am-side-search-wrap">' +
            '<input type="search" placeholder="Filter lessons…" class="am-side-search" id="am-side-q">' +
          '</div>' +
          '<div class="am-side-progress">' +
            '<div class="am-side-progress-meta">' +
              '<span>Progress</span>' +
              '<span id="am-side-pct">' + completedLessons + '/' + totalLessons + ' (' + pct + '%)</span>' +
            '</div>' +
            '<div class="am-side-progress-track">' +
              '<div class="am-side-progress-fill" id="am-side-bar" style="width:' + pct + '%"></div>' +
            '</div>' +
          '</div>' +
          '<div id="am-side-list">' + sidebarHtml(item) + '</div>' +
        '</aside>' +
        '<div class="am-main">' +
          '<div class="am-chapter-head">' +
            '<button class="am-btn am-icon-btn am-side-toggle" type="button" id="am-side-btn" aria-label="Open curriculum">☰</button>' +
            '<div class="am-crumb">' +
              '<span>' + esc(item.sectionTitle) + '</span>' +
              '<span>&rsaquo;</span>' +
              '<b>' + esc(parts.short) + '</b>' +
            '</div>' +
            '<span class="am-spacer"></span>' +
            '<button class="am-btn' + (done ? ' is-done' : '') + '" type="button" id="am-done">' + (done ? '✓ Completed' : 'Mark Completed') + '</button>' +
          '</div>' +
          resourceBarHtml +
          '<article class="am-article am-fade" id="am-article"><div class="am-loading">Loading content…</div></article>' +
          '<div class="am-pager">' +
            (prev ?
              '<a class="am-pager-card am-pager-prev" href="#' + prev.pageId + '/' + prev.conceptId + '">' +
                '<span class="am-pager-dir">← Previous Topic</span>' +
                '<span class="am-pager-title">' + esc(prevShort) + '</span>' +
              '</a>' :
              '<div class="am-pager-card am-pager-prev disabled">' +
                '<span class="am-pager-dir">← Previous Topic</span>' +
                '<span class="am-pager-title">Start of Curriculum</span>' +
              '</div>'
            ) +
            (next ?
              '<a class="am-pager-card am-pager-next" href="#' + next.pageId + '/' + next.conceptId + '">' +
                '<span class="am-pager-dir">Next Topic →</span>' +
                '<span class="am-pager-title">' + esc(nextShort) + '</span>' +
              '</a>' :
              '<div class="am-pager-card am-pager-next disabled">' +
                '<span class="am-pager-dir">Next Topic →</span>' +
                '<span class="am-pager-title">End of Curriculum</span>' +
              '</div>'
            ) +
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

      if (res.videos.length || res.docs.length) {
        var gridCards = [];
        res.videos.forEach(function (v) {
          var vId = v[0], vTitle = v[1] || 'Video Lecture Walkthrough', vAuthor = v[2] ? 'By ' + v[2] : 'Verified Lecture';
          gridCards.push(
            '<a class="am-resource-card video-card" href="https://www.youtube.com/watch?v=' + vId + '" data-video-id="' + vId + '" target="_blank" rel="noopener">' +
              '<div class="am-res-type video">🎥 Video Lecture</div>' +
              '<div class="am-res-title">' + esc(vTitle) + '</div>' +
              '<div class="am-res-author">' + esc(vAuthor) + '</div>' +
            '</a>'
          );
        });
        res.docs.forEach(function (d) {
          var dTitle = d[0] || 'Reference Documentation', dHref = d[1];
          gridCards.push(
            '<a class="am-resource-card doc-card" href="' + dHref + '" target="_blank" rel="noopener">' +
              '<div class="am-res-type doc">📄 Deep-Dive Reading</div>' +
              '<div class="am-res-title">' + esc(dTitle) + '</div>' +
              '<div class="am-res-author">Documentation / Architecture Guide</div>' +
            '</a>'
          );
        });
        if (gridCards.length) {
          var resSec = document.createElement('div');
          resSec.className = 'am-resources-section';
          resSec.innerHTML = '<h3><span>📚 Curated Study Materials & Video Walkthroughs</span></h3>' +
            '<div class="am-resources-grid">' + gridCards.join('') + '</div>';
          article.appendChild(resSec);
        }
      }
    }

    var wBtn = document.getElementById('am-watch-btn');
    if (wBtn) {
      wBtn.addEventListener('click', function () {
        if (window.VideoPanel) {
          window.VideoPanel.open({
            title: parts.short,
            query: parts.short + ' ' + subj,
            videos: res.videos,
            anim: [],
            docs: res.docs,
            tab: 'videos',
            originEl: wBtn
          });
        } else {
          window.open(ytSearchUrl, '_blank', 'noopener');
        }
      });
    }

    var rBtn = document.getElementById('am-read-btn');
    if (rBtn) {
      rBtn.addEventListener('click', function () {
        if (window.VideoPanel) {
          window.VideoPanel.open({
            title: parts.short,
            query: parts.short + ' ' + subj,
            videos: res.videos,
            anim: [],
            docs: res.docs,
            tab: 'read',
            originEl: rBtn
          });
        }
      });
    }

    article.querySelectorAll('.video-card').forEach(function (card) {
      card.addEventListener('click', function (e) {
        if (window.VideoPanel) {
          e.preventDefault();
          var vId = card.getAttribute('data-video-id');
          window.VideoPanel.open({
            title: parts.short,
            query: parts.short + ' ' + subj,
            videos: res.videos,
            anim: [],
            docs: res.docs,
            tab: 'videos',
            originEl: card
          });
          if (vId) window.VideoPanel.openVideo(vId);
        }
      });
    });

    // Sidebar search filter event
    var sideQ = document.getElementById('am-side-q');
    if (sideQ) {
      sideQ.addEventListener('input', function () {
        var list = document.getElementById('am-side-list');
        if (list) list.innerHTML = sidebarHtml(item, sideQ.value);
      });
    }

    document.getElementById('am-done').addEventListener('click', function (e) {
      toggleDone(item);
      var nowDone = isDone(item);
      e.currentTarget.classList.toggle('is-done', nowDone);
      e.currentTarget.textContent = nowDone ? '✓ Completed' : 'Mark Completed';

      var cDone = flat.filter(function (it) { return isDone(it); }).length;
      var cPct = Math.round((cDone / (totalLessons || 1)) * 100);
      var pctEl = document.getElementById('am-side-pct');
      var barEl = document.getElementById('am-side-bar');
      if (pctEl) pctEl.textContent = cDone + '/' + totalLessons + ' (' + cPct + '%)';
      if (barEl) barEl.style.width = cPct + '%';

      var list = document.getElementById('am-side-list');
      if (list) list.innerHTML = sidebarHtml(item, sideQ ? sideQ.value : '');
    });

    var sideBtn = document.getElementById('am-side-btn');
    if (sideBtn) sideBtn.addEventListener('click', function () { document.getElementById('am-side').classList.toggle('open'); });
    root.querySelectorAll('.am-side-link').forEach(function (a) {
      a.addEventListener('click', function () {
        if (window.innerWidth <= 1040) document.getElementById('am-side').classList.remove('open');
      });
    });

    scrollToConcept(item);
    var active = root.querySelector('.am-side-link.active');
    if (active) active.scrollIntoView({ block: 'nearest' });
  }

  function scrollToConcept(item) {
    var anchor = item && item.conceptId;
    if (!anchor) { window.scrollTo({ top: 0 }); return; }
    var el = document.getElementById(anchor);
    var article = document.getElementById('am-article');
    var heads = article ? Array.prototype.slice.call(article.querySelectorAll('h1, h2, h3')) : [];
    if (!el) {
      var clean = anchor.replace(/-/g, '');
      el = heads.find(function (h) {
        var id = h.id.replace(/-/g, '');
        return id.length > 3 && (clean.indexOf(id) !== -1 || id.indexOf(clean) !== -1);
      });
    }
    if (!el && article) {
      var override = (window.tutorialAnchorTargets || {})[item.file + '#' + anchor];
      if (override) el = heads.find(function (h) {
        var textSlug = h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        return textSlug === override;
      });
    }
    if (!el && article) {
      var title = splitTitle(item.conceptTitle).short.toLowerCase();
      var candidates = Array.prototype.slice.call(article.querySelectorAll('h2, h3, h4, p, li, td'));
      el = candidates.find(function (node) { return node.textContent.toLowerCase().indexOf(title) !== -1; });
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
    var saved = localStorage.getItem('learning_hub_theme') || localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    var btn = document.getElementById('am-theme');
    if (btn) btn.addEventListener('click', function () {
      var cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', cur);
      localStorage.setItem('learning_hub_theme', cur);
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
