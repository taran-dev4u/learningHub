#!/usr/bin/env node
/**
 * Generates assets/dsa-resources.js for DSA_Ultimate_Index.html.
 *
 * GROUND RULE: nothing in the output may be invented.
 * Every video id and every URL below comes from a source that is either
 * fetched at build time or deterministic from the problem's own LeetCode slug.
 *
 * Why this file was rewritten (Oct 2026)
 * --------------------------------------
 * The previous generator synthesised "4-5 verified videos" per problem from a
 * hand-written topic table. They were not verified. 7,332 video entries
 * resolved to 2,729 distinct ids; one id was stamped on 109 different
 * problems. Spot checks against YouTube's oEmbed endpoint found ids that
 * 404 (0m1T_UqZ_1M, 4r_iT44_q44 — both listed on 109 problems), real videos
 * attached to the wrong problem (B-uQN5wp6Jg is "Add Two Numbers II,
 * Leetcode-445" and was listed on problem 2), and real videos relabelled per
 * topic (one id carried four different titles). Only 366 of the 7,332 entries
 * were the official NeetCode video for the problem they were listed under.
 *
 * So: a video is emitted only when NeetCode's own problem data names it for
 * that exact LeetCode slug. Problems without one get no video entry, and the
 * rail falls back to a labelled YouTube search, which is honest.
 *
 * Reads are ordered so everything that opens inside the study panel comes
 * first and everything that has to open in a new tab comes last.
 *
 *   npm-free:  node tools/build_dsa_resources.mjs
 *   offline:   node tools/build_dsa_resources.mjs --cache tools/.dsa-cache
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const INDEX = path.join(ROOT, 'DSA_Ultimate_Index.html');
const OUT = path.join(ROOT, 'assets', 'dsa-resources.js');
const CACHE = path.join(ROOT, 'tools', '.dsa-cache');

const SOURCES = {
  neetcode: 'https://raw.githubusercontent.com/neetcode-gh/leetcode/main/.problemSiteData.json',
  doocs: 'https://raw.githubusercontent.com/doocs/leetcode/main/solution/README_EN.md',
};

/* Slugs where our index and doocs disagree on the title. */
const SLUG_ALIAS = { 'coin-change-2': 518, 'implement-strstr': 28 };

