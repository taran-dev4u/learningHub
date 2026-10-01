/* Taran's Learning Hub — single source of truth for navigation + theme.
   Loaded on every page via learning-hub-shared.js. Renders one navbar at any
   folder depth and keeps one theme across every page and sub-site. */
(function () {
  "use strict";

  var THEME_KEY = "learning_hub_theme";
  var LEGACY_KEYS = ["hub_theme", "learning_hub_theme_v2", "dsa-tut-theme", "theme"];

  /* ---------- where is the site root, relative to this page? ---------- */
  function siteRoot() {
    var scripts = document.getElementsByTagName("script");
    for (var i = 0; i < scripts.length; i++) {
      var src = scripts[i].getAttribute("src") || "";
      var m = src.match(/^(.*?)assets\/(learning-hub-shared|hub-nav)\.js/);
      if (m) return m[1];
    }
    return "";
  }
  var ROOT = siteRoot();

  /* ---------- the one list of destinations ---------- */
  var LINKS = [
    { label: "Hub",           short: "Hub",       href: "index.html" },
    { label: "DSA Index",     short: "DSA",       href: "DSA_Ultimate_Index.html" },
    { label: "DSA Tutorial",  short: "DSA Tut",   href: "DSA_Tutorial/index.html" },
    { label: "System Design", short: "Systems",   href: "system_design.html" },
    { label: "SD Tutorial",   short: "SD Tut",    href: "System_Design_Tutorial/index.html" },
    { label: "LLD Tutorial",  short: "LLD",       href: "LLD_Tutorial/index.html" },
    { label: "CS",            short: "CS",        href: "cs_fundamentals.html" },
    { label: "Behavioral",    short: "Behavioral",href: "behavioral.html" },
    { label: "AI",            short: "AI",        href: "ai_engineering.html" },
    { label: "Cloud",         short: "Cloud",     href: "cloud_aws_azure.html" },
    { label: "Interview Prep",short: "Interview", href: "interview_prep.html" },
    { label: "Companies",     short: "Companies", href: "companies.html" },
    { label: "Library",       short: "Library",   href: "library.html" },
    { label: "Auto-Me",       short: "Auto-Me",   href: "auto-me/index.html" }
  ];

  /* ---------- theme ---------- */
  function readStore(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function writeStore(key, value) { try { localStorage.setItem(key, value); } catch (e) {} }

  function preferredTheme() {
    var v = readStore(THEME_KEY);
    if (normalizeTheme(v)) return v;
    for (var i = 0; i < LEGACY_KEYS.length; i++) {
      var legacy = readStore(LEGACY_KEYS[i]);
      if (legacy === "dark" || legacy === "light") return legacy;
    }
    try {
      if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) return "dark";
    } catch (e) {}
    return "light";
  }

  /* Three themes, cycled in this order. "black" is a true-black variant of dark:
     page stylesheets still see .dark, and a token layer in the shared stylesheet
     paints the backgrounds black on top. */
  var THEMES = ["light", "dark", "black"];
  var THEME_ICON = { light: "☀", dark: "◐", black: "●" };
  var THEME_NAME = { light: "Light", dark: "Dark", black: "Black" };

  function normalizeTheme(value) {
    return THEMES.indexOf(value) >= 0 ? value : null;
  }

  function applyTheme(theme, persist) {
    theme = normalizeTheme(theme) || "light";
    var root = document.documentElement;
    var dark = theme !== "light";
    root.classList.toggle("dark", dark);
    root.classList.toggle("light", !dark);
    root.classList.toggle("black", theme === "black");
    root.setAttribute("data-theme", theme);
    if (persist !== false) {
      writeStore(THEME_KEY, theme);
      /* page-level scripts only understand light/dark */
      var legacyValue = dark ? "dark" : "light";
      for (var i = 0; i < LEGACY_KEYS.length; i++) writeStore(LEGACY_KEYS[i], legacyValue);
    }
    var next = THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length];
    var btn = document.querySelector("[data-hub-theme]");
    if (btn) {
      btn.textContent = THEME_ICON[theme];
      var label = "Theme: " + THEME_NAME[theme] + ". Switch to " + THEME_NAME[next];
      btn.setAttribute("aria-label", label);
      btn.setAttribute("title", label);
    }
    window.LearningHubTheme = theme;
    try {
      window.dispatchEvent(new CustomEvent("learning-hub-theme", { detail: { theme: theme } }));
    } catch (e) {}
  }

  function toggleTheme() {
    var cur = normalizeTheme(document.documentElement.getAttribute("data-theme")) || "light";
    applyTheme(THEMES[(THEMES.indexOf(cur) + 1) % THEMES.length], true);
  }

  /* Legacy per-page theme buttons write their own keys; mirror those writes so
     one click changes the theme everywhere instead of only on this page. */
  function interceptLegacyWrites() {
    try {
      var native = localStorage.setItem.bind(localStorage);
      localStorage.setItem = function (key, value) {
        native(key, value);
        if (LEGACY_KEYS.indexOf(key) !== -1 && (value === "dark" || value === "light")) {
          /* a page button flipping to dark must not drop us out of black */
          var want = value === "dark" && window.LearningHubTheme === "black" ? "black" : value;
          if (window.LearningHubTheme !== want) applyTheme(want, true);
        }
      };
    } catch (e) {}
  }

  applyTheme(preferredTheme(), true);
  interceptLegacyWrites();

  /* ---------- navbar ---------- */
  function currentFile() {
    var p = window.location.pathname.replace(/\\/g, "/");
    var parts = p.split("/").filter(Boolean);
    var file = parts.length ? parts[parts.length - 1] : "index.html";
    if (!/\.html?$/.test(file)) { parts.push("index.html"); file = "index.html"; }
    var parent = parts.length > 1 ? parts[parts.length - 2] : "";
    return { file: file, parent: parent };
  }

  function isCurrent(link, here) {
    if (link.external) return false;
    var target = link.href.split("/");
    var targetFile = target[target.length - 1];
    var targetDir = target.length > 1 ? target[target.length - 2] : "";
    if (targetDir) return here.parent === targetDir;
    return here.file === targetFile && !here.parent.match(/^(DSA_Tutorial|LLD_Tutorial|System_Design_Tutorial|auto-me|ConvertedDocs)$/);
  }

  function buildNav() {
    var here = currentFile();
    var nav = document.createElement("nav");
    nav.className = "hub-nav";
    nav.setAttribute("aria-label", "Learning hub navigation");

    var brand = document.createElement("a");
    brand.className = "hub-nav-brand";
    brand.href = ROOT + "index.html";
    brand.innerHTML = "<strong>Learning Hub</strong>";
    nav.appendChild(brand);

    var list = document.createElement("div");
    list.className = "hub-nav-links";
    LINKS.forEach(function (link) {
      var a = document.createElement("a");
      a.href = link.external ? link.href : ROOT + link.href;
      a.textContent = link.short;
      a.setAttribute("data-full", link.label);
      if (link.short !== link.label) a.setAttribute("title", link.label);
      if (link.external) {
        a.target = "_blank";
        a.rel = "noopener";
        a.className = "is-external";
        a.setAttribute("title", link.label + " — opens the live site in a new tab");
      }
      if (isCurrent(link, here)) {
        a.className = (a.className ? a.className + " " : "") + "is-current";
        a.setAttribute("aria-current", "page");
      }
      list.appendChild(a);
    });
    nav.appendChild(list);

    var theme = document.createElement("button");
    theme.type = "button";
    theme.className = "hub-nav-theme";
    theme.setAttribute("data-hub-theme", "");
    nav.appendChild(theme);
    return nav;
  }

  function mountNav() {
    if (document.querySelector("nav.hub-nav")) return;
    var nav = buildNav();
    var legacy = document.querySelector("nav.site-nav, nav.global-learning-nav");
    if (legacy) legacy.parentNode.replaceChild(nav, legacy);
    else document.body.insertBefore(nav, document.body.firstChild);

    /* a page may carry a second, older nav further down — drop it */
    var extras = document.querySelectorAll("nav.site-nav, nav.global-learning-nav");
    for (var i = 0; i < extras.length; i++) extras[i].parentNode.removeChild(extras[i]);

    var skip = document.createElement("a");
    skip.className = "hub-skip-link";
    skip.href = "#hub-main";
    skip.textContent = "Skip to content";
    document.body.insertBefore(skip, document.body.firstChild);
    var main = document.querySelector("main, .wrap, .container, .content-area, #app");
    /* never rename an element that already has an id: page scripts look it up
       (the tutorials render into #am-root, other pages into #app) */
    if (main) {
      if (!main.id) main.id = "hub-main";
      skip.href = "#" + main.id;
    }

    nav.querySelector("[data-hub-theme]").addEventListener("click", toggleTheme);
    applyTheme(document.documentElement.getAttribute("data-theme") || "light", false);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mountNav);
  else mountNav();

  window.LearningHubNav = { links: LINKS, root: ROOT, setTheme: applyTheme, toggleTheme: toggleTheme };
})();

