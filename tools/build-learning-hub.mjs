import fs from "node:fs";
import path from "node:path";

const root = process.cwd();

const sourceDefs = [
  {
    key: "dsa",
    title: "DSA Ultimate Index",
    file: "DSA_Ultimate_Index.html",
    kind: "problem",
    label: "DSA",
    color: "#2f6fdd",
    storage: { done: "dsa_index_solved_v1", bookmark: "dsa_index_bookmark_v1" },
    summary: "Pattern-first LeetCode prep with company tags, lists, notes, and a 14-week plan.",
  },
  {
    key: "sd",
    title: "System Design",
    file: "system_design.html",
    kind: "concept",
    label: "Systems",
    color: "#d84f86",
    storage: { done: "hub_done_sd", bookmark: "hub_bm_sd" },
    summary: "Distributed systems, architecture patterns, reliability, security, and classic designs.",
  },
  {
    key: "cs",
    title: "CS Fundamentals",
    file: "cs_fundamentals.html",
    kind: "concept",
    label: "CS",
    color: "#15875f",
    storage: { done: "hub_done_cs", bookmark: "hub_bm_cs" },
    summary: "Operating systems, networking, databases, concurrency, security, and architecture.",
  },
  {
    key: "bh",
    title: "Behavioral and Leadership",
    file: "behavioral.html",
    kind: "concept",
    label: "Behavioral",
    color: "#c9692d",
    storage: { done: "hub_done_bh", bookmark: "hub_bm_bh" },
    summary: "STAR stories, leadership principles, question categories, and mock strategy.",
  },
  {
    key: "ai",
    title: "AI Engineering",
    file: "ai_engineering.html",
    kind: "concept",
    label: "AI",
    color: "#7b61d8",
    storage: { done: "hub_done_ai", bookmark: "hub_bm_ai" },
    summary: "LLM fundamentals, RAG, agents, evals, fine-tuning, ML, deep learning, and MLOps.",
  },
  {
    key: "cloud",
    title: "Cloud - AWS and Azure",
    file: "cloud_aws_azure.html",
    kind: "concept",
    label: "Cloud",
    color: "#0786a3",
    storage: { done: "hub_done_cloud", bookmark: "hub_bm_cloud" },
    summary: "AWS and Azure service mapping, cloud foundations, IaC, observability, and interview Q&A.",
  },
];

const roadmap = [
  {
    phase: "Weeks 1-2",
    title: "Baseline and tooling",
    focus: "Git, CLI fluency, language syntax, Big-O, debugging, and test hygiene.",
    domains: ["DSA", "CS"],
  },
  {
    phase: "Weeks 3-8",
    title: "Core coding interviews",
    focus: "Arrays, strings, two pointers, sliding window, stacks, queues, trees, graphs, and recursion.",
    domains: ["DSA"],
  },
  {
    phase: "Weeks 9-11",
    title: "Advanced problem solving",
    focus: "Dynamic programming, heaps, binary search, tries, intervals, greedy, and graph variants.",
    domains: ["DSA", "CS"],
  },
  {
    phase: "Weeks 10-13",
    title: "Systems foundation",
    focus: "HTTP, DNS, load balancers, databases, caching, queues, sharding, consistency, and reliability.",
    domains: ["System Design", "CS"],
  },
  {
    phase: "Weeks 12-14",
    title: "Cloud and production",
    focus: "IAM, networking, storage, compute, serverless, observability, IaC, and deployment trade-offs.",
    domains: ["Cloud", "System Design"],
  },
  {
    phase: "Weeks 13-15",
    title: "Role specialization",
    focus: "AI engineering, RAG, agents, evals, MLOps, or deeper backend/frontend tracks based on target roles.",
    domains: ["AI", "Cloud"],
  },
  {
    phase: "Every week",
    title: "Behavioral and mocks",
    focus: "Prepare STAR stories, leadership examples, failure stories, conflict stories, and live mock interviews.",
    domains: ["Behavioral"],
  },
];

const additions = [
  {
    area: "Web and frontend fundamentals",
    why: "Useful for full-stack roles and missing from the original folder as a dedicated track.",
    topics: ["HTML semantics", "CSS layout", "JavaScript runtime", "accessibility", "React fundamentals", "browser performance"],
    resources: [
      ["MDN Web Docs", "https://developer.mozilla.org/en-US/docs/Learn"],
      ["web.dev Learn", "https://web.dev/learn"],
      ["React Learn", "https://react.dev/learn"],
    ],
  },
  {
    area: "Backend API engineering",
    why: "Bridges DSA/system design with real implementation work.",
    topics: ["REST", "GraphQL", "auth sessions", "pagination", "idempotency", "validation", "testing APIs"],
    resources: [
      ["Microsoft REST API Guidelines", "https://github.com/microsoft/api-guidelines"],
      ["Google API Design Guide", "https://cloud.google.com/apis/design"],
      ["FastAPI Tutorial", "https://fastapi.tiangolo.com/tutorial/"],
    ],
  },
  {
    area: "Testing and quality",
    why: "Interviewers increasingly ask how you ship safely, not just how you code.",
    topics: ["unit tests", "integration tests", "contract tests", "test doubles", "CI", "observability-driven debugging"],
    resources: [
      ["Google Testing Blog", "https://testing.googleblog.com/"],
      ["Martin Fowler - Testing", "https://martinfowler.com/testing/"],
      ["Playwright Docs", "https://playwright.dev/docs/intro"],
    ],
  },
  {
    area: "Security and identity depth",
    why: "Security appears in system design, cloud, and backend interviews.",
    topics: ["OAuth2", "OIDC", "JWT", "CSRF", "XSS", "SSRF", "secrets", "threat modeling"],
    resources: [
      ["OWASP Top 10", "https://owasp.org/www-project-top-ten/"],
      ["OAuth 2.0 Simplified", "https://www.oauth.com/"],
      ["PortSwigger Web Security Academy", "https://portswigger.net/web-security"],
    ],
  },
  {
    area: "Portfolio projects",
    why: "A project converts the roadmap into something you can explain with ownership.",
    topics: ["one CRUD app", "one distributed feature", "one cloud deployment", "one AI/RAG feature", "one postmortem"],
    resources: [
      ["GitHub Skills", "https://skills.github.com/"],
      ["12 Factor App", "https://12factor.net/"],
      ["OpenTelemetry Docs", "https://opentelemetry.io/docs/"],
    ],
  },
];

