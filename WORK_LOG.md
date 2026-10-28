# Taran's Learning Hub — Engineering Development & Maintenance Log

> **Autonomous Continuous Development Log**
> **Cadence:** Scheduled every 3 hours (`0 */3 * * *`)
> **Primary Repository:** `E:\Absolute learning\learningHub` (Branch: `main`)
> **Live Site:** [https://taran-dev4u.github.io/learningHub/](https://taran-dev4u.github.io/learningHub/)
> **Companion Hub:** [https://amazon.interview-prep-hub.workers.dev/](https://amazon.interview-prep-hub.workers.dev/)
> **Audit Status:** `tools/audit_site.py` → **0 findings** across 773 scanned pages

---

## 1. System Architecture & Standards

- **Core Principles**:
  - **Zero-Framework, Pure Static Performance**: Served directly via GitHub Pages root.
  - **Shared Runtime Injection Pattern**: Global navbar, 3-theme switcher (`light` / `dark` / `black`), client passcode gate, and study rail injected dynamically via `assets/learning-hub-shared.css` and `assets/learning-hub-shared.js`.
  - **Zero-Audit Baseline**: All changes must pass `python tools/audit_site.py` with **0 findings** and `node tools/verify-learning-hub.mjs` with all checks green.
  - **Strict Idempotency**: All builder scripts (`tools/build_all_in_one_tech_portal.py`, `tools/build-learning-hub.mjs`, `tools/build_dsa_resources.mjs`) use atomic write semantics (`temp-file + rename + retry`) and can be executed repeatedly with zero diff churn.
  - **Synchronized State**: LocalStorage keys (`hub_done_cloud`, `hub_done_dsa`, `hub_done_sd`, etc.) synchronize progress seamlessly across main portals and standalone masterclass pages.

---

## 2. Active Development Inventory

| Surface / Page | Scope & Content | Status | Verification Gate |
|---|---|---|---|
| `index.html` | Universal landing hub, 7 site cards, global catalog search | ✅ Up to date | `build-learning-hub.mjs` |
| `DSA_Ultimate_Index.html` | 47 patterns, 219 subpatterns, 940 problems, expandable Striver A2Z dropdown | ✅ Upgraded to Amazon SDE Hub UX | Playwright + Audit |
| `cloud_aws_azure.html` | **Cloud Platforms Hub**: AWS (36 concepts), Microsoft Azure (19 concepts), GCP (14 concepts) — 14 subsections, 69 concepts, Multi-Cloud Command Deck, sticky domain switcher, focused view isolation | ✅ Redesigned & Active | Playwright + Audit |
| `all_tech.html` | **All-in-One Tech & Software Engineering Portal**: 13 disciplines (Linux, Git, Docker, K8s, Terraform, CI/CD, Kafka, Spark, PostgreSQL, Redis, Java, FastAPI, APIs) — 44 subsections, 170 concepts | ✅ Redesigned & Active | Playwright + Audit |
| `ai_data.html` | **AI & Data Hub**: 4 tracks (AI Engineering, Machine Learning Engineering, Data Science, Data Engineering) — 24 subsections, 96 concepts, Command Deck, sticky pill bar, Domain Isolation Engine | ✅ Redesigned & Active | Playwright + Audit |
| `ai_engineering.html` | **AI Engineering from Scratch Masterclass**: 20 phases, 542 lessons, full MIT curriculum snapshot, direct link integration | ✅ Active with Hub Breadcrumb | Playwright + Audit |
| `tech_aws.html` | Standalone AWS Cloud Architecture Masterclass (7 subsections, 36 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_azure.html` | Standalone Microsoft Azure Cloud Architecture Masterclass (4 subsections, 19 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_gcp.html` | Standalone Google Cloud Platform Architecture Masterclass (3 subsections, 14 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_spark.html` | Standalone Apache Spark Big Data Processing Masterclass (4 subsections, 13 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_linux.html` | Standalone Linux & Terminal Power Engineering Masterclass (3 subsections, 12 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_git.html` | Standalone Git & GitHub Architecture Masterclass (4 subsections, 17 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_docker_k8s.html` | Standalone Docker & Kubernetes Container Orchestration Masterclass (8 subsections, 31 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_cicd.html` | Standalone CI/CD Pipelines & DevOps Automation Masterclass (3 subsections, 12 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_terraform.html` | Standalone Terraform & Infrastructure as Code Masterclass (3 subsections, 12 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_kafka.html` | Standalone Apache Kafka Distributed Streaming Masterclass (4 subsections, 14 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_postgres.html` | Standalone Database Engineering & PostgreSQL Internals Masterclass (4 subsections, 15 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_redis.html` | Standalone In-Memory Caching with Redis Masterclass (3 subsections, 12 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_java.html` | Standalone Java & Spring Boot Microservices Masterclass (4 subsections, 16 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_fastapi.html` | Standalone Python & FastAPI Backend Engineering Masterclass (2 subsections, 8 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_apis.html` | Standalone Production API Design & Architecture Masterclass (2 subsections, 8 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_ml.html` | Standalone Machine Learning Engineering Masterclass (6 subsections, 24 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_data_science.html` | Standalone Data Science & Applied Analytics Masterclass (5 subsections, 20 concepts) | ✅ Deployed | Playwright + Audit |
| `tech_data_eng.html` | Standalone Data Engineering & Lakehouse Architecture Masterclass (6 subsections, 24 concepts) | ✅ Deployed | Playwright + Audit |
| `system_design.html` | 15 topics, 62 subtopics, 322 concepts + video panels & direct timestamps | ✅ Active | Audit + Verify |
| `System_Design_Tutorial/` | 62 deep roadmap lessons with Algomaster theme (100% video coverage) | ✅ Active | `build_sd_resources.py` |
| `AI_Engineering_Tutorial/` | 11 domains, 37 subsections, 177 concepts | ✅ Active | Audit + Verify |
| `interview_prep.html` | 11 sections, 153 items + Amazon companion hub integration | ✅ Fully generated | `build-learning-hub.mjs` |

---

## 3. Scheduled Maintenance & Development Cadence

The autonomous agent is scheduled via recurring cron notification (`0 */3 * * *`, Daemon) to perform the following cycle:
1. **Repository Health Check**: Run `git status`, verify tree cleanliness, test build tools.
2. **Exhaustive Site Audit**: Run `python tools/audit_site.py` across all 773+ pages to catch dead anchors, count mismatches, broken links, orphan chips, and duplicate IDs.
3. **Curriculum Research & Expansion**:
   - Curate missing YouTube direct walkthrough timestamps for concepts lacking video pointers.
   - Expand markdown masterclass content following the FAANG Staff Engineer persona (tables, analogies, formulas, zero shallow summaries).
   - Generate standalone deep-dive pages for remaining top-tier disciplines (e.g. Terraform, Kafka, PostgreSQL internals).
4. **End-to-End Browser Verification**: Execute Playwright headless regression tests for 3-theme rendering, domain switching, progress syncing, and horizontal overflow checks.
5. **Continuous Deployment**: Commit and push verified increments to `origin/main` to trigger GitHub Pages live deployment.

---

## 4. Pending Research & Improvement Backlog

- [x] **Complete System Design 62 Lessons Video Audit**:
  - Verified 100% of 62 roadmap lessons and all 322 concepts in `system_design.html` have verified video links.
- [x] **Expand Standalone Masterclasses (Batch 2)**:
  - Generated and verified:
    - `tech_terraform.html` (Terraform & Infrastructure as Code — 3 subs, 12 concepts)
    - `tech_kafka.html` (Apache Kafka Distributed Streaming — 4 subs, 14 concepts)
    - `tech_postgres.html` (Database Engineering & PostgreSQL Internals — 4 subs, 15 concepts)
- [x] **Expand Standalone Masterclasses (Batch 3)**:
  - Generated and verified:
    - `tech_redis.html` (In-Memory Caching with Redis — 3 subs, 12 concepts)
    - `tech_java.html` (Java & Spring Boot Microservices — 4 subs, 16 concepts)
    - `tech_fastapi.html` (Python & FastAPI Backend Engineering — 2 subs, 8 concepts)
    - `tech_apis.html` (Production API Design & Architecture — 2 subs, 8 concepts)
- [x] **Expand Standalone Masterclasses (Batch 4 - Final Cloud & Big Data Set)**:
  - Generated and verified:
    - `tech_azure.html` (Microsoft Azure Enterprise Cloud Architecture — 4 subs, 19 concepts)
    - `tech_gcp.html` (Google Cloud Platform Architecture — 3 subs, 14 concepts)
    - `tech_spark.html` (Apache Spark Big Data Processing — 4 subs, 13 concepts)
  - **100% of all Cloud Platforms (AWS, Azure, GCP) and All-Tech Disciplines (13 domains) now have dedicated masterclass pages!**
- [ ] **DSA Unique Problem Descriptions**:
  - Replace recycled descriptions across DSA patterns with distinct problem-specific intuition summaries.
- [ ] **Mobile & Performance Polish**:
  - Audit touch targets and sticky bar scroll physics on iOS / Android viewports.

---

## 5. Detailed Session Changelog

### Session: October 28, 2026 (Iteration 2: Scheduled Maintenance & Masterclasses Batch 3)
- **Automated Trigger**: Executed scheduled maintenance check iteration 2.
- **Generated 4 New Standalone Masterclasses (Batch 3)**:
  - Created `tech_redis.html` (3 subsections, 12 concepts, In-Memory Caching with Redis).
  - Created `tech_java.html` (4 subsections, 16 concepts, Java & Spring Boot Microservices).
  - Created `tech_fastapi.html` (2 subsections, 8 concepts, Python & FastAPI Backend Engineering).
  - Created `tech_apis.html` (2 subsections, 8 concepts, Production API Design & Architecture).
  - Total standalone masterclasses expanded from 8 to **12 standalone guides**!
- **Updated Navigation & Cross-Links**:
  - Updated the Domain Deck in `cloud_aws_azure.html` with `Standalone Guide ↗` action links for all 12 masterclasses.
  - Updated the companion footer cards across all 12 masterclasses with deep links to all sister guides.
- **Verification & Green Suite**:
  - `tools/audit_site.py`: **0 findings** across all 781 pages.
  - `tools/verify-learning-hub.mjs`: All checks green.
  - Playwright test: Verified all 12 standalone masterclasses and main portal with zero overflow and zero console errors.

### Session: October 28, 2026 (Iteration 1: Scheduled Maintenance & Masterclasses Batch 2)
- **Automated Trigger**: Executed scheduled maintenance check iteration 1.
- **Audited Video Resources**:
  - Ran deep verification across all tutorial assets: confirmed all 62 lessons in `System_Design_Tutorial/resources.js` and all 322 concepts in `system_design.html` have direct verified videos.
  - Confirmed all 239 concepts in `cloud_aws_azure.html` have direct `watch?v=` links.
- **Generated 3 New Standalone Masterclasses**:
  - Created `tech_terraform.html` (3 subsections, 12 concepts, Terraform & Infrastructure as Code).
  - Created `tech_kafka.html` (4 subsections, 14 concepts, Apache Kafka Distributed Streaming).
  - Created `tech_postgres.html` (4 subsections, 15 concepts, Database Engineering & PostgreSQL Internals).
  - Total standalone masterclasses expanded from 5 to 8!
- **Updated Navigation & Cross-Links**:
  - Updated Domain Deck in `cloud_aws_azure.html` with `Standalone Guide ↗` badges and links for all 8 masterclasses.
  - Updated companion cards on all 8 standalone pages to include links to all sister masterclasses.
  - Enhanced `tools/audit_site.py` with standard `<base href>` resolution.
- **Verification & Green Suite**:
  - `tools/audit_site.py`: **0 findings** across all 777 pages.
  - `tools/verify-learning-hub.mjs`: All checks green.
  - Playwright test: Verified all 8 standalone masterclasses and main portal.

### Session: October 28, 2026 (Phase 1 Refactor & Portal Launch)
- **Refactored `cloud_aws_azure.html` to All-in-One Tech & Engineering Portal**:
  - Renamed and re-branded page identity to **All-in-One Tech & Engineering Portal** covering 16 domains (AWS, Azure, GCP, Linux, Git, Docker, Kubernetes, Terraform, CI/CD, Kafka, Spark, PostgreSQL, Redis, Java, Python, REST & APIs).
  - Designed and deployed **Above-the-Fold Interactive Domain Command Deck** (`#domain-navigator`) featuring 16 responsive discipline cards with badges, concept counts, and focus triggers.
  - Implemented **Sticky Domain Pill Bar** (`#domain-nav-bar`) with horizontal scroll for instant domain switching anywhere on the page.
  - Developed client-side **Domain Isolation Engine** (`switchDomain(slug)`): clicking any domain card or pill isolates that domain into view, hiding the other 15 sections so users never have to scroll through irrelevant topics. Added previous/next domain navigation and "View All 16 Domains" toggle.
  - Added URL hash routing support (`#aws`, `#cicd`, `#git`, `#docker`, `#k8s`, etc.) with automatic search integration.
  - Applied Amazon SDE Prep Hub 3-Theme CSS tokens (`light`, `dark`, `black`).
- **Engineered 5 Standalone Engineering Masterclass Pages**:
  - Generated `tech_aws.html` (7 subsections, 36 concepts, AWS Cloud Architecture).
  - Generated `tech_linux.html` (3 subsections, 12 concepts, Linux & Terminal Power Engineering).
  - Generated `tech_git.html` (4 subsections, 17 concepts, Git & GitHub Architecture).
  - Generated `tech_docker_k8s.html` (8 subsections, 31 concepts, Docker & Kubernetes Orchestration).
  - Generated `tech_cicd.html` (3 subsections, 12 concepts, CI/CD Pipelines & DevOps Automation).
  - Synchronized progress state with `hub_done_cloud` so progress ticks mirror across all pages.
- **Verification & Green Suite**:
  - `python tools/audit_site.py`: **0 findings** across all 773 pages.
  - `node tools/verify-learning-hub.mjs`: All checks passed.
  - Playwright test (`scratch/test_tech_portal_playwright.py`): Verified domain isolation, pill switching, breadcrumbs, checkbox toggles, and zero horizontal overflow (`scrollWidth <= clientWidth`).

### [2026-10-28 07:14 UTC] Built-In Ad-Free Clean Player Mode in Study Panel & YouTube Ad Elimination
- **Root Cause Analysis**:
  - Investigated why Chrome ad blockers permit video ads inside the embedded player on `github.io`.
  - Identified cross-origin iframe sandboxing, Chrome Manifest V3 declarativeNetRequest restrictions, and YouTube's server-stitched video stream insertion.
- **Implemented Built-In Ad-Free Player Engine**:
  - Updated `assets/video-panel.js` and `assets/video-panel.css` with a native `🛡️ Ad-Free: ON / OFF` toggle and engine switcher (`Piped`, `Invidious`, `YouTube`).
  - Defaults to Ad-Free (`Piped`), completely eliminating pre-roll, mid-roll, post-roll, and pop-up ads across all 781 pages.
  - Preserves exact timestamp jumps (`⏱️ Starts at mm:ss`), playback speeds, responsive docking, and user preference in `localStorage`.
- **Verification**:
  - `python tools/audit_site.py`: **0 findings** across all 781 pages.
  - `node tools/verify-learning-hub.mjs`: All checks passed.
  - Playwright visual and functional regression test (`scratch/test_adfree_player_playwright.py`): Verified Piped embed load, YouTube toggle, Invidious switch, and perfect layout in Light and Black themes.
  - Pushed to `origin main` (commit `78d76b6`).

### [2026-10-28 07:39 UTC] Architectural Separation of Cloud Platforms Hub & All-in-One Tech Portal
- **User Architecture Realignment**:
  - Separated Cloud Platforms from Core Software Engineering & Tooling across two dedicated surfaces.
  - Renamed top navbar link from `Cloud Tutorial` (`Cloud Tut`) to `All-Tech` (`all_tech.html`), while preserving `Cloud` (`cloud_aws_azure.html`).
- **Cloud Platforms Hub (`cloud_aws_azure.html`)**:
  - Dedicated strictly to Cloud Providers: AWS (36 concepts), Microsoft Azure (19 concepts), and Google Cloud Platform (14 concepts) — 14 subsections, 69 concepts total.
  - Multi-Cloud Command Deck above the fold with 3 provider cards + cross-link banner to `all_tech.html`.
  - Sticky domain pill bar with `All Cloud (3)`, `AWS`, `Azure`, `GCP`, plus quick link pill to `All-Tech Portal ↗`.
- **All-in-One Tech & Software Engineering Portal (`all_tech.html`)**:
  - Dedicated to core software engineering, infrastructure & backend tooling: Linux (12 concepts), Git & GitHub (17 concepts), Docker (11 concepts), Kubernetes (20 concepts), Terraform IaC (12 concepts), CI/CD (12 concepts), Kafka (14 concepts), Spark (13 concepts), PostgreSQL (15 concepts), Redis (12 concepts), Java & Spring Boot (16 concepts), Python/FastAPI (8 concepts), and API Design (8 concepts) — 44 subsections, 170 concepts total.
  - Core Engineering Command Deck with 13 discipline cards + cross-link banner to `cloud_aws_azure.html`.
  - Sticky domain pill bar with `All Tech (13)`, `Linux`, `Git`, `Docker`, `K8s`, `Terraform`, `CI/CD`, `Kafka`, `Spark`, `PostgreSQL`, `Redis`, `Java`, `FastAPI`, `APIs`, plus quick link pill to `Cloud Platforms ↗`.
  - Domain Isolation Engine allowing 1-click domain filtering and deep URL hash routing (`#linux`, `#docker`, `#k8s`, etc.).
- **Zero Data Loss & Masterclasses**:
  - 100% of 239 concepts preserved with complete curriculum writeups, direct YouTube links with timestamps, and documentation pointers.
  - Updated all 12 standalone masterclasses (`tech_aws.html`, `tech_linux.html`, etc.) with accurate breadcrumb navigation.
- **Verification Suite**:
  - `python tools/audit_site.py`: **0 findings** across all 782 pages.
  - `node tools/verify-learning-hub.mjs`: All 9 pages passed.
  - Playwright visual and functional regression test (`scratch/test_split_pages_playwright.py`): Verified navbar links, domain pills, domain isolation, and crosslink cards across Light and Black themes.
  - Pushed to `origin main` (commit `b7b61f0`).

### [2026-10-28 07:58 UTC] Unified AI & Data Hub (AI · ML · Data Science · Data Engineering) & AI Masterclass Integration
- **User Request & Architecture Alignment**:
  - Transformed the single AI Engineering view into a comprehensive, multi-track **AI & Data Hub** (`ai_data.html`), matching the high-efficiency architecture of the Cloud and All-Tech portals.
  - Updated global top navigation link in `assets/learning-hub-shared.js` from `AI` to `AI & Data` pointing to `ai_data.html`.
- **4 Comprehensive Strategic Tracks (24 Subsections · 96 Concepts)**:
  - **Track 1: AI Engineering (Generative AI, LLMs & Agents)**:
    - 7 subsections, 28 concepts: Foundation Models & Transformers, Prompt Engineering & In-Context Learning, Retrieval-Augmented Generation (RAG) Architecture, Vector Databases & Semantic Storage, Autonomous AI Agents & Multi-Agent Frameworks, Fine-Tuning (PEFT, LoRA, QLoRA, RLHF, DPO), AI Safety, Guardrails & LLM Evaluation.
    - Integrated direct 1-click links to the existing 542-lesson deep masterclass `ai_engineering.html`.
  - **Track 2: Machine Learning Engineering (MLE)**:
    - 6 subsections, 24 concepts: Supervised & Unsupervised Learning Algorithms, Deep Learning Architectures & PyTorch, Feature Engineering & Validation, Model Evaluation & Diagnostics, MLOps: Tracking & Feature Stores, Production Serving & Low-Latency Inference (Triton, vLLM, TensorRT-LLM, ONNX, drift detection).
  - **Track 3: Data Science & Applied Analytics**:
    - 5 subsections, 20 concepts: Exploratory Data Analysis & Feature Insights, Probability & Mathematical Statistics, Inferential Statistics & Hypothesis Testing, A/B Testing & Causal Inference, Time Series Forecasting & Anomaly Detection.
  - **Track 4: Data Engineering & Modern Data Stack**:
    - 6 subsections, 24 concepts: Modern Data Warehousing & Distributed Query Engines (Snowflake, BigQuery, ClickHouse, DuckDB), Distributed Processing with Apache Spark & PySpark, Data Lakehouse Architecture & Open Table Formats (Apache Iceberg, Delta Lake, Parquet), Data Transformation & Dimensional Modeling with dbt (Kimball, SCD Type 1/2/3), Workflow Orchestration & Data Pipelines (Airflow, Dagster, Observability), Real-Time Data Streaming (Kafka, Flink, Event Time & Watermarks).
- **Interactive Command Deck & Domain Isolation**:
  - Interactive above-the-fold Command Deck with 4 track cards featuring dedicated badge chips, focus buttons, and direct masterclass launch links.
  - Sticky domain pill bar (`All Tracks (4)`, `AI`, `Machine`, `Data Science`, `Data Engineering`, plus `Open Full AI Curriculum ↗`).
  - Domain Isolation Engine providing 1-click focus and URL hash synchronisation (`#ai-eng`, `#ml-eng`, `#data-science`, `#data-eng`).
- **Seamless Navigation & Breadcrumbs**:
  - Added sticky backlink breadcrumb `← AI & Data Hub` in `assets/ai-curriculum.js` hero so learners exploring `ai_engineering.html` can immediately return to the central AI & Data Hub.
- **Verification & Green Suite**:
  - `python tools/audit_site.py`: **0 findings** across all 784 pages.
  - `node tools/verify-learning-hub.mjs`: All 10 pages passed.
  - Headless Playwright suite (`scratch/test_ai_data_playwright.py` & `scratch/verify_server_and_screenshots.py`):
    - Zero horizontal overflow (`scrollWidth === clientWidth === 1440px`).
    - Verified full 1289px row width, 942px concept title width, study rail `.hub-actions` mount, star bookmark toggle, and done checkmark toggle.
    - Verified Light and Black themes.

### [2026-10-28 09:05 UTC] Scheduled Maintenance Check & Launch of 3 Standalone AI/Data Masterclasses (Iteration 3)
- **Scheduled Maintenance Execution**:
  - Processed cron task notification `0 */3 * * *` (Iteration 3).
  - Verified repository health: git working tree clean, baseline checks passed.
  - Verified System Design 62 lessons: 100% video coverage confirmed (0 lessons without verified video).
- **Curated & Launched 3 Dedicated Masterclasses**:
  - **Machine Learning Engineering Masterclass (`tech_ml.html`)**:
    - 6 subsections, 24 concepts covering Classical Algorithms, PyTorch, Feature Preprocessing & Leakage, Evaluation & Bias-Variance, MLOps Pipelines & Feature Stores, and Low-Latency Triton/vLLM Serving.
  - **Data Science & Applied Analytics Masterclass (`tech_data_science.html`)**:
    - 5 subsections, 20 concepts covering EDA & Distribution Analysis, Mathematical Probability & Bayes, Parametric & Non-Parametric Hypothesis Testing, A/B Testing & Causal Inference, and Time Series Forecasting.
  - **Data Engineering & Lakehouse Architecture Masterclass (`tech_data_eng.html`)**:
    - 6 subsections, 24 concepts covering Cloud Data Warehouses, Apache Spark & PySpark, Lakehouses (Iceberg/Delta Lake), dbt Modeling, Airflow DAG Orchestration, and Real-Time Kafka/Flink Streaming.
- **Unified Masterclass Navigation & Architecture**:
  - Updated `ai_data.html` Command Deck cards: Tracks 2, 3, and 4 now feature dedicated `Dedicated Masterclass ↗` launch buttons.
  - Added section focus banner buttons (`Open Full Masterclass ↗`) on all tracks in `ai_data.html`.
  - Added top breadcrumbs (`← AI & Data Hub`) on all 3 masterclasses.
  - Added bottom companion grids (`🤖 Companion AI & Data Masterclasses`) cross-linking all 4 AI/Data tracks.
  - Synchronized progress state with `hub_done_ai_data` so progress ticks mirror across all pages.
- **Verification Suite**:
  - `python tools/audit_site.py`: **0 findings** across all 787 pages.
  - `node tools/verify-learning-hub.mjs`: All 13 pages passed.
  - Headless Playwright suite (`scratch/test_ai_masterclasses_playwright.py`):
    - Verified 1440px full-width layout with zero overflow (`scrollWidth === clientWidth`) across all 3 pages.
    - Verified breadcrumbs, sister links, 1289px concept rows, study rail `.hub-actions` mount, and Light/Black themes.
- **Automated Generator**:
  - Created official project generator `tools/build_ai_data_portal.py` for atomic, idempotent builds of `ai_data.html` and the 3 standalone masterclasses.

### [2026-10-28 12:05 UTC] Scheduled Maintenance Check & Launch of Final Cloud & Big Data Masterclasses (Iterations 4 & 5)
- **Scheduled Maintenance Execution**:
  - Processed cron task notifications `0 */3 * * *` (Iterations 4 and 5).
  - Confirmed 0 findings in `tools/audit_site.py` across all pages.
  - Verified clean git state and JS asset integrity.
- **Generated 3 Standalone Masterclasses (Batch 4 - Complete Cloud & Big Data Set)**:
  - **Microsoft Azure Cloud Architecture Masterclass (`tech_azure.html`)**:
    - 4 subsections, 19 concepts covering Entra ID, VM & App Service runtimes, VNet secure topologies, Cosmos DB globally distributed databases, Azure SQL, and AKS microservices.
  - **Google Cloud Platform Architecture Masterclass (`tech_gcp.html`)**:
    - 3 subsections, 14 concepts covering GKE enterprise clusters, Cloud Run scale-to-zero serverless, BigQuery petabyte data warehousing, Cloud Spanner, and global VPC networking.
  - **Apache Spark Big Data Processing Masterclass (`tech_spark.html`)**:
    - 4 subsections, 13 concepts covering RDD primitives, DataFrame APIs, Catalyst optimizer, Tungsten memory management, shuffle stages, and Structured Streaming.
- **100% Masterclass Milestone Achieved**:
  - Every single domain in Cloud Platforms (AWS, Azure, GCP) now has a dedicated masterclass.
  - Every single discipline in the All-in-One Tech Portal (all 13 domains: Linux, Git, Docker/K8s, Terraform, CI/CD, Kafka, Spark, PostgreSQL, Redis, Java, FastAPI, APIs) now has a dedicated masterclass.
  - Every single track in AI & Data (all 4 tracks: AI Engineering, Machine Learning Engineering, Data Science, Data Engineering) now has a dedicated masterclass.
  - Total standalone masterclasses expanded to **18 standalone guides** across the entire hub!
- **Cross-Linking & Navigation**:
  - Updated Command Deck cards in `cloud_aws_azure.html` and `all_tech.html` with `Dedicated Masterclass ↗` buttons and section focus links.
  - Integrated 17-link companion grid (`🚀 Complete Engineering & Cloud Masterclasses`) across all masterclasses.
  - Maintained unified progress synchronization (`window.SITE_SLUG = "cloud"`).
- **Verification Suite**:
  - `python tools/audit_site.py`: **0 findings** across all 790 pages.
  - `node tools/verify-learning-hub.mjs`: All 16 pages passed.
  - Headless Playwright suite (`scratch/test_final_masterclasses_playwright.py`):
    - Zero horizontal overflow (`scrollWidth === clientWidth === 1440px`).
    - Verified breadcrumbs, 1373px concept rows, study rail `.hub-actions` mount, and Light/Black themes.
