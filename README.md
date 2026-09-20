# Taran's Learning Hub

A personal static learning hub generated from the HTML sites in this folder.

## Included sites

- DSA Ultimate Index: 940 problems, 47 sections, 427 resources
- System Design: 322 concepts, 15 sections, 216 resources
- CS Fundamentals: 156 concepts, 7 sections, 43 resources
- Behavioral and Leadership: 145 concepts, 6 sections, 25 resources
- AI Engineering: 177 concepts, 11 sections, 56 resources
- Cloud - AWS and Azure: 194 concepts, 11 sections, 55 resources
- Interview Prep: 92 concepts, 6 sections, 16 resources

## Added tutorial sub-sites

- DSA Tutorial: `DSA_Tutorial/index.html` with 747 generated pages and 699 problem tutorials (one page per problem per pattern; duplicates inside a pattern removed).
- System Design Tutorial Hub: `System_Design_Tutorial/index.html` with 15 sections, 62 mapped topics, and 62 bundled markdown lessons.
- Interview Prep: `interview_prep.html` with answer methods, HR questions, behavioral story themes, technical communication practice, and a word-by-word transcript runner.

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