function read(file) {
  return fs.readFileSync(path.join(root, file), "utf8");
}

function write(file, content) {
  fs.mkdirSync(path.dirname(path.join(root, file)), { recursive: true });
  fs.writeFileSync(path.join(root, file), content, "utf8");
}

function decodeEntities(value = "") {
  const named = {
    amp: "&",
    lt: "<",
    gt: ">",
    quot: "\"",
    apos: "'",
    nbsp: " ",
    mdash: "-",
    ndash: "-",
  };
  return value.replace(/&(#x?[0-9a-fA-F]+|[a-zA-Z]+);/g, (_m, ent) => {
    if (ent[0] === "#") {
      const isHex = ent[1]?.toLowerCase() === "x";
      const num = Number.parseInt(ent.slice(isHex ? 2 : 1), isHex ? 16 : 10);
      return Number.isFinite(num) ? String.fromCodePoint(num) : _m;
    }
    return named[ent] ?? _m;
  });
}

function stripTags(html = "") {
  return decodeEntities(
    html
      .replace(/<script[\s\S]*?<\/script>/gi, " ")
      .replace(/<style[\s\S]*?<\/style>/gi, " ")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim(),
  );
}

function clean(value = "") {
  return stripTags(value)
    .replace(/\s+([,.;:!?])/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
}

function attr(html = "", name) {
  const re = new RegExp(`${name}\\s*=\\s*["']([^"']*)["']`, "i");
  const match = html.match(re);
  return match ? decodeEntities(match[1]).trim() : "";
}

function first(block, re) {
  const match = block.match(re);
  return match ? clean(match[1]) : "";
}

function rawFirst(block, re) {
  const match = block.match(re);
  return match ? match[1] : "";
}

function slugify(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

function blockStarts(html, re) {
  return [...html.matchAll(re)].map((match) => ({
    index: match.index ?? 0,
    id: match[1],
  }));
}

function sliceByStarts(html, starts, endIndex = html.length) {
  return starts.map((start, idx) => {
    const end = starts[idx + 1]?.index ?? endIndex;
    return {
      id: start.id,
      block: html.slice(start.index, end),
    };
  });
}

function extractRows(block) {
  return [...block.matchAll(/<div class="row">([\s\S]*?)<\/div>/gi)]
    .slice(0, 4)
    .map((m) => clean(m[1]))
    .filter(Boolean);
}

function extractResources(block, context = {}) {
  const resources = [];
  const re = /<a\b([^>]*class=["'][^"']*(?:res-link|sub-res-link)[^"']*["'][^>]*)>([\s\S]*?)<\/a>/gi;
  for (const match of block.matchAll(re)) {
    const open = match[1];
    const body = match[2];
    const url = attr(open, "href");
    if (!url || url.startsWith("#")) continue;
    const title = first(body, /<span class="res-title">([\s\S]*?)<\/span>/i) || clean(body);
    const source =
      first(body, /<span class="res-source">([\s\S]*?)<\/span>/i) ||
      first(body, /<span class="src">([\s\S]*?)<\/span>/i) ||
      "";
    resources.push({
      id: `${context.domain || "site"}:${slugify(title)}:${slugify(url)}`,
      title,
      url,
      source,
      domain: context.domain,
      domainTitle: context.domainTitle,
      section: context.section,
      subsection: context.subsection,
    });
  }
  return resources;
}

function extractProblemLinks(block) {
  const links = [];
  const re = /<a\b([^>]*class=["'][^"']*sol-link[^"']*["'][^>]*)>([\s\S]*?)<\/a>/gi;
  for (const match of block.matchAll(re)) {
    const url = attr(match[1], "href");
    if (!url) continue;
    links.push({ title: clean(match[2]) || "Resource", url });
  }
  return links.slice(0, 4);
}

function extractConceptLinks(block) {
  const links = [];
  const resLinks = rawFirst(block, /<div class="res-links">([\s\S]*?)<\/div>/i);
  const re = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi;
  for (const match of resLinks.matchAll(re)) {
    const url = attr(match[1], "href");
    if (!url) continue;
    links.push({ title: clean(match[2]) || "Resource", url });
  }
  return links.slice(0, 4);
}

function parseConceptPage(source, html) {
  const starts = blockStarts(html, /<section class="section" id="([^"]+)"/gi);
  const sections = [];
  const items = [];
  const resources = extractResources(html, { domain: source.key, domainTitle: source.title });

  for (const section of sliceByStarts(html, starts)) {
    const title = first(section.block, /<h2>([\s\S]*?)<\/h2>/i) || section.id;
    const meta = first(section.block, /<div class="meta">([\s\S]*?)<\/div>/i);
    const tagline = first(section.block, /<div class="tagline">([\s\S]*?)<\/div>/i);
    const secResources = extractResources(section.block, {
      domain: source.key,
      domainTitle: source.title,
      section: title,
    });
    const subStarts = blockStarts(section.block, /<div class="subsection">/gi).map((s, idx) => ({
      ...s,
      id: `sub-${idx + 1}`,
    }));
    const subsections = [];

    for (const sub of sliceByStarts(section.block, subStarts)) {
      const subTitle = first(sub.block, /<h3>([\s\S]*?)<\/h3>/i) || title;
      const subDesc = first(sub.block, /<div class="subsection-desc">([\s\S]*?)<\/div>/i);
      const subResources = extractResources(sub.block, {
        domain: source.key,
        domainTitle: source.title,
        section: title,
        subsection: subTitle,
      });
      const conceptMatches = [...sub.block.matchAll(/<li\b([^>]*data-cid=["'][^"']+["'][^>]*)>([\s\S]*?)<\/li>/gi)];
      const subItemIds = [];

      for (const match of conceptMatches) {
        const open = match[1];
        const body = match[2];
        const cid = attr(open, "data-cid");
        const itemTitle =
          first(body, /<div class="cname">([\s\S]*?)<\/div>/i) ||
          decodeEntities(attr(open, "data-name")) ||
          cid;
        const descCandidates = [...body.matchAll(/<div style=["'][^"']*margin-top:2px[^"']*["']>([\s\S]*?)<\/div>/gi)]
          .map((m) => clean(m[1]))
          .filter(Boolean);
        const description = descCandidates[0] || subDesc || tagline;
        const id = `${source.key}:${cid}`;
        subItemIds.push(id);
        items.push({
          id,
          key: cid,
          type: "concept",
          domain: source.key,
          domainTitle: source.title,
          title: itemTitle,
          description,
          section: title,
          subsection: subTitle,
          url: "",
          link: `${source.file}#${section.id}`,
          resources: extractConceptLinks(body),
          search: [itemTitle, description, source.title, title, subTitle, cid].join(" ").toLowerCase(),
        });
      }

      subsections.push({
        title: subTitle,
        description: subDesc,
        itemCount: subItemIds.length,
        resourceCount: subResources.length,
      });
    }

    const sectionItemCount = subsections.reduce((sum, s) => sum + s.itemCount, 0);
    sections.push({
      id: section.id,
      title,
      meta,
      tagline,
      rows: extractRows(section.block),
      link: `${source.file}#${section.id}`,
      itemCount: sectionItemCount,
      resourceCount: secResources.length,
      subsections,
    });
  }

  return { sections, items, resources };
}

function parseDsaPage(source, html) {
  const starts = blockStarts(html, /<section class="pattern" id="([^"]+)"/gi);
  const end = html.search(/<section class="sources">/i);
  const sections = [];
  const resources = extractResources(html, { domain: source.key, domainTitle: source.title });
  const byLc = new Map();

  for (const pattern of sliceByStarts(html, starts, end > -1 ? end : html.length)) {
    const title = first(pattern.block, /<h2>([\s\S]*?)<\/h2>/i) || pattern.id;
    const meta = first(pattern.block, /<div class="meta">([\s\S]*?)<\/div>/i);
    const tagline = first(pattern.block, /<div class="tagline">([\s\S]*?)<\/div>/i);
    const patternResources = extractResources(pattern.block, {
      domain: source.key,
      domainTitle: source.title,
      section: title,
    });
    const subStarts = blockStarts(pattern.block, /<div class="subpattern">/gi).map((s, idx) => ({
      ...s,
      id: `sub-${idx + 1}`,
    }));
    const subsections = [];
    let patternProblemCount = 0;

    for (const sub of sliceByStarts(pattern.block, subStarts)) {
      const subTitle = first(sub.block, /<h3>([\s\S]*?)<\/h3>/i) || title;
      const subDesc = first(sub.block, /<div class="subpattern-desc">([\s\S]*?)<\/div>/i);
      const subResources = extractResources(sub.block, {
        domain: source.key,
        domainTitle: source.title,
        section: title,
        subsection: subTitle,
      });
      const problemMatches = [...sub.block.matchAll(/<li\b([^>]*data-lc=["'][^"']+["'][^>]*)>([\s\S]*?)<\/li>/gi)];
      patternProblemCount += problemMatches.length;

      for (const match of problemMatches) {
        const open = match[1];
        const body = match[2];
        const lc = attr(open, "data-lc");
        if (!lc) continue;
        const problemTitle =
          first(body, /<a class="pname"[^>]*>([\s\S]*?)<\/a>/i) ||
          decodeEntities(attr(open, "data-name")) ||
          `LeetCode ${lc}`;
        const href = attr(rawFirst(body, /(<a class="pname"[^>]*>[\s\S]*?<\/a>)/i), "href");
        const diff = attr(open, "data-diff");
        const companies = attr(open, "data-companies")
          .split(",")
          .map((c) => c.trim())
          .filter(Boolean);
        const lists = [
          attr(open, "data-blind75") ? "Blind 75" : "",
          attr(open, "data-neetcode") ? "NeetCode 150" : "",
          attr(open, "data-grind") ? "Grind 75" : "",
        ].filter(Boolean);
        const existing = byLc.get(lc);
        const placement = {
          section: title,
          subsection: subTitle,
          description: subDesc,
          link: `${source.file}#${pattern.id}`,
        };
        if (existing) {
          existing.placements.push(placement);
          existing.search += ` ${title} ${subTitle} ${subDesc}`.toLowerCase();
        } else {
          byLc.set(lc, {
            id: `${source.key}:${lc}`,
            key: lc,
            type: "problem",
            domain: source.key,
            domainTitle: source.title,
            title: problemTitle,
            description: subDesc || tagline,
            section: title,
            subsection: subTitle,
            url: href,
            link: `${source.file}#${pattern.id}`,
            diff,
            companies,
            lists,
            placements: [placement],
            resources: extractProblemLinks(body),
            search: [problemTitle, lc, diff, companies.join(" "), lists.join(" "), source.title, title, subTitle, subDesc]
              .join(" ")
              .toLowerCase(),
          });
        }
      }

      subsections.push({
        title: subTitle,
        description: subDesc,
        itemCount: problemMatches.length,
        resourceCount: subResources.length,
      });
    }

    sections.push({
      id: pattern.id,
      title,
      meta,
      tagline,
      rows: extractRows(pattern.block),
      link: `${source.file}#${pattern.id}`,
      itemCount: patternProblemCount,
      resourceCount: patternResources.length,
      subsections,
    });
  }

  return { sections, items: [...byLc.values()], resources };
}

function uniqueBy(items, fn) {
  const seen = new Set();
  const out = [];
  for (const item of items) {
    const key = fn(item);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(item);
  }
  return out;
}

function buildData() {
  const parsedSources = [];
  let allItems = [];
  let allResources = [];

  for (const source of sourceDefs) {
    const html = read(source.file);
    const parsed = source.key === "dsa" ? parseDsaPage(source, html) : parseConceptPage(source, html);
    const itemCount = parsed.items.length;
    const resourceCount = uniqueBy(parsed.resources, (r) => `${r.title}|${r.url}`).length;
    const sourceRecord = {
      ...source,
      sections: parsed.sections,
      itemCount,
      resourceCount,
      progressLabel: source.kind === "problem" ? "problems" : "concepts",
    };
    parsedSources.push(sourceRecord);
    allItems = allItems.concat(parsed.items);
    allResources = allResources.concat(parsed.resources);
  }

  allResources = uniqueBy(allResources, (r) => `${r.title}|${r.url}|${r.domain}|${r.section || ""}`);

  const stats = {
    domains: parsedSources.length,
    sections: parsedSources.reduce((sum, s) => sum + s.sections.length, 0),
    subsections: parsedSources.reduce(
      (sum, s) => sum + s.sections.reduce((inner, sec) => inner + sec.subsections.length, 0),
      0,
    ),
    items: allItems.length,
    problems: allItems.filter((i) => i.type === "problem").length,
    concepts: allItems.filter((i) => i.type === "concept").length,
    resources: allResources.length,
    additions: additions.length,
  };

  return {
    generatedAt: new Date().toISOString(),
    stats,
    sources: parsedSources,
    items: allItems,
    resources: allResources,
    roadmap,
    additions,
  };
}

function escHtml(value = "") {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function hubHtml(data) {
  const json = JSON.stringify(data).replace(/</g, "\\u003c");
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A unified learning hub for DSA, system design, CS fundamentals, behavioral interviews, AI engineering, and cloud.">
<title>Learning Hub</title>
<style>
:root {
  --bg: #f7f8fb;
  --surface: #ffffff;
  --surface-2: #eef2f7;
  --text: #171b24;
  --muted: #5d6575;
  --faint: #8a93a3;
  --border: #dce2eb;
  --strong: #253044;
  --accent: #2459d6;
  --accent-2: #0d8b78;
  --shadow: 0 10px 28px rgba(21, 30, 50, .08);
  --radius: 8px;
}
html.dark {
  --bg: #111318;
  --surface: #191d26;
  --surface-2: #222836;
  --text: #edf0f6;
  --muted: #a6adbb;
  --faint: #727b8c;
  --border: #303747;
  --strong: #f5f7fb;
  --accent: #7ca2ff;
  --accent-2: #50d1bd;
  --shadow: 0 12px 30px rgba(0, 0, 0, .25);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  line-height: 1.5;
}
a { color: inherit; }
button, input, select { font: inherit; }
.appbar {
  position: sticky;
  top: 0;
  z-index: 20;
  border-bottom: 1px solid var(--border);
  background: color-mix(in srgb, var(--surface) 88%, transparent);
  backdrop-filter: blur(16px);
}
.appbar-inner {
  max-width: 1480px;
  margin: 0 auto;
  padding: 12px 18px;
  display: grid;
  grid-template-columns: minmax(160px, 220px) minmax(260px, 1fr) auto;
  gap: 12px;
  align-items: center;
}
.brand { min-width: 0; }
.brand-title {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 0;
  color: var(--strong);
}
.brand-sub {
  font-size: 11px;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.searchbox {
  display: grid;
  grid-template-columns: 28px 1fr;
  align-items: center;
  border: 1px solid var(--border);
  background: var(--surface-2);
  border-radius: var(--radius);
  padding: 0 10px;
  min-height: 42px;
}
.searchbox span { color: var(--faint); font-weight: 800; }
.searchbox input {
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--text);
  width: 100%;
  min-width: 0;
}
.bar-actions { display: flex; gap: 8px; align-items: center; justify-content: end; }
.btn, .select {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  min-height: 38px;
  border-radius: var(--radius);
  padding: 0 12px;
  cursor: pointer;
}
.btn:hover, .select:hover { border-color: var(--accent); }
.btn.primary {
  background: var(--strong);
  color: var(--bg);
  border-color: var(--strong);
}
.wrap {
  max-width: 1480px;
  margin: 0 auto;
  padding: 20px 18px 70px;
}
.metrics {
  display: grid;
  grid-template-columns: repeat(6, minmax(120px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}
.metric, .domain-card, .panel, .result, .section-row, .resource-row {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.metric { padding: 12px; min-height: 78px; }
.metric .num { font-size: 24px; font-weight: 850; color: var(--strong); font-variant-numeric: tabular-nums; }
.metric .label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }
.domain-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(150px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}
.domain-card {
  padding: 12px;
  min-height: 156px;
  cursor: pointer;
  border-top: 4px solid var(--domain-color);
}
.domain-card.active { outline: 2px solid color-mix(in srgb, var(--domain-color) 65%, transparent); }
.domain-card h2 { margin: 0 0 6px; font-size: 16px; letter-spacing: 0; }
.domain-card p { margin: 0; color: var(--muted); font-size: 12px; }
.domain-card .counts { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 7px;
  min-height: 24px;
  border-radius: 999px;
  background: var(--surface-2);
  color: var(--muted);
  font-size: 11px;
  font-weight: 700;
}
.progress {
  margin-top: 10px;
  height: 8px;
  border: 1px solid var(--border);
  border-radius: 999px;
  overflow: hidden;
  background: var(--surface-2);
}
.progress span { display: block; height: 100%; width: 0; background: var(--domain-color, var(--accent)); }
.workspace {
  display: grid;
  grid-template-columns: 340px minmax(0, 1fr);
  gap: 16px;
  align-items: start;
}
.sidebar {
  position: sticky;
  top: 82px;
  display: grid;
  gap: 12px;
}
.panel { padding: 14px; }
.panel h2, .main-title h2 {
  margin: 0;
  font-size: 15px;
  letter-spacing: 0;
}
.panel-head, .main-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}
.roadmap-list { display: grid; gap: 8px; }
.roadmap-step {
  border-left: 3px solid var(--accent-2);
  padding: 4px 0 4px 10px;
}
.roadmap-step .phase { color: var(--faint); font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; }
.roadmap-step .title { font-size: 13px; font-weight: 800; }
.roadmap-step .focus { font-size: 12px; color: var(--muted); margin-top: 2px; }
.additions { display: grid; gap: 8px; }
.addition {
  padding: 9px;
  background: var(--surface-2);
  border-radius: var(--radius);
}
.addition strong { font-size: 13px; }
.addition p { margin: 4px 0 0; color: var(--muted); font-size: 12px; }
.mainpane { min-width: 0; display: grid; gap: 12px; }
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px;
}
.filter-group { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--muted);
  border-radius: 999px;
  padding: 7px 10px;
  min-height: 34px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 800;
}
.chip.active {
  background: var(--strong);
  color: var(--bg);
  border-color: var(--strong);
}
.results, .sections, .resources { display: grid; gap: 10px; }
.result {
  padding: 12px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 10px;
  border-left: 4px solid var(--domain-color, var(--accent));
}
.result h3 { margin: 0 0 5px; font-size: 15px; letter-spacing: 0; }
.result p { margin: 0; color: var(--muted); font-size: 13px; }
.result-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}
.result-actions {
  display: grid;
  grid-template-columns: 1fr;
  align-content: start;
  gap: 6px;
  min-width: 104px;
}
.mini-btn {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface-2);
  color: var(--text);
  padding: 6px 8px;
  min-height: 32px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 800;
  text-decoration: none;
  text-align: center;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.mini-btn.done, .mini-btn.bookmarked { background: var(--strong); color: var(--bg); border-color: var(--strong); }
.section-row {
  padding: 11px 12px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px;
  border-left: 4px solid var(--domain-color, var(--accent));
}
.section-row h3 { margin: 0; font-size: 14px; }
.section-row p { margin: 4px 0 0; color: var(--muted); font-size: 12px; }
.resource-row {
  padding: 11px 12px;
  display: grid;
  gap: 6px;
}
.resource-row a { font-weight: 800; text-decoration: none; }
.empty {
  padding: 28px;
  text-align: center;
  color: var(--muted);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
}
.load-row { display: flex; justify-content: center; padding: 8px 0 4px; }
.hidden { display: none !important; }
@media (max-width: 1180px) {
  .metrics { grid-template-columns: repeat(3, minmax(120px, 1fr)); }
  .domain-grid { grid-template-columns: repeat(3, minmax(150px, 1fr)); }
  .workspace { grid-template-columns: 1fr; }
  .sidebar { position: static; grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 760px) {
  .appbar-inner { grid-template-columns: 1fr; }
  .bar-actions {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(72px, 80px) minmax(82px, 92px);
    justify-content: stretch;
  }
  .bar-actions .btn, .bar-actions .select { width: 100%; min-width: 0; padding-left: 8px; padding-right: 8px; }
  .metrics, .domain-grid, .sidebar { grid-template-columns: 1fr; }
  .result, .section-row { grid-template-columns: 1fr; }
  .result-actions { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>
</head>
<body>
<script id="hub-data" type="application/json">${json}</script>
<header class="appbar">
  <div class="appbar-inner">
    <div class="brand">
      <div class="brand-title">Learning Hub</div>
      <div class="brand-sub">One index across DSA, systems, CS, behavioral, AI, and cloud</div>
    </div>
    <label class="searchbox">
      <span>/</span>
      <input id="search" autocomplete="off" placeholder="Search concepts, problems, companies, resources, sections">
    </label>
    <div class="bar-actions">
      <select id="quick-jump" class="select" title="Open source site">
        <option value="">Open site</option>
      </select>
      <button class="btn" id="theme">Theme</button>
      <button class="btn primary" id="random">Random</button>
    </div>
  </div>
</header>
<main class="wrap">
  <section class="metrics" id="metrics"></section>
  <section class="domain-grid" id="domains"></section>
  <div class="workspace">
    <aside class="sidebar">
      <section class="panel">
        <div class="panel-head"><h2>Roadmap</h2><span class="pill" id="roadmap-count"></span></div>
        <div class="roadmap-list" id="roadmap"></div>
      </section>
      <section class="panel">
        <div class="panel-head"><h2>Added Lanes</h2><span class="pill">gap fill</span></div>
        <div class="additions" id="additions"></div>
      </section>
    </aside>
    <section class="mainpane">
      <div class="filters">
        <div class="filter-group" id="type-filter"></div>
        <div class="filter-group" id="status-filter"></div>
        <div class="filter-group" id="difficulty-filter"></div>
        <button class="chip" id="clear">Clear</button>
      </div>
      <section>
        <div class="main-title"><h2 id="results-title">Catalog</h2><span class="pill" id="result-count"></span></div>
        <div class="results" id="results"></div>
        <div class="load-row"><button class="btn hidden" id="load-more">Load more</button></div>
      </section>
      <section>
        <div class="main-title"><h2>Section Map</h2><span class="pill" id="section-count"></span></div>
        <div class="sections" id="sections"></div>
      </section>
      <section>
        <div class="main-title"><h2>Resource Library</h2><span class="pill" id="resource-count"></span></div>
        <div class="resources" id="resources"></div>
      </section>
    </section>
  </div>
</main>
<script>
(function () {
  const data = JSON.parse(document.getElementById("hub-data").textContent);
  const byDomain = Object.fromEntries(data.sources.map(function (s) { return [s.key, s]; }));
  const state = { domain: "all", type: "all", status: "all", diff: "all", q: "", shown: 80 };
  const themeKey = "learning_hub_theme_v1";

  function qs(id) { return document.getElementById(id); }
  function esc(value) {
    return String(value || "").replace(/[&<>"']/g, function (ch) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch];
    });
  }
  function readSet(key) {
    try { return new Set(JSON.parse(localStorage.getItem(key) || "[]")); }
    catch (_e) { return new Set(); }
  }
  function writeSet(key, set) { localStorage.setItem(key, JSON.stringify(Array.from(set))); }
  function storage(item) { return byDomain[item.domain].storage; }
  function isDone(item) { return readSet(storage(item).done).has(item.key); }
  function isBookmarked(item) { return readSet(storage(item).bookmark).has(item.key); }
  function toggleSet(key, value) {
    const set = readSet(key);
    if (set.has(value)) set.delete(value); else set.add(value);
    writeSet(key, set);
  }
  function pct(done, total) { return total ? Math.round((done / total) * 100) : 0; }
  function domainDone(source) {
    const set = readSet(source.storage.done);
    const valid = new Set(data.items.filter(function (i) { return i.domain === source.key; }).map(function (i) { return i.key; }));
    return Array.from(set).filter(function (key) { return valid.has(key); }).length;
  }
  function currentItems() {
    const q = state.q.toLowerCase();
    return data.items.filter(function (item) {
      if (state.domain !== "all" && item.domain !== state.domain) return false;
      if (state.type !== "all" && item.type !== state.type) return false;
      if (state.status === "done" && !isDone(item)) return false;
      if (state.status === "open" && isDone(item)) return false;
      if (state.status === "bookmarked" && !isBookmarked(item)) return false;
      if (state.diff !== "all" && item.diff !== state.diff) return false;
      if (q && !item.search.includes(q)) return false;
      return true;
    });
  }
  function currentResources() {
    const q = state.q.toLowerCase();
    return data.resources.filter(function (res) {
      if (state.domain !== "all" && res.domain !== state.domain) return false;
      if (!q) return true;
      return [res.title, res.source, res.domainTitle, res.section, res.subsection].join(" ").toLowerCase().includes(q);
    });
  }
  function renderMetrics() {
    const done = data.sources.reduce(function (sum, s) { return sum + domainDone(s); }, 0);
    const metrics = [
      [data.stats.domains, "source sites"],
      [data.stats.sections, "sections"],
      [data.stats.subsections, "subsections"],
      [data.stats.problems, "unique problems"],
      [data.stats.concepts, "concepts"],
      [done + " / " + data.stats.items, "completed"],
    ];
    qs("metrics").innerHTML = metrics.map(function (m) {
      return '<article class="metric"><div class="num">' + esc(m[0]) + '</div><div class="label">' + esc(m[1]) + '</div></article>';
    }).join("");
  }
  function renderDomains() {
    qs("domains").innerHTML = data.sources.map(function (source) {
      const done = domainDone(source);
      const percent = pct(done, source.itemCount);
      return '<article class="domain-card ' + (state.domain === source.key ? "active" : "") + '" data-domain="' + esc(source.key) + '" style="--domain-color:' + esc(source.color) + '">' +
        '<h2>' + esc(source.title) + '</h2>' +
        '<p>' + esc(source.summary) + '</p>' +
        '<div class="counts"><span class="pill">' + source.sections.length + ' sections</span><span class="pill">' + source.itemCount + ' ' + esc(source.progressLabel) + '</span><span class="pill">' + source.resourceCount + ' resources</span></div>' +
        '<div class="progress" title="' + percent + '% complete"><span style="width:' + percent + '%"></span></div>' +
      '</article>';
    }).join("");
    document.querySelectorAll(".domain-card").forEach(function (card) {
      card.addEventListener("click", function () {
        state.domain = state.domain === card.dataset.domain ? "all" : card.dataset.domain;
        state.shown = 80;
        render();
      });
    });
  }
  function makeChip(group, value, label, active) {
    return '<button class="chip ' + (active ? "active" : "") + '" data-group="' + group + '" data-value="' + value + '">' + esc(label) + '</button>';
  }
  function renderFilters() {
    qs("type-filter").innerHTML =
      makeChip("type", "all", "All", state.type === "all") +
      makeChip("type", "problem", "Problems", state.type === "problem") +
      makeChip("type", "concept", "Concepts", state.type === "concept");
    qs("status-filter").innerHTML =
      makeChip("status", "all", "Any status", state.status === "all") +
      makeChip("status", "open", "Open", state.status === "open") +
      makeChip("status", "done", "Done", state.status === "done") +
      makeChip("status", "bookmarked", "Bookmarked", state.status === "bookmarked");
    qs("difficulty-filter").innerHTML =
      makeChip("diff", "all", "Any difficulty", state.diff === "all") +
      makeChip("diff", "E", "Easy", state.diff === "E") +
      makeChip("diff", "M", "Medium", state.diff === "M") +
      makeChip("diff", "H", "Hard", state.diff === "H");
    document.querySelectorAll(".chip[data-group]").forEach(function (chip) {
      chip.addEventListener("click", function () {
        state[chip.dataset.group] = chip.dataset.value;
        state.shown = 80;
        render();
      });
    });
  }
  function itemHtml(item) {
    const source = byDomain[item.domain];
    const done = isDone(item);
    const bookmarked = isBookmarked(item);
    const tags = [
      source.label,
      item.type === "problem" ? "LC " + item.key : item.key,
      item.diff ? ({ E: "Easy", M: "Medium", H: "Hard" }[item.diff] || item.diff) : "",
      item.section,
      item.subsection,
    ].filter(Boolean);
    const resources = (item.resources || []).slice(0, 2).map(function (r) {
      return '<a class="mini-btn" href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(r.title) + '</a>';
    }).join("");
    const external = item.url ? '<a class="mini-btn" href="' + esc(item.url) + '" target="_blank" rel="noopener">External</a>' : "";
    return '<article class="result" style="--domain-color:' + esc(source.color) + '">' +
      '<div><h3>' + esc(item.title) + '</h3><p>' + esc(item.description || "") + '</p>' +
      '<div class="result-meta">' + tags.map(function (t) { return '<span class="pill">' + esc(t) + '</span>'; }).join("") + '</div></div>' +
      '<div class="result-actions">' +
        '<button class="mini-btn ' + (done ? "done" : "") + '" data-done="' + esc(item.id) + '">' + (done ? "Done" : "Mark done") + '</button>' +
        '<button class="mini-btn ' + (bookmarked ? "bookmarked" : "") + '" data-bookmark="' + esc(item.id) + '">' + (bookmarked ? "Saved" : "Save") + '</button>' +
        '<a class="mini-btn" href="' + esc(item.link) + '">Open page</a>' + external + resources +
      '</div></article>';
  }
  function renderResults() {
    const items = currentItems();
    qs("result-count").textContent = items.length + " matches";
    qs("results-title").textContent = state.domain === "all" ? "Catalog" : byDomain[state.domain].title + " Catalog";
    const visible = items.slice(0, state.shown);
    qs("results").innerHTML = visible.length ? visible.map(itemHtml).join("") : '<div class="empty">No catalog items match the current filters.</div>';
    qs("load-more").classList.toggle("hidden", items.length <= state.shown);
    document.querySelectorAll("[data-done]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const item = data.items.find(function (i) { return i.id === btn.dataset.done; });
        toggleSet(storage(item).done, item.key);
        render();
      });
    });
    document.querySelectorAll("[data-bookmark]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const item = data.items.find(function (i) { return i.id === btn.dataset.bookmark; });
        toggleSet(storage(item).bookmark, item.key);
        render();
      });
    });
  }
  function renderSections() {
    const sources = state.domain === "all" ? data.sources : [byDomain[state.domain]];
    const rows = [];
    sources.forEach(function (source) {
      source.sections.forEach(function (section) {
        if (state.q) {
          const hay = [source.title, section.title, section.tagline, section.rows.join(" ")].join(" ").toLowerCase();
          if (!hay.includes(state.q.toLowerCase())) return;
        }
        rows.push({ source: source, section: section });
      });
    });
    qs("section-count").textContent = rows.length + " shown";
    qs("sections").innerHTML = rows.slice(0, 60).map(function (row) {
      return '<article class="section-row" style="--domain-color:' + esc(row.source.color) + '">' +
        '<div><h3>' + esc(row.source.label) + ' / ' + esc(row.section.title) + '</h3><p>' + esc(row.section.tagline || row.section.meta || "") + '</p>' +
        '<div class="result-meta"><span class="pill">' + row.section.itemCount + ' items</span><span class="pill">' + row.section.subsections.length + ' subsections</span><span class="pill">' + row.section.resourceCount + ' resources</span></div></div>' +
        '<a class="mini-btn" href="' + esc(row.section.link) + '">Open</a></article>';
    }).join("") || '<div class="empty">No sections match the current filters.</div>';
  }
  function renderResources() {
    const resources = currentResources();
    qs("resource-count").textContent = resources.length + " resources";
    qs("resources").innerHTML = resources.slice(0, 80).map(function (res) {
      const source = byDomain[res.domain];
      return '<article class="resource-row" style="--domain-color:' + esc(source.color) + '">' +
        '<a href="' + esc(res.url) + '" target="_blank" rel="noopener">' + esc(res.title) + '</a>' +
        '<div class="result-meta"><span class="pill">' + esc(source.label) + '</span>' +
        (res.section ? '<span class="pill">' + esc(res.section) + '</span>' : '') +
        (res.source ? '<span class="pill">' + esc(res.source) + '</span>' : '') +
        '</div></article>';
    }).join("") || '<div class="empty">No resources match the current filters.</div>';
  }
  function renderRoadmap() {
    qs("roadmap-count").textContent = data.roadmap.length + " phases";
    qs("roadmap").innerHTML = data.roadmap.map(function (step) {
      return '<div class="roadmap-step"><div class="phase">' + esc(step.phase) + '</div><div class="title">' + esc(step.title) + '</div><div class="focus">' + esc(step.focus) + '</div><div class="result-meta">' + step.domains.map(function (d) { return '<span class="pill">' + esc(d) + '</span>'; }).join("") + '</div></div>';
    }).join("");
    qs("additions").innerHTML = data.additions.map(function (add) {
      return '<div class="addition"><strong>' + esc(add.area) + '</strong><p>' + esc(add.why) + '</p><div class="result-meta">' + add.topics.slice(0, 4).map(function (t) { return '<span class="pill">' + esc(t) + '</span>'; }).join("") + '</div></div>';
    }).join("");
  }
  function renderJump() {
    qs("quick-jump").innerHTML = '<option value="">Open site</option>' + data.sources.map(function (source) {
      return '<option value="' + esc(source.file) + '">' + esc(source.title) + '</option>';
    }).join("");
  }
  function render() {
    renderMetrics();
    renderDomains();
    renderFilters();
    renderResults();
    renderSections();
    renderResources();
  }

  const savedTheme = localStorage.getItem(themeKey);
  if (savedTheme === "dark" || (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
    document.documentElement.classList.add("dark");
  }
  qs("theme").addEventListener("click", function () {
    const isDark = document.documentElement.classList.toggle("dark");
    localStorage.setItem(themeKey, isDark ? "dark" : "light");
  });
  qs("search").addEventListener("input", function (event) {
    state.q = event.target.value.trim().toLowerCase();
    state.shown = 80;
    render();
  });
  qs("clear").addEventListener("click", function () {
    state.domain = "all"; state.type = "all"; state.status = "all"; state.diff = "all"; state.q = ""; state.shown = 80;
    qs("search").value = "";
    render();
  });
  qs("load-more").addEventListener("click", function () {
    state.shown += 80;
    renderResults();
  });
  qs("random").addEventListener("click", function () {
    const items = currentItems();
    if (!items.length) return;
    const pick = items[Math.floor(Math.random() * items.length)];
    window.location.href = pick.link;
  });
  qs("quick-jump").addEventListener("change", function (event) {
    if (event.target.value) window.location.href = event.target.value;
  });

  renderJump();
  renderRoadmap();
  render();
})();
</script>
</body>
</html>
`;
}

function pagesWorkflow() {
  return `name: Deploy static learning hub

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: \${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Configure Pages
        uses: actions/configure-pages@v5
      - name: Upload static site
        uses: actions/upload-pages-artifact@v3
        with:
          path: .
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
`;
}

function readme(data) {
  return `# Learning Hub

A static one-stop learning hub generated from the HTML sites in this folder.

## Included sites

${data.sources.map((s) => `- ${s.title}: ${s.itemCount} ${s.progressLabel}, ${s.sections.length} sections, ${s.resourceCount} resources`).join("\n")}

## Local preview

Open \`index.html\` directly, or serve the folder with any static file server.

## GitHub Pages

This repo includes a GitHub Actions workflow at \`.github/workflows/pages.yml\`.
After pushing to the \`main\` branch, GitHub Pages deploys the static site.
The default public URL format is:

\`https://<github-user-or-org>.github.io/<repo-name>/\`
`;
}

function updateSourceNavs() {
  for (const source of sourceDefs) {
    const filePath = path.join(root, source.file);
    const html = fs.readFileSync(filePath, "utf8");
    fs.writeFileSync(filePath, html.replace(/href=["']hub\.html["']/g, 'href="index.html"'), "utf8");
  }
}

const data = buildData();
write("learning-hub-data.json", `${JSON.stringify(data, null, 2)}\n`);
write("index.html", hubHtml(data));
write("hub.html", hubHtml(data));
write(".nojekyll", "");
write(".github/workflows/pages.yml", pagesWorkflow());
write("README.md", readme(data));
updateSourceNavs();

console.log(`Learning hub generated: ${data.stats.domains} sites, ${data.stats.sections} sections, ${data.stats.items} items, ${data.stats.resources} resources.`);
