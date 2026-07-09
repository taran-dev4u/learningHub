(function () {
  var PASSWORD = "736537";
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
      if (input.value === PASSWORD) {
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
