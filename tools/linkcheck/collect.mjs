#!/usr/bin/env node
/**
 * Walks the whole site and writes every checkable outbound link to
 * tools/linkcheck/links.json, with enough context to find it again.
 *
 *   node tools/linkcheck/collect.mjs [--section dsa|system-design|...]
 *
 * Search URLs (google.com/search, youtube.com/results) are deliberately left
 * out: they always resolve, so checking them proves nothing. CDN assets are
 * left out for the same reason.
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const SKIP_DIR = new Set(['.git', '.venv', 'node_modules', '__pycache__', 'tools']);
const SKIP_HOST = new Set(['cdnjs.cloudflare.com', 'cdn.jsdelivr.net', 'unpkg.com', 'fonts.googleapis.com', 'fonts.gstatic.com']);
const SKIP_URL = /google\.[a-z.]+\/search|youtube\.com\/results|bing\.com\/search|duckduckgo\.com\/\?q=/;

/* which file belongs to which study section, so a run can take one at a time */
export const SECTIONS = {
  dsa: ['DSA_Ultimate_Index.html', 'assets/dsa-resources.js', 'DSA_Tutorial/'],
  'system-design': ['system_design.html', 'System_Design_Tutorial/'],
  lld: ['LLD_Tutorial/'],
  'cs-fundamentals': ['cs_fundamentals.html'],
  cloud: ['cloud_aws_azure.html'],
  ai: ['ai_engineering.html'],
  behavioral: ['behavioral.html'],
  'interview-prep': ['interview_prep.html'],
  hub: ['index.html', 'library.html', 'auto-me/'],
};

function sectionOf(rel) {
  for (const [name, prefixes] of Object.entries(SECTIONS)) {
    if (prefixes.some((p) => (p.endsWith('/') ? rel.startsWith(p) : rel === p))) return name;
  }
  return 'other';
}

export function ytId(u) {
  try {
    const x = new URL(u);
    const h = x.hostname.replace(/^www\.|^m\./, '');
    if (h === 'youtu.be') return x.pathname.slice(1).split('/')[0] || null;
    if (h === 'youtube.com' || h === 'youtube-nocookie.com') {
      if (x.pathname === '/watch') return x.searchParams.get('v');
      const m = x.pathname.match(/^\/(?:embed|shorts|live)\/([^/?#]+)/);
      if (m) return m[1];
    }
  } catch { /* not a url */ }
  return null;
}

export function collect(only) {
  const files = [];
  (function walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      if (e.isDirectory()) { if (!SKIP_DIR.has(e.name)) walk(path.join(dir, e.name)); continue; }
      if (/\.(html|js|json)$/.test(e.name)) files.push(path.join(dir, e.name));
    }
  })(ROOT);

  const out = new Map();
  for (const file of files) {
    const rel = path.relative(ROOT, file).replace(/\\/g, '/');
    const section = sectionOf(rel);
    if (only && section !== only) continue;
    let text;
    try { text = fs.readFileSync(file, 'utf8'); } catch { continue; }
    for (const m of text.matchAll(/https:\/\/[^\s"'<>\\)\]]+/g)) {
      let url = m[0].replace(/[.,;:]+$/, '');
      if (SKIP_URL.test(url)) continue;
      let host;
      try { host = new URL(url).hostname; } catch { continue; }
      if (SKIP_HOST.has(host)) continue;
      const id = ytId(url);
      const key = id ? 'yt:' + id : url;
      if (!out.has(key)) out.set(key, { key, url, host, youtubeId: id, sections: new Set(), files: new Set() });
      out.get(key).sections.add(section);
      out.get(key).files.add(rel);
    }
  }
  /* assets/dsa-resources.js stores video ids bare, not as URLs, so the regex
     above never sees them — pull them out of the registry itself. */
  if (!only || only === 'dsa') {
    const regPath = path.join(ROOT, 'assets', 'dsa-resources.js');
    if (fs.existsSync(regPath)) {
      const sandbox = { window: {} };
      try {
        // eslint-disable-next-line no-new-func
        new Function('window', fs.readFileSync(regPath, 'utf8'))(sandbox.window);
      } catch { /* leave the registry out if it will not parse */ }
      const reg = sandbox.window.dsaResources || {};
      for (const [row, p2] of Object.entries(reg)) {
        for (const v of p2.videos || []) {
          if (!v || !v[0]) continue;
          const key = 'yt:' + v[0];
          if (!out.has(key)) {
            out.set(key, {
              key, url: 'https://www.youtube.com/watch?v=' + v[0], host: 'www.youtube.com',
              youtubeId: v[0], sections: new Set(), files: new Set(),
              claim: { title: v[1] || '', channel: v[2] || '' }, rows: new Set(),
            });
          }
          const rec = out.get(key);
          rec.sections.add('dsa');
          rec.files.add('assets/dsa-resources.js');
          (rec.rows = rec.rows || new Set()).add(row);
          if (!rec.claim) rec.claim = { title: v[1] || '', channel: v[2] || '' };
        }
      }
    }
  }

  return [...out.values()].map((x) => ({
    ...x,
    sections: [...x.sections],
    files: [...x.files].slice(0, 6),
    rows: x.rows ? [...x.rows] : undefined,
  }));
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const i = process.argv.indexOf('--section');
  const only = i > -1 ? process.argv[i + 1] : null;
  const links = collect(only);
  const dir = path.join(ROOT, 'tools', 'linkcheck');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'links.json'), JSON.stringify(links, null, 1));
  const yt = links.filter((l) => l.youtubeId).length;
  console.log(`collected ${links.length} distinct links (${yt} YouTube videos)${only ? ` for section ${only}` : ''}`);
}
