# Eight-source AI engineering companion

The core 542-lesson curriculum remains the pinned Rohit Ghumare import in
`catalog.json` and `source/`. The companion adds eight requested public
repositories without pretending they are part of that original source.

- `companion-guides.json`: 20 original Learning Hub study guides. Each has an
  explanation, a decision table, a worked case and an exercise. Phase 17 also
  has an 18-part inference engineering deep dive corresponding to the topics
  in Amit Shekhar's Module 12.
- `decision-playbook.json`: seven original, detailed decision guides inspired
  by the source playbook's topic map. Each includes explanations, a comparison
  table, subtopics, a worked case and a practice exercise. The AI page exposes
  this as a separate "Decision playbook" tab.
- `engineer-path.json`: the original focused engineering path. Core stages and
  optional specializations cover all 20 phases, with direct lesson links,
  build assignments, decision tables, release criteria, and official references.
  Progress on its focus lessons uses the existing lesson completion storage.
- `aishwaryanr/awesome-generative-ai-guide`: the main GenAI resource. Its
  pinned MIT-licensed snapshot is indexed in full, with
  readable text opened inline and binary media linked to the pinned original.
  The dedicated tab organizes journeys, nine topic pages, interview roles,
  courses, projects, research updates, and video notes. Its headings also
  appear in the phase topic index.
- `companion-data.json`: the complete file inventory, indexed Markdown and
  notebook headings, and interview prompts at the pinned revisions.
  Counts are computed by `tools/build_ai_companion.py`, not typed into the UI.
- `companion-content/`: seven compressed packs holding all nonempty UTF-8 source
  files from repositories with MIT or Apache-2.0 licenses. Markdown lessons,
  notebooks and code open in the existing right-side reader. Notebook
  markdown and code cells are displayed in order; saved image outputs and
  interactive execution remain available in the pinned original file.
- `COMPANION_ATTRIBUTION.md` and `companion-licenses/`: source revisions and
  licenses. The playbook repo declares no license; only its short heading
  titles and links are indexed. Learning Hub tables are independently written.

The companion appears on `ai_engineering.html`, on every phase landing page,
and in the AI curriculum sidebar. Its topic, question and file browsers are
searchable and filterable. Licensed text files open inline, and every file
also has a link to its pinned upstream original. The file browser includes
code and media, while the topic browser lists teaching headings; these are
separate counts. The question browser provides an original answer framework
by subject, not fabricated answers to every question.

## Rebuild

The ignored `scratch/` snapshots are required for the builder. Download the
currently pinned snapshots and rebuild with:

```text
python tools/fetch_ai_companion.py
python tools/build_ai_companion.py
python tools/build_ai_page.py
python tools/audit_site.py
node tools/verify-learning-hub.mjs
```

To review newer upstream revisions, run the fetcher with `--latest`, inspect
the changed topics and licenses, then rebuild. The builder rejects truncated
GitHub trees, mismatched paths and any file whose Git blob hash differs from
the pinned tree inventory.

## Coverage boundaries

The eight repositories overlap heavily with the core syllabus. This import
indexes their entire tracked file trees and readable headings while the study
guides explain the major decisions in original prose. An indexed source
heading is a pointer to its full upstream lesson, not a claim that its entire
body was rewritten locally. `AIMLInterviews` currently contains many Chinese
and Persian source files; translated copies are kept in the file inventory,
and the primary topic index favors the root source tree. The
`youtube-tutorials` catalog has empty `video_url` values at the pinned
revision, so the site links its verified lesson and code files rather than
inventing direct YouTube IDs.
