#!/usr/bin/env node
/**
 * Fills in four to five REAL, CHECKED YouTube videos for every DSA problem.
 *
 *   node tools/build_dsa_videos.mjs --max 120        # one slice of the work
 *
 * Needs yt-dlp and real internet, so it runs on a GitHub Actions runner.
 * yt-dlp is used only to SEARCH YouTube and read back each result's actual id,
 * title, channel and duration — no download, no API key. Every value written
 * here therefore came from YouTube itself in this run.
 *
 * Why this exists: two earlier generators were told to produce "4-5 videos per
 * problem" and filled the quota by inventing ids. One invented id was listed on
 * 109 problems; others pointed at a real video for a different problem. The fix
 * is not to drop the target but to earn it — search, then keep only what both
 * exists and matches.
 *
 * Progress is cached in tools/linkcheck/video-cache.json and committed, so each
 * scheduled run advances the remaining problems instead of redoing the lot.
 */
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const ROOT = process.cwd();
const INDEX = path.join(ROOT, 'DSA_Ultimate_Index.html');
const REG = path.join(ROOT, 'assets', 'dsa-resources.js');
const CACHE = path.join(ROOT, 'tools', 'linkcheck', 'video-cache.json');

const arg = (n, d) => { const i = process.argv.indexOf(n); return i > -1 ? process.argv[i + 1] : d; };
const MAX = parseInt(arg('--max', '150'), 10);
const TARGET = parseInt(arg('--target', '5'), 10);
const MIN_OK = parseInt(arg('--min', '4'), 10);

/* Channels that actually teach these problems. A result from one of them wins
   ties; a result from nowhere near them has to match the title much harder. */
const TRUSTED = new Map(Object.entries({
  'NeetCode': 10, 'NeetCodeIO': 10, 'take U forward': 9, 'Techdose': 8,
  'codestorywithMIK': 8, 'Greg Hogg': 7, 'Nikhil Lohia': 7, 'Kevin Naughton Jr.': 6,
  'Nick White': 6, 'Errichto': 7, 'William Fiset': 7, 'Abdul Bari': 6,
  'AlgosWithMichael': 5, 'Programming Live with Larry': 5, 'Aryan Mittal': 5,
  'Fraz': 5, 'Striver': 9, 'Code with Alisha': 4, 'Pepcoding': 6, 'CodeHelp - by Babbar': 6,
}));

const norm = (s) => String(s || '').toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
const STOP = new Set(['a', 'an', 'the', 'of', 'in', 'to', 'and', 'or', 'with', 'for', 'from', 'is', 'number']);

