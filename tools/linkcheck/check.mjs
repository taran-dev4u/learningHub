#!/usr/bin/env node
/**
 * Checks the links collected by collect.mjs and writes a report.
 *
 *   node tools/linkcheck/check.mjs [--max 4000] [--section dsa]
 *
 * Needs real internet, so it runs on a GitHub Actions runner, not in the
 * Claude sandbox or the desktop bridge — both of those can only reach GitHub
 * and the package registries, which is why dead links kept shipping.
 *
 * A YouTube video is checked through the oEmbed endpoint, which returns the
 * video's REAL title and channel. That is what catches an id that exists but
 * belongs to a different problem — the failure that made the rail untrustworthy.
 *
 * Results are cached in tools/linkcheck/cache.json and reused for 30 days, so a
 * scheduled run only pays for what it has not seen.
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DIR = path.join(ROOT, 'tools', 'linkcheck');
const CACHE_FILE = path.join(DIR, 'cache.json');
const CACHE_DAYS = 30;
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36';

const arg = (n, d) => { const i = process.argv.indexOf(n); return i > -1 ? process.argv[i + 1] : d; };
const MAX = parseInt(arg('--max', '100000'), 10);
const CONC = parseInt(arg('--concurrency', '10'), 10);

const cache = fs.existsSync(CACHE_FILE) ? JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8')) : {};
const fresh = (e) => e && e.at && (Date.now() - e.at) < CACHE_DAYS * 864e5;

async function withTimeout(fn, ms) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), ms);
  try { return await fn(ac.signal); } finally { clearTimeout(t); }
}

async function checkYouTube(id) {
  const api = 'https://www.youtube.com/oembed?url=' + encodeURIComponent('https://www.youtube.com/watch?v=' + id) + '&format=json';
  try {
    const r = await withTimeout((signal) => fetch(api, { signal, headers: { 'user-agent': UA } }), 15000);
    if (r.status === 200) {
      const j = await r.json();
      return { status: 'ok', title: j.title, channel: j.author_name };
    }
    /* 401 and 404 both mean the video is gone or private */
    if (r.status === 401 || r.status === 403 || r.status === 404) return { status: 'dead', code: r.status };
    return { status: 'unknown', code: r.status };
  } catch (e) {
    return { status: 'unknown', error: String(e.message || e).slice(0, 80) };
  }
}

async function checkUrl(url) {
  for (const method of ['HEAD', 'GET']) {
    try {
      const r = await withTimeout((signal) => fetch(url, {
        method, redirect: 'follow', signal,
        headers: { 'user-agent': UA, accept: 'text/html,application/xhtml+xml,*/*' },
      }), 20000);
      if (r.status === 405 || r.status === 501) continue;        // HEAD not allowed, retry as GET
      if (r.status >= 200 && r.status < 400) return { status: 'ok', code: r.status, final: r.url !== url ? r.url : undefined };
      if (r.status === 404 || r.status === 410) return { status: 'dead', code: r.status };
      /* a CI runner gets blocked by Cloudflare and friends; that is not proof
         the page is gone, so it is reported separately and never auto-removed */
      if (r.status === 403 || r.status === 429 || r.status === 503) return { status: 'blocked', code: r.status };
      return { status: 'unknown', code: r.status };
    } catch (e) {
      if (method === 'GET') return { status: 'unknown', error: String(e.message || e).slice(0, 80) };
    }
  }
  return { status: 'unknown' };
}

