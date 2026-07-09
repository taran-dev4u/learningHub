/* DSA Tutorial — shared JS: theme, copy buttons, progress, hub search */
(function () {
  // Theme (persisted)
  var KEY = 'dsa-tut-theme';
  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    try { localStorage.setItem(KEY, t); } catch (e) {}
    var b = document.querySelector('.theme-btn');
    if (b) b.textContent = t === 'light' ? '🌙' : '☀️';
  }
  var saved = 'dark';
  try { saved = localStorage.getItem(KEY) || 'dark'; } catch (e) {}
  document.addEventListener('DOMContentLoaded', function () {
    setTheme(saved);

    // Syntax highlighting (highlight.js loaded from CDN in <head>)
    if (window.hljs) {
      document.querySelectorAll('pre:not(.viz) code').forEach(function (el) {
        if (!el.className) el.classList.add('language-python');
      });
      hljs.highlightAll();
    }

    // Reading progress bar
    var bar = document.createElement('div');
    bar.className = 'scroll-progress';
    document.body.appendChild(bar);
    function onScroll() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // Keyboard navigation: ← previous page, → next page
    var pager = document.querySelectorAll('.pager a[href]');
    var prevHref = null, nextHref = null;
    pager.forEach(function (a) {
      if (a.textContent.indexOf('Previous') >= 0) prevHref = a.getAttribute('href');
      if (a.textContent.indexOf('Next') >= 0) nextHref = a.getAttribute('href');
    });
    document.addEventListener('keydown', function (e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowLeft' && prevHref) window.location.href = prevHref;
      if (e.key === 'ArrowRight' && nextHref) window.location.href = nextHref;
    });

    // Back-to-top button
    var top = document.createElement('button');
    top.className = 'to-top'; top.textContent = '↑'; top.title = 'Back to top';
    top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    document.body.appendChild(top);
    window.addEventListener('scroll', function () {
      top.style.display = document.documentElement.scrollTop > 600 ? 'block' : 'none';
    }, { passive: true });
    var b = document.querySelector('.theme-btn');
    if (b) b.addEventListener('click', function () {
      setTheme(document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
    });

    // Copy buttons on all code blocks
    document.querySelectorAll('pre:not(.viz)').forEach(function (pre) {
      var btn = document.createElement('button');
      btn.className = 'copy-btn'; btn.textContent = 'copy';
      btn.addEventListener('click', function () {
        var txt = pre.innerText.replace(/^copy\n?/, '');
        navigator.clipboard.writeText(txt).then(function () {
          btn.textContent = 'copied!'; setTimeout(function(){ btn.textContent = 'copy'; }, 1200);
        });
      });
      pre.appendChild(btn);
    });

    // Solved checkboxes (persisted by data-id)
    var PKEY = 'dsa-tut-progress';
    var prog = {};
    try { prog = JSON.parse(localStorage.getItem(PKEY) || '{}'); } catch (e) {}
    document.querySelectorAll('input[data-id]').forEach(function (cb) {
      var id = cb.getAttribute('data-id');
      cb.checked = !!prog[id];
      cb.addEventListener('change', function () {
        if (cb.checked) prog[id] = 1; else delete prog[id];
        try { localStorage.setItem(PKEY, JSON.stringify(prog)); } catch (e) {}
        updateCounts();
      });
    });
    function updateCounts() {
      document.querySelectorAll('[data-count-of]').forEach(function (el) {
        var prefix = el.getAttribute('data-count-of');
        var boxes = document.querySelectorAll('input[data-id^="' + prefix + '"]');
        var done = 0;
        boxes.forEach(function (b) { if (b.checked) done++; });
        el.textContent = done + '/' + boxes.length + ' solved';
      });
    }
    updateCounts();

    // Hub search
    var s = document.getElementById('hub-search');
    if (s) s.addEventListener('input', function () {
      var q = s.value.toLowerCase();
      document.querySelectorAll('[data-search]').forEach(function (el) {
        el.style.display = el.getAttribute('data-search').indexOf(q) >= 0 ? '' : 'none';
      });
    });
  });
})();
