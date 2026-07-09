# Taran's Learning Hub

A personal static learning hub generated from the HTML sites in this folder.

## Included sites

- DSA Ultimate Index: 609 problems, 29 sections, 518 resources
- System Design: 322 concepts, 15 sections, 263 resources
- CS Fundamentals: 156 concepts, 7 sections, 53 resources
- Behavioral and Leadership: 145 concepts, 6 sections, 37 resources
- AI Engineering: 180 concepts, 11 sections, 60 resources
- Cloud - AWS and Azure: 194 concepts, 11 sections, 58 resources

## Added tutorial sub-sites

- DSA Tutorial: `DSA_Tutorial/index.html` with 755 generated pages and 707 problem tutorials.
- System Design Tutorial Hub: `System_Design_Tutorial/index.html` with 15 sections, 62 mapped topics, and 102 bundled markdown lessons.

## Current UI

- `index.html` and `hub.html` show only the six page entry cards.
- Each source page has shared cross-site navigation.
- Resource panels start closed by default.
- Progress and bookmarks are stored locally in the browser.
- DSA and System Design pages link to their deeper local tutorial sub-sites.

## Local preview

Open `index.html` directly, or serve the folder with any static file server.

## GitHub Pages

This repo includes a GitHub Actions workflow at `.github/workflows/pages.yml`.
After pushing to the `main` branch, GitHub Pages deploys the static site.
The default public URL format is:

`https://<github-user-or-org>.github.io/<repo-name>/`
