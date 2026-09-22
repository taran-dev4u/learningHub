/* ==========================================================================
   VideoPanel v2 — a resizable right-side study panel, in-page.
   Tabs:  ▶ Videos  ·  🎬 Animated  ·  📄 Read   (+ Google search, always)
   - Videos / Animated play YouTube embeds with a thumbnail playlist.
   - Read shows solutions and articles inside the panel:
       GitHub markdown  -> fetched raw and rendered (marked + DOMPurify)
       GitHub code file -> fetched raw and shown with highlighting
       sites that allow framing -> iframe
       everything else  -> a card with "Open in new tab" + Google
   Self-contained: no hard dependencies. Exposes window.VideoPanel.

   VideoPanel.open({ title, videos, anim, docs:[[label,url],...], query, tab, docIndex, index })
   VideoPanel.close()
   Also intercepts plain clicks on YouTube links and on readable doc links
   (Ctrl/Cmd/Shift-click still opens the site normally).
   ========================================================================== */
(function () {
  'use strict';
  if (window.VideoPanel) return;

  var W_KEY = 'video_panel_width_v1';
  var MIN_W = 340, MAX_FRAC = 0.8;
  // Hosts verified to allow being shown inside another page.
  var FRAME_HOSTS = [
    'walkccc.me', 'leetcode.doocs.org', 'neetcode.io', 'java-design-patterns.com', 'docs.oracle.com',
    'docs.python.org', 'en.wikipedia.org', 'genai.owasp.org', 'sre.google', 'pages.cs.wisc.edu',
    'www.allthingsdistributed.com', 'static.googleusercontent.com'
  ];
  var CDN = {
    marked: 'https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js',
    purify: 'https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.6/purify.min.js'
  };
  var el, frame, list, titleEl, kickerEl, openLink, moreLink, googleLink, tabsEl, videoView, readView, docsEl, viewer;
  var state = { videos: [], anim: [], docs: [], tab: 'videos', idx: 0, title: '', query: '', doc: -1 };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function isMobile() { return window.innerWidth < 900; }
  function savedWidth() {
    var w = 0;
    try { w = parseInt(localStorage.getItem(W_KEY), 10) || 0; } catch (e) {}
    if (!w) w = Math.round(window.innerWidth * 0.42);
    return Math.max(MIN_W, Math.min(w, Math.round(window.innerWidth * MAX_FRAC)));
  }
  function applyWidth(w) {
    if (!el) return;
    if (isMobile()) {
      el.style.width = '';
      document.documentElement.style.removeProperty('--vp-offset');
      return;
    }
    el.style.width = w + 'px';
    if (el.classList.contains('vp-open')) document.documentElement.style.setProperty('--vp-offset', w + 'px');
  }
  function googleUrl(q) { return 'https://www.google.com/search?q=' + encodeURIComponent(q || ''); }

  /* ---------- doc classification ---------- */
  function docKind(href) {
    var u;
    try { u = new URL(href, location.href); } catch (e) { return { kind: 'link' }; }
    var h = u.hostname, p = u.pathname.split('/').filter(Boolean);
    if (h === 'github.com' && p.length >= 5 && p[2] === 'blob') {
      var raw = 'https://raw.githubusercontent.com/' + p[0] + '/' + p[1] + '/' + p.slice(3).join('/');
      return { kind: /\.(md|markdown)$/i.test(u.pathname) ? 'md' : 'code', raw: raw, repo: p[0] + '/' + p[1], branch: p[3], dir: p.slice(4, -1).join('/') };
    }
    if (h === 'github.com' && p.length === 2) {
      return { kind: 'md', raw: 'https://raw.githubusercontent.com/' + p[0] + '/' + p[1] + '/HEAD/README.md', repo: p[0] + '/' + p[1], branch: 'HEAD', dir: '' };
    }
    if (h === 'raw.githubusercontent.com' && p.length >= 4) {
      return { kind: /\.(md|markdown)$/i.test(u.pathname) ? 'md' : 'code', raw: u.href, repo: p[0] + '/' + p[1], branch: p[2], dir: p.slice(3, -1).join('/') };
    }
    if (u.protocol === 'https:' && FRAME_HOSTS.indexOf(h) >= 0) return { kind: 'frame', src: u.href };
    return { kind: 'link' };
  }
  function readable(href) { return docKind(href).kind !== 'link'; }
  function hostOf(href) { try { return new URL(href, location.href).hostname.replace(/^www\./, ''); } catch (e) { return ''; } }

  function loadScript(src) {
    return new Promise(function (res, rej) {
      var s = document.createElement('script');
      s.src = src; s.async = true; s.onload = res; s.onerror = rej;
      document.head.appendChild(s);
    });
  }
  var libs = null;
  function ensureLibs() {
    if (window.marked && window.DOMPurify) return Promise.resolve();
    if (!libs) libs = Promise.all([
      window.marked ? 0 : loadScript(CDN.marked),
      window.DOMPurify ? 0 : loadScript(CDN.purify)
    ]);
    return libs;
  }

  /* ---------- build ---------- */
  function build() {
    if (el) return;
    el = document.createElement('aside');
    el.className = 'vp-panel';
    el.setAttribute('aria-label', 'Study panel');
    el.innerHTML =
      '<div class="vp-resize" title="Drag to resize" aria-hidden="true"></div>' +
      '<div class="vp-head">' +
        '<div class="vp-titles"><span class="vp-kicker">▶ Watch</span><b class="vp-title"></b></div>' +
        '<div class="vp-actions">' +
          '<a class="vp-btn vp-google" target="_blank" rel="noopener noreferrer" title="Search Google for this topic">G</a>' +
          '<button type="button" class="vp-btn vp-size" data-size="s" title="Narrow">⇤</button>' +
          '<button type="button" class="vp-btn vp-size" data-size="l" title="Wide">⇥</button>' +
          '<a class="vp-btn vp-open-yt" target="_blank" rel="noopener noreferrer" title="Open in a new tab">↗</a>' +
          '<button type="button" class="vp-btn vp-close" title="Close (Esc)" aria-label="Close panel">✕</button>' +
        '</div>' +
      '</div>' +
      '<div class="vp-tabs" role="tablist"></div>' +
      '<div class="vp-video-view">' +
        '<div class="vp-player"><iframe class="vp-frame" title="YouTube video player" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>' +
        '<div class="vp-list-head"><span>More videos on this topic</span></div>' +
        '<div class="vp-list"></div>' +
        '<a class="vp-more" target="_blank" rel="noopener noreferrer">Search YouTube for more ↗</a>' +
      '</div>' +
      '<div class="vp-read-view" hidden>' +
        '<div class="vp-docs"></div>' +
        '<div class="vp-viewer"></div>' +
      '</div>';
    document.body.appendChild(el);
    frame = el.querySelector('.vp-frame');
    list = el.querySelector('.vp-list');
    titleEl = el.querySelector('.vp-title');
    kickerEl = el.querySelector('.vp-kicker');
    openLink = el.querySelector('.vp-open-yt');
    moreLink = el.querySelector('.vp-more');
    googleLink = el.querySelector('.vp-google');
    tabsEl = el.querySelector('.vp-tabs');
    videoView = el.querySelector('.vp-video-view');
    readView = el.querySelector('.vp-read-view');
    docsEl = el.querySelector('.vp-docs');
    viewer = el.querySelector('.vp-viewer');

    el.querySelector('.vp-close').addEventListener('click', close);
    el.querySelectorAll('.vp-size').forEach(function (b) {
      b.addEventListener('click', function () {
        var w = b.dataset.size === 's' ? Math.round(window.innerWidth * 0.30) : Math.round(window.innerWidth * 0.6);
        w = Math.max(MIN_W, Math.min(w, Math.round(window.innerWidth * MAX_FRAC)));
        try { localStorage.setItem(W_KEY, String(w)); } catch (e) {}
        applyWidth(w);
      });
    });
    list.addEventListener('click', function (e) {
      var item = e.target.closest('[data-vp-i]');
      if (item) play(parseInt(item.dataset.vpI, 10));
    });
    tabsEl.addEventListener('click', function (e) {
      var t = e.target.closest('[data-vp-tab]');
      if (t) setTab(t.dataset.vpTab);
    });
    docsEl.addEventListener('click', function (e) {
      var d = e.target.closest('[data-vp-doc]');
      if (d) showDoc(parseInt(d.dataset.vpDoc, 10));
    });

    var handle = el.querySelector('.vp-resize');
    handle.addEventListener('pointerdown', function (e) {
      if (isMobile()) return;
      e.preventDefault();
      handle.setPointerCapture(e.pointerId);
      el.classList.add('vp-dragging');
      function move(ev) {
        var w = Math.round(window.innerWidth - ev.clientX);
        applyWidth(Math.max(MIN_W, Math.min(w, Math.round(window.innerWidth * MAX_FRAC))));
      }
      function up() {
        handle.releasePointerCapture(e.pointerId);
        handle.removeEventListener('pointermove', move);
        handle.removeEventListener('pointerup', up);
        el.classList.remove('vp-dragging');
        try { localStorage.setItem(W_KEY, String(parseInt(el.style.width, 10))); } catch (err) {}
      }
      handle.addEventListener('pointermove', move);
      handle.addEventListener('pointerup', up);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && el.classList.contains('vp-open')) close();
    });
    window.addEventListener('resize', function () { if (el.classList.contains('vp-open')) applyWidth(savedWidth()); });
  }

  /* ---------- tabs ---------- */
  function renderTabs() {
    var tabs = [
      ['videos', '▶ Videos', state.videos.length],
      ['anim', '🎬 Animated', state.anim.length],
      ['read', '📄 Read', state.docs.length]
    ];
    tabsEl.innerHTML = tabs.map(function (t) {
      return '<button type="button" role="tab" class="vp-tab' + (state.tab === t[0] ? ' active' : '') + (t[2] ? '' : ' empty') +
        '" data-vp-tab="' + t[0] + '" aria-selected="' + (state.tab === t[0]) + '">' + t[1] + ' <span>' + t[2] + '</span></button>';
    }).join('') +
      '<a class="vp-tab vp-tab-google" target="_blank" rel="noopener noreferrer" href="' + esc(googleUrl(state.query)) + '" title="Google: ' + esc(state.query) + '">Google ↗</a>';
  }
  function curVideos() { return state.tab === 'anim' ? state.anim : state.videos; }

  function setTab(tab) {
    state.tab = tab;
    renderTabs();
    var isRead = tab === 'read';
    videoView.hidden = isRead;
    readView.hidden = !isRead;
    kickerEl.textContent = tab === 'anim' ? '🎬 Animated' : isRead ? '📄 Read' : '▶ Watch';
    if (isRead) {
      frame.src = 'about:blank';
      renderDocs();
      showDoc(state.doc >= 0 ? state.doc : 0);
      return;
    }
    viewer.innerHTML = '';
    var vids = curVideos();
    el.querySelector('.vp-list-head').style.display = vids.length > 1 ? '' : 'none';
    moreLink.href = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(state.query + (tab === 'anim' ? ' animation visualized' : ''));
    if (!vids.length) {
      frame.src = 'about:blank';
      list.innerHTML = '<div class="vp-empty"><b>No ' + (tab === 'anim' ? 'animated' : '') + ' videos picked for this topic yet.</b>' +
        '<p>Search YouTube for an animated explanation instead:</p>' +
        '<a class="vp-cta" target="_blank" rel="noopener noreferrer" href="' + esc(moreLink.href) + '">🎬 “' + esc(state.query) + '” animation ↗</a></div>';
      el.querySelector('.vp-player').style.display = 'none';
      openLink.removeAttribute('href');
      return;
    }
    el.querySelector('.vp-player').style.display = '';
    renderList();
    play(tab === 'videos' ? Math.min(state.idx, vids.length - 1) : 0);
  }

  function renderList() {
    list.innerHTML = curVideos().map(function (v, i) {
      return '<button type="button" class="vp-item" data-vp-i="' + i + '">' +
        '<span class="vp-thumb"><img loading="lazy" alt="" src="https://i.ytimg.com/vi/' + esc(v[0]) + '/mqdefault.jpg">' +
        (v[3] ? '<span class="vp-dur">' + esc(v[3]) + '</span>' : '') + '</span>' +
        '<span class="vp-meta"><span class="vp-vt">' + esc(v[1] || 'Video') + '</span>' +
        '<span class="vp-ch">' + esc(v[2] || '') + '</span></span></button>';
    }).join('');
  }

  function play(i) {
    var v = curVideos()[i];
    if (!v) return;
    if (state.tab === 'videos') state.idx = i;
    frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(v[0]) + '?autoplay=1&rel=0&modestbranding=1';
    openLink.href = 'https://www.youtube.com/watch?v=' + encodeURIComponent(v[0]);
    openLink.title = 'Open this video on YouTube';
    list.querySelectorAll('.vp-item').forEach(function (b, k) { b.classList.toggle('active', k === i); });
  }

  /* ---------- reader ---------- */
  function renderDocs() {
    if (!state.docs.length) { docsEl.innerHTML = ''; return; }
    docsEl.innerHTML = state.docs.map(function (d, i) {
      var k = docKind(d[1]).kind;
      var icon = k === 'md' || k === 'code' ? '🐙' : k === 'frame' ? '📄' : '↗';
      return '<button type="button" class="vp-doc' + (i === state.doc ? ' active' : '') + '" data-vp-doc="' + i + '" title="' + esc(d[1]) + '">' +
        '<span class="vp-doc-i">' + icon + '</span><span class="vp-doc-l">' + esc(d[0]) + '</span><span class="vp-doc-h">' + esc(hostOf(d[1])) + '</span></button>';
    }).join('');
  }

  function fallback(d, note) {
    viewer.innerHTML = '<div class="vp-fallback">' +
      '<div class="vp-fb-host">' + esc(hostOf(d[1])) + '</div>' +
      '<h3>' + esc(d[0]) + '</h3>' +
      '<p>' + esc(note || 'This site does not allow being shown inside another page, so it opens in a new tab.') + '</p>' +
      '<div class="vp-fb-actions">' +
        '<a class="vp-cta" href="' + esc(d[1]) + '" target="_blank" rel="noopener noreferrer">Open in new tab ↗</a>' +
        '<a class="vp-cta ghost" href="' + esc(googleUrl(state.query)) + '" target="_blank" rel="noopener noreferrer">Search Google ↗</a>' +
      '</div></div>';
  }

  function absolutize(root, info, docUrl) {
    var rawBase = 'https://raw.githubusercontent.com/' + info.repo + '/' + info.branch + '/' + (info.dir ? info.dir + '/' : '');
    var ghBase = 'https://github.com/' + info.repo + '/blob/' + info.branch + '/' + (info.dir ? info.dir + '/' : '');
    root.querySelectorAll('img[src]').forEach(function (im) {
      var s = im.getAttribute('src');
      if (!/^(https?:|data:)/i.test(s)) { try { im.src = new URL(s, rawBase).href; } catch (e) {} }
      im.loading = 'lazy';
    });
    root.querySelectorAll('a[href]').forEach(function (a) {
      var h = a.getAttribute('href');
      if (h.charAt(0) === '#') return;
      if (!/^(https?:|mailto:)/i.test(h)) { try { a.href = new URL(h, ghBase).href.replace('/blob/' + info.branch + '/', /\/$/.test(h) ? '/tree/' + info.branch + '/' : '/blob/' + info.branch + '/'); } catch (e) {} }
      a.target = '_blank'; a.rel = 'noopener noreferrer';
    });
  }

  function showDoc(i) {
    var d = state.docs[i];
    viewer.innerHTML = '';
    if (!d) {
      viewer.innerHTML = '<div class="vp-fallback"><h3>No direct solution or article saved for this card yet.</h3><p>Search Google for a write-up:</p>' +
        '<div class="vp-fb-actions"><a class="vp-cta" href="' + esc(googleUrl(state.query)) + '" target="_blank" rel="noopener noreferrer">Search Google ↗</a></div></div>';
      return;
    }
    state.doc = i;
    docsEl.querySelectorAll('.vp-doc').forEach(function (b, k) { b.classList.toggle('active', k === i); });
    openLink.href = d[1];
    openLink.title = 'Open in a new tab';
    var info = docKind(d[1]);
    if (info.kind === 'frame') {
      viewer.innerHTML = '<iframe class="vp-doc-frame" title="' + esc(d[0]) + '" referrerpolicy="no-referrer" sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-forms"></iframe>' +
        '<div class="vp-frame-note">Not loading? <a href="' + esc(d[1]) + '" target="_blank" rel="noopener noreferrer">Open in new tab ↗</a></div>';
      viewer.querySelector('iframe').src = info.src;
      return;
    }
    if (info.kind === 'link') { fallback(d); return; }
    viewer.innerHTML = '<div class="vp-loading">Loading from GitHub…</div>';
    var token = {};
    showDoc.token = token;
    Promise.all([fetch(info.raw).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); }), info.kind === 'md' ? ensureLibs() : 0])
      .then(function (res) {
        if (showDoc.token !== token) return;
        var text = res[0];
        var wrap = document.createElement('div');
        wrap.className = 'vp-md';
        if (info.kind === 'md') {
          var html = window.marked.parse ? window.marked.parse(text) : window.marked(text);
          wrap.innerHTML = window.DOMPurify.sanitize(html, { ADD_ATTR: ['target'] });
          absolutize(wrap, info, d[1]);
        } else {
          var ext = (info.raw.match(/\.([a-z0-9+]+)$/i) || [])[1] || '';
          var lang = { py: 'python', java: 'java', cpp: 'cpp', js: 'javascript', ts: 'typescript', go: 'go', cs: 'csharp', kt: 'kotlin' }[ext] || ext;
          wrap.innerHTML = '<div class="vp-code-head"><b>' + esc(info.raw.split('/').pop()) + '</b><span>' + esc(info.repo) + '</span></div><pre><code class="language-' + esc(lang) + '"></code></pre>';
          wrap.querySelector('code').textContent = text;
        }
        wrap.insertAdjacentHTML('beforeend', '<p class="vp-src">Source: <a href="' + esc(d[1]) + '" target="_blank" rel="noopener noreferrer">' + esc(d[1].replace(/^https:\/\//, '')) + ' ↗</a></p>');
        viewer.innerHTML = '';
        viewer.appendChild(wrap);
        viewer.scrollTop = 0;
        if (window.hljs) wrap.querySelectorAll('pre code').forEach(function (c) { try { window.hljs.highlightElement(c); } catch (e) {} });
      })
      .catch(function () {
        if (showDoc.token !== token) return;
        fallback(d, 'Could not load this page inside the panel right now.');
      });
  }

  /* ---------- open / close ---------- */
  function clean(v) { return (v || []).filter(function (x) { return x && x[0]; }); }
  function open(opts) {
    build();
    opts = opts || {};
    state.videos = clean(opts.videos);
    state.anim = clean(opts.anim);
    state.docs = (opts.docs || []).filter(function (x) { return x && x[1]; });
    state.title = opts.title || '';
    state.query = opts.query || opts.title || '';
    state.idx = Math.max(0, opts.index || 0);
    state.doc = opts.docIndex == null ? -1 : opts.docIndex;
    if (!state.videos.length && !state.anim.length && !state.docs.length) return false;
    var tab = opts.tab || (state.videos.length ? 'videos' : state.anim.length ? 'anim' : 'read');
    titleEl.textContent = state.title;
    titleEl.title = state.title;
    googleLink.href = googleUrl(state.query);
    googleLink.title = 'Google: ' + state.query;
    el.classList.add('vp-open');
    document.documentElement.classList.add('vp-active');
    applyWidth(savedWidth());
    setTab(tab);
    return true;
  }

  function close() {
    if (!el) return;
    el.classList.remove('vp-open');
    document.documentElement.classList.remove('vp-active');
    document.documentElement.style.removeProperty('--vp-offset');
    frame.src = 'about:blank';
    viewer.innerHTML = '';
  }

  function ytId(href) {
    try {
      var u = new URL(href, location.href);
      var h = u.hostname.replace(/^www\.|^m\./, '');
      if (h === 'youtu.be') return u.pathname.slice(1).split('/')[0] || null;
      if (h === 'youtube.com' || h === 'youtube-nocookie.com') {
        if (u.pathname === '/watch') return u.searchParams.get('v');
        var m = u.pathname.match(/^\/(?:embed|shorts|live)\/([^/?#]+)/);
        if (m) return m[1];
      }
    } catch (e) {}
    return null;
  }

  // Topic = nearest H1/H2 above the link inside an article.
  function topicFor(a, scope) {
    var topic = a.dataset.vtopic || '';
    var n = scope && scope.closest('article') ? scope : null;
    while (n && !topic) {
      var prev = n.previousElementSibling;
      while (prev && !/^H[12]$/.test(prev.tagName)) prev = prev.previousElementSibling;
      if (prev) topic = prev.textContent.trim(); else n = n.parentElement && n.parentElement.tagName !== 'ARTICLE' ? n.parentElement : null;
    }
    return topic;
  }
  // Videos listed under a heading containing "Animated" go to the Animated tab.
  function isAnimList(scope) {
    var p = scope && scope.previousElementSibling;
    while (p && !/^H[1-4]$/.test(p.tagName)) p = p.previousElementSibling;
    return !!(p && /animat/i.test(p.textContent));
  }
  function collectVideos(scope) {
    var vids = [];
    (scope ? scope.querySelectorAll('a[href]') : []).forEach(function (x) {
      var xid = ytId(x.getAttribute('href'));
      if (!xid || vids.some(function (v) { return v[0] === xid; })) return;
      var ch = x.dataset.vchannel || '', dur = x.dataset.vdur || '';
      var li = x.closest('li');
      if (li && !ch) {
        var m = li.textContent.slice(li.textContent.indexOf(x.textContent) + x.textContent.length).match(/[—-]\s*(.+?)\s*·\s*(\d{1,2}:\d{2}(?::\d{2})?)/);
        if (m) { ch = m[1]; dur = m[2]; }
      }
      vids.push([xid, (x.dataset.vtitle || x.textContent || '').replace(/^[\s▶🎬]+/, '').trim(), ch, dur]);
    });
    return vids;
  }
  // Within an article section (between two H2s), find the sibling video/animated/doc lists.
  function sectionLists(a) {
    var art = a.closest('article');
    if (!art) return null;
    var top = a;
    while (top.parentElement && top.parentElement !== art) top = top.parentElement;
    if (top.parentElement !== art) return null;
    var h = top; while (h && !/^H[12]$/.test(h.tagName)) h = h.previousElementSibling;
    var out = { videos: [], anim: [], docs: [] }, n = h ? h.nextElementSibling : art.firstElementChild;
    while (n && !(n !== top && /^H[12]$/.test(n.tagName))) {
      if (/^(UL|OL)$/.test(n.tagName)) {
        var v = collectVideos(n);
        if (v.length) (isAnimList(n) ? out.anim : out.videos).push.apply(isAnimList(n) ? out.anim : out.videos, v);
        n.querySelectorAll('a[href]').forEach(function (x) {
          var hr = x.href;
          if (ytId(hr) || /google\.[a-z.]+\/search|youtube\.com\/results/.test(hr) || x.hostname === location.hostname) return;
          if (!out.docs.some(function (d) { return d[1] === hr; })) out.docs.push([x.textContent.trim().replace(/^[\s📄🐙↗]+/, ''), hr]);
        });
      }
      n = n.nextElementSibling;
    }
    return out;
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.closest('.vp-panel, nav, header, [data-no-panel]') || a.hasAttribute('data-no-panel')) return;
    var href = a.getAttribute('href');
    var id = ytId(href);
    var isDoc = !id && readable(href);
    if (!id && !isDoc) return;
    e.preventDefault();
    var scope = a.closest('[data-video-scope], ul, ol, .rm-links, .card-actions') || a.parentElement;
    var sec = sectionLists(a);
    var topic = topicFor(a, scope);
    var vids, anim = [], docs = [], start = 0, tab, docIndex = 0;
    if (sec) { vids = sec.videos; anim = sec.anim; docs = sec.docs; }
    else {
      vids = id ? collectVideos(scope) : [];
      if (scope) scope.querySelectorAll('a[href]').forEach(function (x) {
        if (!ytId(x.getAttribute('href')) && readable(x.getAttribute('href')) && !docs.some(function (d) { return d[1] === x.href; })) docs.push([x.textContent.trim(), x.href]);
      });
    }
    if (id) {
      var inAnim = anim.some(function (v) { return v[0] === id; });
      var arr = inAnim ? anim : vids;
      if (!arr.some(function (v) { return v[0] === id; })) arr.unshift([id, a.textContent.trim(), '', '']);
      arr.forEach(function (v, k) { if (v[0] === id) start = k; });
      tab = inAnim ? 'anim' : 'videos';
    } else {
      if (!docs.some(function (d) { return d[1] === a.href; })) docs.unshift([a.textContent.trim(), a.href]);
      docs.forEach(function (d, k) { if (d[1] === a.href) docIndex = k; });
      tab = 'read';
    }
    var title = topic || (id ? (vids[start] && vids[start][1]) : a.textContent.trim()) || 'Study';
    open({ title: title, videos: vids, anim: anim, docs: docs, index: tab === 'videos' ? start : 0, docIndex: docIndex, tab: tab, query: a.dataset.vquery || title });
    if (tab === 'anim' && start) play(start);
  }, true);

  window.VideoPanel = { open: open, close: close, ytId: ytId, readable: readable };
})();
