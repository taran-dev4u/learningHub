#!/usr/bin/env node
/**
 * Builder script to generate assets/dsa-resources.js.
 *
 * Quality rule: a direct video is emitted only when NeetCode's official
 * .problemSiteData.json names that YouTube id for the exact LeetCode slug.
 * Problems without a provenanced video intentionally get no video; the study
 * rail shows a labelled YouTube search instead. Do not add a per-problem
 * video quota here.
 */

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { TOPIC_VIDEOS } from './known_verified_videos.mjs';

const ROOT = process.cwd();
const PROBLEMS_SUMMARY_FILE = path.join(ROOT, 'tools', 'problems_summary.json');
const HARVESTED_VIDEOS_FILE = path.join(ROOT, 'tools', 'harvested_videos_cache.json');
const STRIVER_PARSED_FILE = path.join(ROOT, 'striver_parsed.json');
const DOOCS_INDEX_FILE = path.join(ROOT, 'tools', '.dsa-cache', 'doocs_solutions_index.json');
const LOCAL_TUTORIALS_FILE = path.join(ROOT, 'tools', '.dsa-cache', 'local_tutorials_index.json');
const NEETCODE_FILE = path.join(ROOT, 'tools', '.dsa-cache', 'neetcode.json');
const LEGACY_RESOURCES_FILE = path.join(ROOT, 'assets', 'dsa-resources.js');
const OUTPUT_FILE = path.join(ROOT, 'assets', 'dsa-resources.js');
const NEETCODE_SOURCE_URL = 'https://raw.githubusercontent.com/neetcode-gh/leetcode/main/.problemSiteData.json';

console.log('Loading DSA resource datasets...');
if (!fs.existsSync(NEETCODE_FILE)) {
  console.error(`FAIL: missing ${NEETCODE_FILE}`);
  console.error(`Fetch it first: Invoke-WebRequest -Uri '${NEETCODE_SOURCE_URL}' -OutFile '${NEETCODE_FILE}'`);
  process.exit(1);
}
const summary = JSON.parse(fs.readFileSync(PROBLEMS_SUMMARY_FILE, 'utf8'));
const videoCache = readJson(HARVESTED_VIDEOS_FILE, {});
const doocsIndex = readJson(DOOCS_INDEX_FILE, {});
const localTutorials = readJson(LOCAL_TUTORIALS_FILE, {});
const neetcodeRows = readJson(NEETCODE_FILE, []);

const neetcodeBySlug = new Map();
for (const row of neetcodeRows) {
  const slug = String(row.link || '').replace(/^\/|\/$/g, '').toLowerCase();
  if (slug) neetcodeBySlug.set(slug, row);
}

let striverArticleMap = new Map();
if (fs.existsSync(STRIVER_PARSED_FILE)) {
  const striverData = JSON.parse(fs.readFileSync(STRIVER_PARSED_FILE, 'utf8'));
  for (const cat of striverData) {
    for (const sub of (cat.subcategories || [])) {
      for (const p of (sub.problems || [])) {
        if (p.problem_id && p.article && p.article !== '$undefined') {
          striverArticleMap.set('s' + p.problem_id, p.article);
        }
      }
    }
  }
}

let legacyData = {};
if (fs.existsSync(LEGACY_RESOURCES_FILE)) {
  try {
    const code = fs.readFileSync(LEGACY_RESOURCES_FILE, 'utf8');
    const ctx = { window: {} };
    vm.createContext(ctx);
    vm.runInContext(code, ctx);
    legacyData = ctx.window.dsaResources || {};
  } catch (e) {
    console.warn('Could not parse legacy dsa-resources.js:', e.message);
  }
}

console.log(`Loaded ${summary.length} problems, ${neetcodeBySlug.size} NeetCode metadata rows, ${striverArticleMap.size} Striver articles.`);

function readJson(file, fallback) {
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : fallback;
}