/* does the video's real title actually belong to this problem? */
const norm = (s) => String(s || '').toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
const STOP = new Set(['a', 'an', 'the', 'of', 'in', 'to', 'and', 'or', 'with', 'for', 'from', 'two', 'ii', 'i']);
export function titleMatches(realTitle, problemTitle, lcNumber) {
  const real = norm(realTitle);
  /* A title that cites a LeetCode number settles it either way. This is what
     catches "Add Two Numbers II ... Leetcode-445" sitting under problem 2 —
     the words match almost perfectly, the problem does not. */
  const cited = [...real.matchAll(/\b(?:leetcode|lc|problem)\s*#?\s*(\d{1,4})\b/g)].map((m) => m[1]);
  if (lcNumber && cited.length) return cited.includes(String(lcNumber));
  if (lcNumber && new RegExp(`(^|[^0-9])${lcNumber}([^0-9]|$)`).test(real)) return true;
  const want = norm(problemTitle).split(' ').filter((w) => w.length > 2 && !STOP.has(w));
  if (!want.length) return false;
  const hit = want.filter((w) => real.includes(w)).length;
  return hit / want.length >= 0.7;
}

if (import.meta.url !== `file://${process.argv[1]}`) {
  /* imported for titleMatches only — do not run the check */
} else {
  await (async () => {
const links = JSON.parse(fs.readFileSync(path.join(DIR, 'links.json'), 'utf8'));
const section = arg('--section', null);
const queue = links.filter((l) => (!section || l.sections.includes(section)) && !fresh(cache[l.key])).slice(0, MAX);
console.log(`${links.length} links, ${links.length - queue.length} cached, checking ${queue.length}`);

let done = 0;
async function worker() {
  for (;;) {
    const l = queue.shift();
    if (!l) return;
    const res = l.youtubeId ? await checkYouTube(l.youtubeId) : await checkUrl(l.url);
    cache[l.key] = { ...res, at: Date.now() };
    if (++done % 200 === 0) {
      console.log(`  ${done} checked`);
      fs.writeFileSync(CACHE_FILE, JSON.stringify(cache));
    }
  }
}
await Promise.all(Array.from({ length: CONC }, worker));
fs.writeFileSync(CACHE_FILE, JSON.stringify(cache));

/* ---------- report ---------- */
const bySection = {};
const dead = [], blocked = [], mismatched = [];
for (const l of links) {
  const r = cache[l.key];
  if (!r) continue;
  for (const s of l.sections) {
    bySection[s] = bySection[s] || { total: 0, ok: 0, dead: 0, blocked: 0, unknown: 0, mismatched: 0 };
    bySection[s].total++;
    bySection[s][r.status === 'ok' ? 'ok' : r.status]++;
  }
  if (r.status === 'dead') dead.push({ ...l, ...r });
  else if (r.status === 'blocked') blocked.push({ ...l, ...r });
  else if (r.status === 'ok' && l.claim && l.claim.title && r.title) {
    /* the registry said this video was about X; YouTube says it is about Y */
    const rowNum = (l.rows || []).map((x) => (/^\d+$/.test(x) ? x : null)).find(Boolean) || null;
    if (!titleMatches(r.title, l.claim.title.replace(/\s*[—-]\s*.*$/, ''), rowNum)) {
      mismatched.push({ ...l, real: r.title, realChannel: r.channel });
      for (const s of l.sections) bySection[s].mismatched++;
    }
  }
}

fs.writeFileSync(path.join(DIR, 'report.json'), JSON.stringify({ generated: new Date().toISOString(), bySection, dead, blocked, mismatched }, null, 1));

const lines = ['# Link health', '', `_Checked ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC._`, '',
  '| Section | Links | OK | Dead | Blocked | Unverifiable | Wrong video |', '|---|--:|--:|--:|--:|--:|--:|'];
for (const [s, v] of Object.entries(bySection).sort()) {
  lines.push(`| ${s} | ${v.total} | ${v.ok} | ${v.dead} | ${v.blocked} | ${v.unknown} | ${v.mismatched} |`);
}
lines.push('', `**${dead.length} dead**, **${mismatched.length} videos whose real title does not match what the page claims**, ${blocked.length} blocked to the runner (not proof of death).`, '');
if (dead.length) {
  lines.push('## Dead links', '');
  for (const d of dead.slice(0, 200)) lines.push(`- \`${d.url}\` (${d.code || d.error || ''}) — ${d.files.join(', ')}`);
  if (dead.length > 200) lines.push(`- …and ${dead.length - 200} more, see report.json`);
  lines.push('');
}
if (mismatched.length) {
  lines.push('## Videos listed under the wrong problem', '');
  for (const m of mismatched.slice(0, 200)) lines.push(`- \`${m.youtubeId}\` listed as **${m.claim.title}** is really **${m.real}** (${m.realChannel})`);
  if (mismatched.length > 200) lines.push(`- …and ${mismatched.length - 200} more, see report.json`);
}
fs.writeFileSync(path.join(ROOT, 'LINK_HEALTH.md'), lines.join('\n') + '\n');
console.log(`dead ${dead.length} | wrong-video ${mismatched.length} | blocked ${blocked.length}`);
  })();
}
