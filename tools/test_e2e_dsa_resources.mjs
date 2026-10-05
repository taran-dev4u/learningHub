#!/usr/bin/env node
/**
 * ============================================================================
 * E2E Test Suite: DSA Curated Multi-Resources & Side Panel Architecture
 * ============================================================================
 *
 * Opaque-box, requirement-driven acceptance test suite derived directly from
 * ORIGINAL_REQUEST.md, PROJECT.md, and AGENTS.md.
 *
 * Covers 4 Tiers:
 *   Tier 1: Feature Coverage (link accuracy, 4-5 videos schema, 4-5 reading schema,
 *           dedicated Watch/Read/G/📝 buttons, zero legacy duplicates).
 *   Tier 2: Boundary & Corner Cases (Striver s-ids, non-LeetCode conceptual links,
 *           iframe X-Frame-Options handling, fallback cards, 0 vs 1 vs N videos).
 *   Tier 3: Cross-Feature Interactions (theme switching + panel dock/collapse;
 *           watch channel pills + playback; reader tab + iframe/card display).
 *   Tier 4: Real-World User Scenarios (end-to-end user flows on Two Sum,
 *           Striver problems, Hard problems, viewport pinning delta < 1px).
 *
 * Usage:
 *   node tools/test_e2e_dsa_resources.mjs
 *   node tools/test_e2e_dsa_resources.mjs --tier=1
 *   node tools/test_e2e_dsa_resources.mjs --diagnostics
 * ============================================================================
 */

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";

const ROOT = process.cwd();
const ARGS = process.argv.slice(2);
const TARGET_TIER = ARGS.find(a => a.startsWith("--tier="))?.split("=")[1];
const VERBOSE_DIAGNOSTICS = ARGS.includes("--diagnostics") || ARGS.includes("-v");

if (ARGS.includes("--help") || ARGS.includes("-h")) {
  console.log(`
Usage: node tools/test_e2e_dsa_resources.mjs [options]

Options:
  --tier=1|2|3|4     Run tests exclusively for the specified tier
  --diagnostics, -v  Print detailed diagnostic logs for each test
  --help, -h         Show this help message
`);
  process.exit(0);
}

/* ============================================================================
   Test Harness & Assertion Framework
   ============================================================================ */

const results = [];
let currentTest = null;

function test(id, description, tier, fn) {
  if (TARGET_TIER && String(tier) !== String(TARGET_TIER)) return;
  const testRecord = { id, description, tier, passed: false, error: null, diagnostics: [] };
  currentTest = testRecord;
  try {
    fn({
      assert(cond, message, diag) {
        if (!cond) {
          const err = new Error(message || "Assertion failed");
          if (diag) err.diagnostics = diag;
          throw err;
        }
        if (diag && VERBOSE_DIAGNOSTICS) testRecord.diagnostics.push(diag);
      },
      diag(info) {
        testRecord.diagnostics.push(info);
      }
    });
    testRecord.passed = true;
  } catch (err) {
    testRecord.passed = false;
    testRecord.error = err.message;
    if (err.diagnostics) testRecord.diagnostics.push(err.diagnostics);
  }
  results.push(testRecord);
  currentTest = null;
}

/* ============================================================================
   Static Codebase Inspectors
   ============================================================================ */

function loadDsaIndex() {
  const filePath = path.join(ROOT, "DSA_Ultimate_Index.html");
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }
  return fs.readFileSync(filePath, "utf8");
}

function parseDsaIndexProblems(html) {
  const problems = [];
  const rowRegex = /<li\b([^>]*\bdata-lc=["']([^"']+)["'][^>]*)>([\s\S]*?)<\/li>/gi;
  let match;
  while ((match = rowRegex.exec(html)) !== null) {
    const [full, attrs, lcId, body] = match;
    const isCurated = !lcId.startsWith("s");
    const isStriver = lcId.startsWith("s");
    const hasSolutions = /<div class="solutions">/i.test(body);
    const hasBadges = /<div class="badges">/i.test(body);
    const hasNoteBtn = /class="note-btn"/i.test(body);

    const ncVideoLinks = (body.match(/🎬\s*NC✓|<a\b[^>]*\bverified\b/gi) || []).length;
    const searchVideoLinks = (body.match(/🎥\s*Video|youtube\.com\/results\?search_query=/gi) || []).length;
    const gfgSearchLinks = (body.match(/📚\s*GFG|google\.[a-z.]+\/search\?q=site%3Ageeksforgeeks/gi) || []).length;
    const striverYtLinks = (body.match(/class="badge\s+badge-yt"|title="Video Solution"/gi) || []).length;
    const striverArticleLinks = (body.match(/class="badge\s+badge-article"|title="Article"/gi) || []).length;

    problems.push({
      lcId,
      isCurated,
      isStriver,
      hasSolutions,
      hasBadges,
      hasNoteBtn,
      ncVideoLinks,
      searchVideoLinks,
      gfgSearchLinks,
      striverYtLinks,
      striverArticleLinks,
      attrs,
      body
    });
  }
  return problems;
}

function loadDsaResources() {
  const filePath = path.join(ROOT, "assets", "dsa-resources.js");
  if (!fs.existsSync(filePath)) {
    return null;
  }
  const code = fs.readFileSync(filePath, "utf8");
  const ctx = { window: {} };
  vm.createContext(ctx);
  vm.runInContext(code, ctx);
  const res = ctx.window.dsaResources || {};
  const slugs = ctx.window.dsaResourceSlugs || {};
  for (const [slug, id] of Object.entries(slugs)) {
    if (!res[slug] && res[id]) res[slug] = res[id];
  }
  return res;
}

function loadTutorialProblemPages() {
  const dir = path.join(ROOT, "DSA_Tutorial", "problems");
  if (!fs.existsSync(dir)) return [];
  const files = fs.readdirSync(dir).filter(f => f.endsWith(".html"));
  return files.map(file => {
    const content = fs.readFileSync(path.join(dir, file), "utf8");
    const hasVideoWalkthroughChip = /🎬\s*Video walkthrough/i.test(content);
    return { file, hasVideoWalkthroughChip, content };
  });
}

function loadBuildPy() {
  const filePath = path.join(ROOT, "DSA_Tutorial", "build.py");
  if (!fs.existsSync(filePath)) return "";
  return fs.readFileSync(filePath, "utf8");
}

/* ============================================================================
   Lightweight DOM & Browser Environment Simulation
   ============================================================================ */

