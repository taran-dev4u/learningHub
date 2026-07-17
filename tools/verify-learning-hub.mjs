// Static verification for the learning hub.
// Usage: node tools/verify-learning-hub.mjs
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const pages = [
  "index.html",
  "hub.html",
  "DSA_Ultimate_Index.html",
  "system_design.html",
  "cs_fundamentals.html",
  "behavioral.html",
  "ai_engineering.html",
  "cloud_aws_azure.html",
  "interview_prep.html",
];

let failures = 0;
function check(name, ok, detail = "") {
  if (ok) {
    console.log(`  ok   ${name}`);
  } else {
    failures += 1;
    console.log(`  FAIL ${name}${detail ? ` — ${detail}` : ""}`);
  }
}

for (const file of pages) {
  const html = fs.readFileSync(path.join(root, file), "utf8");
  const isHub = file === "index.html" || file === "hub.html";
  console.log(`\n${file}`);
  check("no empty href", !html.includes('href=""'));
  check("no 'undefined' text", !/undefined/.test(html));
  check("no NaN", !/>NaN</.test(html));
  check("no default-open resources", !/resources-section open/.test(html));
  if (isHub) {
    const cards = (html.match(/class="page-card"/g) || []).length;
    check("exactly eight page cards", cards === 8, `found ${cards}`);
  } else {
    const navs = (html.match(/<nav class="site-nav"/g) || []).length;
    check("exactly one site nav", navs === 1, `found ${navs}`);
    const current = (html.match(/aria-current="page"/g) || []).length;
    check("exactly one current nav marker", current === 1, `found ${current}`);
    const cids = [...html.matchAll(/data-cid=["']([^"']+)["']/g)].map((m) => m[1]);
    const dupes = cids.filter((c, i) => cids.indexOf(c) !== i);
    check("no duplicate data-cid", dupes.length === 0, [...new Set(dupes)].slice(0, 5).join(", "));
  }
}

console.log("");
if (failures) {
  console.error(`Verification failed: ${failures} check(s).`);
  process.exit(1);
}
console.log("All verification checks passed.");
