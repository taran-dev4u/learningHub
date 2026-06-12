# Taran's Learning Hub - Project Context And Handoff

Last updated: 2026-06-12

Live site: https://taran-dev4u.github.io/learningHub/

Repository: https://github.com/taran-dev4u/learningHub

Workspace path: `E:\Absolute learning\learningHub`

Latest deployed commit at the time of this document: `48eb7ca Add extracted source maps and direct topic links`

## 1. What This Project Is

Taran's Learning Hub is a static personal learning website that combines several interview-preparation and engineering-learning websites/pages into one connected learning hub.

The goal is not to be a generic landing page. It is meant to be Taran's personal one-stop study control center, with all major learning tracks available from a single hub and each page connected by shared navigation, progress tracking, bookmarks, curated resources, topic-specific search links, and extracted source maps.

The site is static HTML/CSS/JavaScript. There is no React/Vite/framework runtime. GitHub Pages deploys the folder directly.

## 2. How The Project Started

The project started as a folder of separate static learning websites/pages. The initial request was to combine all websites in the folder into a learning hub where everything could be found in one place, all pages could be connected, and the result could be deployed to GitHub Pages.

The project history in git is:

- `dcf7f54` on 2026-06-10: built the first unified learning hub.
- `5170d15` on 2026-06-10: added the GitHub Pages static workflow.
- `f3a8dca` on 2026-06-11: redesigned the hub into Taran's personal page-first learning hub.
- `48eb7ca` on 2026-06-11: added extracted source maps and direct topic links from GFG, DesignGurus, Thita, and uploaded source files.

## 3. User Requirements Captured

The user asked for these major requirements:

1. Combine all the websites/pages in the folder into a single personal learning hub.
2. Deploy the result to GitHub Pages and provide the public link.
3. `index.html` / `hub.html` should only show the main page entries, not global roadmap panels, global catalogs, global section maps, or resource-library UI.
4. The hub should show six entry cards only:
   - DSA
   - System Design
   - CS Fundamentals
   - Behavioral
   - AI Engineering
   - Cloud
5. Every source page should have a shared advanced navigation bar so the user can move to any other website/page.
6. The site is for personal use and should support Taran's own learning path, progress, clarity, and resource access.
7. Extract content from each page and identify what can be improved.
8. Research missing topics/subtopics and add or flag them.
9. Normalize topic and subtopic formatting.
10. Fix YouTube and Google search links so they use clean topic-specific queries.
11. For DSA fallback links, use clean LeetCode-style search queries.
12. For concepts, use clean `{topic} {domain context} explained` / `{topic} {domain context} tutorial` fallback queries.
13. Keep all resource dropdown panels closed by default.
14. Make the design polished and easy to control.
15. Create a content audit artifact that is not shown on the hub landing page.
16. Extract content from the user-provided uploaded/downloaded files and add it into the website where required.
17. Extract contents from the GeeksforGeeks System Design tutorial and add missing topics/subtopics into the System Design website.
18. Provide direct website links related to topics, subtopics, and resources.

Important requirement to preserve: the hub landing page should remain page-first and minimal. Do not re-add the global roadmap/catalog/resource-library UI to `index.html` or `hub.html`.

## 4. Source Inputs Used

### Local Source Pages In The Repo

These are the six main generated/source pages:

- `E:\Absolute learning\learningHub\DSA_Ultimate_Index.html`
- `E:\Absolute learning\learningHub\system_design.html`
- `E:\Absolute learning\learningHub\cs_fundamentals.html`
- `E:\Absolute learning\learningHub\behavioral.html`
- `E:\Absolute learning\learningHub\ai_engineering.html`
- `E:\Absolute learning\learningHub\cloud_aws_azure.html`

### User-Provided Downloaded Files Referenced During Extraction

The user mentioned these files from `C:\Users\mamid\Downloads`:

- `Grokking System Design Interview_ Original Course.html`
- `Behavioral Interview Sheet - STAR Method, Patterns & AI Practice _ Thita.ai.html`
- `datascience_thita.ai`
- `Learning Paths - Structured Interview Preparation _ Thita.ai - AI Interview Coaching Platform.html`
- `System Design Interview Prep - Master HLD in 20 Hours _ Thita.ai.html`

Content from these was extracted into the generated source-map panels and audit:

