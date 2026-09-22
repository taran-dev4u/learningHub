/* ==========================================================================
   VideoPanel — watch YouTube videos in a resizable side panel, in-page.
   Self-contained: no dependencies. Exposes window.VideoPanel.

   VideoPanel.open({ title, videos:[[id, title, channel, duration], ...], index, query })
   VideoPanel.close()
   Also intercepts plain clicks on youtube.com/watch and youtu.be links
   (Ctrl/Cmd/Shift-click still opens YouTube normally).
   ========================================================================== */
(function () {
  'use strict';
  if (window.VideoPanel) return;

  var W_KEY = 'video_panel_width_v1';
  var MIN_W = 340, MAX_FRAC = 0.78;
  var el, frame, list, titleEl, openLink, moreLink, state = { videos: [], idx: 0, title: '', query: '' };

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

  function build() {
    if (el) return;
    el = document.createElement('aside');
    el.className = 'vp-panel';
    el.setAttribute('aria-label', 'Video player');
    el.innerHTML =
      '<div class="vp-resize" title="Drag to resize" aria-hidden="true"></div>' +
      '<div class="vp-head">' +
        '<div class="vp-titles"><span class="vp-kicker">▶ Watch</span><b class="vp-title"></b></div>' +
        '<div class="vp-actions">' +
          '<button type="button" class="vp-btn vp-size" data-size="s" title="Narrow">⇤</button>' +
          '<button type="button" class="vp-btn vp-size" data-size="l" title="Wide">⇥</button>' +
          '<a class="vp-btn vp-open-yt" target="_blank" rel="noopener noreferrer" title="Open this video on YouTube">↗</a>' +
          '<button type="button" class="vp-btn vp-close" title="Close (Esc)" aria-label="Close video panel">✕</button>' +
        '</div>' +
      '</div>' +
      '<div class="vp-player"><iframe class="vp-frame" title="YouTube video player" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>' +
      '<div class="vp-list-head"><span>More videos on this topic</span></div>' +
      '<div class="vp-list"></div>' +
      '<a class="vp-more" target="_blank" rel="noopener noreferrer">Search YouTube for more ↗</a>';
    document.body.appendChild(el);
    frame = el.querySelector('.vp-frame');
    list = el.querySelector('.vp-list');
    titleEl = el.querySelector('.vp-title');
    openLink = el.querySelector('.vp-open-yt');
    moreLink = el.querySelector('.vp-more');

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
      if (!item) return;
      play(parseInt(item.dataset.vpI, 10));
    });

    // drag to resize (desktop)
    var handle = el.querySelector('.vp-resize');
    handle.addEventListener('pointerdown', function (e) {
      if (isMobile()) return;
      e.preventDefault();
      handle.setPointerCapture(e.pointerId);
      el.classList.add('vp-dragging');
      function move(ev) {
        var w = Math.round(window.innerWidth - ev.clientX);
        w = Math.max(MIN_W, Math.min(w, Math.round(window.innerWidth * MAX_FRAC)));
        applyWidth(w);
      }
      function up(ev) {
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

  function renderList() {
    list.innerHTML = state.videos.map(function (v, i) {
      return '<button type="button" class="vp-item' + (i === state.idx ? ' active' : '') + '" data-vp-i="' + i + '">' +
        '<span class="vp-thumb"><img loading="lazy" alt="" src="https://i.ytimg.com/vi/' + esc(v[0]) + '/mqdefault.jpg">' +
        (v[3] ? '<span class="vp-dur">' + esc(v[3]) + '</span>' : '') + '</span>' +
        '<span class="vp-meta"><span class="vp-vt">' + esc(v[1] || 'Video') + '</span>' +
        '<span class="vp-ch">' + esc(v[2] || '') + '</span></span></button>';
    }).join('');
  }

  function play(i) {
    var v = state.videos[i];
    if (!v) return;
    state.idx = i;
    frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(v[0]) + '?autoplay=1&rel=0&modestbranding=1';
    openLink.href = 'https://www.youtube.com/watch?v=' + encodeURIComponent(v[0]);
    list.querySelectorAll('.vp-item').forEach(function (b, k) { b.classList.toggle('active', k === i); });
  }

  function open(opts) {
    build();
    opts = opts || {};
    state.videos = (opts.videos || []).filter(function (v) { return v && v[0]; });
    state.title = opts.title || '';
    state.query = opts.query || opts.title || '';
    if (!state.videos.length) return false;
    titleEl.textContent = state.title;
    moreLink.href = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(state.query);
    el.querySelector('.vp-list-head').style.display = state.videos.length > 1 ? '' : 'none';
    renderList();
    el.classList.add('vp-open');
    document.documentElement.classList.add('vp-active');
    applyWidth(savedWidth());
    play(Math.max(0, Math.min(opts.index || 0, state.videos.length - 1)));
    return true;
  }

  function close() {
    if (!el) return;
    el.classList.remove('vp-open');
    document.documentElement.classList.remove('vp-active');
    document.documentElement.style.removeProperty('--vp-offset');
    frame.src = 'about:blank';
  }

  // Parse a YouTube URL into a video id.
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

  // Any plain click on a YouTube video link opens it in the panel.
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.closest('.vp-panel') || a.hasAttribute('data-no-panel')) return;
    var id = ytId(a.getAttribute('href'));
    if (!id) return;
    e.preventDefault();
    // Sibling YouTube links in the same block become the playlist.
    var scope = a.closest('[data-video-scope], ul, ol, .rm-links, .card-actions') || a.parentElement;
    var vids = [], start = 0;
    (scope ? scope.querySelectorAll('a[href]') : [a]).forEach(function (x) {
      var xid = ytId(x.getAttribute('href'));
      if (!xid || vids.some(function (v) { return v[0] === xid; })) return;
      if (x === a) start = vids.length;
      // "Title — Channel · 12:34" written after the link in a list item
      var ch = x.dataset.vchannel || '', dur = x.dataset.vdur || '';
      var li = x.closest('li');
      if (li && !ch) {
        var m = li.textContent.slice(li.textContent.indexOf(x.textContent) + x.textContent.length).match(/[—-]\s*(.+?)\s*·\s*(\d{1,2}:\d{2}(?::\d{2})?)/);
        if (m) { ch = m[1]; dur = m[2]; }
      }
      vids.push([xid, (x.dataset.vtitle || x.textContent || '').replace(/^[\s▶🎬]+/, '').trim(), ch, dur]);
    });
    // topic = nearest heading above the link inside an article
    var topic = a.dataset.vtopic || '';
    if (!topic) {
      var n = scope && scope.closest('article') ? scope : null;
      while (n && !topic) {
        var prev = n.previousElementSibling;
        while (prev && !/^H[12]$/.test(prev.tagName)) prev = prev.previousElementSibling;
        if (prev) topic = prev.textContent.trim(); else n = n.parentElement && n.parentElement.tagName !== 'ARTICLE' ? n.parentElement : null;
      }
    }
    var title = topic || (vids[start] && vids[start][1]) || 'Video';
    open({ title: title, videos: vids.length ? vids : [[id, a.textContent.trim(), '', '']], index: start, query: a.dataset.vquery || title });
  }, true);

  window.VideoPanel = { open: open, close: close, ytId: ytId };
})();
