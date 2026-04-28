---
name: configure-hugo
description: >
  Install and configure llm-wiki-hugo-cms in a wiki repository so it
  renders as a static Hugo site. Use when the user says "set up Hugo",
  "add Hugo to this wiki", "make this wiki publishable", or "configure
  Hugo rendering". Requires Hugo extended ≥ 0.147.0.
type: skill
status: active
last_updated: "2026-04-28"
tags: [hugo, publishing, configuration]
owner: jguibert@gmail.com
metadata:
  version: "0.2.0"
---

# configure-hugo

Install `llm-wiki-hugo-cms` into an existing wiki repository and configure
it to render the wiki as a static Hugo site.

## Prerequisites

- Hugo extended ≥ 0.147.0 installed on the user's machine
- An existing wiki managed by llm-wiki (must have `wiki.toml` and `wiki/`)

## Step 1 — Read the wiki identity and repo path

```
wiki_spaces_list(name: "<name>")
→ { name: "research", path: "/home/user/wikis/research", ... }
```

Collect the wiki `name` (needed for `hugo.toml` title) and `path` (the repo
root — all subsequent file operations use `<path>/site/...`).

## Step 2 — Check for existing scaffold

The scaffold lives at `<path>/site/hugo.toml`. Check whether that file
exists directly on the filesystem. If it does, skip to Step 4.

## Step 3 — Install the scaffold

Tell the user to run:

```bash
cd <wiki-repo-path>
git clone https://github.com/geronimo-iia/llm-wiki-hugo-cms _hugo_cms
cp -r _hugo_cms/site .
cp -r _hugo_cms/templates/.github .
rm -rf _hugo_cms
```

Then confirm the files are present before continuing.

## Step 4 — Configure hugo.toml

Read `<repo-path>/site/hugo.toml` directly from disk (repo path from
`wiki_spaces_list`). Update two fields:

```toml
baseURL = "https://<github-username>.github.io/<repo-name>/"
title   = "<wiki name from wiki.toml>"
```

Write the updated file directly to disk. Everything else — `contentDir`,
module mounts, excludeFiles, frontmatter mapping, taxonomies — is
pre-configured and must not be changed.

## Step 5 — Commit the installation

Ask the user to confirm, then commit all new files directly with git:

```bash
cd <wiki-repo-path>
git add site/ .github/
git commit -m "feat: add Hugo site scaffold"
```

This commits `site/` and `.github/workflows/hugo-deploy.yml` — files that
live at the repo root, outside `wiki/`, so `wiki_content_commit` cannot
be used here.

## Step 6 — Preview

Instruct the user:

```bash
cd <wiki-repo-path>/site
hugo server --buildDrafts
```

The URL is printed by Hugo (e.g. `http://localhost:1313/<repo-name>/`).

## Step 6 — Deploy (optional)

If the user wants GitHub Pages deployment:

1. Enable GitHub Pages in the repo settings: Settings → Pages → Source: GitHub Actions
2. Push to `main` — the workflow at `.github/workflows/hugo-deploy.yml` builds and deploys automatically

## What gets rendered

- All pages in `wiki/` with valid frontmatter
- Type and tag taxonomy pages
- Section index pages

## What is excluded

- `inbox/`, `raw/`, `schemas/` directories
- `.json` and `.txt` files (wiki exports)
- Pages with `status: draft` or `status: stub` are excluded from production
  but visible with `hugo server --buildDrafts`