- DesignGurus Grokking System Design: direct lesson and case-study links.
- Thita Behavioral Sheet: 8 behavioral patterns and 32 subpatterns with direct tutoring/practice links.
- Thita Data Science path: 13 data science/ML topics added as an AI Engineering foundations bridge.
- Thita System Design HLD: 8 high-level design path groups.
- Thita LLD path: 8 low-level design path groups.

### External Research / Trusted References

These references are recorded in `content-audit.md`:

- https://roadmap.sh/system-design
- https://roadmap.sh/computer-science
- https://roadmap.sh/ai-engineer
- https://roadmap.sh/aws
- https://cookbook.openai.com/
- https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- https://learn.microsoft.com/en-us/azure/well-architected/
- https://owasp.org/www-project-top-ten/
- https://github.com/donnemartin/system-design-primer
- https://www.geeksforgeeks.org/system-design/system-design-tutorial/
- https://www.designgurus.io/course/grokking-the-system-design-interview
- https://www.thita.ai/behavioral-sheet
- https://www.thita.ai/system-design
- https://thita.ai/dashboard/learning-path/data-science
- https://thita.ai/dashboard/learning-path/lld

## 5. Current File Map

Root files:

- `index.html`: primary live hub landing page. Shows exactly six page cards.
- `hub.html`: duplicate/alternate hub landing page. Also shows exactly six page cards.
- `DSA_Ultimate_Index.html`: DSA page with 609 problems.
- `system_design.html`: System Design page with concept map, extracted source map, direct GFG/DesignGurus/Thita links.
- `cs_fundamentals.html`: CS Fundamentals page.
- `behavioral.html`: Behavioral and Leadership page with Thita behavioral extracted source map.
- `ai_engineering.html`: AI Engineering page with Thita Data Science extracted source map.
- `cloud_aws_azure.html`: Cloud AWS/Azure page.
- `learning-hub-data.json`: generated inventory of pages, sections, items, resources, progress keys, coverage data, roadmap metadata, and additions.
- `content-audit.md`: generated audit and maintenance reference.
- `README.md`: short user-facing repo summary.
- `.nojekyll`: makes GitHub Pages serve the static files without Jekyll processing.
- `PROJECT_CONTEXT.md`: this handoff document.

Tooling and deployment:

- `tools/build-learning-hub.mjs`: main generator and transformation script.
- `tools/gap-content.mjs`: data module with the gap-coverage sections and resource libraries injected into the pages.
- `tools/hub-page.mjs`: hub landing page template (cards, global search, review queue, progress backup/restore).
- `tools/verify-learning-hub.mjs`: static verification checks (`node tools/verify-learning-hub.mjs`).
- `search-index.json`: generated compact index used by the hub's global search and review queue.
- `.gitattributes`: forces LF line endings to stop cross-OS diff noise.
- `.github/workflows/static.yml` and `.github/workflows/pages.yml`: GitHub Actions workflows that deploy the repo to GitHub Pages on pushes to `main` (both exist; they share the `pages` concurrency group so they queue rather than conflict; `pages.yml` is regenerated by the build script).

## 6. Build And Deployment

Build command:

```powershell
node tools/build-learning-hub.mjs
```

Note: after changing injected content in `tools/gap-content.mjs`, run the build twice — the first run injects the new sections, the second re-parses the pages so the hub/audit counts include them.

Syntax check and verification:

```powershell
node --check tools/build-learning-hub.mjs
node tools/verify-learning-hub.mjs
```

Deployment:

1. Commit changes to `main`.
2. Push to `origin/main`.
3. GitHub Actions workflow `.github/workflows/pages.yml` runs automatically.
4. GitHub Pages publishes the static folder.
5. Live URL: https://taran-dev4u.github.io/learningHub/

The workflow uses:

- `actions/checkout@v4`
- `actions/configure-pages@v5`
- `actions/upload-pages-artifact@v3`
- `actions/deploy-pages@v4`

## 7. Current Site Inventory

Generated data timestamp: `2026-06-11T18:33:20.839Z`

Overall totals:

- Domains/pages: 6
- Sections: 73
- Subsections: 318
- Items: 1,422
- Resources: 917

Per page:

