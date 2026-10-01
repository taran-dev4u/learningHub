#!/usr/bin/env node
/**
 * Validation Script for assets/dsa-resources.js
 * Verifies 100% compliance across all 940 distinct DSA problems.
 */

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const ROOT = process.cwd();
const DSA_RESOURCES_PATH = path.join(ROOT, 'assets', 'dsa-resources.js');
const DSA_INDEX_PATH = path.join(ROOT, 'DSA_Ultimate_Index.html');

console.log('====================================================');
console.log('DSA Resources Registry Validation');
console.log('====================================================');

// 1. File existence
if (!fs.existsSync(DSA_RESOURCES_PATH)) {
  console.error('FAIL: assets/dsa-resources.js not found!');
  process.exit(1);
}

// 2. Syntax check
const code = fs.readFileSync(DSA_RESOURCES_PATH, 'utf8');
const ctx = { window: {} };
try {
  vm.createContext(ctx);
  vm.runInContext(code, ctx);
} catch (err) {
  console.error('FAIL: Syntax or execution error in assets/dsa-resources.js:', err.message);
  process.exit(1);
}

const data = ctx.window.dsaResources;
if (!data || typeof data !== 'object') {
  console.error('FAIL: window.dsaResources is not defined or not an object');
  process.exit(1);
}

console.log(`PASS: assets/dsa-resources.js loaded successfully. Total keys: ${Object.keys(data).length}`);

// 3. Extract all 940 distinct problem IDs from DSA_Ultimate_Index.html
const html = fs.readFileSync(DSA_INDEX_PATH, 'utf8');
const rowRegex = /<li\b([^>]*\bdata-lc=["']([^"']+)["'][^>]*)>([\s\S]*?)<\/li>/gi;
let match;
const expectedProblems = new Map();

function getAttr(tagStr, attrName) {
  const m = tagStr.match(new RegExp(`\\b${attrName}=["']([^"']*)["']`, 'i'));
  return m ? m[1] : '';
}

while ((match = rowRegex.exec(html)) !== null) {
  const attrs = match[1];
  const lcId = match[2];
  const innerHtml = match[3];

  if (expectedProblems.has(lcId)) continue;

  const aRegex = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi;
  let aMatch;
  let title = '';
  let href = '';
  while ((aMatch = aRegex.exec(innerHtml)) !== null) {
    const aAttrs = aMatch[1];
    const aText = aMatch[2].replace(/<[^>]+>/g, '').trim();
    const aClass = getAttr(aAttrs, 'class');
    const aHref = getAttr(aAttrs, 'href');
    if (/\b(?:pname|problem-name)\b/i.test(aClass)) {
      title = aText;
      href = aHref;
    }
  }

  let slug = '';
  const slugM = href.match(/leetcode\.com\/problems\/([a-z0-9-]+)/i);
  if (slugM) slug = slugM[1].toLowerCase();

  expectedProblems.set(lcId, {
    lcId,
    title,
    href,
    slug,
    isStriver: lcId.startsWith('s')
  });
}

console.log(`Discovered ${expectedProblems.size} distinct problem IDs in DSA_Ultimate_Index.html (expected 940)`);
if (expectedProblems.size !== 940) {
  console.error(`FAIL: Expected exactly 940 distinct problems, found ${expectedProblems.size}`);
  process.exit(1);
}

// 4. Validate each problem
let errors = [];
let totalVideos = 0;
let totalReads = 0;
let verifiedProblemCount = 0;

const validPlatforms = /walkccc\.me|leetcode\.doocs\.org|neetcode\.io|algo\.monster|geeksforgeeks\.org|takeuforward\.org|leetcode\.com|raw\.githubusercontent\.com/i;

