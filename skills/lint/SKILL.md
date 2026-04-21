---
name: lint
description: >
  Audit wiki structure for orphan pages, missing stubs, empty
  sections, and broken links. Offer to fix issues. Use when the
  user says "lint", "audit", "check structure", or "find problems".
type: skill
status: active
last_updated: "2025-07-18"
disable-model-invocation: true
tags: [lint, audit, quality, structure]
owner: geronimo
---

# Lint

Structural audit — find orphans, missing stubs, empty sections, and
broken links. Offer to fix issues automatically.

## MCP tools used

- `wiki_list` — get all pages with type/status filters
- `wiki_content_read` — read page frontmatter and body
- `wiki_search` — find candidate connections
- `wiki_content_write` — write fixes
- `wiki_ingest` — validate and index fixes

## Steps

### 1. List all pages

```
wiki_list(page_size: 100)
```

Paginate through all pages. Collect slug, type, status, and title for
each.

### 2. Check each page

For each page, read its content and check:

#### Orphan detection

Does this page have backlinks? Check if any other page references it
in `sources`, `concepts`, or body `[[wikilinks]]`. Pages with no
inbound links are orphans.

#### Broken links

Do the slugs in `sources` and `concepts` frontmatter resolve to
existing pages? Read the page and check each slug against the page
list.

#### Empty sections

If the page is `type: section`, does it have children? A section with
no pages underneath is empty.

#### Missing stubs

Do `sources` or `concepts` reference slugs that don't exist? These
are missing stubs that should be created.

#### Untyped sources

Pages with `type: source-summary` or missing type that appear to be
source summaries should use a specific source type (`paper`, `article`,
`documentation`, etc.).

### 3. Report findings

Present findings grouped by category:

- **Orphan pages** — no inbound links
- **Broken links** — frontmatter references non-existent slugs
- **Empty sections** — sections with no children
- **Missing stubs** — referenced pages that don't exist
- **Untyped sources** — source pages without specific types

### 4. Offer fixes

For each category, offer to fix:

- **Missing stubs** — create stub pages with minimal frontmatter
- **Empty sections** — suggest pages to move or create under the section
- **Broken links** — remove dead references or create the missing pages
- **Orphan pages** — suggest connections to existing pages

### 5. Apply fixes

For each accepted fix:

```
wiki_content_write(uri: "<slug>", content: "<fixed content>")
wiki_ingest(path: "<path>")
```

## Linking policy

When suggesting new links, apply the backlink quality test: would a
reader of page A genuinely benefit from knowing about page B? Do not
link for graph density — link for navigation quality.