| Page | File | Sections | Items | Resources | Progress key | Bookmark key |
|---|---|---:|---:|---:|---|---|
| DSA Ultimate Index | `DSA_Ultimate_Index.html` | 29 | 609 problems | 510 | `dsa_index_solved_v1` | `dsa_index_bookmark_v1` |
| System Design | `system_design.html` | 13 | 255 concepts | 251 | `hub_done_sd` | `hub_bm_sd` |
| CS Fundamentals | `cs_fundamentals.html` | 6 | 128 concepts | 34 | `hub_done_cs` | `hub_bm_cs` |
| Behavioral and Leadership | `behavioral.html` | 5 | 121 concepts | 24 | `hub_done_bh` | `hub_bm_bh` |
| AI Engineering | `ai_engineering.html` | 10 | 150 concepts | 54 | `hub_done_ai` | `hub_bm_ai` |
| Cloud - AWS and Azure | `cloud_aws_azure.html` | 10 | 159 concepts | 44 | `hub_done_cloud` | `hub_bm_cloud` |

## 8. Page Section Outline

### DSA Ultimate Index

- Two Pointer Patterns: 37 items, 7 subsections, 20 resources.
- Array/Matrix Manipulation Patterns: 24 items, 10 subsections, 25 resources.
- Linked List Manipulation Patterns: 22 items, 5 subsections, 20 resources.
- Tree Traversal Patterns (DFS & BFS): 54 items, 6 subsections, 21 resources.
- Sliding Window Patterns: 33 items, 4 subsections, 13 resources.
- Stack Patterns: 32 items, 6 subsections, 20 resources.
- Heap (Priority Queue) Patterns: 30 items, 4 subsections, 15 resources.
- Binary Search Patterns: 29 items, 5 subsections, 15 resources.
- Graph Traversal Patterns (DFS & BFS): 69 items, 11 subsections, 45 resources.
- Greedy Patterns: 25 items, 7 subsections, 20 resources.
- Backtracking Patterns: 27 items, 7 subsections, 22 resources.
- Dynamic Programming (DP) Patterns: 50 items, 12 subsections, 26 resources.
- String Manipulation Patterns: 23 items, 7 subsections, 21 resources.
- Bit Manipulation Patterns: 16 items, 4 subsections, 15 resources.
- Design Patterns: 43 items, 2 subsections, 12 resources.
- Segment Tree & Fenwick Tree Patterns: 12 items, 2 subsections, 12 resources.
- Prefix Sum & Difference Array Patterns: 13 items, 4 subsections, 11 resources.
- Hash Map & Cache Design Patterns: 10 items, 5 subsections, 14 resources.
- Math, Number Theory & Geometry Patterns: 20 items, 5 subsections, 17 resources.
- Trie / Prefix Tree Patterns: 17 items, 5 subsections, 14 resources.
- Intervals & Line Sweep Patterns: 16 items, 4 subsections, 12 resources.
- Tree Dynamic Programming Patterns: 8 items, 4 subsections, 12 resources.
- Advanced Dynamic Programming Patterns: 30 items, 5 subsections, 14 resources.
- Advanced Graph Algorithm Patterns: 27 items, 9 subsections, 26 resources.
- Multi-Source BFS Patterns: 6 items, 1 subsection, 6 resources.
- Iterator & Data-Stream Design Patterns: 13 items, 6 subsections, 17 resources.
- Sorting Algorithms & Selection Patterns: 8 items, 4 subsections, 15 resources.
- Randomized Algorithm Patterns: 6 items, 4 subsections, 9 resources.
- Advanced String Algorithm Patterns: 7 items, 3 subsections, 13 resources.

### System Design

- Foundations: 27 items, 5 subsections, 32 resources.
- Networking & Communication: 31 items, 5 subsections, 35 resources.
- Databases: 38 items, 6 subsections, 33 resources.
- Caching: 24 items, 5 subsections, 23 resources.
- Messaging & Streaming: 19 items, 4 subsections, 23 resources.
- Reliability & Resilience Patterns: 17 items, 4 subsections, 18 resources.
- Architecture Patterns: 17 items, 3 subsections, 18 resources.
- Distributed Systems Deep Dive: 13 items, 3 subsections, 16 resources.
- Storage Systems: 5 items, 1 subsection, 6 resources.
- Observability & Monitoring: 10 items, 2 subsections, 11 resources.
- Security: 12 items, 2 subsections, 8 resources.
- Classic System Designs: 27 items, 3 subsections, 24 resources.
- Interview Approach: 15 items, 3 subsections, 14 resources.

