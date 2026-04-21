---
name: ingest
description: >
  Process source files into synthesized wiki pages. Read sources,
  search for existing knowledge, write pages with frontmatter,
  validate and commit. Use when the user drops files in inbox/ or
  says "ingest", "process this", or "add to wiki".
type: skill
status: active
last_updated: "2025-07-18"
disable-model-invocation: true
argument-hint: "[file-or-folder-path]"
tags: [ingest, workflow, sources]
owner: geronimo
---

# Ingest

Process source files into synthesized wiki pages. This is the primary
knowledge-building workflow — it turns raw sources into structured,
cross-referenced wiki content.

## MCP tools used

- `wiki_search` — find existing pages on the same topic
- `wiki_content_read` — read existing pages and source files
- `wiki_content_write` — write pages into the wiki tree
- `wiki_ingest` — validate frontmatter, update index, commit
- `wiki_content_commit` — commit if auto_commit is off

## Steps

### 1. Read the source

Read the source file from `inbox/` or the provided path. Understand
what it contains, what claims it makes, what topics it covers.

### 2. Search for existing knowledge

```
wiki_search(query: "<topic from source>")
```

Find existing pages on the same topic. Check if concept pages,
source pages, or section indexes already cover this ground.

### 3. Read existing pages

```
wiki_content_read(uri: "<relevant-slug>")
```

Read the existing pages to understand the current state of knowledge.
This is critical — the wiki accumulates, it does not replace.

### 4. Decide: update or create

- If a concept page already covers this topic → update it with new
  claims and sources
- If no existing page → create a new one
- If the source introduces a new concept → create a concept page
- If the source is a summary of a specific document → create a source
  page with the appropriate type

### 5. Write pages

Write complete Markdown files with frontmatter using
`wiki_content_write`. Follow the **frontmatter** skill for correct
field values per type.

Get the frontmatter scaffold for the target type:

```
wiki_schema(action: "show", type: "<type>", template: true)
```

Fill in the template values, then write:

```
wiki_content_write(uri: "<slug>", content: "<full markdown>")
```

For each page:
- Set the correct `type` (concept, paper, article, etc.)
- Write all required fields for that type (the template shows them)
- Add `sources`, `concepts`, `tags`, `confidence`, `claims` as relevant
- Write a structured body with clear sections

### 6. Validate and index

```
wiki_ingest(path: "<path-relative-to-wiki-root>")
```

The engine validates frontmatter against the type's JSON Schema,
updates the tantivy search index, and commits to git (if
`ingest.auto_commit` is true). If validation fails, the file is
rejected with a clear error message showing which fields are
missing or invalid.

### 7. Preserve existing values (accumulation contract)

When updating an existing page:

1. Read the current page first with `wiki_content_read`
2. Preserve existing list values — do not drop `tags`, `read_when`,
   `sources`, `concepts`, or `claims` added by prior ingests
3. Add new values to lists, do not replace them
4. Update scalar fields (`summary`, `tldr`, `confidence`) only when
   there is a clear reason
5. Write the complete file, then ingest

## Linking policy

When adding links between pages — in frontmatter (`sources`,
`concepts`) or body (`[[wikilinks]]`) — apply this test: would a
reader of this page benefit from navigating to the linked page?

If the connection is only surface-level (shared keyword, same broad
domain), omit the link. Prefer fewer meaningful links over many weak
ones.

## Source type selection

Classify by the source material's nature, not its topic:

| Type | Source nature |
|------|-------------|
| `paper` | Academic — research papers, preprints |
| `article` | Editorial — blog posts, news, essays |
| `documentation` | Reference — product docs, API references |
| `clipping` | Web capture — browser clips, bookmarks |
| `transcript` | Spoken — meeting transcripts, podcasts |
| `note` | Informal — freeform drafts, quick captures |
| `data` | Structured — CSV, JSON, datasets |
| `book-chapter` | Published — book excerpts |
| `thread` | Discussion — forum threads, social media |

A blog post about academic research is `article`, not `paper`.
