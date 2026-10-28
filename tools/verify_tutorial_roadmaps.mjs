import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = path.resolve(import.meta.dirname, '..');
const tutorials = [
  ['System_Design_Tutorial', ['contentBundle.js', 'topics.js', 'anchor-targets.js']],
  ['LLD_Tutorial', ['contentBundle.js', 'topics.js', 'roadmap-additions.js']],
];
const slug = (value) => String(value).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
const errors = [];

for (const [directory, scripts] of tutorials) {
  const context = { window: {} };
  vm.createContext(context);
  for (const script of scripts) {
    vm.runInContext(fs.readFileSync(path.join(root, directory, script), 'utf8'), context, {
      filename: path.join(directory, script),
    });
  }
  const topics = context.window.topicsData;
  const bundle = context.window.contentBundle;
  const targets = context.window.tutorialAnchorTargets || {};
  const used = new Set();
  let rows = 0;
  for (const section of topics) {
    if (!section.subsections?.length) errors.push(`${directory}: empty section ${section.section}`);
    for (const sub of section.subsections) {
      const md = bundle[sub.file];
      if (!md) { errors.push(`${directory}: missing lesson ${sub.file}`); continue; }
      const headings = [...md.matchAll(/^#{1,3} (.+)$/gm)].map((match) => slug(match[1]));
      if (!sub.concepts?.length) errors.push(`${directory}: empty lesson ${sub.file}`);
      for (const concept of sub.concepts) {
        rows++;
        const key = `${sub.id}/${concept.anchor}`;
        if (used.has(key)) errors.push(`${directory}: duplicate route ${key}`);
        used.add(key);
        const exact = headings.includes(concept.anchor);
        const clean = concept.anchor.replace(/-/g, '');
        const partial = headings.some((heading) => {
          const h = heading.replace(/-/g, '');
          return h.length > 3 && (clean.includes(h) || h.includes(clean));
        });
        const mapped = targets[`${sub.file}#${concept.anchor}`];
        if (mapped && !headings.includes(mapped)) errors.push(`${directory}: invalid heading target ${sub.file}#${concept.anchor} -> ${mapped}`);
        const short = concept.title.split(/\s+[—–]\s+|:\s+/)[0];
        const phrase = md.toLowerCase().includes(concept.title.toLowerCase()) || md.toLowerCase().includes(short.toLowerCase());
        if (!exact && !partial && !mapped && !phrase) errors.push(`${directory}: no destination for ${sub.file}#${concept.anchor}`);
      }
    }
  }
  console.log(`${directory}: ${topics.length} sections, ${rows} roadmap rows checked`);
}

const aiRoot = path.join(root, 'AI_Engineering_Tutorial');
if (fs.existsSync(path.join(aiRoot, 'catalog.json'))) {
  const catalog = JSON.parse(fs.readFileSync(path.join(aiRoot, 'catalog.json'), 'utf8'));
  const source = JSON.parse(fs.readFileSync(path.join(aiRoot, 'source/index.json'), 'utf8'));
  const ids = new Set(catalog.entries.map((entry) => entry.id));
  for (const entry of catalog.entries) {
    if (!source.files[entry.contentPath]) errors.push(`AI: missing source ${entry.contentPath}`);
  }
  for (const group of catalog.groups) {
    if (!group.entries.length || group.entries.some((id) => !ids.has(id))) errors.push(`AI: invalid group ${group.id}`);
  }
  console.log(`AI_Engineering_Tutorial: ${catalog.groups.length} groups, ${catalog.entries.length} complete source destinations checked`);
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else console.log('All tutorial roadmap destinations resolve.');
