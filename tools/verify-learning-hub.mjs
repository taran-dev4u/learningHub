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
  const isHub = file === "index.html";
  if (file === "hub.html") {
    // hub.html is a 442-byte redirect to index.html, not a copy of it.
    check("hub.html is a redirect to index.html", /http-equiv="refresh"|location\.replace/i.test(html) && html.includes("index.html"));
    continue;
  }
  console.log(`\n${file}`);
  check("no empty href", !html.includes('href=""'));
  check("no 'undefined' text", !/undefined/.test(html));
  check("no NaN", !/>NaN</.test(html));
  check("no default-open resources", !/resources-section open/.test(html));
  if (isHub) {
    // one card per generated site; read the expected number from the data the
    // generator wrote rather than hardcoding it (it was stuck at 8 for months)
    const expected = JSON.parse(fs.readFileSync(path.join(root, "learning-hub-data.json"), "utf8")).stats.domains;
    const cards = (html.match(/class="page-card"/g) || []).length;
    check(`one page card per site (${expected})`, cards === expected, `found ${cards}`);
  } else {
    // The static <nav class="site-nav"> was retired in Sep 2026: every page now gets
    // one navbar injected at runtime by assets/learning-hub-shared.js, which also sets
    // aria-current. So assert the wiring is present and no legacy nav came back.
    check("loads the shared script", html.includes('assets/learning-hub-shared.js'));
    check("loads the shared stylesheet", html.includes('assets/learning-hub-shared.css'));
    const legacy = (html.match(/<nav class="(?:site-nav|global-learning-nav)"/g) || []).length;
    check("no legacy static navbar", legacy === 0, `found ${legacy}`);
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