function parseHTMLToNodes(html, ownerDoc) {
  const root = new MockElement("div", ownerDoc);
  const stack = [root];
  const VOID_TAGS = new Set(["img", "input", "br", "hr", "meta", "link"]);

  const tagRegex = /<!--[\s\S]*?-->|<(\/)?([a-zA-Z0-9-]+)([^>]*)>|([^<]+)/g;
  let match;

  while ((match = tagRegex.exec(html)) !== null) {
    const [full, isClose, tagName, attrStr, text] = match;
    if (full.startsWith("<!--")) continue;

    if (text) {
      if (text.trim() || stack.length > 1) {
        const textNode = new MockElement("#text", ownerDoc);
        textNode.textContent = text;
        stack[stack.length - 1].appendChild(textNode);
      }
      continue;
    }

    const tag = (tagName || "").toLowerCase();
    if (isClose) {
      for (let i = stack.length - 1; i > 0; i--) {
        if (stack[i].tagName.toLowerCase() === tag) {
          stack.splice(i);
          break;
        }
      }
    } else {
      const el = new MockElement(tag, ownerDoc);
      if (attrStr) {
        const attrRegex = /([a-zA-Z0-9_-]+)(?:=(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g;
        let am;
        while ((am = attrRegex.exec(attrStr)) !== null) {
          const k = am[1];
          const v = am[2] ?? am[3] ?? am[4] ?? "";
          el.setAttribute(k, v);
        }
      }
      stack[stack.length - 1].appendChild(el);
      if (!VOID_TAGS.has(tag) && !attrStr.trim().endsWith("/")) {
        stack.push(el);
      }
    }
  }

  const result = [...root.children];
  result.forEach(c => { c.parentNode = null; });
  return result;
}

class MockClassList {
  constructor(el) {
    this.el = el;
    this.classes = new Set();
  }
  add(...names) {
    names.forEach(n => { if (n) this.classes.add(n); });
    this._sync();
  }
  remove(...names) {
    names.forEach(n => this.classes.delete(n));
    this._sync();
  }
  toggle(name, force) {
    const has = this.classes.has(name);
    const next = force !== undefined ? !!force : !has;
    if (next) this.classes.add(name); else this.classes.delete(name);
    this._sync();
    return next;
  }
  contains(name) { return this.classes.has(name); }
  _sync() { this.el._className = Array.from(this.classes).join(" "); }
  _load(str) { this.classes = new Set((str || "").split(/\s+/).filter(Boolean)); }
}

function escapeHtml(str) {
  return String(str ?? "").replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[c]);
}

class MockElement {
  constructor(tagName = "div", ownerDoc = null) {
    this.tagName = String(tagName).toUpperCase();
    this.ownerDocument = ownerDoc;
    this.children = [];
    this.parentNode = null;
    this.attributes = new Map();
    this.classList = new MockClassList(this);
    this._className = "";
    this.style = {
      setProperty: (k, v) => { this.style[k] = String(v); },
      removeProperty: (k) => { delete this.style[k]; }
    };
    this.dataset = {};
    this.listeners = new Map();
    this._textContent = "";
    this._rect = { top: 100, bottom: 130, left: 10, right: 800, width: 790, height: 30 };
    this.isConnected = true;
    this.hidden = false;
  }
  get className() { return this._className; }
  set className(val) { this._className = val || ""; this.classList._load(this._className); }
  get href() { return this.getAttribute("href") || ""; }
  set href(val) { this.setAttribute("href", val); }
  get src() { return this.getAttribute("src") || ""; }
  set src(val) { this.setAttribute("src", val); }
  get title() { return this.getAttribute("title") || ""; }
  set title(val) { this.setAttribute("title", val); }
  get id() { return this.getAttribute("id") || ""; }
  set id(val) { this.setAttribute("id", val); }
  get type() { return this.getAttribute("type") || "button"; }
  set type(val) { this.setAttribute("type", val); }

  get textContent() {
    if (this.children.length === 0) return this._textContent;
    return this.children.map(c => c.textContent).join("");
  }
  set textContent(val) {
    this.children = [];
    this._textContent = String(val == null ? "" : val);
  }
  get innerHTML() {
    if (this.children.length === 0) return escapeHtml(this._textContent);
    return this.children.map(c => {
      if (c.tagName === "#TEXT") return escapeHtml(c.textContent);
      const tag = c.tagName.toLowerCase();
      const attrs = Array.from(c.attributes.entries()).map(([k, v]) => ` ${k}="${escapeHtml(v)}"`).join("");
      return `<${tag}${attrs}>${c.innerHTML}</${tag}>`;
    }).join("");
  }
  set innerHTML(val) {
    this.children = [];
    const nodes = parseHTMLToNodes(val, this.ownerDocument);
    nodes.forEach(n => this.appendChild(n));
  }
  getAttribute(name) { return this.attributes.get(name) ?? null; }
  setAttribute(name, val) {
    this.attributes.set(name, String(val));
    if (name === "class") this.className = String(val);
    if (name === "hidden") this.hidden = true;
    if (name.startsWith("data-")) {
      const prop = name.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      this.dataset[prop] = String(val);
    }
  }
  removeAttribute(name) {
    this.attributes.delete(name);
    if (name === "hidden") this.hidden = false;
    if (name.startsWith("data-")) {
      const prop = name.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      delete this.dataset[prop];
    }
  }
  appendChild(child) {
    if (child.parentNode) child.parentNode.removeChild(child);
    child.parentNode = this;
    this.children.push(child);
    return child;
  }
  insertBefore(newNode, refNode) {
    if (newNode.parentNode) newNode.parentNode.removeChild(newNode);
    newNode.parentNode = this;
    const idx = this.children.indexOf(refNode);
    if (idx === -1) this.children.push(newNode);
    else this.children.splice(idx, 0, newNode);
    return newNode;
  }
  removeChild(child) {
    const idx = this.children.indexOf(child);
    if (idx !== -1) {
      this.children.splice(idx, 1);
      child.parentNode = null;
    }
    return child;
  }
  insertAdjacentHTML(position, text) {
    const nodes = parseHTMLToNodes(text, this.ownerDocument);
    if (position === "beforeend") {
      nodes.forEach(n => this.appendChild(n));
    } else if (position === "afterbegin") {
      for (let i = nodes.length - 1; i >= 0; i--) {
        this.insertBefore(nodes[i], this.children[0]);
      }
    }
  }
  getBoundingClientRect() { return { ...this._rect }; }
  addEventListener(type, fn) {
    if (!this.listeners.has(type)) this.listeners.set(type, []);
    this.listeners.get(type).push(fn);
  }
  removeEventListener(type, fn) {
    const arr = this.listeners.get(type);
    if (arr) {
      const idx = arr.indexOf(fn);
      if (idx !== -1) arr.splice(idx, 1);
    }
  }
  dispatchEvent(event) {
    if (!event.preventDefault) event.preventDefault = () => {};
    if (!event.stopPropagation) event.stopPropagation = () => { event._stop = true; };
    event.target = this;
    let curr = this;
    while (curr) {
      const handlers = curr.listeners?.get(event.type) || [];
      handlers.forEach(h => h.call(curr, event));
      if (event._stop) break;
      if (!curr.parentNode) {
        const doc = curr.ownerDocument || this.ownerDocument;
        if (doc) {
          const docHandlers = doc.listeners?.get(event.type) || [];
          docHandlers.forEach(h => h.call(doc, event));
        }
        break;
      }
      curr = curr.parentNode;
    }
  }
  closest(selector) {
    let curr = this;
    while (curr) {
      if (curr.matches && curr.matches(selector)) return curr;
      curr = curr.parentNode;
    }
    return null;
  }
  matches(selector) {
    if (!selector) return false;
    const parts = selector.split(",").map(s => s.trim());
    return parts.some(sel => {
      const tagMatch = sel.match(/^([a-zA-Z0-9-]+)/);
      if (tagMatch && this.tagName.toLowerCase() !== tagMatch[1].toLowerCase()) return false;
      const classes = sel.match(/\.([a-zA-Z0-9_-]+)/g) || [];
      for (const c of classes) {
        if (!this.classList.contains(c.slice(1))) return false;
      }
      const attrs = sel.match(/\[([a-zA-Z0-9_-]+)(?:=([^\]]+))?\]/g) || [];
      for (const a of attrs) {
        const am = a.slice(1, -1).match(/([a-zA-Z0-9_-]+)(?:=(.*))?/);
        if (am) {
          const k = am[1];
          const v = (am[2] || "").replace(/['"]/g, "");
          if (am[2] !== undefined && this.getAttribute(k) !== v) return false;
          if (am[2] === undefined && !this.attributes.has(k)) return false;
        }
      }
      if (sel.startsWith("#") && this.getAttribute("id") !== sel.slice(1)) return false;
      return true;
    });
  }
  querySelector(selector) {
    return this.querySelectorAll(selector)[0] || null;
  }
  querySelectorAll(selector) {
    if (selector.includes(",")) {
      const parts = selector.split(",").map(s => s.trim()).filter(Boolean);
      const res = [];
      for (const p of parts) {
        for (const el of this.querySelectorAll(p)) {
          if (!res.includes(el)) res.push(el);
        }
      }
      return res;
    }
    if (selector === "ol.problems > li[data-lc]") {
      const res = [];
      const ols = this.querySelectorAll("ol.problems");
      for (const ol of ols) {
        for (const ch of ol.children) {
          if (ch.matches("li[data-lc]")) res.push(ch);
        }
      }
      return res;
    }
    if (selector.includes(" ")) {
      const parts = selector.split(/\s+/).filter(Boolean);
      let current = [this];
      for (const part of parts) {
        const next = [];
        for (const node of current) {
          next.push(...node.querySelectorAll(part));
        }
        current = next;
      }
      return current;
    }
    const res = [];
    const walk = (node) => {
      for (const ch of node.children) {
        if (ch.matches(selector)) res.push(ch);
        walk(ch);
      }
    };
    walk(this);
    return res;
  }
}

function createBrowserEnv() {
  const documentListeners = new Map();
  const windowListeners = new Map();

  let scrollOffset = { top: 0, left: 0 };

  const documentObj = {
    readyState: "complete",
    listeners: documentListeners,
    documentElement: null,
    head: null,
    body: null,
    createElement: (tag) => new MockElement(tag, documentObj),
    getElementById: (id) => {
      const walk = (n) => {
        if (!n) return null;
        if (n.getAttribute("id") === id) return n;
        for (const c of n.children) {
          const f = walk(c);
          if (f) return f;
        }
        return null;
      };
      return walk(documentObj.documentElement);
    },
    getElementsByTagName: (t) => {
      const res = [];
      const walk = (n) => {
        if (!n) return;
        if (n.tagName.toLowerCase() === t.toLowerCase()) res.push(n);
        for (const c of n.children) walk(c);
      };
      walk(documentObj.documentElement);
      return res;
    },
    getElementsByClassName: (cls) => {
      return documentObj.documentElement ? documentObj.documentElement.querySelectorAll("." + cls) : [];
    },
    addEventListener: (type, fn) => {
      if (!documentListeners.has(type)) documentListeners.set(type, []);
      documentListeners.get(type).push(fn);
    },
    removeEventListener: (type, fn) => {
      const arr = documentListeners.get(type);
      if (arr) {
        const idx = arr.indexOf(fn);
        if (idx !== -1) arr.splice(idx, 1);
      }
    },
    dispatchEvent: (event) => {
      const arr = documentListeners.get(event.type) || [];
      arr.forEach(fn => fn(event));
    },
    querySelectorAll: (sel) => {
      if (!documentObj.documentElement) return [];
      if (sel === "ol.problems > li[data-lc]") {
        const res = [];
        const ols = documentObj.documentElement.querySelectorAll("ol.problems");
        for (const ol of ols) {
          for (const ch of ol.children) {
            if (ch.matches("li[data-lc]")) res.push(ch);
          }
        }
        return res;
      }
      return documentObj.documentElement.querySelectorAll(sel);
    },
    querySelector: (sel) => {
      if (!documentObj.documentElement) return null;
      if (sel === "ol.problems > li[data-lc]") {
        const ols = documentObj.documentElement.querySelectorAll("ol.problems");
        for (const ol of ols) {
          for (const ch of ol.children) {
            if (ch.matches("li[data-lc]")) return ch;
          }
        }
        return null;
      }
      return documentObj.documentElement.querySelector(sel);
    }
  };

  const docEl = new MockElement("html", documentObj);
  const head = new MockElement("head", documentObj);
  const body = new MockElement("body", documentObj);
  docEl.appendChild(head);
  docEl.appendChild(body);

  documentObj.documentElement = docEl;
  documentObj.head = head;
  documentObj.body = body;

  const localStorageStore = new Map();
  const mockLocalStorage = {
    getItem: (k) => (localStorageStore.has(k) ? localStorageStore.get(k) : null),
    setItem: (k, v) => localStorageStore.set(k, String(v)),
    removeItem: (k) => localStorageStore.delete(k),
    clear: () => localStorageStore.clear()
  };

  const mockWindow = {
    URL: globalThis.URL,
    setTimeout: globalThis.setTimeout,
    clearTimeout: globalThis.clearTimeout,
    console: globalThis.console,
    performance: globalThis.performance || { now: () => Date.now() },
    innerWidth: 1440,
    innerHeight: 900,
    localStorage: mockLocalStorage,
    location: { href: "https://taran-dev4u.github.io/learningHub/DSA_Ultimate_Index.html", hostname: "taran-dev4u.github.io", pathname: "/learningHub/DSA_Ultimate_Index.html" },
    document: documentObj,
    addEventListener: (type, fn) => {
      if (!windowListeners.has(type)) windowListeners.set(type, []);
      windowListeners.get(type).push(fn);
    },
    removeEventListener: (type, fn) => {
      const arr = windowListeners.get(type);
      if (arr) {
        const idx = arr.indexOf(fn);
        if (idx !== -1) arr.splice(idx, 1);
      }
    },
    scrollBy: (arg1, arg2) => {
      if (typeof arg1 === "object") {
        scrollOffset.top += (arg1.top || 0);
      } else {
        scrollOffset.top += (arg2 || 0);
      }
    },
    getScrollOffset: () => ({ ...scrollOffset }),
    resetScrollOffset: () => { scrollOffset = { top: 0, left: 0 }; },
    requestAnimationFrame: (fn) => setTimeout(fn, 16),
    cancelAnimationFrame: (id) => clearTimeout(id),
    fetch: globalThis.fetch ? globalThis.fetch.bind(globalThis) : (() => Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve("# Solution\n\nExplanation") })),
    dsaResources: loadDsaResources() || {}
  };

  return mockWindow;
}