### CS Fundamentals

- Operating Systems: 28 items, 5 subsections, 4 resources.
- Networking: 23 items, 5 subsections, 4 resources.
- Databases: 22 items, 5 subsections, 4 resources.
- Concurrency & Parallelism: 22 items, 4 subsections, 4 resources.
- Security: 19 items, 3 subsections, 4 resources.
- Computer Architecture: 14 items, 3 subsections, 3 resources.

### Behavioral and Leadership

- STAR Framework & Storytelling: 12 items, 3 subsections, 3 resources.
- Amazon's 16 Leadership Principles: 48 items, 16 subsections, 4 resources.
- Question Categories (any company): 26 items, 8 subsections, 2 resources.
- Story Bank - 12 stories you need: 18 items, 2 subsections, 2 resources.
- Interview Strategy & Mock Practice: 17 items, 4 subsections, 3 resources.

### AI Engineering

- LLM Fundamentals: 15 items, 3 subsections, 4 resources.
- Prompt Engineering: 15 items, 3 subsections, 4 resources.
- RAG (Retrieval-Augmented Generation): 19 items, 3 subsections, 4 resources.
- Agents & Tool Use: 16 items, 3 subsections, 4 resources.
- Evals & Testing: 10 items, 2 subsections, 4 resources.
- Fine-tuning & Training: 10 items, 2 subsections, 4 resources.
- Production LLM Systems: 15 items, 4 subsections, 3 resources.
- Classical Machine Learning: 23 items, 4 subsections, 4 resources.
- Deep Learning: 11 items, 2 subsections, 4 resources.
- MLOps: 16 items, 4 subsections, 4 resources.

### Cloud - AWS and Azure

- Cloud Foundations: 39 items, 4 subsections, 4 resources.
- Identity & Access (IAM / Entra ID): 8 items, 2 subsections, 3 resources.
- Compute: 14 items, 3 subsections, 4 resources.
- Storage: 11 items, 2 subsections, 2 resources.
- Networking: 15 items, 3 subsections, 3 resources.
- Databases: 10 items, 2 subsections, 2 resources.
- Messaging & Events: 9 items, 2 subsections, 2 resources.
- Monitoring & Observability: 7 items, 2 subsections, 2 resources.
- Infrastructure as Code: 6 items, 1 subsection, 4 resources.
- AWS Interview Q&A (250 Questions): 40 items, 5 subsections, 4 resources.

## 9. Features Implemented

### Hub Landing Page

Files:

- `index.html`
- `hub.html`
- generated by `simpleHubHtml(data)` in `tools/build-learning-hub.mjs`

Current behavior:

- Shows only six entry cards.
- Each card has:
  - page title
  - personal purpose
  - section count
  - item count
  - resource count
  - local progress bar
  - Open button
- Uses `localStorage` progress keys from each source page.
- Has a theme toggle.
- Does not show old global roadmap/catalog/resource library UI.

### Cross-Site Navigation

Files:

- generated by `siteNavHtml(source)` in `tools/build-learning-hub.mjs`
- styled by `siteNavStyle()`
- behavior from `siteNavScript()`

Current behavior:

- Every source page has a sticky navigation bar.
- Links:
  - Hub
  - DSA
  - Systems
  - CS
  - Behavioral
  - AI
  - Cloud
- Current page is highlighted with `aria-current="page"`.
- Navigation is responsive with a mobile menu.
- Includes a theme toggle.
- Includes progress text where useful.

### Progress And Bookmarks

Progress and bookmarks are stored in browser `localStorage`.

Each source page has its own keys:

- DSA done: `dsa_index_solved_v1`
- DSA bookmark: `dsa_index_bookmark_v1`
- System Design done: `hub_done_sd`
- System Design bookmark: `hub_bm_sd`
- CS done: `hub_done_cs`
- CS bookmark: `hub_bm_cs`
- Behavioral done: `hub_done_bh`
- Behavioral bookmark: `hub_bm_bh`
- AI done: `hub_done_ai`
- AI bookmark: `hub_bm_ai`
- Cloud done: `hub_done_cloud`
- Cloud bookmark: `hub_bm_cloud`

Do not rename these keys unless you intentionally want to reset user progress.

### Resource Dropdowns

Requirement: all resource dropdowns should start closed.

Implementation:

- `transformSourcePage(source)` removes `resources-section open` classes.
- Click behavior is preserved because resource headers still toggle `.open`.

Verification from last deployment:

- Each source page had `openResources=0`.

### Link Cleanup

Relevant functions:

- `rewriteProblemSearchLinks(html)` for DSA.
- `rewriteConceptSearchLinks(html, source)` for concept pages.

Behavior:

- Removes emoji/bad punctuation/Q&A prefixes from fallback searches.
- DSA fallback query format uses LeetCode-style problem context.
- Concept fallback query format:
  - YouTube: `{topic} {domain context} explained`
  - Google: `{topic} {domain context} tutorial`

### Cloud Q&A Formatting

Relevant function:

- `formatCloudQa(html)`

Behavior:

- Cleans long Cloud interview entries into structured Q/A display.
- Adds `.qa-name`, `.qa-question`, and `.qa-answer` style hooks.

### Coverage Panels

Each page gets a coverage panel before its table of contents.

Relevant function:

- `coveragePanelHtml(source)`

Coverage sources:

- DSA: NeetCode / Striver-style pattern coverage.
- System Design: roadmap.sh System Design + System Design Primer + GFG tutorial.
- CS: roadmap.sh Computer Science.
- Behavioral: STAR and leadership-story coverage.
- AI: roadmap.sh AI Engineer + OpenAI Cookbook + production LLM practice.
- Cloud: roadmap.sh AWS + AWS/Azure Well-Architected guidance.

### Source Extract Panels

Relevant functions:

- `sourceExtractHtml(source)`
- `systemDesignSourceExtractHtml()`
- `behavioralSourceExtractHtml()`
- `aiSourceExtractHtml()`

Current panels:

- `system_design.html`: GFG, DesignGurus, Thita HLD, Thita LLD source map.
- `behavioral.html`: Thita Behavioral Sheet source map.
- `ai_engineering.html`: Thita Data Science Path source map.

No source extract panel is currently added to DSA, CS, or Cloud.

## 10. System Design Extraction Details

The user specifically asked to extract:

https://www.geeksforgeeks.org/system-design/system-design-tutorial/

What was added:

- GFG topic map grouped into 14 categories.
- GFG priority gaps.
- 115 direct GFG topic links.
- 55 direct DesignGurus lesson/case-study links.
- Thita HLD outline.
- Thita LLD outline.

Live location:

- `system_design.html`
- section heading: `Extracted Source Map: GFG, DesignGurus and Thita`

The System Design source-map panel currently contains:

- 179 total source links.
- 121 GFG links, including top resources plus direct topic links.
- 56 DesignGurus links, including course home plus direct lesson/case-study links.
- 2 Thita links.

GFG priority gaps added/flagged:

- HLD vs LLD distinction and when to switch levels.
- Functional vs non-functional requirement checklist.
- System life cycle / SDLC and requirements gathering.
- HLD diagrams, activity diagrams, and UML diagram practice.
- LLD foundations: OOP, OOAD, interfaces, SOLID, DRY, KISS, YAGNI.
- Testing and delivery: unit, integration, load, stress, CI/CD.
- Cost estimation and cost-vs-performance trade-offs.
- Backup and disaster recovery planning.
- Ticket booking / BookMyShow and Messenger-style design prompts.

GFG outline groups:

- Basics and Requirements
- High-Level Design
- Scalability and Capacity
- Databases and Storage
- Reliability Qualities
- Traffic and Performance
- Communication and Integration
- Event-Driven Systems
- Testing and Delivery
- Security and Recovery
- Distributed Systems
- Cost and Optimization
- Low-Level Design
- Interview Practice

## 11. Behavioral Extraction Details

Source:

- Thita Behavioral Sheet uploaded/downloaded file.
- Public reference: https://www.thita.ai/behavioral-sheet

Live location:

- `behavioral.html`
- section heading: `Extracted Source Map: Thita Behavioral Sheet`

Extracted patterns:

- STAR Method
- Conflict Resolution
- Team Leadership
- Project Management
- Communication
- Problem Solving
- Adaptability
- Cultural Fit

Each pattern has 4 subpatterns, for 32 subpatterns total.

The page includes 33 Thita links:

- 1 Behavioral Sheet link.
- 32 direct tutoring/practice links generated with:
  - `category=Behavioral`
  - `pattern=<pattern>`
  - `subpattern=<subpattern>`
  - `teaching_mode=feynman`
  - `persona=samuel-brooks`