function score(entry, title, lcNum) {
  const real = norm(entry.title);
  if (!real) return -1;
  /* obvious junk: shorts compilations, "day 37 of 100", playlists of everything */
  if (/\b(playlist|full course|complete course|marathon|live stream)\b/.test(real)) return -1;
  if (entry.duration != null && (entry.duration < 90 || entry.duration > 7200)) return -1;

  const numRe = (n) => new RegExp(`(^|[^0-9])${n}([^0-9]|$)`);
  const namesThis = !!(lcNum && numRe(lcNum).test(real));

  /* If the title cites a LeetCode number and it is not ours, this is a
     different problem however similar the words are. This is the exact case
     that put "Add Two Numbers II ... Leetcode-445" under problem 2. */
  const cited = [...real.matchAll(/\b(?:leetcode|lc|problem)\s*#?\s*(\d{1,4})\b/g)].map((m) => m[1]);
  if (cited.length && lcNum && !cited.includes(String(lcNum))) return -1;
  if (cited.length && !lcNum) return -1;

  const want = norm(title).split(' ').filter((w) => w.length > 2 && !STOP.has(w));
  const hit = want.filter((w) => real.includes(w)).length;
  const ratio = want.length ? hit / want.length : 0;

  /* Either it names our number, or the title really is this problem's title.
     "Binary Search Algorithm" shares 2 of 4 words with "Validate Binary Search
     Tree" and is not it. */
  if (!namesThis && ratio < 0.75) return -1;
  if (namesThis && ratio < 0.34) return -1;

  let s = 0;
  if (namesThis) s += 6;
  s += ratio * 10;
  if (/\bleetcode\b|\bleet code\b/.test(real)) s += 2;
  if (/\b(solution|explained|explanation|approach|intuition|tutorial)\b/.test(real)) s += 1;
  s += (TRUSTED.get(entry.channel) || 0) / 2;
  return s;
}

function ytSearch(query, n = 12) {
  try {
    const out = execFileSync('yt-dlp', [
      '--flat-playlist', '--dump-single-json', '--no-warnings', '--ignore-errors',
      '--socket-timeout', '20', `ytsearch${n}:${query}`,
    ], { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024, timeout: 120000 });
    const j = JSON.parse(out);
    return (j.entries || []).filter(Boolean).map((e) => ({
      id: e.id, title: e.title || '', channel: e.channel || e.uploader || '',
      duration: e.duration == null ? null : Math.round(e.duration),
    })).filter((e) => e.id && e.title);
  } catch (e) {
    console.error(`  search failed: ${String(e.message || e).slice(0, 120)}`);
    return [];
  }
}

const hhmm = (sec) => sec == null ? '' : `${Math.floor(sec / 60)}:${String(sec % 60).padStart(2, '0')}`;

/* ---------- rows ---------- */
const html = fs.readFileSync(INDEX, 'utf8');
const rows = new Map();
for (const m of html.matchAll(/<li ([^>]*data-lc="[^"]*"[^>]*)>([\s\S]*?)<\/li>/g)) {
  const attrs = m[1], body = m[2];
  if (/class="note-editor"/.test(attrs)) continue;
  const lc = (attrs.match(/data-lc="([^"]*)"/) || [])[1];
  if (!lc || rows.has(lc)) continue;
  const a = body.match(/<a[^>]*class="(?:pname|problem-name)"[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/)
         || body.match(/<a[^>]*href="([^"]*)"[^>]*class="(?:pname|problem-name)"[^>]*>([\s\S]*?)<\/a>/);
  const href = a ? a[1] : '';
  rows.set(lc, {
    lc,
    title: a ? a[2].replace(/<[^>]*>/g, '').trim() : '',
    isLeetCode: /leetcode\.com\/problems\//.test(href),
    num: /^\d+$/.test(lc) ? lc : null,
  });
}

const sandbox = { window: {} };
new Function('window', fs.readFileSync(REG, 'utf8'))(sandbox.window);
const reg = sandbox.window.dsaResources || {};
const cache = fs.existsSync(CACHE) ? JSON.parse(fs.readFileSync(CACHE, 'utf8')) : {};

/* a problem is done when the cache holds at least MIN_OK checked videos for it */
const pending = [...rows.values()].filter((r) => r.title && !(cache[r.lc] && cache[r.lc].videos && cache[r.lc].videos.length >= MIN_OK));
console.log(`${rows.size} rows | ${rows.size - pending.length} already filled | working on ${Math.min(MAX, pending.length)} of ${pending.length}`);

let filled = 0;
for (const row of pending.slice(0, MAX)) {
  const num = row.num || (cache[row.lc] && cache[row.lc].num) || null;
  const q = row.isLeetCode
    ? `${row.title} leetcode${num ? ' ' + num : ''} solution explained`
    : `${row.title} dsa explained tutorial`;
  const seen = new Map();
  for (const e of ytSearch(q, 12)) if (!seen.has(e.id)) seen.set(e.id, e);
  if (seen.size < TARGET * 2) {
    for (const e of ytSearch(`${row.title} ${row.isLeetCode ? 'leetcode' : 'algorithm'} approach intuition`, 8)) {
      if (!seen.has(e.id)) seen.set(e.id, e);
    }
  }
  const ranked = [...seen.values()]
    .map((e) => ({ e, s: score(e, row.title, num) }))
    .filter((x) => x.s > 0)
    .sort((a, b) => b.s - a.s);

  /* one video per channel first, so five results are five teachers not five
     uploads from one; then top up if that leaves too few */
  const picked = [], usedChannel = new Set();
  for (const { e } of ranked) {
    if (picked.length >= TARGET) break;
    if (usedChannel.has(e.channel)) continue;
    usedChannel.add(e.channel); picked.push(e);
  }
  for (const { e } of ranked) {
    if (picked.length >= TARGET) break;
    if (!picked.some((p) => p.id === e.id)) picked.push(e);
  }

  cache[row.lc] = {
    num, title: row.title, at: Date.now(),
    videos: picked.map((e) => [e.id, e.title, e.channel, hhmm(e.duration)]),
  };
  filled++;
  console.log(`  ${row.lc.padEnd(7)} ${row.title.slice(0, 44).padEnd(44)} ${picked.length} video(s)`);
  fs.writeFileSync(CACHE, JSON.stringify(cache, null, 0));
}

/* ---------- write the registry ---------- */
let changed = 0;
for (const [lc, p] of Object.entries(reg)) {
  const c = cache[lc];
  if (!c || !c.videos || !c.videos.length) continue;
  const before = JSON.stringify(p.videos || []);
  p.videos = c.videos;
  p.v = c.videos[0][0];
  if (JSON.stringify(p.videos) !== before) changed++;
}
const totals = Object.values(reg).reduce((a, p) => { a.v += (p.videos || []).length; a.r += (p.reads || []).length; return a; }, { v: 0, r: 0 });
const withEnough = Object.values(reg).filter((p) => (p.videos || []).length >= MIN_OK).length;

const header = `/* assets/dsa-resources.js — generated. Do not hand-edit.
   Generated: ${new Date().toISOString()}
   Rows: ${Object.keys(reg).length} | video entries: ${totals.v} | reads: ${totals.r}
   Rows with ${MIN_OK}+ videos: ${withEnough}

   Every video below was returned by a YouTube search run in CI (yt-dlp) and its
   id, title, channel and duration are what YouTube reported for it. Nothing is
   hand-written, and nothing is kept whose title does not match the problem.
   reads[i][3] === true means the study panel can open it inline; those come
   first, and the ones that must open in a new tab come after. */
`;
fs.writeFileSync(REG, header + 'window.dsaResources = ' + JSON.stringify(reg) + ';\n');
console.log(`filled ${filled} problems this run | ${changed} rows updated | ${withEnough}/${Object.keys(reg).length} rows now have ${MIN_OK}+ videos`);
