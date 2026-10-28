# AI curriculum source import

The main AI page and this tutorial entry use the same complete source snapshot.
`catalog.json` is the study syllabus. `source/index.json` maps every original
repository file to a content-addressed record in `source/packs/*.json.gz`.
`source/inventory.json` records the upstream Git blob hashes. Original files are
stored unchanged; synthetic readable views of JSON manifests are clearly kept
under `@generated/` in the data index.

The reader loads only the packs needed for the selected lesson. Source code and
HTML are displayed as source, never executed. The website's visual-guide text
is included, with links to the original interactive simulations. Planned source
material stays marked planned. The prior concept guide remains in
`concept-guide.html`, including its original browser progress keys.

## Rebuild or refresh

1. Clone the upstream repository outside the website checkout and select the
   revision you intend to import.
2. Fetch its complete GitHub tree inventory into a temporary JSON file using
   `https://api.github.com/repos/rohitg00/ai-engineering-from-scratch/git/trees/REVISION?recursive=1`.
3. Install the import dependencies from `tools/requirements-ai-import.txt`.
4. From the Learning Hub repository root, run:

```text
python tools/import_ai_curriculum.py UPSTREAM_CHECKOUT TREE_INVENTORY_JSON
python tools/build_ai_page.py
node tools/build-learning-hub.mjs
python tools/verify_ai_curriculum.py
python tools/audit_site.py
node tools/verify-learning-hub.mjs
```

The importer refuses missing files or Git blob mismatches. The verifier checks
every source byte, catalogue destination, core lesson, manual section, artifact,
quiz, and stated count. `coverage.json` contains the measured import totals.
Both entry pages use a content-derived release identifier for their scripts,
styles, catalogue and source-pack requests.

MIT attribution and the upstream copyright notice are preserved in
`SOURCE_LICENSE.txt`. The precise revision is recorded in every manifest and
displayed in the page footer.