(function () {
  // Client-side gate only (a static site cannot keep a real secret).
  // The literal passcode is no longer in the source; two independent
  // 32-bit digests of it are compared instead.
  var PASS_DJB2 = 0xdcba3946;
  var PASS_SDBM = 0x365c1c7f;
  var PASS_LEN = 6;
  function digests(value) {
    var s = String(value == null ? "" : value), a = 5381, b = 0, i, c;
    for (i = 0; i < s.length; i++) {
      c = s.charCodeAt(i);
      a = ((a * 33) ^ c) >>> 0;
      b = (c + (b << 6) + (b << 16) - b) >>> 0;
    }
    return [a, b];
  }
  function passwordMatches(value) {
    if (String(value).length !== PASS_LEN) return false;
    var d = digests(value);
    return d[0] === PASS_DJB2 && d[1] === PASS_SDBM;
  }
  var AUTH_KEY = "taran_learning_hub_unlocked_v1";
  var WATCHED_KEYS = [
    /^dsa_index_solved_v1$/,
    /^dsa_index_bookmark_v1$/,
    /^hub_done_/,
    /^hub_bm_/,
    /^sd_tutorial_done_v1$/,
    /^interview_prep_/,
  ];

  function storageGet(key) {
    try { return localStorage.getItem(key); } catch (_e) { return null; }
  }

  function storageSet(key, value) {
    try { localStorage.setItem(key, value); } catch (_e) {}
  }

  function isUnlocked() {
    return storageGet(AUTH_KEY) === "1";
  }

  if (!isUnlocked()) {
    document.documentElement.classList.add("learning-hub-locked");
  }

  function readSet(key) {
    try { return new Set(JSON.parse(localStorage.getItem(key) || "[]")); }
    catch (_e) { return new Set(); }
  }

  function writeSet(key, set) {
    try {
      localStorage.setItem(key, JSON.stringify(Array.from(set)));
      window.dispatchEvent(new CustomEvent("learning-hub-progress-updated", { detail: { key: key } }));
    } catch (_e) {}
  }

  function watched(key) {
    return !!key && WATCHED_KEYS.some(function (pattern) { return pattern.test(key); });
  }

  window.LearningHubShared = {
    authKey: AUTH_KEY,
    readSet: readSet,
    writeSet: writeSet,
    normalizeTitle: function (value) {
      return String(value || "")
        .toLowerCase()
        .replace(/&/g, "and")
        .replace(/[^a-z0-9]+/g, " ")
        .replace(/\s+/g, " ")
        .trim();
    },
  };

  window.addEventListener("storage", function (event) {
    if (!watched(event.key)) return;
    window.dispatchEvent(new CustomEvent("learning-hub-progress-external", { detail: { key: event.key } }));
    if (window.learningHubDisableProgressReload) return;
    window.setTimeout(function () { window.location.reload(); }, 120);
  });

  function mountLock() {
    if (isUnlocked()) {
      document.documentElement.classList.remove("learning-hub-locked");
      return;
    }
    if (document.getElementById("learning-hub-lock")) return;
    var overlay = document.createElement("div");
    overlay.id = "learning-hub-lock";
    overlay.innerHTML =
      '<section class="learning-lock-card" role="dialog" aria-modal="true" aria-labelledby="learning-lock-title">' +
        '<h1 id="learning-lock-title">Taran&#39;s Learning Hub</h1>' +
        '<p>This personal learning hub is locked on this browser. Enter the password to open the study pages.</p>' +
        '<form class="learning-lock-form" id="learning-lock-form">' +
          '<label>Password<input id="learning-lock-password" type="password" inputmode="numeric" autocomplete="current-password" autofocus></label>' +
          '<button type="submit">Unlock Hub</button>' +
          '<p class="learning-lock-error" id="learning-lock-error" aria-live="polite"></p>' +
        '</form>' +
      '</section>';
    document.body.appendChild(overlay);
    var input = document.getElementById("learning-lock-password");
    var error = document.getElementById("learning-lock-error");
    document.getElementById("learning-lock-form").addEventListener("submit", function (event) {
      event.preventDefault();
      if (passwordMatches(input.value)) {
        storageSet(AUTH_KEY, "1");
        document.documentElement.classList.remove("learning-hub-locked");
        overlay.remove();
      } else {
        error.textContent = "Wrong password. Try again.";
        input.select();
      }
    });
    window.setTimeout(function () { input.focus(); }, 50);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountLock);
  } else {
    mountLock();
  }
})();


/* ---------- in-page YouTube side panel on every hub page ---------- */
(function () {
  if (window.__hubVideoPanelLoaded) return;
  window.__hubVideoPanelLoaded = true;
  var root = "";
  var scripts = document.getElementsByTagName("script");
  for (var i = 0; i < scripts.length; i++) {
    var m = (scripts[i].getAttribute("src") || "").match(/^(.*?)assets\/learning-hub-shared\.js/);
    if (m) { root = m[1]; break; }
  }
  var css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = root + "assets/video-panel.css?v=2";
  document.head.appendChild(css);
  var js = document.createElement("script");
  js.src = root + "assets/video-panel.js?v=2";
  js.defer = true;
  document.head.appendChild(js);

  /* row-level action buttons that open the panel */
  var railCss = document.createElement("link");
  railCss.rel = "stylesheet";
  railCss.href = root + "assets/study-rail.css?v=1";
  document.head.appendChild(railCss);
  var railJs = document.createElement("script");
  railJs.src = root + "assets/study-rail.js?v=1";
  railJs.defer = true;
  document.head.appendChild(railJs);
})();
