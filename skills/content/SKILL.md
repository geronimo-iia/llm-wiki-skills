---
name: content
description: >
  Read, create, update, and organize wiki pages and sections —
  direct content operations outside of ingest and crystallize
  workflows.
type: skill
status: active
last_updated: "2025-07-21"
disable-model-invocation: true
argument-hint: "[slug] [--type concept|doc|section|skill|paper|...]"
when_to_use: >
  Reading a page, creating a page or section, updating existing
  content, or organizing wiki structure.
tags: [content, write, create, read, update, section, authoring]
owner: jguibert@gmail.com
metadata:
  version: "0.2.0"
---

# Content

Direct operations on wiki pages and sections. This skill covers
deliberate content work — reading, creating, updating, and organizing
pages outside of the [ingest](../ingest/SKILL.md) (inbox→raw) and
[crystallize](../crystallize/SKILL.md) (session→page) workflows.

Content operations do not validate or index — that's what
`wiki_ingest` does. Always ingest after writing.

When `llm-wiki serve --watch` is active, external edits are indexed
automatically — manual ingest is only needed for programmatic writes
via `wiki_content_write`.

## Page anatomy

A wiki page is a Markdown file with YAML frontmatter. The file is
always: frontmatter block + blank line + body.

```
---
title: "Mixture of Experts"
summary: "Sparse routing of tokens to expert subnetworks."
type: concept
status: active
...
---

## Overview

MoE routes tokens to sparse expert subnetworks…
```

Start body content at `##` level. `#` is reserved for the page title
(derived from frontmatter `title`).

For frontmatter field conventions, see the
[frontmatter](../frontmatter/SKILL.md) skill.

## Flat page vs bundle

A flat page is a single `.md` file:

```
concepts/scaling-laws.md
```

A bundle is a folder containing `index.md` and co-located assets:

```
concepts/mixture-of-experts/
├── index.md
├── moe-routing.png
└── vllm-config.yaml
```

Use a bundle when the page has associated assets (images, diagrams,
data files). Assets always belong to one page — there is no shared
asset folder.

## Assets

Assets in a bundle are referenced with short relative paths:

```markdown
![MoE routing](./moe-routing.png)
See [vllm-config.yaml](./vllm-config.yaml)
```

List a page's assets:

```
wiki_content_read(uri: "<slug>", list_assets: true)
```

## Slug resolution

A slug is a path without extension, relative to `wiki/`. Resolution
checks two forms in order:

1. `concepts/mixture-of-experts.md` → flat file
2. `concepts/mixture-of-experts/index.md` → bundle

The same slug is used regardless of which form is on disk.

## Wiki links

`[[slug]]` links to another wiki page in the body:

```markdown
See [[concepts/scaling-laws]] for background.
```

Wiki links create graph edges (generic `links-to` relation).
Deduplicated per page — each slug appears once in the link list.

## Read a page

```
wiki_content_read(uri: "<slug>")
```

Accepts a slug (`concepts/moe`), short URI (`wiki://concepts/moe`),
or full URI (`wiki://research/concepts/moe`).

Strip frontmatter with `no_frontmatter: true`.

When a page has `superseded_by` set, the output includes a notice
pointing to the replacement.

### Backlinks

Pass `backlinks: true` to discover which pages link to this one:

```
wiki_content_read(uri: "concepts/moe", backlinks: true)
```

Response is JSON:

```json
{
  "content": "# Mixture of Experts\n...",
  "backlinks": [
    { "slug": "concepts/scaling-laws", "title": "Scaling Laws" },
    { "slug": "papers/switch-transformer", "title": "Switch Transformer" }
  ]
}
```

`backlinks` is an array of `{ slug, title }` for every page whose body
contains `[[concepts/moe]]`. Returns an empty array when nothing links
to this page. No overhead when `backlinks` is omitted (default).

## Page history

```
wiki_history(slug: "<slug>")
```

Returns git commit history for the page — hash, date, message,
author. Use to assess freshness, track changes, or find the last
ingest commit. Rename tracking is enabled by default (`--follow`).