## 12. AI / Data Science Extraction Details

Source:

- Thita Data Science learning path uploaded/downloaded file.
- Public/app reference: https://thita.ai/dashboard/learning-path/data-science

Live location:

- `ai_engineering.html`
- section heading: `Extracted Source Map: Thita Data Science Path`

Extracted topics:

- Business Analytics and Metrics
- Data Manipulation and Preprocessing
- Deep Learning Fundamentals
- Exploratory Data Analysis
- Feature Selection and Dimensionality Reduction
- Full Pattern Problem Practice
- Model Selection and Validation
- Natural Language Processing
- Statistics and Probability Fundamentals
- Supervised Learning - Classification
- Supervised Learning - Regression
- Time Series Analysis
- Unsupervised Learning

Direct resources added:

- Thita Data Science Learning Path
- Kaggle Learn Python
- Kaggle Learn Pandas
- Kaggle Learn Data Visualization
- Kaggle Intro to Machine Learning
- Google Machine Learning Crash Course
- scikit-learn User Guide
- TensorFlow Tutorials
- Hugging Face NLP Course

## 13. Content Audit

File:

- `content-audit.md`

Purpose:

- Maintains an inventory of all pages.
- Records research references.
- Lists global actions applied.
- Lists per-page sections/subsections/items/resources.
- Flags duplicate/weak subsection names.
- Records missing/priority candidates.
- Records extracted source maps and direct links.

Important: this file is a maintenance artifact. It is not shown on the hub landing page.

## 14. Generator Architecture

Main file:

- `tools/build-learning-hub.mjs`

Important data structures:

- `sourceDefs`: six source page definitions.
- `roadmap`: older global roadmap data. It is still in the generator/data file but not shown on the simplified hub landing page.
- `additions`: extra learning lanes. Also retained in data but not shown on the simplified hub landing page.
- `coverageBySource`: per-page coverage notes/resources.
- `gfgSystemDesignOutline`: GFG extracted topic map.
- `gfgSystemDesignPriorityGaps`: System Design improvement candidates.
- `gfgSystemDesignResources`: key canonical GFG links.
- `gfgSystemDesignLinks`: 115 direct GFG topic links.
- `designGurusSystemDesignLinks`: 55 direct DesignGurus links.
- `thitaHldOutline`: Thita HLD extracted outline.
- `thitaLldOutline`: Thita LLD extracted outline.
- `thitaBehavioralPatterns`: Thita Behavioral extracted pattern/subpattern list.
- `thitaDataScienceOutline`: Thita Data Science extracted topic list.
- `dataScienceDirectResources`: direct AI/ML/data science resources.

Important functions:

- `simpleHubHtml(data)`: generates `index.html` and `hub.html`.
- `siteNavStyle()`: injects shared CSS for nav, coverage panels, source panels, and Q/A formatting.
- `siteNavHtml(source)`: builds the shared nav for each source page.
- `siteNavScript()`: theme/progress/nav behavior for source pages.
- `coveragePanelHtml(source)`: builds per-page coverage panels.
- `systemDesignSourceExtractHtml()`: builds System Design source extract.
- `behavioralSourceExtractHtml()`: builds Behavioral source extract.
- `aiSourceExtractHtml()`: builds AI/Data Science source extract.
- `sourceExtractHtml(source)`: routes source pages to the correct extract panel.
- `rewriteProblemSearchLinks(html)`: fixes DSA fallback links.
- `rewriteConceptSearchLinks(html, source)`: fixes concept fallback links.
- `formatCloudQa(html)`: formats Cloud Q/A entries.
- `removeGeneratedPageChrome(html)`: prevents duplicate generated nav/coverage/source panels on repeated builds.
- `transformSourcePage(source)`: transforms each source HTML page.
- `buildContentAudit(data)`: writes `content-audit.md`.

## 15. Development Rules For Future Agents

When changing the site:

1. Prefer editing `tools/build-learning-hub.mjs`.
2. Run `node tools/build-learning-hub.mjs` to regenerate pages.
3. Avoid hand-editing generated sections in the HTML pages unless absolutely necessary, because the generator can overwrite them.
4. Keep `index.html` and `hub.html` as six-card-only hub pages.
5. Do not re-add the old global roadmap/catalog/resource-library UI to the hub landing page.
6. Keep resource dropdowns closed by default.
7. Preserve localStorage keys unless intentionally migrating progress.
8. Keep direct source links in the source extract panels.
9. Update `content-audit.md` through the generator when adding new research or extracted sources.
10. Keep deployment static and GitHub Pages compatible.

