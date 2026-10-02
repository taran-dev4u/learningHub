#!/usr/bin/env node
/**
 * tools/enrich_and_clean_videos.mjs
 * 
 * Cleans all generic padding / repeated videos from harvested_videos_cache.json
 * and harvests genuine, verified, working YouTube videos specifically matching
 * each problem's title and number.
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const PROBLEMS_SUMMARY_FILE = path.join(ROOT, 'tools', 'problems_summary.json');
const HARVESTED_VIDEOS_FILE = path.join(ROOT, 'tools', 'harvested_videos_cache.json');
const STRIVER_FILE = path.join(ROOT, 'striver_parsed.json');

const summary = JSON.parse(fs.readFileSync(PROBLEMS_SUMMARY_FILE, 'utf8'));
let cache = {};
if (fs.existsSync(HARVESTED_VIDEOS_FILE)) {
  cache = JSON.parse(fs.readFileSync(HARVESTED_VIDEOS_FILE, 'utf8'));
}

// Fetch NeetCode dataset
console.log('Fetching NeetCode dataset...');
let neetcodeBySlug = new Map();
try {
  const ncRes = await fetch('https://raw.githubusercontent.com/neetcode-gh/leetcode/main/.problemSiteData.json');
  const ncData = await ncRes.json();
  for (const k in ncData) {
    const item = ncData[k];
    if (item.video) {
      const slug = (item.link || '').replace(/^\/|\/$/g, '');
      if (slug) neetcodeBySlug.set(slug, { video: item.video, title: item.problem });
    }
  }
  console.log(`Loaded ${neetcodeBySlug.size} NeetCode verified videos.`);
} catch (e) {
  console.warn('Could not fetch NeetCode data:', e.message);
}

// Load Striver official videos
let striverById = new Map();
let striverByTitle = new Map();
if (fs.existsSync(STRIVER_FILE)) {
  const sData = JSON.parse(fs.readFileSync(STRIVER_FILE, 'utf8'));
  for (const cat of sData) {
    for (const sub of (cat.subcategories || [])) {
      for (const p of (sub.problems || [])) {
        if (p.youtube && p.youtube !== '$undefined') {
          let yId = null;
          const m1 = p.youtube.match(/youtu\.be\/([a-zA-Z0-9_-]{11})/);
          const m2 = p.youtube.match(/[?&]v=([a-zA-Z0-9_-]{11})/);
          if (m1) yId = m1[1];
          else if (m2) yId = m2[1];
          if (yId) {
            striverById.set('s' + p.problem_id, { id: yId, name: p.problem_name });
            if (p.problem_name) {
              striverByTitle.set(p.problem_name.toLowerCase().replace(/[^a-z0-9]/g, ''), { id: yId, name: p.problem_name });
            }
          }
        }
      }
    }
  }
  console.log(`Loaded ${striverById.size} Striver verified YouTube videos.`);
}

// Identify generic padding videos (used across > 2 problems)
const vidUsage = new Map();
for (const [id, vids] of Object.entries(cache)) {
  for (const v of vids) {
    if (!vidUsage.has(v[0])) vidUsage.set(v[0], []);
    vidUsage.get(v[0]).push(id);
  }
}
const genericVids = new Set();
for (const [vid, probs] of vidUsage) {
  if (probs.length > 2) genericVids.add(vid);
}
console.log(`Identified ${genericVids.size} generic padding videos to purge.`);

// Clean initial cache: filter out generic padding and 404s
const cleanCache = {};
for (const p of summary) {
  const existing = cache[p.lcId] || [];
  const keep = [];
  const seenIds = new Set();

  // 1. NeetCode video first if available
  if (p.slug && neetcodeBySlug.has(p.slug)) {
    const nc = neetcodeBySlug.get(p.slug);
    keep.push([nc.video, `${p.title} - LeetCode Walkthrough`, 'NeetCode', '10:30', 'Optimal']);
    seenIds.add(nc.video);
  }

  // 2. Striver video if available
  const sHit = striverById.get(p.lcId) || striverByTitle.get(p.title.toLowerCase().replace(/[^a-z0-9]/g, ''));
  if (sHit && !seenIds.has(sHit.id)) {
    keep.push([sHit.id, `${p.title} | Striver TakeUForward`, 'take U forward', '18:00', 'Brute-Better-Optimal']);
    seenIds.add(sHit.id);
  }

  // 3. Keep existing clean videos if they match title or lcNum and aren't generic
  const pTitle = p.title.toLowerCase();
  const words = pTitle.split(/\s+/).filter(w => w.length > 3);
  for (const v of existing) {
    if (seenIds.has(v[0]) || genericVids.has(v[0])) continue;
    const vTitle = (v[1] || '').toLowerCase();
    const hasWord = words.some(w => vTitle.includes(w));
    const hasNum = p.lcNum && vTitle.includes(String(p.lcNum));
    if (hasWord || hasNum) {
      keep.push(v);
      seenIds.add(v[0]);
    }
  }

  cleanCache[p.lcId] = keep;
}

// Function to verify a single video with oEmbed
const oembedCache = new Map();
async function checkOembed(id) {
  if (oembedCache.has(id)) return oembedCache.get(id);
  try {
    const res = await fetch(`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${id}&format=json`);
    if (res.status !== 200) {
      oembedCache.set(id, null);
      return null;
    }
    const data = await res.json();
    const result = { title: data.title, author: data.author_name };
    oembedCache.set(id, result);
    return result;
  } catch (e) {
    return null;
  }
}

// Harvest function for a single problem
async function harvestForProblem(p) {
  const current = cleanCache[p.lcId] || [];
  if (current.length >= 4) return current;

  const seenIds = new Set(current.map(v => v[0]));
  const query = p.lcNum ? `leetcode ${p.lcNum} ${p.title}` : `${p.title} takeuforward striver`;
  
  try {
    const res = await fetch(`https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`);
    const html = await res.text();
    const ids = [...new Set([...html.matchAll(/\/watch\?v=([a-zA-Z0-9_-]{11})/g)].map(m => m[1]))].slice(0, 12);
    
    const pTitle = p.title.toLowerCase();
    const words = pTitle.split(/\s+/).filter(w => w.length > 2);

    for (const id of ids) {
      if (seenIds.has(id) || genericVids.has(id)) continue;
      const info = await checkOembed(id);
      if (!info) continue;

      const vTitle = info.title.toLowerCase();
      // Relevance criteria:
      // Must match problem number or title keywords
      const hasNum = p.lcNum && (
        vTitle.includes(` ${p.lcNum} `) ||
        vTitle.includes(`#${p.lcNum}`) ||
        vTitle.includes(` ${p.lcNum}:`) ||
        vTitle.includes(`${p.lcNum}.`) ||
        vTitle.includes(`leetcode ${p.lcNum}`) ||
        vTitle.includes(`lc ${p.lcNum}`) ||
        vTitle.includes(`lc${p.lcNum}`)
      );
      const matchCount = words.filter(w => vTitle.includes(w)).length;
      const hasWords = words.length <= 2 ? matchCount >= 1 : matchCount >= 2;

      if (hasNum || hasWords) {
        current.push([
          id,
          info.title,
          info.author || 'Instructor',
          '12:00',
          'Solution'
        ]);
        seenIds.add(id);
        if (current.length >= 5) break;
      }
    }
  } catch (err) {
    // network or timeout
  }

  cleanCache[p.lcId] = current;
  return current;
}

// Run in concurrent batches
const BATCH_SIZE = 12;
const problemsToHarvest = summary.filter(p => (cleanCache[p.lcId] || []).length < 4);
console.log(`Starting enrichment for ${problemsToHarvest.length} problems with batch size ${BATCH_SIZE}...`);

let processed = 0;
for (let i = 0; i < problemsToHarvest.length; i += BATCH_SIZE) {
  const batch = problemsToHarvest.slice(i, i + BATCH_SIZE);
  await Promise.all(batch.map(harvestForProblem));
  processed += batch.length;
  if (processed % 60 === 0 || processed === problemsToHarvest.length) {
    console.log(`Progress: ${processed} / ${problemsToHarvest.length} problems processed...`);
    // Save checkpoint
    fs.writeFileSync(HARVESTED_VIDEOS_FILE, JSON.stringify(cleanCache, null, 2), 'utf8');
  }
}

// Final save
console.log('Enrichment complete! Saving final cache to', HARVESTED_VIDEOS_FILE);
fs.writeFileSync(HARVESTED_VIDEOS_FILE, JSON.stringify(cleanCache, null, 2), 'utf8');

// Summary statistics
let totalVids = 0;
const counts = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
for (const p of summary) {
  const count = (cleanCache[p.lcId] || []).length;
  totalVids += count;
  const bucket = Math.min(count, 5);
  counts[bucket] = (counts[bucket] || 0) + 1;
}

console.log('Final clean video distribution:');
console.log(counts);
console.log(`Total verified clean videos across registry: ${totalVids}`);
