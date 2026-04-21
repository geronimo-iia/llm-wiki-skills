---
name: write-page
description: >
  Create a wiki page of any type. Scaffold frontmatter from the
  type registry, fill in type-specific fields, validate and commit.
  Use when the user says "create a page", "write a doc",
  "add a concept", "new section", or wants to create a page
  outside of ingest or crystallize workflows.
type: skill
status: active
last_updated: "2025-07-18"
disable-model-invocation: true
argument-hint: "[slug] [--type concept|doc|section|skill|paper|...]"
tags: [write, create, page, authoring]
owner: geronimo
---

# Write Page

Create a wiki page of any type with correct frontmatter and structure.
This is the skill for deliberate page creation — when the user wants to
write a page that isn't driven by source ingestion or session
crystallization.

## MCP tools used

- `wiki_schema` — list types, get frontmatter template
- `wiki_search` — find existing pages on the same topic
- `wiki_content_new` — scaffold a page with frontmatter
- `wiki_content_write` — write the page content
- `wiki_ingest` — validate, index, commit
- `wiki_content_read` — read pages to update with new links

## Steps

### 1. Determine the target type

From the user's intent, determine the page type:

- "add a concept" → `concept`
- "write a doc" → `doc`
- "new section" → `section`
- "create a skill" → `skill`
- "add a paper summary" → `paper`
- If unclear, ask the user

### 2. Read registered types

```
wiki_schema(action: "list")
```

See all registered types and their descriptions. Choose the right
type for the page being created.

### 3. Search for duplicates

```
wiki_search(query: "<topic>")
```

Avoid creating duplicate pages. Find existing pages to link to.

### 4. Determine the slug

Ask the user or derive from the title. Slugs are lowercase,
hyphenated, relative to `wiki/`:

- `concepts/mixture-of-experts`
- `sources/switch-transformer-2021`
- `docs/api-reference`

### 5. Get the type template

```
wiki_schema(action: "show", type: "<type>", template: true)
```

This returns the frontmatter scaffold with all required and common
fields for the type. Use it as the starting point.

### 6. Create the page

```
wiki_content_new(uri: "<slug>", type: "<type>")
```

For sections: `wiki_content_new(uri: "<slug>", section: true)`
For bundles: `wiki_content_new(uri: "<slug>", bundle: true)`

### 7. Fill in type-specific fields

Fill the template values. Follow the **frontmatter** skill for
field conventions. Key differences by type:

**section** — `title`, `summary` only. No additional fields.

**concept** — `sources`, `concepts`, `confidence`, `claims`,
`read_when` (required), `tldr`.

**doc** — `sources` (informed-by), `read_when`.

**source types** (paper, article, etc.) — `tldr`, `sources` (cites),
`concepts` (informs), `confidence`, `claims`, `read_when`.

**skill** — `name`, `description` (not `title`/`summary`),
`disable-model-invocation`, `allowed-tools`, `argument-hint`.

### 8. Write the body

Structure the body with clear sections appropriate to the type.

### 9. Save the page

```
wiki_content_write(uri: "<slug>", content: "<full markdown>")
```

### 10. Validate and index

```
wiki_ingest(path: "<path-relative-to-wiki-root>")
```

### 11. Update related pages

If the new page should link to/from existing pages, update those
pages. Read before write — preserve existing list values.

```
wiki_content_read(uri: "<related-slug>")
wiki_content_write(uri: "<related-slug>", content: "<updated>")
wiki_ingest(path: "<related-path>")
```