## Wiki overview

```
wiki_stats()
```

Returns page counts, type/status distribution, orphans, graph
connectivity, staleness, and index health in one call.

## List pages

```
wiki_list()
wiki_list(type: "concept")
wiki_list(status: "draft")
wiki_list(type: "section", page_size: 50)
```

Paginated results ordered alphabetically by slug. Each entry includes
slug, URI, title, type, status, and tags. Facets (`type`, `status`,
`tags` distributions) are always included.

## Search pages

```
wiki_search(query: "<topic>")
wiki_search(query: "<topic>", type: "concept")
```

## Create a page

Check for duplicates first:

```
wiki_search(query: "<topic>")
```

Get the frontmatter scaffold:

```
wiki_schema(action: "show", type: "<type>", template: true)
```

Create the page:

```
wiki_content_new(uri: "<slug>", type: "<type>")
```

The page is scaffolded with frontmatter and a body template based on
the type (from `schemas/<type>.md`). For custom types, add a `.md`
file next to the schema.

For a bundle:

```
wiki_content_new(uri: "<slug>", bundle: true)
```

Write the content and ingest:

```
wiki_content_write(uri: "<slug>", content: "<full markdown>")
wiki_ingest(path: "<path-relative-to-wiki-root>")
```

Slugs are lowercase, hyphenated, relative to `wiki/`:
`concepts/mixture-of-experts`, `sources/switch-transformer-2021`.

## Update a page

Read before write — respect the accumulation contract:

1. Read the current page: `wiki_content_read(uri: "<slug>")`
2. Preserve existing list values (`tags`, `read_when`, `sources`,
   `concepts`, `claims`) — add, do not replace
3. Update scalar fields only with clear reason
4. Write the complete file and ingest:

```
wiki_content_write(uri: "<slug>", content: "<updated markdown>")
wiki_ingest(path: "<path-relative-to-wiki-root>")
```

## Create a section

A section is a directory with an `index.md` that groups related pages.
Sections use `type: section` and have no additional fields beyond base.

```
wiki_content_new(uri: "<slug>", section: true)
```

Missing parent sections are created automatically with their
`index.md`.

```
wiki/concepts/
├── index.md                    ← section index (type: section)
├── scaling-laws.md
└── mixture-of-experts.md
```

Sections are excluded from search results by default
(`--include-sections` to include them). They serve as navigation,
not knowledge.

## Organize sections

List existing sections:

```
wiki_list(type: "section", page_size: 50)
```

Read a section's index page:

```
wiki_content_read(uri: "<section-slug>")
```

Update a section's index to reflect its current contents — add
links to child pages, update the summary.

## Commit changes

Content operations do not commit to git automatically. Commit
explicitly after writing:

```
wiki_content_commit(slugs: "<slug>")
wiki_content_commit(slugs: "<slug1>,<slug2>")
wiki_content_commit()
```

When committing by slug, the engine stages the right files:
- Flat page → single `.md` file
- Bundle → entire bundle folder
- Section → entire section folder recursively

`wiki_ingest` commits automatically when `ingest.auto_commit` is
true in the wiki config.

## View page changes

Use `wiki_history` to get commit hashes, then `git diff` to see
what changed:

```
wiki_history(slug: "<slug>", limit: 2)
```

Then in bash:

```bash
git -C <repo_root> diff <from_hash> <to_hash> -- wiki/<slug>.md
```

For uncommitted changes (edits not yet ingested):

```bash
git -C <repo_root> diff -- wiki/<slug>.md
```

## Suggest links

After creating or updating a page, suggest related pages to link:

```
wiki_suggest(slug: "<slug>")
```

Returns candidates with scores, reasons, and suggested frontmatter
fields. Apply the backlink quality test before adding suggestions.

## Update related pages

After creating or updating a page, check if related pages need
backlinks. Read before write — preserve existing values.

Apply the backlink quality test: would a reader benefit from
navigating there?