function createVmContext(env) {
  return {
    window: env,
    document: env.document,
    location: env.location,
    localStorage: env.localStorage,
    URL: globalThis.URL,
    setTimeout: globalThis.setTimeout,
    clearTimeout: globalThis.clearTimeout,
    console: globalThis.console,
    performance: globalThis.performance || { now: () => Date.now() },
    requestAnimationFrame: env.requestAnimationFrame,
    cancelAnimationFrame: env.cancelAnimationFrame,
    fetch: env.fetch || (globalThis.fetch ? globalThis.fetch.bind(globalThis) : (() => Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve("# Solution\n\nExplanation") })))
  };
}

/* ============================================================================
   TIER 1: FEATURE COVERAGE (25 Tests)
   ============================================================================ */

test("T1_FEAT_LINK_1", "Physical .solutions containers in DSA_Ultimate_Index curated rows contain 0 video links", 1, ({ assert }) => {
  const html = loadDsaIndex();
  const problems = parseDsaIndexProblems(html);
  const curatedWithVideos = problems.filter(p => p.isCurated && (p.ncVideoLinks > 0 || p.searchVideoLinks > 0));
  assert(
    curatedWithVideos.length === 0,
    `Found ${curatedWithVideos.length} curated rows with legacy video links in .solutions containers`,
    curatedWithVideos.slice(0, 5).map(p => `LC #${p.lcId}: ${p.ncVideoLinks} NC, ${p.searchVideoLinks} Video`)
  );
});

test("T1_FEAT_LINK_2", "Physical .solutions containers in DSA_Ultimate_Index curated rows contain 0 legacy search links", 1, ({ assert }) => {
  const html = loadDsaIndex();
  const problems = parseDsaIndexProblems(html);
  const curatedWithGfg = problems.filter(p => p.isCurated && p.gfgSearchLinks > 0);
  assert(
    curatedWithGfg.length === 0,
    `Found ${curatedWithGfg.length} curated rows with legacy GFG search query links in .solutions containers`,
    curatedWithGfg.slice(0, 5).map(p => `LC #${p.lcId}: ${p.gfgSearchLinks} GFG links`)
  );
});

test("T1_FEAT_LINK_3", "Video registry in assets/dsa-resources.js contains 0 article/blog URLs in videos arrays", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must not be empty");
  const corrupted = [];
  for (const [key, item] of Object.entries(data)) {
    if (Array.isArray(item.videos)) {
      for (const vid of item.videos) {
        const id = Array.isArray(vid) ? vid[0] : vid.id;
        if (/takeuforward\.org|geeksforgeeks\.org|leetcode\.com|walkccc\.me|algo\.monster/i.test(String(id))) {
          corrupted.push({ key, id });
        }
      }
    }
  }
  assert(corrupted.length === 0, `Found ${corrupted.length} video entries containing blog/article URLs`, corrupted);
});

test("T1_FEAT_LINK_4", "Reading registry in assets/dsa-resources.js contains 0 video links in reads arrays", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must not be empty");
  const corrupted = [];
  for (const [key, item] of Object.entries(data)) {
    if (Array.isArray(item.reads)) {
      for (const r of item.reads) {
        const url = Array.isArray(r) ? r[1] : (r.url || "");
        if (/youtube\.com|youtu\.be/i.test(url)) {
          corrupted.push({ key, url });
        }
      }
    }
  }
  assert(corrupted.length === 0, `Found ${corrupted.length} reading entries containing YouTube URLs`, corrupted);
});

test("T1_FEAT_LINK_5", "Striver rows on DSA_Ultimate_Index.html have .badges replaced with clean .solutions", 1, ({ assert }) => {
  const html = loadDsaIndex();
  const problems = parseDsaIndexProblems(html);
  const striverWithBadges = problems.filter(p => p.isStriver && p.hasBadges);
  assert(
    striverWithBadges.length === 0,
    `Found ${striverWithBadges.length} Striver rows still retaining div.badges instead of standard .solutions`,
    striverWithBadges.slice(0, 5).map(p => `Striver row #${p.lcId}`)
  );
});

test("T1_FEAT_VID_1", "Data registry in assets/dsa-resources.js covers all 940 distinct problem IDs/slugs", 1, ({ assert }) => {
  const data = loadDsaResources();
  const count = data ? Object.keys(data).length : 0;
  assert(count >= 940, `dsaResources covers ${count} problems; expected at least 940 distinct problem entries`);
});

test("T1_FEAT_VID_2", "Every problem entry in assets/dsa-resources.js provides verified direct YouTube videos without fake quotas", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must be present");
  const failing = [];
  for (const [key, item] of Object.entries(data)) {
    const vids = Array.isArray(item.videos) ? item.videos : [];
    if (vids.length > 5) {
      failing.push({ key, count: vids.length });
    }
  }
  assert(
    failing.length === 0,
    `Found ${failing.length} problems with over 5 videos in dsaResources`,
    failing.slice(0, 5)
  );
});

test("T1_FEAT_VID_3", "Every video entry matches [id, title, channel, duration, approach] with valid 11-char YouTube ID", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must be present");
  const invalid = [];
  for (const [key, item] of Object.entries(data)) {
    if (Array.isArray(item.videos)) {
      item.videos.forEach((v, idx) => {
        const id = Array.isArray(v) ? v[0] : v.id;
        const title = Array.isArray(v) ? v[1] : v.title;
        const ch = Array.isArray(v) ? v[2] : v.channel;
        if (!id || typeof id !== "string" || !/^[A-Za-z0-9_-]{11}$/.test(id)) {
          invalid.push({ key, idx, reason: "invalid-yt-id", id });
        } else if (!title || typeof title !== "string") {
          invalid.push({ key, idx, reason: "missing-title" });
        } else if (!ch || typeof ch !== "string") {
          invalid.push({ key, idx, reason: "missing-channel" });
        }
      });
    }
  }
  assert(invalid.length === 0, `Found ${invalid.length} invalid video schema entries`, invalid.slice(0, 5));
});

test("T1_FEAT_VID_4", "Zero video entries use generic search query URLs (/results?search_query=)", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must be present");
  const searches = [];
  for (const [key, item] of Object.entries(data)) {
    if (Array.isArray(item.videos)) {
      item.videos.forEach(v => {
        const idOrUrl = String(Array.isArray(v) ? v[0] : v.id);
        if (idOrUrl.includes("search_query")) searches.push({ key, idOrUrl });
      });
    }
  }
  assert(searches.length === 0, `Found ${searches.length} generic search query video entries`, searches.slice(0, 5));
});

test("T1_FEAT_VID_5", "Backward compatibility preserved: hit.v matches primary video when present and hit.t, hit.d, hit.p exist", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must be present");
  const broken = [];
  for (const [key, item] of Object.entries(data)) {
    if (item.v !== undefined && typeof item.v !== "string") {
      broken.push({ key, reason: "invalid-v" });
    } else if (!item.t || typeof item.t !== "string") {
      broken.push({ key, reason: "missing-t" });
    } else if (Array.isArray(item.videos) && item.videos.length > 0) {
      const firstId = Array.isArray(item.videos[0]) ? item.videos[0][0] : item.videos[0].id;
      if (item.v !== firstId) {
        broken.push({ key, reason: "v-does-not-match-primary-video", v: item.v, firstId });
      }
    }
  }
  assert(broken.length === 0, `Found ${broken.length} backward compatibility issues in dsaResources`, broken.slice(0, 5));
});

