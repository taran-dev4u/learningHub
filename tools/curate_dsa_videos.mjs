#!/usr/bin/env node
/**
 * Validate and complete tools/harvested_videos_cache.json.
 *
 * This script is intentionally conservative:
 * - every YouTube id is checked with oEmbed;
 * - LeetCode-number conflicts are rejected;
 * - titles must match the target problem/topic;
 * - output is capped and ordered by instructor/source quality.
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const SUMMARY_FILE = path.join(ROOT, 'tools', 'problems_summary.json');
const VIDEO_CACHE_FILE = path.join(ROOT, 'tools', 'harvested_videos_cache.json');
const OEMBED_CACHE_FILE = path.join(ROOT, 'tools', '.dsa-cache', 'dsa_video_oembed_cache.json');
const NEETCODE_FILE = path.join(ROOT, 'tools', '.dsa-cache', 'neetcode.json');
const MIN_VIDEOS = 5;
const SEARCH_LIMIT = 18;
const CONCURRENCY = 10;

const summary = JSON.parse(fs.readFileSync(SUMMARY_FILE, 'utf8'));
const videoCache = JSON.parse(fs.readFileSync(VIDEO_CACHE_FILE, 'utf8'));
const oembedCache = fs.existsSync(OEMBED_CACHE_FILE)
  ? JSON.parse(fs.readFileSync(OEMBED_CACHE_FILE, 'utf8'))
  : {};
const neetcodeRows = fs.existsSync(NEETCODE_FILE)
  ? JSON.parse(fs.readFileSync(NEETCODE_FILE, 'utf8'))
  : [];

const neetcodeBySlug = new Map();
for (const row of neetcodeRows) {
  const slug = String(row.link || '').replace(/^\/|\/$/g, '').toLowerCase();
  if (slug && row.video) neetcodeBySlug.set(slug, row.video);
}

const NUMBER_WORDS = new Map([
  ['0', 'zero'], ['1', 'one'], ['2', 'two'], ['3', 'three'], ['4', 'four'],
  ['5', 'five'], ['6', 'six'], ['7', 'seven'], ['8', 'eight'], ['9', 'nine'],
]);
const ROMANS = new Set(['ii', 'iii', 'iv', 'v']);
const CHANNEL_RANK = [
  ['neetcode', 120],
  ['take u forward', 110],
  ['striver', 110],
  ['techdose', 95],
  ['greg hogg', 90],
  ['nick white', 86],
  ['kevin naughton', 82],
  ['destination faang', 78],
  ['professor oakes', 74],
  ['codebix', 70],
  ['hello byte', 70],
  ['back to back', 68],
  ['tushar roy', 68],
  ['fisher coder', 62],
];

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function writeJsonAtomic(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = file + '.tmp.' + Date.now();
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2), 'utf8');
  fs.renameSync(tmp, file);
}

function words(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/\b(\d)\b/g, (_, d) => NUMBER_WORDS.get(d) || d)
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
    .split(/\s+/)
    .filter((w) => w && !['leetcode', 'leet', 'code', 'solution', 'solutions', 'problem', 'explained', 'python', 'java', 'javascript', 'cpp', 'amazon', 'microsoft'].includes(w));
}

function norm(value) {
  return words(value).join(' ');
}

function titleTokens(title) {
  const toks = words(title);
  return toks.filter((w) => w.length > 2 || NUMBER_WORDS.has(w));
}

function videoIdFromUrl(value) {
  const s = String(value || '');
  return s.match(/(?:v=|youtu\.be\/|embed\/|shorts\/)([A-Za-z0-9_-]{11})/)?.[1] || null;
}

function explicitLeetCodeNumbers(title) {
  const out = new Set();
  const s = String(title || '').toLowerCase();
  const re = /(?:leetcode|leet\s*code|\blc\b)\s*[#:.\- ]*\s*(\d{1,4})|#\s*(\d{1,4})/g;
  let m;
  while ((m = re.exec(s))) out.add(Number(m[1] || m[2]));
  return [...out].filter(Boolean);
}

function romanSuffixConflict(target, candidate) {
  const targetSet = new Set(words(target));
  const cand = words(candidate);
  if ([...ROMANS].some((r) => targetSet.has(r))) return false;
  const targetNorm = norm(target);
  const candNorm = cand.join(' ');
  return [...ROMANS].some((r) => cand.includes(r) && candNorm.includes(targetNorm + ' ' + r));
}

function relevance(problem, videoTitle) {
  const target = titleTokens(problem.title);
  const candidate = new Set(titleTokens(videoTitle));
  if (!target.length || !candidate.size) return 0;
  const targetNorm = norm(problem.title);
  const videoNorm = norm(videoTitle);
  const direct = videoNorm.includes(targetNorm) ? 0.55 : 0;
  const overlap = target.filter((w) => candidate.has(w)).length / target.length;
  return Math.max(overlap, direct);
}

function isRelevant(problem, videoTitle) {
  const nums = explicitLeetCodeNumbers(videoTitle);
  if (problem.lcNum && nums.length && !nums.includes(Number(problem.lcNum))) return false;
  if (romanSuffixConflict(problem.title, videoTitle)) return false;

  const score = relevance(problem, videoTitle);
  if (problem.lcNum && nums.includes(Number(problem.lcNum)) && score >= 0.25) return true;
  if (score >= 0.7) return true;
  if (problem.lcNum && nums.includes(Number(problem.lcNum))) return true;
  return false;
}

function rank(problem, video) {
  const [id, title, channel] = video;
  const author = String(channel || '').toLowerCase();
  let score = 0;
  if (problem.slug && neetcodeBySlug.get(problem.slug) === id) score += 1000;
  for (const [needle, value] of CHANNEL_RANK) {
    if (author.includes(needle)) {
      score += value;
      break;
    }
  }
  const nums = explicitLeetCodeNumbers(title);
  if (problem.lcNum && nums.includes(Number(problem.lcNum))) score += 40;
  score += relevance(problem, title) * 50;
  return score;
}

async function oembed(id) {
  if (oembedCache[id] !== undefined) return oembedCache[id];
  const target = 'https://www.youtube.com/watch?v=' + id;
  const url = 'https://www.youtube.com/oembed?url=' + encodeURIComponent(target) + '&format=json';
  try {
    const res = await fetch(url);
    if (!res.ok) {
      oembedCache[id] = null;
      return null;
    }
    const data = await res.json();
    oembedCache[id] = { title: data.title || '', author: data.author_name || '' };
    return oembedCache[id];
  } catch {
    oembedCache[id] = null;
    return null;
  }
}

async function searchIds(query) {
  try {
    const res = await fetch('https://www.youtube.com/results?search_query=' + encodeURIComponent(query));
    if (!res.ok) return [];
    const html = await res.text();
    return [...new Set([...html.matchAll(/(?:watch\?v=|videoId":"|\\"videoId\\":\\")([A-Za-z0-9_-]{11})/g)].map((m) => m[1]))].slice(0, SEARCH_LIMIT);
  } catch {
    return [];
  }
}

function queries(problem) {
  if (problem.lcNum) {
    return [
      `leetcode ${problem.lcNum} ${problem.title} solution`,
      `${problem.title} leetcode ${problem.lcNum} explained`,
      `${problem.title} leetcode ${problem.lcNum} python`,
    ];
  }
  return [
    `${problem.title} striver dsa`,
    `${problem.title} data structures algorithms explained`,
    `${problem.title} dsa tutorial`,
  ];
}

async function normalizeCandidate(problem, candidate) {
  const id = candidate && candidate[0] ? candidate[0] : videoIdFromUrl(candidate && candidate[1]);
  if (!id || !/^[A-Za-z0-9_-]{11}$/.test(id)) return null;
  const meta = await oembed(id);
  if (!meta || !isRelevant(problem, meta.title)) return null;
  return [id, meta.title, meta.author || candidate[2] || 'YouTube', candidate[3] || '', 'Verified direct match'];
}

async function curateProblem(problem) {
  const initial = [];
  if (problem.slug && neetcodeBySlug.has(problem.slug)) {
    initial.push([neetcodeBySlug.get(problem.slug), problem.title, 'NeetCode', '', 'Official NeetCode metadata']);
  }
  initial.push(...(videoCache[problem.lcId] || []));

  const byId = new Map();
  for (const cand of initial) {
    const video = await normalizeCandidate(problem, cand);
    if (video) byId.set(video[0], video);
  }

  for (const query of queries(problem)) {
    if (byId.size >= MIN_VIDEOS) break;
    const ids = await searchIds(query);
    for (const id of ids) {
      if (byId.has(id)) continue;
      const video = await normalizeCandidate(problem, [id]);
      if (video) byId.set(id, video);
      if (byId.size >= MIN_VIDEOS) break;
    }
  }

  const videos = [...byId.values()]
    .sort((a, b) => rank(problem, b) - rank(problem, a))
    .slice(0, MIN_VIDEOS);
  videoCache[problem.lcId] = videos;
  return videos.length;
}

async function main() {
  let next = 0;
  const failures = [];
  let done = 0;

  async function worker() {
    while (next < summary.length) {
      const problem = summary[next++];
      const count = await curateProblem(problem);
      done++;
      if (count < MIN_VIDEOS) failures.push({ id: problem.lcId, title: problem.title, count });
      if (done % 50 === 0 || done === summary.length) {
        console.log(`curated ${done}/${summary.length}; short=${failures.length}`);
        writeJsonAtomic(VIDEO_CACHE_FILE, videoCache);
        writeJsonAtomic(OEMBED_CACHE_FILE, oembedCache);
      }
      await sleep(40);
    }
  }

  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  writeJsonAtomic(VIDEO_CACHE_FILE, videoCache);
  writeJsonAtomic(OEMBED_CACHE_FILE, oembedCache);

  const counts = {};
  for (const p of summary) {
    const n = (videoCache[p.lcId] || []).length;
    counts[n] = (counts[n] || 0) + 1;
  }
  console.log('video distribution:', counts);
  if (failures.length) {
    console.error(`FAIL: ${failures.length} problems still have fewer than ${MIN_VIDEOS} videos`);
    failures.slice(0, 30).forEach((f) => console.error(`  - ${f.id} ${f.title}: ${f.count}`));
    process.exit(1);
  }
  console.log('OK: every DSA row has at least 5 verified direct videos.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
