#!/usr/bin/env node
/**
 * Removes reads that the link check proved dead from assets/dsa-resources.js,
 * and lists the dead links in the HTML pages for a human to look at.
 *
 *   node tools/prune_dead_reads.mjs [--apply]
 *
 * Only `dead` (404/410, or a YouTube id that is gone) is ever removed.
 * `blocked` means a CI runner was refused by Cloudflare and proves nothing, so
 * those are left alone — otherwise every run would delete half of GeeksforGeeks.
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const CACHE = path.join(ROOT, 'tools', 'linkcheck', 'cache.json');
const REG = path.join(ROOT, 'assets', 'dsa-resources.js');
const APPLY = process.argv.includes('--apply');

if (!fs.existsSync(CACHE)) { console.error('no link-check cache yet — run tools/linkcheck/check.mjs first'); process.exit(0); }
const cache = JSON.parse(fs.readFileSync(CACHE, 'utf8'));
const isDead = (url) => { const e = cache[url]; return !!(e && e.status === 'dead'); };

const sandbox = { window: {} };
new Function('window', fs.readFileSync(REG, 'utf8'))(sandbox.window);
const reg = sandbox.window.dsaResources || {};

let removed = 0, rowsTouched = 0, emptied = 0;
const byHost = {};
for (const p of Object.values(reg)) {
  const before = (p.reads || []).length;
  p.reads = (p.reads || []).filter((r) => {
    if (!isDead(r[1])) return true;
    const h = (() => { try { return new URL(r[1]).hostname; } catch { return '?'; } })();
    byHost[h] = (byHost[h] || 0) + 1;
    removed++;
    return false;
  });
  if (p.reads.length !== before) rowsTouched++;
  if (!p.reads.length) emptied++;
}

console.log(`dead reads: ${removed} across ${rowsTouched} rows`);
for (const [h, n] of Object.entries(byHost).sort((a, b) => b[1] - a[1])) console.log(`   ${String(n).padStart(5)} ${h}`);
if (emptied) console.log(`warning: ${emptied} rows would be left with no reads at all`);

if (!APPLY) { console.log('\n(dry run — pass --apply to write)'); process.exit(0); }
if (!removed) { console.log('nothing to do'); process.exit(0); }

const src = fs.readFileSync(REG, 'utf8');
const header = src.slice(0, src.indexOf('window.dsaResources'));
fs.writeFileSync(REG, header + 'window.dsaResources = ' + JSON.stringify(reg) + ';\n');
console.log('assets/dsa-resources.js rewritten');