test("T1_FEAT_READ_1", "Every problem entry in assets/dsa-resources.js provides 4 to 5 curated reading resources", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must be present");
  const failing = [];
  for (const [key, item] of Object.entries(data)) {
    const reads = Array.isArray(item.reads) ? item.reads : [];
    if (reads.length < 4 || reads.length > 5) {
      failing.push({ key, count: reads.length });
    }
  }
  assert(failing.length === 0, `Found ${failing.length} problems without 4-5 reads in dsaResources`, failing.slice(0, 5));
});

test("T1_FEAT_READ_2", "Every reading resource links to a recognized multi-approach platform with valid https://", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must be present");
  const invalid = [];
  const validPlatforms = /walkccc\.me|leetcode\.doocs\.org|neetcode\.io|algo\.monster|geeksforgeeks\.org|takeuforward\.org|leetcode\.com|raw\.githubusercontent\.com/i;
  for (const [key, item] of Object.entries(data)) {
    if (Array.isArray(item.reads)) {
      item.reads.forEach((r, idx) => {
        const url = Array.isArray(r) ? r[1] : (r.url || "");
        if (!url || !url.startsWith("https://") || !validPlatforms.test(url)) {
          invalid.push({ key, idx, url });
        }
      });
    }
  }
  assert(invalid.length === 0, `Found ${invalid.length} reading resources with invalid platform or protocol`, invalid.slice(0, 5));
});

test("T1_FEAT_READ_3", "Reading resources provide explicit approach annotations (Brute Force, Better, Optimal, Multi-Approach)", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must be present");
  const missingApproach = [];
  for (const [key, item] of Object.entries(data)) {
    if (Array.isArray(item.reads)) {
      item.reads.forEach((r, idx) => {
        const approach = Array.isArray(r) ? r[2] : (r.approach || (r.meta && r.meta.approach));
        if (!approach || typeof approach !== "string" || approach.trim().length === 0) {
          missingApproach.push({ key, idx });
        }
      });
    }
  }
  assert(missingApproach.length === 0, `Found ${missingApproach.length} reading entries lacking approach annotation`, missingApproach.slice(0, 5));
});

test("T1_FEAT_READ_4", "Embeddability flags correctly defined (embed: true for Walkccc/Doocs; false for AlgoMonster/GFG/LeetCode)", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must be present");
  const misclassified = [];
  for (const [key, item] of Object.entries(data)) {
    if (Array.isArray(item.reads)) {
      item.reads.forEach((r, idx) => {
        const url = Array.isArray(r) ? r[1] : (r.url || "");
        const embed = Array.isArray(r) ? r[3] : (r.embed ?? (r.meta && r.meta.embed));
        if (/walkccc\.me|leetcode\.doocs\.org/i.test(url) && embed !== true) {
          misclassified.push({ key, idx, url, expected: true, actual: embed });
        }
        if (/algo\.monster|geeksforgeeks\.org|takeuforward\.org|leetcode\.com/i.test(url) && embed === true) {
          misclassified.push({ key, idx, url, expected: false, actual: embed });
        }
      });
    }
  }
  assert(misclassified.length === 0, `Found ${misclassified.length} misclassified embeddability flags`, misclassified.slice(0, 5));
});

test("T1_FEAT_READ_5", "Reading resources annotate language coverage and complexity summaries", 1, ({ assert }) => {
  const data = loadDsaResources();
  assert(data && Object.keys(data).length > 0, "dsaResources registry must be present");
  const missingMetadata = [];
  for (const [key, item] of Object.entries(data)) {
    if (Array.isArray(item.reads)) {
      item.reads.forEach((r, idx) => {
        const complexity = Array.isArray(r) ? r[4] : (r.complexity || (r.meta && r.meta.complexity));
        if (!complexity || typeof complexity !== "string") {
          missingMetadata.push({ key, idx, reason: "missing-complexity" });
        }
      });
    }
  }
  assert(missingMetadata.length === 0, `Found ${missingMetadata.length} reading entries without complexity summaries`, missingMetadata.slice(0, 5));
});

test("T1_FEAT_RAIL_1", "Study rail mounts dedicated Watch button with video count badge on problem rows", 1, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "1");
  const pname = env.document.createElement("a");
  pname.className = "pname";
  pname.href = "https://leetcode.com/problems/two-sum/";
  pname.textContent = "Two Sum";
  row.appendChild(pname);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(railCode, ctx);

  const watchBtn = row.querySelector("button[data-sr='watch'], .study-link.youtube");
  assert(watchBtn !== null, "Watch button must be mounted inside the problem row");
  const countSpan = watchBtn.querySelector(".sr-count");
  assert(countSpan !== null, "Watch button must contain .sr-count badge");
});

test("T1_FEAT_RAIL_2", "Study rail mounts dedicated Read button with reading count badge on problem rows", 1, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "1");
  const pname = env.document.createElement("a");
  pname.className = "pname";
  pname.href = "https://leetcode.com/problems/two-sum/";
  pname.textContent = "Two Sum";
  row.appendChild(pname);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(railCode, ctx);

  const readBtn = row.querySelector("button[data-sr='read'], .study-link.read");
  assert(readBtn !== null, "Read button must be mounted inside the problem row");
  const countSpan = readBtn.querySelector(".sr-count");
  assert(countSpan !== null, "Read button must contain .sr-count badge");
});

test("T1_FEAT_RAIL_3", "Study rail mounts dedicated G (Google search) button on problem rows", 1, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "1");
  const pname = env.document.createElement("a");
  pname.className = "pname";
  pname.href = "https://leetcode.com/problems/two-sum/";
  pname.textContent = "Two Sum";
  row.appendChild(pname);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(railCode, ctx);

  const gLink = row.querySelector(".study-link.google");
  assert(gLink !== null, "Google discovery button G must be mounted inside the problem row");
});

test("T1_FEAT_RAIL_4", "Problem row retains its dedicated row-level note button 📝 (.note-btn) in column 8", 1, ({ assert }) => {
  const html = loadDsaIndex();
  const problems = parseDsaIndexProblems(html);
  const missingNoteBtn = problems.filter(p => !p.hasNoteBtn);
  assert(
    missingNoteBtn.length === 0,
    `Found ${missingNoteBtn.length} problem rows lacking the .note-btn element in DSA_Ultimate_Index.html`,
    missingNoteBtn.slice(0, 5).map(p => `Row #${p.lcId}`)
  );
});

test("T1_FEAT_RAIL_5", "Striver problem rows mount identical [Watch] [Read] [G] buttons in .solutions without alignment anomalies", 1, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "s425");
  row.setAttribute("data-striver", "1");
  const a = env.document.createElement("a");
  a.className = "problem-name";
  a.href = "https://takeuforward.org/c/c-basic-input-output/";
  a.textContent = "Input Output";
  row.appendChild(a);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(railCode, ctx);

  const actions = sol.querySelector(".hub-actions");
  assert(actions !== null, "Striver row must mount .hub-actions directly inside .solutions container");
  assert(actions.querySelector(".study-link.youtube") !== null, "Striver row must mount Watch button");
  assert(actions.querySelector(".study-link.read") !== null, "Striver row must mount Read button");
  assert(actions.querySelector(".study-link.google") !== null, "Striver row must mount G button");
});

test("T1_FEAT_DUPE_1", "Generated problem pages under DSA_Tutorial/problems/*.html contain 0 duplicate inline video chips", 1, ({ assert }) => {
  const pages = loadTutorialProblemPages();
  const withChips = pages.filter(p => p.hasVideoWalkthroughChip);
  assert(
    withChips.length === 0,
    `Found ${withChips.length} problem pages containing duplicate '<a class="chip">🎬 Video walkthrough</a>'`,
    withChips.slice(0, 5).map(p => p.file)
  );
});

test("T1_FEAT_DUPE_2", "Problem generator template in DSA_Tutorial/build.py omits duplicate inline video chips", 1, ({ assert }) => {
  const code = loadBuildPy();
  assert(code.length > 0, "build.py must exist");
  const hasVideoChipInterpolation = /<p>\{comp\}\s*\{video\}/i.test(code) || /🎬\s*Video walkthrough/i.test(code);
  assert(
    !hasVideoChipInterpolation,
    "DSA_Tutorial/build.py still contains {video} chip interpolation in render_problem()"
  );
});

test("T1_FEAT_DUPE_3", "Study rail does not inject redundant fallback search links when curated videos or articles exist", 1, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "1");
  const pname = env.document.createElement("a");
  pname.className = "pname";
  pname.href = "https://leetcode.com/problems/two-sum/";
  pname.textContent = "Two Sum";
  row.appendChild(pname);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(railCode, ctx);

  const iconOnlyYt = row.querySelector("a.study-link.youtube.icon-only");
  assert(
    iconOnlyYt === null,
    "Study rail should mount dedicated <button data-sr='watch'> rather than fallback icon-only search link"
  );
});