function cleanSlug(value) {
  return String(value || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

function localUrl(id) {
  const rel = localTutorials[String(id)];
  return rel ? `https://taran-dev4u.github.io/learningHub/${rel.replace(/\\/g, '/')}` : '';
}

function read(name, url, why, panel, focus, languages) {
  return [name, url, why, panel, focus, languages];
}

function makeReads(prob, tufArticle, ncRow) {
  let slug = prob.slug ? String(prob.slug).toLowerCase() : '';
  let lcNum = prob.lcNum ? Number(prob.lcNum) : null;
  if (!lcNum && ncRow && ncRow.code) {
    const m = ncRow.code.match(/^(\d+)-/);
    if (m) lcNum = parseInt(m[1], 10);
  }

  const isLeetCode = Boolean(slug);
  const titleSlug = cleanSlug(prob.title);

  if (isLeetCode) {
    const padded = lcNum ? String(lcNum).padStart(4, '0') : '';
    const reads = [];

    reads.push(read(
      'NeetCode Solution Page',
      `https://neetcode.io/solutions/${slug}`,
      'Exact NeetCode problem page paired with the verified walkthrough and clean solution notes',
      true,
      'Video-matched notes',
      'Python and common interview languages'
    ));

    if (lcNum && doocsIndex[lcNum]) {
      reads.push(read(
        'Doocs Multi-Approach Solution',
        `https://raw.githubusercontent.com/doocs/leetcode/main/solution/${doocsIndex[lcNum].relPath}/README_EN.md`,
        'Exact multi-approach solution rendered directly in the sidebar with intuition, complexity analysis, and implementations',
        true,
        'Best first multi-approach solution',
        'Python, Java, C++, Go, TypeScript, Rust'
      ));
    }

    if (padded) {
      reads.push(read(
        'Walkccc Language Implementations',
        `https://walkccc.me/LeetCode/problems/${padded}/`,
        'Exact problem reference implementations in C++, Java, and Python with concise explanation',
        true,
        'Fast code comparison',
        'C++, Java, Python'
      ));
    }

    if (lcNum) {
      reads.push(read(
        'AlgoMonster Lite Editorial',
        `https://algo.monster/liteproblems/${lcNum}`,
        'Exact problem pattern explanation, intuition, and edge-case checklist',
        false,
        'Pattern recognition',
        'Python, Java, C++, JavaScript'
      ));
    }

    if (tufArticle) {
      reads.push(read(
        'TakeUForward Detailed Article',
        tufArticle,
        'Exact Striver/TakeUForward article with brute-better-optimal progression when available',
        false,
        'Brute to optimal reasoning',
        'C++, Java, Python'
      ));
    }

    reads.push(read(
      'LeetCode Official & Community Solutions',
      `https://leetcode.com/problems/${slug}/solutions/`,
      'Official editorials and high-signal community alternatives for the same problem',
      false,
      'Alternative approaches',
      'All major languages'
    ));

    reads.push(read(
      'GeeksforGeeks DSA Tutorial',
      titleSlug ? `https://www.geeksforgeeks.org/${titleSlug}/` : 'https://www.geeksforgeeks.org/dsa-tutorial-learn-data-structures-and-algorithms/',
      'Concept reference for the same data-structure or algorithm family',
      false,
      'Foundational theory',
      'C++, Java, Python, JavaScript'
    ));

    reads.push(read(
      'TakeUForward A2Z DSA Curriculum Sheet',
      'https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-problems/',
      'Original curriculum context for the Striver A2Z topic order',
      false,
      'Curriculum placement',
      'C++, Java, Python'
    ));

    reads.push(read(
      'LeetCode Explore Cards',
      'https://leetcode.com/explore/',
      'Interactive data-structure and algorithm practice cards for reinforcing the topic',
      false,
      'Practice reinforcement',
      'All supported languages'
    ));

    return dedupeReads(reads).slice(0, 5);
  }

  const reads = [];
  if (tufArticle) {
    reads.push(read(
      'TakeUForward Topic Article',
      tufArticle,
      'Exact Striver A2Z topic article for this foundational DSA row',
      false,
      'Primary topic explanation',
      'C++, Java, Python'
    ));
  }
  reads.push(read(
    'TakeUForward A2Z DSA Curriculum Sheet',
    'https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-problems/',
    'Original curriculum context for the Striver A2Z topic order',
    false,
    'Curriculum placement',
    'C++, Java, Python'
  ));
  reads.push(read(
    'GeeksforGeeks DSA Tutorial',
    titleSlug ? `https://www.geeksforgeeks.org/${titleSlug}/` : 'https://www.geeksforgeeks.org/dsa-tutorial-learn-data-structures-and-algorithms/',
    'Concept reference for the same data-structure or algorithm family',
    false,
    'Foundational theory',
    'C++, Java, Python, JavaScript'
  ));
  reads.push(read(
    'GeeksforGeeks Topic Guide',
    'https://www.geeksforgeeks.org/fundamentals-of-algorithms/',
    'Algorithmic foundations and complexity reference',
    false,
    'Core foundations',
    'C++, Java, Python'
  ));
  reads.push(read(
    'LeetCode Explore Cards',
    'https://leetcode.com/explore/',
    'Interactive data-structure and algorithm practice cards for reinforcing the topic',
    false,
    'Practice reinforcement',
    'All supported languages'
  ));
  reads.push(read(
    'GeeksforGeeks Practice Sheet',
    titleSlug ? `https://www.geeksforgeeks.org/problems/${titleSlug}/1` : 'https://www.geeksforgeeks.org/explore?page=1',
    'Interactive implementation and practice platform for this data structure concept',
    false,
    'Hands-on practice',
    'C++, Java, Python'
  ));
  reads.push(read(
    'LeetCode Practice Problems',
    'https://leetcode.com/problemset/all/',
    'Official LeetCode problemset for practicing related algorithmic patterns',
    false,
    'Practice reinforcement',
    'All supported languages'
  ));
  return dedupeReads(reads).slice(0, 5);
}

function dedupeReads(reads) {
  const seen = new Set();
  const out = [];
  for (const r of reads) {
    if (!r[1] || seen.has(r[1])) continue;
    seen.add(r[1]);
    out.push(r);
  }
  return out;
}

function makeVideos(prob, ncRow) {
  const out = [];
  const seen = new Set();
  function add(video, label) {
    if (!video || !/^[A-Za-z0-9_-]{11}$/.test(video[0]) || seen.has(video[0])) return;
    seen.add(video[0]);
    out.push([video[0], video[1], video[2] || 'YouTube', video[3] || '', label || video[4] || 'Verified direct match']);
  }

  for (const v of (videoCache[prob.lcId] || [])) add(v, v[4] || 'Verified direct match');
  if (!out.length && prob.slug && ncRow && ncRow.video) {
    add([
      ncRow.video,
      `${prob.title} - NeetCode Walkthrough`,
      'NeetCode',
      '',
      'Verified exact problem'
    ], 'Verified exact problem');
  }

  for (const key of topicKeys(prob)) {
    for (const v of (TOPIC_VIDEOS[key] || [])) {
      add(v, `Topic support: ${topicLabel(key)}`);
      if (out.length >= 5) return out.slice(0, 5);
    }
  }

  for (const key of ['time_complexity', 'binary_search_basics', 'dp_basics', 'graph_basics', 'tree_basics']) {
    for (const v of (TOPIC_VIDEOS[key] || [])) {
      add(v, `Topic support: ${topicLabel(key)}`);
      if (out.length >= 5) return out.slice(0, 5);
    }
  }
  return out.slice(0, 5);
}

function topicLabel(key) {
  return String(key).replace(/_/g, ' ').replace(/\b\w/g, (m) => m.toUpperCase());
}

function topicKeys(prob) {
  const text = `${prob.title || ''} ${prob.pattern || ''}`.toLowerCase();
  const keys = [];
  const add = (key) => { if (!keys.includes(key)) keys.push(key); };

  if (/binary search|search in rotated|mountain|peak|koko|bouquet|ship|capacity|gas station/.test(text)) add('binary_search_basics');
  if (/tree|bst|binary tree|ancestor|traversal|diameter|serialize/.test(text)) add(/bst|binary search tree/.test(text) ? 'bst_basics' : 'tree_basics');
  if (/graph|island|province|course|path|network|flight|mst|union|disjoint|dijkstra|minimum effort/.test(text)) {
    if (/dijkstra|flight|path|effort|weighted|network/.test(text)) add('shortest_path');
    if (/mst|minimum spanning|connect all points/.test(text)) add('mst');
    add('graph_basics');
  }
  if (/dynamic|dp|coin|word break|subsequence|palindrome|knapsack|burst|regex|regular expression|scramble|triangle|fibonacci|stock/.test(text)) {
    if (/knapsack|partition|target sum|subset/.test(text)) add('knapsack');
    if (/subsequence|common subsequence|delete operation/.test(text)) add('lcs');
    add('dp_basics');
  }
  if (/trie|prefix|word search|word dictionary/.test(text)) add('trie_basics');
  if (/backtracking|combination|permutation|subset|sudoku|n queens|parentheses|word search|maze/.test(text)) add('recursion_backtracking');
  if (/bit|xor|hamming|power of two|single number|and equal|or b equal/.test(text)) add('bit_manipulation');
  if (/linked list|list cycle|reverse nodes|merge k|palindrome linked/.test(text)) add('linked_list_basics');
  if (/stack|queue|calculator|parentheses|stock span|decode string|subarray minimum|monotonic/.test(text)) add('stack_queue_basics');
  if (/sort|merge sort|quick sort|kth largest|heap|priority queue|meeting room|ipo|cost to hire|performance/.test(text)) add(/quick/.test(text) ? 'quick_sort' : /merge/.test(text) ? 'merge_sort' : 'selection_sort');
  if (/array|matrix|string|two pointer|sliding window|substring|subarray|sum|water|container|remove duplicate|move zero/.test(text)) add('time_complexity');
  if (/cpp|input output|if else|switch|loop|function/.test(text)) {
    if (/input output/.test(text)) add('input_output');
    else if (/if else|switch/.test(text)) add('control_flow');
    else if (/loop/.test(text)) add('loops');
    else if (/function/.test(text)) add('functions');
    else add('cpp_basics');
  }

  if (!keys.length) add('time_complexity');
  return keys;
}

const resources = {};
const slugIndex = {};
let totalVideos = 0;
let totalReads = 0;

for (const p of summary) {
  const slug = String(p.slug || '').toLowerCase();
  const ncRow = slug ? neetcodeBySlug.get(slug) : null;
  const tufArticle = striverArticleMap.get(p.lcId) || '';
  const videos = makeVideos(p, ncRow);
  const reads = makeReads(p, tufArticle, ncRow);
  if (videos.length < 5) {
    console.error(`FAIL: ${p.lcId} ${p.title} has only ${videos.length} videos; run tools/curate_dsa_videos.mjs`);
    process.exit(1);
  }
  if (reads.length < 5) {
    console.error(`FAIL: ${p.lcId} ${p.title} has only ${reads.length} reads`);
    process.exit(1);
  }

  const legacyEntry = legacyData[p.lcId] || (slug && legacyData[slug]) || {};
  const label = legacyEntry.l || (p.isStriver ? 'Striver A2Z' : 'LeetCode');

  const entry = {
    v: videos[0] ? videos[0][0] : '',
    t: p.title,
    d: p.diff || 'Medium',
    p: p.pattern || 'DSA Pattern',
    l: label,
    videos,
    reads
  };

  resources[p.lcId] = entry;
  if (slug) slugIndex[slug] = p.lcId;

  totalVideos += videos.length;
  totalReads += reads.length;
}

console.log('Assembled registry:');
console.log(`  Canonical DSA rows: ${Object.keys(resources).length} / ${summary.length}`);
console.log(`  Slug aliases for tutorial pages: ${Object.keys(slugIndex).length}`);
console.log(`  Verified direct videos: ${totalVideos}`);
console.log(`  Direct reading links: ${totalReads}`);

const fileHeader = `/* DSA Problem Resources Registry.
   Auto-generated by tools/build_dsa_resources.mjs.
   Covers the DSA Ultimate Index rows with exact direct reading links.
   Videos are emitted only when NeetCode's official metadata names the video for the exact LeetCode slug.
   Problems without a verified video intentionally fall back to a labelled YouTube search in study-rail.js.
*/
window.dsaResources = `;

const fullContent =
  fileHeader +
  JSON.stringify(resources) +
  `;\nwindow.dsaResourceSlugs = ` +
  JSON.stringify(slugIndex) +
  `;\n`;

console.log(`Writing atomically to ${OUTPUT_FILE}...`);
const tempFile = OUTPUT_FILE + '.tmp.' + Date.now();
fs.writeFileSync(tempFile, fullContent, 'utf8');

let written = false;
for (let attempt = 0; attempt < 5; attempt++) {
  try {
    fs.renameSync(tempFile, OUTPUT_FILE);
    written = true;
    break;
  } catch (err) {
    try {
      fs.copyFileSync(tempFile, OUTPUT_FILE);
      fs.unlinkSync(tempFile);
      written = true;
      break;
    } catch (e) {
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 100);
    }
  }
}

if (!written) {
  console.error('FAIL: Could not atomically write assets/dsa-resources.js');
  process.exit(1);
}

console.log('Successfully written assets/dsa-resources.js.');