async function load(name, url) {
  fs.mkdirSync(CACHE, { recursive: true });
  const file = path.join(CACHE, name);
  if (fs.existsSync(file) && process.argv.includes('--cache')) return fs.readFileSync(file, 'utf8');
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${name}: HTTP ${res.status} from ${url}`);
  const text = await res.text();
  fs.writeFileSync(file, text);
  return text;
}

const slugify = (s) => String(s).toLowerCase().replace(/['’]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
const esc = (s) => String(s == null ? '' : s);

/* ---------- 1. the rows, read out of the page itself ---------- */
function readRows() {
  const html = fs.readFileSync(INDEX, 'utf8');
  const patterns = [];
  const pRe = /<(?:section|div) class="pattern" id="([^"]+)"[^>]*>([\s\S]*?)(?=<(?:section|div) class="pattern" id="|<\/body>)/g;
  let pm;
  while ((pm = pRe.exec(html))) {
    const title = (pm[2].match(/<h2[^>]*>([\s\S]*?)<\/h2>/) || [, ''])[1].replace(/<[^>]*>/g, '').trim();
    patterns.push({ id: pm[1], title, block: pm[2] });
  }
  const rows = new Map();
  for (const pat of patterns) {
    const liRe = /<li ([^>]*data-lc="[^"]*"[^>]*)>([\s\S]*?)<\/li>/g;
    let m;
    while ((m = liRe.exec(pat.block))) {
      const attrs = m[1], body = m[2];
      if (/class="note-editor"/.test(attrs)) continue;
      const lc = (attrs.match(/data-lc="([^"]*)"/) || [])[1];
      if (!lc || rows.has(lc)) continue;
      /* the curated rows write class before href, the Striver rows write href
         before class — match either order or every Striver row drops out */
      const a =
        body.match(/<a[^>]*class="(?:pname|problem-name)"[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/) ||
        body.match(/<a[^>]*href="([^"]*)"[^>]*class="(?:pname|problem-name)"[^>]*>([\s\S]*?)<\/a>/);
      const href = a ? a[1] : '';
      const tags = [];
      if (/data-blind75=/.test(attrs)) tags.push('B75');
      if (/data-neetcode=/.test(attrs)) tags.push('NC150');
      if (/data-grind=/.test(attrs)) tags.push('Grind');
      if (/data-striver=/.test(attrs)) tags.push('Striver');
      rows.set(lc, {
        lc,
        title: a ? a[2].replace(/<[^>]*>/g, '').trim() : '',
        diff: { E: 'Easy', M: 'Medium', H: 'Hard' }[(attrs.match(/data-diff="([^"]*)"/) || [])[1]] || '',
        href,
        slug: (href.match(/leetcode\.com\/problems\/([a-z0-9-]+)/) || [])[1] || '',
        pattern: pat.title,
        list: tags.join('|'),
      });
    }
  }
  return [...rows.values()];
}

/* ---------- 2. the two upstream datasets ---------- */
function parseNeetcode(json) {
  const bySlug = new Map();
  for (const x of JSON.parse(json)) {
    const slug = String(x.link || '').replace(/^\/|\/$/g, '');
    if (slug && x.video) bySlug.set(slug, { video: x.video, problem: x.problem, pattern: x.pattern });
  }
  return bySlug;
}
function parseDoocs(md) {
  const byNum = new Map(), bySlug = new Map();
  for (const m of md.matchAll(/\|\s*(\d+)\s*\|\s*\[([^\]]+)\]\((\/solution\/[^)]+README_EN\.md)\)/g)) {
    const num = String(parseInt(m[1], 10));
    const rec = { num, title: m[2], path: m[3] };
    if (!byNum.has(num)) byNum.set(num, rec);
    const s = slugify(m[2]);
    if (!bySlug.has(s)) bySlug.set(s, rec);
  }
  return { byNum, bySlug };
}

/* ---------- 3. reads, panel-openable first ---------- */
/* `panel` true means assets/video-panel.js can render it inside the side
   panel: raw.githubusercontent.com is fetched and rendered as markdown, and
   the hosts in its FRAME_HOSTS list are iframed. Everything else opens in a
   new tab, and is listed after the panel ones. */
function buildReads(row, doocs, ncHit) {
  const panel = [], external = [];
  const num = /^\d+$/.test(row.lc) ? row.lc : null;

  if (doocs) {
    panel.push([
      'Approach walkthrough — every approach, in English',
      'https://raw.githubusercontent.com/doocs/leetcode/main' + doocs.path.replace(/^\/solution/, '/solution'),
      'Problem restated, then each approach in turn with the reasoning, the complexity and reference code',
      true,
    ]);
  }
  const n = num || (doocs ? doocs.num : null);
  if (n) {
    panel.push([
      'Reference solutions — C++, Java, Python',
      'https://walkccc.me/LeetCode/problems/' + String(n).padStart(4, '0') + '/',
      'The same solution written out in each language, side by side',
      true,
    ]);
  }
  if (ncHit && row.slug) {
    panel.push([
      'NeetCode editorial',
      'https://neetcode.io/problems/' + row.slug,
      'The write-up that goes with the NeetCode video',
      true,
    ]);
  }
  if (row.slug) {
    external.push([
      'Community solutions ↗',
      'https://leetcode.com/problems/' + row.slug + '/solutions/',
      'Opens on leetcode.com — hundreds of user write-ups, sorted by votes',
      false,
    ]);
  }
  if (n) {
    external.push([
      'Lite editorial ↗',
      'https://algo.monster/liteproblems/' + n,
      'Opens on algo.monster — a short worked explanation',
      false,
    ]);
  }
  if (!row.slug && row.href) {
    external.push([row.title + ' — topic article ↗', row.href, 'The article this row links to', false]);
    external.push([
      'Striver A2Z sheet ↗',
      'https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/',
      'The sheet this row belongs to',
      false,
    ]);
  }
  return panel.concat(external);
}

/* ---------- 4. main ---------- */
const [ncRaw, doocsRaw] = await Promise.all([load('neetcode.json', SOURCES.neetcode), load('doocs.md', SOURCES.doocs)]);
const nc = parseNeetcode(ncRaw);
const doocs = parseDoocs(doocsRaw);
const rows = readRows();

const out = {};
const stats = { rows: rows.length, video: 0, doocs: 0, panelFirst: 0, noPanel: 0 };

for (const row of rows) {
  const ncHit = row.slug ? nc.get(row.slug) : null;
  let d = /^\d+$/.test(row.lc) ? doocs.byNum.get(row.lc) : null;
  if (!d && row.slug) d = doocs.bySlug.get(row.slug) || (SLUG_ALIAS[row.slug] ? doocs.byNum.get(String(SLUG_ALIAS[row.slug])) : null);
  if (d) stats.doocs++;

  const videos = [];
  if (ncHit) {
    stats.video++;
    videos.push([ncHit.video, row.title + ' — NeetCode walkthrough', 'NeetCode', '']);
  }
  const reads = buildReads(row, d, ncHit);
  if (reads.length && reads[0][3]) stats.panelFirst++;
  if (!reads.some((r) => r[3])) stats.noPanel++;

  out[row.lc] = {
    v: ncHit ? ncHit.video : '',
    t: esc(row.title),
    d: esc(row.diff),
    p: esc(row.pattern),
    l: esc(row.list),
    videos,
    reads,
  };
}

const header = `/* assets/dsa-resources.js — generated by tools/build_dsa_resources.mjs. Do not hand-edit.
   Generated: ${new Date().toISOString()}
   Rows: ${stats.rows} | verified NeetCode videos: ${stats.video} | English approach write-ups: ${stats.doocs}

   Every value here is traceable to a source fetched at build time:
     videos  <- neetcode-gh/leetcode .problemSiteData.json, matched on the LeetCode slug
     reads   <- doocs/leetcode solution/README_EN.md index, plus URLs derived from the
                problem's own slug or number.
   A problem with no NeetCode video gets no video entry; the rail then shows a
   labelled YouTube search rather than a video that might be the wrong one.
   reads[i][3] === true means the study panel can open it inline; those are
   listed first, and the ones that must open in a new tab come after. */
`;
fs.writeFileSync(OUT, header + 'window.dsaResources = ' + JSON.stringify(out) + ';\n');
console.log(JSON.stringify(stats, null, 1));
console.log('wrote', path.relative(ROOT, OUT), (fs.statSync(OUT).size / 1024).toFixed(0) + 'KB');