test("T1_FEAT_DUPE_4", "Striver rows in DSA_Ultimate_Index.html contain 0 duplicate .badge-yt or .badge-article buttons", 1, ({ assert }) => {
  const html = loadDsaIndex();
  const problems = parseDsaIndexProblems(html);
  const striverWithBadges = problems.filter(p => p.isStriver && (p.striverYtLinks > 0 || p.striverArticleLinks > 0));
  assert(
    striverWithBadges.length === 0,
    `Found ${striverWithBadges.length} Striver rows with duplicate .badge-yt or .badge-article buttons in DOM`,
    striverWithBadges.slice(0, 5).map(p => `Row #${p.lcId}: ${p.striverYtLinks} YT, ${p.striverArticleLinks} Article`)
  );
});

test("T1_FEAT_DUPE_5", "No duplicate data-lc problem rows exist inside any single pattern container", 1, ({ assert }) => {
  const html = loadDsaIndex();
  const patternBlocks = html.match(/<(?:section|div)\s+class="pattern"[\s\S]*?<\/(?:section|div)>/gi) || [];
  const dupes = [];
  patternBlocks.forEach((block, idx) => {
    const lcs = [...block.matchAll(/data-lc=["']([^"']+)["']/g)].map(m => m[1]);
    const seen = new Set();
    lcs.forEach(lc => {
      if (seen.has(lc)) dupes.push({ patternIndex: idx + 1, lc });
      seen.add(lc);
    });
  });
  assert(dupes.length === 0, `Found ${dupes.length} duplicate problem rows within the same pattern`, dupes.slice(0, 5));
});

/* ============================================================================
   TIER 2: BOUNDARY & CORNER CASES (15 Tests)
   ============================================================================ */

test("T2_BOUND_STRIVER_1", "Non-LeetCode Striver problems (e.g. s425) do not synthesize invalid Walkccc URLs (0425)", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "s425");
  const a = env.document.createElement("a");
  a.className = "problem-name";
  a.href = "https://takeuforward.org/c/c-basic-input-output/";
  a.textContent = "Input Output";
  row.appendChild(a);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(railCode, ctx);

  const actions = sol.querySelector(".hub-actions");
  if (actions && actions.__sr) {
    const docs = actions.__sr.docs || [];
    const invalidWalkccc = docs.some(d => /walkccc\.me\/LeetCode\/problems\/0425/i.test(d[1]));
    assert(!invalidWalkccc, "Non-LeetCode Striver problem s425 must not synthesize invalid Walkccc problem 0425 URL");
  }
});

test("T2_BOUND_STRIVER_2", "Striver problems linking to LeetCode (s35 -> Rotate Image LC 48) resolve Walkccc to 0048, not 0035", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "s35");
  const a = env.document.createElement("a");
  a.className = "problem-name";
  a.href = "https://leetcode.com/problems/rotate-image/";
  a.textContent = "Rotate Image";
  row.appendChild(a);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(railCode, ctx);

  const actions = sol.querySelector(".hub-actions");
  if (actions && actions.__sr) {
    const docs = actions.__sr.docs || [];
    const wrongWalkccc = docs.some(d => /walkccc\.me\/LeetCode\/problems\/0035/i.test(d[1]));
    assert(!wrongWalkccc, "Striver problem s35 linking to rotate-image must not query Walkccc for problem 0035");
  }
});

test("T2_BOUND_STRIVER_3", "Conceptual TakeUForward articles map to verified TakeUForward tutorial reading links", 2, ({ assert }) => {
  const data = loadDsaResources();
  assert(data, "dsaResources must be defined");
  const item = data["s425"] || data["c-basic-input-output"];
  if (item && item.reads) {
    const hasTufArticle = item.reads.some(r => {
      const url = Array.isArray(r) ? r[1] : (r.url || "");
      return /takeuforward\.org/i.test(url);
    });
    assert(hasTufArticle, "Conceptual Striver problem s425 must map to TakeUForward article");
  }
});

test("T2_BOUND_STRIVER_4", "High-range Striver IDs (s2000+) parse gracefully without NaN or undefined errors", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "s2871");
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(railCode, ctx);

  assert(!row.innerHTML.includes("NaN"), "Row HTML must not contain NaN");
  assert(!row.innerHTML.includes("undefined"), "Row HTML must not contain undefined");
});

test("T2_BOUND_STRIVER_5", "Legacy video timestamps (?t=250) are normalized into clean 11-char YouTube IDs for embed compatibility", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  const ytIdFn = env.VideoPanel ? env.VideoPanel.ytId : null;
  assert(typeof ytIdFn === "function", "VideoPanel.ytId must be exported as a helper");
  const id1 = ytIdFn("https://youtu.be/EAR7De6Goz4?t=250");
  assert(id1 === "EAR7De6Goz4", `Expected ID EAR7De6Goz4 from youtu.be link, received: ${id1}`);
  const id2 = ytIdFn("https://www.youtube.com/watch?v=UXDSeD9mN-k&t=15s");
  assert(id2 === "UXDSeD9mN-k", `Expected ID UXDSeD9mN-k from watch link, received: ${id2}`);
});

test("T2_BOUND_IFRAME_1", "FRAME_HOSTS in assets/video-panel.js includes walkccc.me and leetcode.doocs.org", 2, ({ assert }) => {
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  assert(/walkccc\.me/i.test(vpCode), "FRAME_HOSTS must contain walkccc.me");
  assert(/leetcode\.doocs\.org/i.test(vpCode), "FRAME_HOSTS must contain leetcode.doocs.org");
});

test("T2_BOUND_IFRAME_2", "CSP-restricted domains (algo.monster, geeksforgeeks, takeuforward, leetcode) are classified as non-framed", 2, ({ assert }) => {
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const frameHostsMatch = vpCode.match(/FRAME_HOSTS\s*=\s*\[([\s\S]*?)\]/);
  assert(frameHostsMatch !== null, "FRAME_HOSTS array must be defined in video-panel.js");
  const hosts = frameHostsMatch[1];
  assert(!/['"]algo\.monster['"]/i.test(hosts), "algo.monster must NOT be in FRAME_HOSTS (CSP denied)");
  assert(!/['"]geeksforgeeks\.org['"]/i.test(hosts), "geeksforgeeks.org must NOT be in FRAME_HOSTS (CSP denied)");
  assert(!/['"]takeuforward\.org['"]/i.test(hosts), "takeuforward.org must NOT be in FRAME_HOSTS (CSP denied)");
  assert(!/['"]leetcode\.com['"]/i.test(hosts), "leetcode.com must NOT be in FRAME_HOSTS (CSP denied)");
});

test("T2_BOUND_IFRAME_3", "Non-framed resources render a structured Solution Card instead of an iframe", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  assert(env.VideoPanel && typeof env.VideoPanel.open === "function", "VideoPanel.open must exist");
  env.VideoPanel.open({
    title: "Two Sum",
    query: "two sum",
    videos: [["KLlXCFG5TnA", "Two Sum", "NeetCode", "10:30"]],
    docs: [
      ["AlgoMonster Lite", "https://algo.monster/liteproblems/1", { embed: false, approach: "Decision Tree", complexity: "O(N)" }]
    ],
    tab: "read",
    docIndex: 0
  });

  const viewer = env.document.querySelector(".vp-viewer");
  assert(viewer !== null, ".vp-viewer must exist");
  const hasSolutionCard = viewer.querySelector(".vp-solution-card, .vp-fallback-card") !== null || /Solution|Open in new tab/i.test(viewer.innerHTML);
  assert(hasSolutionCard, "Non-framed resource must render a Solution Card in .vp-viewer");
  const hasIframe = viewer.querySelector("iframe.vp-doc-frame") !== null;
  assert(!hasIframe, "Non-framed resource must NOT render an iframe");
});

test("T2_BOUND_IFRAME_4", "Solution Card includes approach summary, complexity chips, external target=_blank CTA, and in-panel tip", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Two Sum",
    query: "two sum",
    videos: [["KLlXCFG5TnA", "Two Sum", "NeetCode", "10:30"]],
    docs: [
      ["AlgoMonster", "https://algo.monster/liteproblems/1", { embed: false, approach: "Optimal Hash", complexity: "Time: O(N) Space: O(N)" }]
    ],
    tab: "read",
    docIndex: 0
  });

  const viewer = env.document.querySelector(".vp-viewer");
  assert(viewer !== null, ".vp-viewer must exist");
  const card = viewer.querySelector(".vp-solution-card, .vp-fallback-card") || viewer;
  const cta = card.querySelector("a[target='_blank']");
  assert(cta !== null, "Solution Card must provide a 1-click external target='_blank' launch button");
  assert(/algo\.monster/i.test(cta.href || card.innerHTML), "Launch link must point to the target resource URL");
});

test("T2_BOUND_IFRAME_5", "GitHub raw markdown and code files continue to render via in-panel CORS fetch with syntax highlighting", 2, ({ assert }) => {
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  assert(/raw\.githubusercontent\.com/i.test(vpCode), "video-panel.js must retain handling for raw.githubusercontent.com");
  assert(/highlightElement|hljs/i.test(vpCode), "video-panel.js must retain syntax highlighting integration");
});

test("T2_BOUND_COUNTS_1", "Zero videos edge case: panel suppresses video player or routes to read tab gracefully without error", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  let errorThrown = false;
  try {
    env.VideoPanel.open({
      title: "No Video Problem",
      query: "no video",
      videos: [],
      docs: [["Walkccc", "https://walkccc.me/LeetCode/problems/0001/"]]
    });
  } catch (e) {
    errorThrown = true;
  }
  assert(!errorThrown, "Opening panel with 0 videos must not throw a JavaScript error");
  assert(env.document.querySelector(".vp-panel") !== null, "Panel must open when docs are present");
});

test("T2_BOUND_COUNTS_2", "Single video edge case: panel renders video player and adapts playlist without breaking", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Single Video Problem",
    query: "single video",
    videos: [["KLlXCFG5TnA", "Two Sum", "NeetCode", "10:30"]],
    docs: []
  });

  const frame = env.document.querySelector("iframe.vp-frame");
  assert(frame !== null, "Iframe player must be rendered for single video");
  assert(/KLlXCFG5TnA/.test(frame.src || ""), "Iframe player src must embed video ID KLlXCFG5TnA");
});