for (const [lcId, prob] of expectedProblems) {
  // Can be keyed by lcId or slug
  let entry = data[lcId];
  if (!entry && prob.slug) entry = data[prob.slug];

  if (!entry) {
    errors.push(`[${lcId}] Missing entry in dsaResources for "${prob.title}" (slug: "${prob.slug}")`);
    continue;
  }

  verifiedProblemCount++;

  // Validate backwards compatibility
  if (!entry.v || typeof entry.v !== 'string') {
    errors.push(`[${lcId}] Missing or invalid primary video ID 'v'`);
  }
  if (!entry.t || typeof entry.t !== 'string') {
    errors.push(`[${lcId}] Missing or invalid title 't'`);
  }
  if (!entry.d || typeof entry.d !== 'string') {
    errors.push(`[${lcId}] Missing or invalid difficulty 'd'`);
  }
  if (!entry.p || typeof entry.p !== 'string') {
    errors.push(`[${lcId}] Missing or invalid pattern 'p'`);
  }

  // Validate videos array
  if (!Array.isArray(entry.videos)) {
    errors.push(`[${lcId}] Missing 'videos' array`);
  } else {
    if (entry.videos.length < 4 || entry.videos.length > 5) {
      errors.push(`[${lcId}] Expected 4 to 5 videos, got ${entry.videos.length}`);
    }
    totalVideos += entry.videos.length;

    // Check entry.v matches primary video
    if (entry.videos.length > 0) {
      const firstId = Array.isArray(entry.videos[0]) ? entry.videos[0][0] : entry.videos[0].id;
      if (entry.v !== firstId) {
        errors.push(`[${lcId}] Backwards-compatible 'v' (${entry.v}) does not match first video ID (${firstId})`);
      }
    }

    entry.videos.forEach((vid, vIdx) => {
      const id = Array.isArray(vid) ? vid[0] : vid.id;
      const title = Array.isArray(vid) ? vid[1] : vid.title;
      const ch = Array.isArray(vid) ? vid[2] : vid.channel;
      const dur = Array.isArray(vid) ? vid[3] : vid.duration;
      const app = Array.isArray(vid) ? vid[4] : vid.approach;

      if (!id || typeof id !== 'string' || !/^[A-Za-z0-9_-]{11}$/.test(id)) {
        errors.push(`[${lcId}] Video #${vIdx + 1} has invalid 11-char YouTube ID: "${id}"`);
      }
      if (String(id).includes('search_query') || String(id).includes('results?')) {
        errors.push(`[${lcId}] Video #${vIdx + 1} is a search query URL! Must be direct video ID.`);
      }
      if (/takeuforward\.org|geeksforgeeks\.org|leetcode\.com|walkccc\.me/i.test(String(id))) {
        errors.push(`[${lcId}] Video #${vIdx + 1} contains an article/blog URL!`);
      }
      if (!title || typeof title !== 'string' || title.trim().length === 0) {
        errors.push(`[${lcId}] Video #${vIdx + 1} is missing title`);
      }
      if (!ch || typeof ch !== 'string' || ch.trim().length === 0) {
        errors.push(`[${lcId}] Video #${vIdx + 1} is missing channel`);
      }
    });
  }

  // Validate reads array
  if (!Array.isArray(entry.reads)) {
    errors.push(`[${lcId}] Missing 'reads' array`);
  } else {
    if (entry.reads.length < 4 || entry.reads.length > 5) {
      errors.push(`[${lcId}] Expected 4 to 5 reads, got ${entry.reads.length}`);
    }
    totalReads += entry.reads.length;

    entry.reads.forEach((r, rIdx) => {
      const name = Array.isArray(r) ? r[0] : r.name;
      const url = Array.isArray(r) ? r[1] : r.url;
      const approach = Array.isArray(r) ? r[2] : (r.approach || (r.meta && r.meta.approach));
      const embed = Array.isArray(r) ? r[3] : (r.embed ?? (r.meta && r.meta.embed));
      const complexity = Array.isArray(r) ? r[4] : (r.complexity || (r.meta && r.meta.complexity));

      if (!url || typeof url !== 'string' || !url.startsWith('https://') || !validPlatforms.test(url)) {
        errors.push(`[${lcId}] Read #${rIdx + 1} invalid URL or platform: "${url}"`);
      }
      if (/youtube\.com|youtu\.be/i.test(String(url))) {
        errors.push(`[${lcId}] Read #${rIdx + 1} contains a YouTube URL in reads array: "${url}"`);
      }
      if (!approach || typeof approach !== 'string' || approach.trim().length === 0) {
        errors.push(`[${lcId}] Read #${rIdx + 1} is missing approach annotation`);
      }
      if (/walkccc\.me|leetcode\.doocs\.org/i.test(url) && embed !== true) {
        errors.push(`[${lcId}] Read #${rIdx + 1} (${url}) must have embed: true`);
      }
      if (/algo\.monster|geeksforgeeks\.org|takeuforward\.org|leetcode\.com/i.test(url) && embed === true) {
        errors.push(`[${lcId}] Read #${rIdx + 1} (${url}) must have embed: false`);
      }
      if (!complexity || typeof complexity !== 'string' || complexity.trim().length === 0) {
        errors.push(`[${lcId}] Read #${rIdx + 1} is missing complexity summary`);
      }
    });

    // Check non-LeetCode conceptual Striver problems: no broken Walkccc URLs!
    if (prob.isStriver && !prob.slug) {
      const hasBrokenWalkccc = entry.reads.some(r => {
        const u = Array.isArray(r) ? r[1] : r.url;
        return /walkccc\.me/i.test(u);
      });
      if (hasBrokenWalkccc) {
        errors.push(`[${lcId}] Non-LeetCode Striver conceptual problem "${prob.title}" has invalid Walkccc URL`);
      }
    }
  }
}

console.log('----------------------------------------------------');
console.log(`Validation Results:`);
console.log(`  Total problems checked: ${expectedProblems.size}`);
console.log(`  Problems verified in registry: ${verifiedProblemCount} / 940`);
console.log(`  Total curated direct videos: ${totalVideos}`);
console.log(`  Total curated reading links: ${totalReads}`);
console.log(`  Errors / Violations: ${errors.length}`);
console.log('----------------------------------------------------');

if (errors.length > 0) {
  console.error(`FAIL: ${errors.length} validation errors found!`);
  console.error('Sample errors (first 10):');
  errors.slice(0, 10).forEach(e => console.error('  - ' + e));
  process.exit(1);
} else {
  console.log('SUCCESS: All 940 distinct DSA problems 100% verified with valid 4-5 direct videos and 4-5 curated reads!');
  process.exit(0);
}
