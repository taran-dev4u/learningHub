# Taran's Learning Hub

A personal static learning hub generated from the HTML sites in this folder.

## Included sites

- DSA Ultimate Index: 940 problems, 47 sections, 425 resources
- System Design: 322 concepts, 15 sections, 222 resources
- CS Fundamentals: 156 concepts, 7 sections, 43 resources
- Behavioral and Leadership: 145 concepts, 6 sections, 25 resources
- AI Engineering: 2543 study items, 38 sections, 2269 resources
- Cloud & DevOps Engineering: 0 concepts, 0 sections, 17 resources
- Interview Prep: 153 concepts, 11 sections, 44 resources

## Added tutorial sub-sites

- DSA Tutorial: `DSA_Tutorial/index.html` with 747 generated pages and 699 problem tutorials (one page per problem per pattern; duplicates inside a pattern removed).
- System Design Tutorial Hub: `System_Design_Tutorial/index.html` with 15 sections, 62 mapped topics, and 62 bundled markdown lessons.
- AI Engineering: `ai_engineering.html` and `AI_Engineering_Tutorial/index.html` share the complete MIT curriculum snapshot: 542 core lessons, 6 manuals, 51 labs, 79 projects, 67 certification lessons, 309 cheat sheets, 13 paths, 250 glossary terms, and all 9782 tracked source files. Revision: `3f9715c62a3bedcffb68a260f1a65ee2dd9cc10a`.
- Interview Prep: `interview_prep.html` with answer methods, behavioral stories, Generative AI & LLM systems, Autonomous AI Agents, Forward Deployed Engineering (FDE), AI system design case studies, and a word-by-word transcript runner.

## Current UI

- `index.html` and `hub.html` show the page entry cards.
- Every page shares one navigation bar and one theme, rendered by `assets/learning-hub-shared.js`.
- Resource panels start closed by default.
- Progress and bookmarks are stored locally in the browser and refresh across open tabs.
- DSA and System Design cards/pages link to their deeper local tutorial sub-sites.
- The site has a browser-side password gate for casual access control.

## Local preview

Open `index.html` directly, or serve the folder with any static file server.

## GitHub Pages

This repo includes a GitHub Actions workflow at `.github/workflows/pages.yml`.
After pushing to the `main` branch, GitHub Pages deploys the static site.
The default public URL format is:

`https://<github-user-or-org>.github.io/<repo-name>/`