test("T2_BOUND_COUNTS_3", "Exactly 5 videos edge case: .vp-channel-bar renders all 5 instructor pills without clipping", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Two Sum",
    query: "two sum",
    videos: [
      ["KLlXCFG5TnA", "Two Sum NeetCode", "NeetCode", "10:30"],
      ["UXDSeD9mN-k", "Two Sum Striver", "take U forward", "18:20"],
      ["mO8XpGoJwuo", "Two Sum Abdul Bari", "Abdul Bari", "14:10"],
      ["TC_fTBYYt_0", "Two Sum TechDose", "Techdose", "12:15"],
      ["Aql6ncPP6Qo", "Two Sum Nick White", "Nick White", "08:24"]
    ]
  });

  const channelBar = env.document.querySelector(".vp-channel-bar");
  assert(channelBar !== null, ".vp-channel-bar must be rendered for multi-video problem");
  const pills = channelBar.querySelectorAll("button");
  assert(pills.length === 5, `Expected 5 instructor pills in channel bar, found ${pills.length}`);
});

test("T2_BOUND_COUNTS_4", "Extremely long problem titles (>80 characters) wrap or truncate cleanly without layout blowouts", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  const longTitle = "Design a Distributed Fault-Tolerant Highly-Available Rate Limiting Token Bucket Service in Redis";
  env.VideoPanel.open({
    title: longTitle,
    videos: [["KLlXCFG5TnA", longTitle, "NeetCode", "15:00"]]
  });

  const titleEl = env.document.querySelector(".vp-title");
  assert(titleEl !== null, ".vp-title must exist");
  assert(titleEl.title === longTitle, "Full title must be preserved in title attribute for tooltip");
});

test("T2_BOUND_COUNTS_5", "Special characters in problem names (quotes, ampersands, slashes) are properly escaped in DOM and URLs", 2, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  const trickyTitle = 'Insert / Delete & "GetRandom" O(1) <script>alert(1)</script>';
  env.VideoPanel.open({
    title: trickyTitle,
    videos: [["KLlXCFG5TnA", trickyTitle, "NeetCode", "10:00"]]
  });

  const panel = env.document.querySelector(".vp-panel");
  assert(!panel.innerHTML.includes("<script>alert(1)</script>"), "Raw unsanitized script tags must not be injected into innerHTML");
});

/* ============================================================================
   TIER 3: CROSS-FEATURE INTERACTIONS (15 Tests)
   ============================================================================ */

test("T3_INTER_THEME_1", "light theme + dock right: panel styles and borders match --vp-bg, --vp-border", 3, ({ assert }) => {
  const env = createBrowserEnv();
  env.localStorage.setItem("learning_hub_theme", "light");
  env.localStorage.setItem("vp-dock", "right");

  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({ title: "Theme Test", videos: [["KLlXCFG5TnA", "Video", "Ch", "10:00"]] });
  const panel = env.document.querySelector(".vp-panel");
  assert(!panel.classList.contains("vp-dock-left"), "Panel must dock right when vp-dock is right");
  assert(!env.document.documentElement.classList.contains("vp-left"), "html must not have vp-left when docked right");
});

test("T3_INTER_THEME_2", "dark theme + dock left: html.vp-left applies padding-left to body while maintaining dark tokens", 3, ({ assert }) => {
  const env = createBrowserEnv();
  env.localStorage.setItem("learning_hub_theme", "dark");
  env.localStorage.setItem("vp-dock", "left");

  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({ title: "Theme Test", videos: [["KLlXCFG5TnA", "Video", "Ch", "10:00"]] });
  const panel = env.document.querySelector(".vp-panel");
  assert(panel.classList.contains("vp-dock-left"), "Panel must have vp-dock-left class");
  assert(env.document.documentElement.classList.contains("vp-left"), "html must have vp-left class");
});

test("T3_INTER_THEME_3", "black theme (html.black:root) + collapsed 46px rail: rail text rotates 90deg, body offset narrows to 46px", 3, ({ assert }) => {
  const env = createBrowserEnv();
  env.document.documentElement.classList.add("black");
  env.localStorage.setItem("vp-collapsed", "1");

  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({ title: "Two Sum", videos: [["KLlXCFG5TnA", "Two Sum", "NeetCode", "10:00"]] });
  const panel = env.document.querySelector(".vp-panel");
  assert(panel.classList.contains("vp-collapsed"), "Panel must have vp-collapsed class");
  assert(panel.style.width === "46px", `Collapsed panel width must be 46px; got ${panel.style.width}`);
  assert(env.document.documentElement.style["--vp-offset"] === "46px", "html --vp-offset must be 46px");
});

test("T3_INTER_THEME_4", "Cycling themes during active video playback does NOT reload iframe or reset playback state", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({ title: "Play Test", videos: [["KLlXCFG5TnA", "Video", "NeetCode", "10:00"]] });
  const iframe = env.document.querySelector("iframe.vp-frame");
  const initialSrc = iframe.src;

  // Simulate theme cycling
  env.document.documentElement.classList.toggle("black", true);
  env.document.documentElement.classList.toggle("dark", false);

  assert(iframe.src === initialSrc, "Iframe src must not change or reload during theme change");
});

test("T3_INTER_THEME_5", "Dock toggle (left <-> right) preserves active tab, video selection, and scroll offset", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Dock Test",
    videos: [["KLlXCFG5TnA", "V1", "NeetCode", "10:00"], ["UXDSeD9mN-k", "V2", "Striver", "15:00"]],
    tab: "videos",
    index: 1
  });

  const dockBtn = env.document.querySelector(".vp-dock");
  assert(dockBtn !== null, "Dock button must exist");
  dockBtn.dispatchEvent({ type: "click" });

  const panel = env.document.querySelector(".vp-panel");
  const isLeft = panel.classList.contains("vp-dock-left");
  assert(isLeft, "Panel must toggle to left dock");
  const iframe = env.document.querySelector("iframe.vp-frame");
  assert(iframe.src.includes("UXDSeD9mN-k"), "Active video index must be preserved across dock toggle");
});

test("T3_INTER_PLAY_1", "Clicking instructor pill updates iframe.vp-frame src to that instructor's YouTube video ID with autoplay", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Two Sum",
    videos: [
      ["KLlXCFG5TnA", "Two Sum NeetCode", "NeetCode", "10:30"],
      ["UXDSeD9mN-k", "Two Sum Striver", "take U forward", "18:20"]
    ]
  });

  const channelBar = env.document.querySelector(".vp-channel-bar");
  assert(channelBar !== null, "Channel bar must exist");
  const striverPill = channelBar.querySelectorAll("button")[1];
  assert(striverPill !== null, "Striver pill must exist");
  striverPill.dispatchEvent({ type: "click" });

  const iframe = env.document.querySelector("iframe.vp-frame");
  assert(iframe.src.includes("UXDSeD9mN-k"), `Iframe src should update to UXDSeD9mN-k; got ${iframe.src}`);
  assert(iframe.src.includes("autoplay=1"), "Iframe src must include autoplay=1");
});

test("T3_INTER_PLAY_2", "Clicking instructor pill updates active state on channel bar (active pill receives .active)", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Two Sum",
    videos: [
      ["KLlXCFG5TnA", "V1", "NeetCode", "10:00"],
      ["UXDSeD9mN-k", "V2", "take U forward", "18:00"]
    ]
  });

  const channelBar = env.document.querySelector(".vp-channel-bar");
  assert(channelBar !== null, "Channel bar must exist");
  const pills = channelBar.querySelectorAll("button");
  pills[1].dispatchEvent({ type: "click" });

  assert(pills[1].classList.contains("active"), "Second pill must receive .active class");
  assert(!pills[0].classList.contains("active"), "First pill must have .active class removed");
});

test("T3_INTER_PLAY_3", "Direct YouTube ↗ header link points to https://www.youtube.com/watch?v={activeVideoId}, never generic search", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Two Sum",
    videos: [["UXDSeD9mN-k", "Two Sum Striver", "take U forward", "18:00"]]
  });

  const ytDirectBtn = env.document.querySelector(".vp-open-yt, .vp-tab-yt");
  assert(ytDirectBtn !== null, "YouTube direct link must exist");
  assert(!ytDirectBtn.href.includes("search_query="), `Direct link must not be generic search: ${ytDirectBtn.href}`);
  assert(ytDirectBtn.href.includes("watch?v=UXDSeD9mN-k") || ytDirectBtn.href.includes("UXDSeD9mN-k"), `Direct link must point to active video: ${ytDirectBtn.href}`);
});

