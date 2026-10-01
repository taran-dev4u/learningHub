/* ============================================================================
   Study rail — row-level action buttons for every roadmap in the learning hub.

   Mirrors the Amazon SDE Preparation Hub: each row gets a right-aligned group
   of small buttons — the row's own source link, "Watch" and "Read" (which open
   the existing side panel, assets/video-panel.js) and a Google / YouTube
   discovery button. No markup is added to any page: rows are decorated at
   runtime, lazily, as they scroll into view.
   ============================================================================ */
(function () {
  "use strict";
  if (window.__hubStudyRail) return;
  window.__hubStudyRail = true;

  var MAX = 14;

  function clean(s) { return String(s == null ? "" : s).replace(/\s+/g, " ").trim(); }
  function googleUrl(q) { return "https://www.google.com/search?q=" + encodeURIComponent(q || ""); }
  function ytSearchUrl(q) { return "https://www.youtube.com/results?search_query=" + encodeURIComponent(q || ""); }

  function ytId(href) {
    if (!href) return null;
    if (window.VideoPanel && window.VideoPanel.ytId) return window.VideoPanel.ytId(href);
    try {
      var u = new URL(href, location.href), h = u.hostname.replace(/^www\.|^m\./, "");
      if (h === "youtu.be") return u.pathname.slice(1).split("/")[0] || null;
      if (h === "youtube.com" || h === "youtube-nocookie.com") {
        if (u.pathname === "/watch") return u.searchParams.get("v");
        var m = u.pathname.match(/^\/(?:embed|shorts|live)\/([^/?#]+)/);
        if (m) return m[1];
      }
    } catch (e) {}
    return null;
  }
  function readable(href) {
    return !!(href && window.VideoPanel && window.VideoPanel.readable && window.VideoPanel.readable(href));
  }
  function isSearch(href) { return /google\.[a-z.]+\/search|youtube\.com\/results|bing\.com\/search/.test(href || ""); }
  function isLocal(a) {
    try { return new URL(a.href, location.href).hostname === location.hostname; } catch (e) { return true; }
  }

  /* ---------- harvest links out of a DOM scope ---------- */
  function harvest(scope, out) {
    out = out || { videos: [], docs: [] };
    if (!scope) return out;
    var anchors = scope.querySelectorAll ? scope.querySelectorAll("a[href]") : [];
    for (var i = 0; i < anchors.length; i++) {
      var a = anchors[i], href = a.getAttribute("href");
      if (!href || href.charAt(0) === "#" || isSearch(a.href)) continue;
      if (a.closest(".hub-actions")) continue;
      var id = ytId(href);
      if (id) {
        if (out.videos.length < MAX && !out.videos.some(function (v) { return v[0] === id; })) {
          out.videos.push([id, clean(a.getAttribute("data-vtitle") || a.textContent) || "Video", clean(a.getAttribute("data-vchannel")), clean(a.getAttribute("data-vdur"))]);
        }
        continue;
      }
      if (isLocal(a)) continue;
      if (out.docs.length < MAX && !out.docs.some(function (d) { return d[1] === a.href; })) {
        out.docs.push([clean(a.textContent).replace(/^[📝🎥🔗📄↗\s]+/, "") || "Link", a.href]);
      }
    }
    return out;
  }

  /* ---------- the rail ---------- */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function count(n) {
    var s = el("span", "sr-count", String(n));
    return s;
  }
  function link(cls, label, href, title) {
    var a = el("a", "study-link " + cls, label);
    a.href = href;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    if (title) a.title = title;
    return a;
  }

  function buildRail(d) {
    var wrap = el("div", "hub-actions");
    wrap.setAttribute("data-no-panel", "");
    var readableDocs = d.docs.filter(function (x) { return readable(x[1]); });

    if (d.primary && d.primary[1]) {
      wrap.appendChild(link("custom primary-link", d.primary[0], d.primary[1], "Open " + d.primary[0] + " in a new tab"));
    }
    if (d.videos.length) {
      var w = el("button", "study-link youtube", "Watch");
      w.type = "button";
      w.setAttribute("data-sr", "watch");
      w.title = "Watch " + d.videos.length + " video" + (d.videos.length > 1 ? "s" : "") + " for this topic in the side panel";
      w.appendChild(count(d.videos.length));
      wrap.appendChild(w);
    } else {
      wrap.appendChild(link("youtube icon-only", "", ytSearchUrl(d.query), "Search YouTube: " + d.query));
    }
    if (readableDocs.length) {
      var r = el("button", "study-link read", "Read");
      r.type = "button";
      r.setAttribute("data-sr", "read");
      r.title = "Read " + readableDocs.length + " article" + (readableDocs.length > 1 ? "s" : "") + " in the side panel";
      r.appendChild(count(readableDocs.length));
      wrap.appendChild(r);
    }
    wrap.appendChild(link("google icon-only", "", googleUrl(d.query), "Search Google: " + d.query));
    wrap.__sr = d;
    return wrap;
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-sr]") : null;
    if (!b) return;
    var host = b.closest(".hub-actions");
    var d = host && host.__sr;
    if (!d) return;
    e.preventDefault();
    e.stopPropagation();
    if (!window.VideoPanel) { window.open(b.getAttribute("data-sr") === "watch" ? ytSearchUrl(d.query) : googleUrl(d.query), "_blank", "noopener"); return; }
    window.VideoPanel.open({
      title: d.title,
      query: d.query,
      videos: d.videos,
      anim: [],
      docs: d.docs,
      tab: b.getAttribute("data-sr") === "read" ? "read" : "videos"
    });
  }, true);

  /* ---------- surfaces ---------- */
  function topicQuery(title, extra) { return clean(title + " " + (extra || "")); }

  var SURFACES = [
    {
      /* DSA Ultimate Index — one row per problem */
      name: "dsa-index",
      rows: function () { return document.querySelectorAll("ol.problems > li[data-lc]"); },
      read: function (li) {
        var name = li.querySelector(".pname, .problem-name");
        var title = clean(name ? name.textContent : li.getAttribute("data-name"));
        var found = harvest(li.querySelector(".solutions") || li);
        /* the problem name itself already links to LeetCode, so no source button */
        return { title: title, query: topicQuery(title, "leetcode solution"), videos: found.videos, docs: found.docs, primary: null };
      },
      mount: function (li, rail) { (li.querySelector(".solutions") || li).appendChild(rail); }
    },
    {
      /* DSA Tutorial — pattern pages list their problems */
      name: "dsa-pattern",
      rows: function () { return document.querySelectorAll("ul.plist > li"); },
      read: function (li) {
        var a = li.querySelector("a[href]");
        var num = li.querySelector(".num");
        var title = clean(a ? a.textContent : "");
        var url = li.getAttribute("data-lc-url");
        return {
          title: title,
          query: topicQuery(title, "leetcode " + clean(num ? num.textContent : "")),
          videos: [], docs: [],
          primary: url ? ["LeetCode", url] : null
        };
      },
      mount: function (li, rail) { li.appendChild(rail); }
    },
    {
      /* DSA Tutorial — a single problem page */
      name: "dsa-problem",
      rows: function () {
        var h = document.querySelector(".container h1");
        return h && document.querySelector("a.lc-icon, a.chip") ? [h] : [];
      },
      read: function (h) {
        var title = clean(h.textContent);
        var found = harvest(h.parentElement || document.querySelector(".container"));
        var lc = document.querySelector("a.lc-icon");
        return {
          title: title,
          query: topicQuery(title, "leetcode solution explained"),
          videos: found.videos, docs: found.docs,
          primary: lc ? ["LeetCode", lc.href] : null
        };
      },
      mount: function (h, rail) {
        var box = el("div", "sr-page-actions");
        box.appendChild(rail);
        h.parentNode.insertBefore(box, h.nextSibling);
      }
    },
    {
      /* Concept pages: system design, CS, behavioral, AI, cloud, interview prep */
      name: "concepts",
      rows: function () { return document.querySelectorAll("li[data-cid]"); },
      read: function (li) {
        var name = li.querySelector(".cname");
        var title = clean(name ? name.textContent : li.getAttribute("data-name"));
        var sub = li.closest(".subsection");
        var section = li.closest("section.section, section, .pattern") || sub;
        var found = harvest(li);
        if (!found.videos.length && !found.docs.length && sub) {
          found = harvest(sub.querySelector(".sub-resources, .res-grid, .resources-body"));
        }
        if (!found.videos.length && !found.docs.length && section) {
          found = harvest(section.querySelector(".resources-section .res-grid, .res-grid, .sub-resources"));
        }
        var heading = (sub && sub.querySelector("h3")) || (section && section.querySelector("h2"));
        return {
          title: title,
          query: topicQuery(title, clean(heading ? heading.textContent : "")),
          videos: found.videos, docs: found.docs, primary: null
        };
      },
      mount: function (li, rail) {
        /* the row already carried two bare search links; the rail replaces them */
        var legacy = li.querySelector(".res-links");
        if (legacy) legacy.parentNode.removeChild(legacy);
        li.appendChild(rail);
      }
    },
    {
      /* System Design / LLD tutorials — the roadmap rows */
      name: "am-roadmap",
      rows: function () { return document.querySelectorAll(".am-rows > a.am-row"); },
      read: function (row) {
        var title = clean((row.querySelector(".am-title") || row).textContent);
        var found = lessonLinks(row.getAttribute("href") || "");
        return {
          title: title,
          query: topicQuery(title, document.title.replace(/\s*[—|].*$/, "")),
          videos: found.videos, docs: found.docs, primary: null
        };
      },
      mount: function (row, rail) {
        var wrap = el("div", "am-row-wrap");
        row.parentNode.insertBefore(wrap, row);
        wrap.appendChild(row);
        wrap.appendChild(rail);
      }
    }
  ];

  /* Pull the links out of the markdown lesson that backs a roadmap row. */
  function slugOf(headingLine) {
    return headingLine.replace(/^#+\s+/, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
  }
  function lessonLinks(hash) {
    var out = { videos: [], docs: [] };
    var parts = String(hash).replace(/^#/, "").split("/");
    if (parts.length < 2 || !window.topicsData || !window.contentBundle) return out;
    var file = null;
    window.topicsData.forEach(function (sec) {
      (sec.subsections || []).forEach(function (sub) { if (sub.id === parts[0]) file = sub.file; });
    });
    var md = file && window.contentBundle[file];
    if (!md) return out;
    var heads = [], re = /^##\s+.*$/gm, m;
    while ((m = re.exec(md))) heads.push({ i: m.index, t: m[0] });
    var start = -1, end = md.length;
    for (var j = 0; j < heads.length; j++) {
      if (slugOf(heads[j].t) === parts[1]) { start = heads[j].i; end = heads[j + 1] ? heads[j + 1].i : md.length; break; }
    }
    var body = start < 0 ? "" : md.slice(start, end);
    var link = /\[([^\]]*)\]\((https?:\/\/[^\s)]+)\)|(?:^|\s)(https?:\/\/[^\s)<]+)/g, l;
    while ((l = link.exec(body))) {
      var href = l[2] || l[3], label = clean(l[1]) || "Link";
      if (!href || isSearch(href)) continue;
      var id = ytId(href);
      if (id) {
        if (out.videos.length < MAX && !out.videos.some(function (v) { return v[0] === id; })) out.videos.push([id, label, "", ""]);
      } else if (out.docs.length < MAX && !out.docs.some(function (d) { return d[1] === href; })) {
        out.docs.push([label, href]);
      }
    }
    return out;
  }

  /* ---------- lazy decoration ---------- */
  var io = null;
  function decorate(node, surface) {
    if (node.__srDone) return;
    node.__srDone = true;
    var d;
    try { d = surface.read(node); } catch (e) { return; }
    if (!d || !d.title) return;
    try { surface.mount(node, buildRail(d)); } catch (e) {}
  }
  function observe(nodes, surface) {
    if (!nodes || !nodes.length) return;
    if (!("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(nodes, function (n) { decorate(n, surface); });
      return;
    }
    if (!io) {
      io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          io.unobserve(entry.target);
          decorate(entry.target, entry.target.__srSurface);
        });
      }, { rootMargin: "500px 0px" });
    }
    Array.prototype.forEach.call(nodes, function (n) {
      if (n.__srDone || n.__srSurface) return;
      n.__srSurface = surface;
      io.observe(n);
    });
  }
  function scan() {
    SURFACES.forEach(function (s) {
      var nodes;
      try { nodes = s.rows(); } catch (e) { return; }
      observe(nodes, s);
    });
  }

  function start() {
    scan();
    var amRoot = document.getElementById("am-root");
    if (amRoot && "MutationObserver" in window) {
      var t = null;
      new MutationObserver(function () {
        clearTimeout(t);
        t = setTimeout(scan, 120);
      }).observe(amRoot, { childList: true, subtree: true });
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();

  window.HubStudyRail = { scan: scan };
})();