## 16. Verification History

The last deployment was verified with:

```powershell
node --check tools/build-learning-hub.mjs
node tools/build-learning-hub.mjs
git diff --check
```

Static checks verified:

- No empty `href=""`.
- No `undefined`.
- No `NaN`.
- No default-open `resources-section open`.
- Each source page has exactly one shared nav.
- Each source page has exactly one current nav marker.
- Source extract panels exist on System Design, Behavioral, and AI only.
- `index.html` and `hub.html` each have exactly six page cards and six Open links.
- The old global roadmap/catalog/resource-library UI is not present on the hub landing page.

Live GitHub Pages checks verified:

- `https://taran-dev4u.github.io/learningHub/` returned status 200 and contained six page cards.
- `https://taran-dev4u.github.io/learningHub/system_design.html` returned status 200 and contained `Direct GFG Topic Links`.
- `https://taran-dev4u.github.io/learningHub/behavioral.html` returned status 200 and contained `Extracted Source Map: Thita Behavioral Sheet`.
- `https://taran-dev4u.github.io/learningHub/ai_engineering.html` returned status 200 and contained `Extracted Source Map: Thita Data Science Path`.

Note: local in-app browser testing was attempted during the last update, but the browser plugin blocked local loopback/file navigation in that environment. Static checks and live GitHub Pages checks were used instead.

## 16b. June 2026 Improvement Pass

Changes applied on 2026-06-12:

1. Gap-coverage sections (audit "missing/priority candidates") added to five pages via `tools/gap-content.mjs`, fully wired into progress/bookmarks/filters: System Design section 14 "Interview Engineering Toolkit" (41 concepts), CS section 7 "Languages, Runtimes & Engineering Practice" (28), Behavioral section 6 "Competency Deep Dives" (24), AI section 11 "Production AI Engineering" (30), Cloud section 11 "Architecture & Governance" (35). New concepts use cids `N.x.y` continuing each page's numbering; injected blocks are wrapped in `gen-gap`/`gen-toc` markers and regenerated each build.
2. Resource libraries added as panels on the thin pages (CS, Behavioral, Cloud) plus a DSA "Practice System" panel with weekly drills.
3. Hub upgrades (`tools/hub-page.mjs`): overall stats strip, global search across all items (uses `search-index.json`), a bookmark review queue, and progress Backup/Restore buttons (localStorage export/import as JSON).
4. Repo hygiene: `.gitattributes` (LF), `tools/verify-learning-hub.mjs` static checks.
5. New totals: 78 sections, 1,580 items, 981 resources.

## 17. Current Known Limitations / Future Work

- The source extract panels are intentionally large, especially System Design. They prioritize direct access and context over compactness.
- `roadmap` and `additions` still exist in `learning-hub-data.json` and the generator, but the simplified hub landing page does not render them.
- Some source links, especially Thita dashboard/tutoring links, may require user login when opened.
- The project currently has no automated browser-based test suite.
- There is no package.json because the generator uses Node built-ins only.
- If more uploaded HTML files are added later, extract their outline into generator constants and include direct links in a source panel or audit section.

## 18. Quick Start For A Future Model

If a future model needs to work on this project, start with these files in this order:

1. `PROJECT_CONTEXT.md`
2. `README.md`
3. `content-audit.md`
4. `tools/build-learning-hub.mjs`
5. `learning-hub-data.json`
6. The specific HTML page involved in the requested change.

Basic workflow:

```powershell
cd "E:\Absolute learning\learningHub"
git -c safe.directory='E:/Absolute learning/learningHub' status --short --branch
node --check tools/build-learning-hub.mjs
node tools/build-learning-hub.mjs
git -c safe.directory='E:/Absolute learning/learningHub' diff --check
```

Deployment workflow:

```powershell
git -c safe.directory='E:/Absolute learning/learningHub' add --all
git -c safe.directory='E:/Absolute learning/learningHub' commit -m "<message>"
git -c safe.directory='E:/Absolute learning/learningHub' push origin main
```

Public URL after deploy:

https://taran-dev4u.github.io/learningHub/