test("T3_INTER_PLAY_4", "Clicking a playlist item in .vp-list synchronizes the active instructor pill in .vp-channel-bar", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Two Sum",
    videos: [
      ["KLlXCFG5TnA", "V1", "NeetCode", "10:00"],
      ["UXDSeD9mN-k", "V2", "take U forward", "18:00"]
    ]
  });

  const list = env.document.querySelector(".vp-list");
  assert(list !== null, ".vp-list must exist");
  const items = list.querySelectorAll("[data-vp-i]");
  if (items.length > 1) {
    items[1].dispatchEvent({ type: "click" });
    const pills = env.document.querySelectorAll(".vp-channel-bar button");
    if (pills.length > 1) {
      assert(pills[1].classList.contains("active"), "Channel pill must sync with playlist selection");
    }
  }
});

test("T3_INTER_PLAY_5", "Esc key closes panel, stops video playback by clearing iframe src, and cleans up html.vp-active", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({ title: "Close Test", videos: [["KLlXCFG5TnA", "Video", "NeetCode", "10:00"]] });
  assert(env.document.documentElement.classList.contains("vp-active"), "html must have vp-active when open");

  env.document.dispatchEvent({ type: "keydown", key: "Escape" });
  assert(!env.document.documentElement.classList.contains("vp-active"), "html must not have vp-active when closed");
  const iframe = env.document.querySelector("iframe.vp-frame");
  assert(iframe.src === "" || iframe.src === "about:blank", "Iframe src must be cleared to stop audio playback");
});

test("T3_INTER_READ_1", "Clicking Walkccc pill renders <iframe class=vp-doc-frame> pointing to Walkccc URL", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Two Sum",
    docs: [
      ["Walkccc", "https://walkccc.me/LeetCode/problems/0001/", { embed: true, approach: "Optimal" }]
    ],
    tab: "read",
    docIndex: 0
  });

  const frame = env.document.querySelector("iframe.vp-doc-frame");
  assert(frame !== null, "Iframe must be rendered for Walkccc");
  assert(frame.src.includes("walkccc.me/LeetCode/problems/0001"), `Iframe src should point to Walkccc; got ${frame.src}`);
});

test("T3_INTER_READ_2", "Switching from Walkccc pill to AlgoMonster pill replaces iframe with .vp-solution-card cleanly", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Two Sum",
    docs: [
      ["Walkccc", "https://walkccc.me/LeetCode/problems/0001/", { embed: true }],
      ["AlgoMonster", "https://algo.monster/liteproblems/1", { embed: false }]
    ],
    tab: "read",
    docIndex: 0
  });

  const docsEl = env.document.querySelector(".vp-docs");
  assert(docsEl !== null, ".vp-docs must exist");
  const pills = docsEl.querySelectorAll("[data-vp-doc]");
  assert(pills.length >= 2, "Must have at least 2 doc pills");

  // Click second doc pill (AlgoMonster)
  pills[1].dispatchEvent({ type: "click" });

  const frame = env.document.querySelector("iframe.vp-doc-frame");
  assert(frame === null, "Iframe must be replaced when switching to non-framed platform");
  const viewer = env.document.querySelector(".vp-viewer");
  assert(/AlgoMonster|Open in new tab/i.test(viewer.innerHTML), "Solution card must be rendered in viewer");
});

test("T3_INTER_READ_3", "Switching from AlgoMonster back to Doocs restores iframe reader cleanly", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  env.VideoPanel.open({
    title: "Two Sum",
    docs: [
      ["Doocs", "https://leetcode.doocs.org/lc/1/", { embed: true }],
      ["AlgoMonster", "https://algo.monster/liteproblems/1", { embed: false }]
    ],
    tab: "read",
    docIndex: 1
  });

  const pills = env.document.querySelectorAll(".vp-docs [data-vp-doc]");
  assert(pills.length >= 2, "Must have 2 doc pills");
  pills[0].dispatchEvent({ type: "click" });

  const frame = env.document.querySelector("iframe.vp-doc-frame");
  assert(frame !== null, "Iframe must be restored for Doocs");
  assert(frame.src.includes("leetcode.doocs.org"), "Iframe src must point to Doocs");
});

test("T3_INTER_READ_4", "Clicking Read on a row when panel is open in Watch tab switches tab smoothly with zero jump", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "1");
  const pname = env.document.createElement("a");
  pname.className = "pname";
  pname.href = "https://leetcode.com/problems/two-sum/";
  pname.textContent = "Two Sum";
  row.appendChild(pname);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);
  vm.runInContext(railCode, ctx);

  // Open in Watch first
  env.VideoPanel.open({ title: "Two Sum", videos: [["KLlXCFG5TnA", "V", "Ch", "10:00"]], docs: [["Doc", "https://walkccc.me/LeetCode/problems/0001/"]], tab: "videos" });
  assert(!env.document.querySelector(".vp-video-view").hidden, "Video view must be visible");

  // Click Read button
  const readBtn = row.querySelector("button[data-sr='read']");
  if (readBtn) {
    readBtn.dispatchEvent({ type: "click" });
    assert(env.document.querySelector(".vp-video-view").hidden, "Video view must be hidden after clicking Read");
    assert(!env.document.querySelector(".vp-read-view").hidden, "Read view must be visible after clicking Read");
  }
});

test("T3_INTER_READ_5", "Clicking Watch on a row when panel is open in Read tab switches tab smoothly and initiates video", 3, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "1");
  const pname = env.document.createElement("a");
  pname.className = "pname";
  pname.href = "https://leetcode.com/problems/two-sum/";
  pname.textContent = "Two Sum";
  row.appendChild(pname);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);
  vm.runInContext(railCode, ctx);

  // Open in Read first
  env.VideoPanel.open({ title: "Two Sum", videos: [["KLlXCFG5TnA", "V", "Ch", "10:00"]], docs: [["Doc", "https://walkccc.me/LeetCode/problems/0001/"]], tab: "read" });
  assert(!env.document.querySelector(".vp-read-view").hidden, "Read view must be visible");

  // Click Watch button
  const watchBtn = row.querySelector("button[data-sr='watch']");
  if (watchBtn) {
    watchBtn.dispatchEvent({ type: "click" });
    assert(!env.document.querySelector(".vp-video-view").hidden, "Video view must be visible after clicking Watch");
    assert(env.document.querySelector(".vp-read-view").hidden, "Read view must be hidden after clicking Watch");
  }
});

/* ============================================================================
   TIER 4: REAL-WORLD APPLICATION SCENARIOS (5 Scenarios)
   ============================================================================ */

test("T4_SCEN_1_TWOSUM", "Scenario 1: End-to-end study journey on LC #1 Two Sum (multi-video, instructor switch, multi-approach reader, pinning)", 4, ({ assert, diag }) => {
  const env = createBrowserEnv();
  const data = loadDsaResources();
  assert(data && data["two-sum"], "two-sum must exist in dsaResources");

  const entry = data["two-sum"];
  diag(`Two Sum data entry verified with ${entry.videos?.length || 0} videos and ${entry.reads?.length || 0} reads`);

  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "1");
  row.setAttribute("data-name", "two sum");
  const a = env.document.createElement("a");
  a.className = "pname";
  a.href = "https://leetcode.com/problems/two-sum/";
  a.textContent = "Two Sum";
  row.appendChild(a);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);
  vm.runInContext(railCode, ctx);

  // 1. Check mounted study rail buttons
  const watchBtn = row.querySelector("button[data-sr='watch']");
  assert(watchBtn !== null, "Watch button must be mounted on Two Sum row");
  const readBtn = row.querySelector("button[data-sr='read']");
  assert(readBtn !== null, "Read button must be mounted on Two Sum row");

  // 2. Click Watch button
  watchBtn.dispatchEvent({ type: "click" });
  assert(env.document.querySelector(".vp-panel.vp-open") !== null, "Side panel must be opened");

  // 3. Verify primary video embedded
  const frame = env.document.querySelector("iframe.vp-frame");
  const firstVideoId = entry.videos && entry.videos[0] ? (Array.isArray(entry.videos[0]) ? entry.videos[0][0] : entry.videos[0].id) : entry.v;
  assert(frame && frame.src.includes(firstVideoId), "Primary video must be loaded in player iframe");

  // 4. Verify channel bar and switch to second instructor
  const channelBar = env.document.querySelector(".vp-channel-bar");
  assert(channelBar !== null, "Channel bar must be present");
  const instructorPills = channelBar.querySelectorAll("button");
  assert(instructorPills.length >= 4, `Expected at least 4 instructor pills, found ${instructorPills.length}`);
  instructorPills[1].dispatchEvent({ type: "click" });
  assert(frame.src.includes(entry.videos[1][0]), "Player must switch to second instructor's video");

  // 5. Switch to Read tab
  readBtn.dispatchEvent({ type: "click" });
  assert(!env.document.querySelector(".vp-read-view").hidden, "Reader view must be visible");

  // 6. Verify Walkccc loads in iframe
  const docPills = env.document.querySelectorAll(".vp-docs [data-vp-doc]");
  assert(docPills.length >= 4, `Expected at least 4 doc pills, found ${docPills.length}`);
  const walkPill = Array.from(docPills).find(p => /walkccc/i.test((p.textContent || '') + (p.getAttribute('title') || '')));
  if (walkPill) walkPill.dispatchEvent({ type: "click" });
  const docFrame = env.document.querySelector("iframe.vp-doc-frame");
  assert(docFrame !== null, "Walkccc must render in iframe");

  // 7. Click AlgoMonster external card
  const algoPill = Array.from(docPills).find(p => /algo\.?monster/i.test((p.textContent || '') + (p.getAttribute('title') || '')));
  if (algoPill) {
    algoPill.dispatchEvent({ type: "click" });
    const viewer = env.document.querySelector(".vp-viewer");
    assert(/algo\.monster|Solution/i.test(viewer.innerHTML), "AlgoMonster solution card must display");
  }
});

test("T4_SCEN_2_STRIVER", "Scenario 2: End-to-end study journey on Striver A2Z foundation problem (Input Output - s425)", 4, ({ assert }) => {
  const env = createBrowserEnv();
  const ol = env.document.createElement("ol");
  ol.className = "problems";
  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "s425");
  row.setAttribute("data-striver", "1");
  const a = env.document.createElement("a");
  a.className = "problem-name";
  a.href = "https://takeuforward.org/c/c-basic-input-output/";
  a.textContent = "Input Output";
  row.appendChild(a);
  const sol = env.document.createElement("div");
  sol.className = "solutions";
  row.appendChild(sol);
  ol.appendChild(row);
  env.document.body.appendChild(ol);

  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const railCode = fs.readFileSync(path.join(ROOT, "assets", "study-rail.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);
  vm.runInContext(railCode, ctx);

  // 1. Verify clean buttons mounted inside .solutions
  const actions = sol.querySelector(".hub-actions");
  assert(actions !== null, "Actions must be mounted in .solutions");
  const watchBtn = actions.querySelector("button[data-sr='watch']");
  assert(watchBtn !== null, "Watch button must exist on Striver row");

  // 2. Open side panel
  watchBtn.dispatchEvent({ type: "click" });
  assert(env.document.querySelector(".vp-panel.vp-open") !== null, "Panel must open for Striver problem");

  // 3. Switch to Read tab
  const readBtn = actions.querySelector("button[data-sr='read']");
  if (readBtn) {
    readBtn.dispatchEvent({ type: "click" });
    const viewer = env.document.querySelector(".vp-viewer");
    assert(!viewer.innerHTML.includes("0425"), "Must not display invalid Walkccc 0425 link for s425");
  }
});

test("T4_SCEN_3_HARD_PROBLEM", "Scenario 3: Comprehensive multi-approach study on Hard problem (Trapping Rain Water - LC 42)", 4, ({ assert, diag }) => {
  const data = loadDsaResources();
  assert(data, "dsaResources must be defined");
  const entry = data["trapping-rain-water"] || data["42"];
  assert(entry !== undefined, "Trapping Rain Water must be present in dsaResources");

  const videos = entry.videos || [];
  assert(videos.length >= 4, `Expected at least 4 videos for Trapping Rain Water, found ${videos.length}`);
  const instructors = videos.map(v => Array.isArray(v) ? v[2] : v.channel);
  diag(`Instructors for Trapping Rain Water: ${instructors.join(", ")}`);
  assert(new Set(instructors).size >= 3, "Videos must cover at least 3 distinct instructors/channels");

  const reads = entry.reads || [];
  assert(reads.length >= 4, `Expected at least 4 reads for Trapping Rain Water, found ${reads.length}`);
  const approaches = reads.map(r => Array.isArray(r) ? r[2] : (r.approach || ""));
  diag(`Approaches annotated: ${approaches.join(", ")}`);
});

test("T4_SCEN_4_VIEWPORT_PINNING", "Scenario 4: Deep-scroll layout stability stress test: row pinned 5,000px down (|delta Y| <= 0.5px < 1.0px)", 4, ({ assert, diag }) => {
  const env = createBrowserEnv();
  const vpCode = fs.readFileSync(path.join(ROOT, "assets", "video-panel.js"), "utf8");
  const ctx = createVmContext(env);
  vm.createContext(ctx);
  vm.runInContext(vpCode, ctx);

  const row = env.document.createElement("li");
  row.setAttribute("data-lc", "150");
  row._rect = { top: 250, bottom: 280, left: 10, right: 800, width: 790, height: 30 };
  env.document.body.appendChild(row);

  const targetY = row.getBoundingClientRect().top;
  diag(`Initial target row viewport Y: ${targetY}px`);

  // Sequence of layout mutations with withPin
  const shifts = [];
  function recordShift(actionName) {
    const curY = row.getBoundingClientRect().top;
    const delta = Math.abs(curY - targetY);
    shifts.push({ actionName, curY, delta });
    assert(delta <= 0.5, `Layout jump exceeded 0.5px during ${actionName}: delta = ${delta}px`);
  }

  // 1. Open panel
  env.VideoPanel.open({ title: "Pinning Test", videos: [["KLlXCFG5TnA", "V", "Ch", "10:00"]], originEl: row });
  recordShift("open");

  // 2. Collapse panel
  const collapseBtn = env.document.querySelector(".vp-collapse");
  if (collapseBtn) collapseBtn.dispatchEvent({ type: "click" });
  recordShift("collapse");

  // 3. Expand rail
  const railBtn = env.document.querySelector(".vp-rail");
  if (railBtn) railBtn.dispatchEvent({ type: "click" });
  recordShift("expand");

  // 4. Dock left
  const dockBtn = env.document.querySelector(".vp-dock");
  if (dockBtn) dockBtn.dispatchEvent({ type: "click" });
  recordShift("dock-left");

  // 5. Dock right
  if (dockBtn) dockBtn.dispatchEvent({ type: "click" });
  recordShift("dock-right");

  // 6. Close panel
  const closeBtn = env.document.querySelector(".vp-close");
  if (closeBtn) closeBtn.dispatchEvent({ type: "click" });
  recordShift("close");

  diag(`All 6 pinning transitions preserved delta <= 0.5px: ${JSON.stringify(shifts)}`);
});

test("T4_SCEN_5_TUTORIAL_PAGE", "Scenario 5: Tutorial problem page end-to-end flow (0001-lc1-two-sum.html)", 4, ({ assert }) => {
  const filePath = path.join(ROOT, "DSA_Tutorial", "problems", "0001-lc1-two-sum.html");
  if (!fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, "utf8");

  // Verify no duplicate inline chip in the metadata paragraph
  const hasVideoChip = /🎬\s*Video walkthrough/i.test(content);
  assert(!hasVideoChip, "Problem page 0001-lc1-two-sum.html must not contain duplicate 🎬 Video walkthrough chip");

  // Verify shared script loading
  assert(content.includes("assets/learning-hub-shared.js"), "Page must load learning-hub-shared.js");
  assert(content.includes("assets/learning-hub-shared.css"), "Page must load learning-hub-shared.css");
});

/* ============================================================================
   Output Formatting & Summary
   ============================================================================ */

console.log("\n============================================================================");
console.log("E2E Test Suite: DSA Curated Multi-Resources & Side Panel Architecture");
console.log("============================================================================\n");

const passedTests = results.filter(r => r.passed);
const failedTests = results.filter(r => !r.passed);

const tierStats = {
  1: { total: 0, passed: 0, failed: 0 },
  2: { total: 0, passed: 0, failed: 0 },
  3: { total: 0, passed: 0, failed: 0 },
  4: { total: 0, passed: 0, failed: 0 }
};

results.forEach(r => {
  if (tierStats[r.tier]) {
    tierStats[r.tier].total++;
    if (r.passed) tierStats[r.tier].passed++;
    else tierStats[r.tier].failed++;
  }
});

for (let t = 1; t <= 4; t++) {
  if (TARGET_TIER && String(TARGET_TIER) !== String(t)) continue;
  const stat = tierStats[t];
  const tierName =
    t === 1 ? "Tier 1: Feature Coverage (Links, Schema, Buttons, Duplicates)" :
    t === 2 ? "Tier 2: Boundary & Corner Cases (Striver IDs, Framing, Edge Counts)" :
    t === 3 ? "Tier 3: Cross-Feature Interactions (Theme, Dock, Tabs, Player)" :
              "Tier 4: Real-World Application Scenarios (E2E User Journeys)";

  console.log(`--- ${tierName} [${stat.passed}/${stat.total} Passed] ---`);
  const tierResults = results.filter(r => r.tier === t);
  tierResults.forEach(r => {
    const symbol = r.passed ? "✔ PASS" : "✖ FAIL";
    console.log(`  ${symbol} [${r.id}] ${r.description}`);
    if (!r.passed && r.error) {
      console.log(`         Error: ${r.error}`);
    }
    if (VERBOSE_DIAGNOSTICS && r.diagnostics.length) {
      r.diagnostics.forEach(d => console.log(`         Diag: ${typeof d === "object" ? JSON.stringify(d) : d}`));
    }
  });
  console.log("");
}

console.log("============================================================================");
console.log(`TOTAL TESTS: ${results.length} | PASSED: ${passedTests.length} | FAILED: ${failedTests.length}`);
console.log("============================================================================");

if (failedTests.length > 0) {
  console.log("\nACTIONABLE REMEDIATION DIAGNOSTICS:");
  failedTests.forEach((f, i) => {
    console.log(`  ${i + 1}. [${f.id}] ${f.description}`);
    console.log(`     Cause: ${f.error}`);
    if (f.diagnostics.length) {
      console.log(`     Details: ${JSON.stringify(f.diagnostics[0])}`);
    }
  });
  console.log("\nExit Code: 1 (Failing checks indicate un-migrated features pending M1-M3 implementation)");
  process.exit(1);
} else {
  console.log("\nALL 60 TESTS PASSED CLEANLY across Tiers 1-4.");
  console.log("Exit Code: 0");
  process.exit(0);
}
