---
name: ingest
description: >
  Process source files from inbox/ into synthesized wiki pages —
  scan the inbox queue, read each file, search for existing
  knowledge, write pages with frontmatter, validate and commit.
  Source files move to raw/ on successful ingest.
type: skill
status: active
last_updated: "2026-04-27"
disable-model-invocation: true
argument-hint: "[file-or-folder-path]"
when_to_use: >
  Processing files from inbox/, ingesting new sources, or adding
  content to the wiki.
tags: [ingest, workflow, sources]
owner: jguibert@gmail.com
metadata:
  version: "0.4.0"
---

# Ingest

Process source files from the `inbox/` queue into synthesized,
cross-referenced wiki pages. The engine moves each source to `raw/`
on successful ingest — the move is the record of completion.

## Workflow

### Step 0 — Discover the wiki root

```
wiki_spaces_list()
```

The response includes the wiki path for each registered space. All
paths below (`inbox/`, `raw/`) are relative to the default wiki's
path.

### Step 1 — Scan inbox/

If the user provided a path, use it (must be inside `inbox/`):

```
wiki_ingest(path: "<user-provided-path>", dry_run: true)
```

Otherwise scan the entire queue:

```
wiki_ingest(path: "inbox/", dry_run: true)
```

If no files are found, report "No files to process." and stop.

Process files one at a time — complete all sub-steps for one file
before moving to the next.

### Step 2 — Process each file

For each file in inbox/, in order:

#### 2a. Read the source

Read the file and understand what it contains — topics, claims,
key concepts, structure.

Natively readable: `.md`, `.txt`, `.csv`, `.json`, `.yaml`, `.html`,
`.xml`, and most text-based files.

If reading fails (binary, unsupported format): note the reason and
skip to step 2g. The file stays in inbox/ for manual handling.

#### 2b. Classify the source

Determine the source type by the material's nature, not its topic:

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

Identify the main topic and domain. Ask: *what does a reader learn
from this?* That drives placement, not the document format.

If the source type is ambiguous (e.g. a PDF that could be a paper
or documentation), ask the user before proceeding.

#### 2c. Find integration points

For the **first file** in a session, orient with the full wiki map:

```
wiki_list(format: "llms")
```

This produces all pages grouped by type with summaries in a single
call — use it to understand what already exists before searching for
specific candidates. Subsequent files in the same session can skip
this call since the map is already in context.

Search for existing pages on the same topic:

```
wiki_search(query: "<main topic from source>")
wiki_search(query: "<candidate page title>")
```

Also check by type to find related source and concept pages:

```
wiki_search(query: "<topic>", type: "concept")
wiki_search(query: "<topic>", type: "<source-type>")
```

Read the most relevant results:

```
wiki_content_read(uri: "<relevant-slug>")
```

This serves two purposes:
- **Duplicate detection** — if a page already covers this subject,
  prefer updating it over creating a new one
- **Context** — understand the current state of knowledge so the
  new page integrates naturally

If multiple candidate pages could be the integration target, ask
the user which one to update.

#### 2d. Decide: create or update

- If a concept page already covers this topic → update it with new
  claims and sources
- If no existing page → create a new one
- If the source introduces a new concept → create a concept page
- If the source is a summary of a specific document → create a source
  page with the classified type
- One source can produce multiple pages — a rich document may warrant
  a source page plus new concept pages

#### 2e. Write pages

Get the frontmatter scaffold for the target type:

```
wiki_schema(action: "show", type: "<type>", template: true)
```

Follow the **frontmatter** skill for correct field values per type.

**Creating a new page:**

If the source has associated assets (images, PDFs, diagrams), create
a page bundle so assets live alongside the page:

```
wiki_content_new(uri: "<slug>", bundle: true)
```

Otherwise create a regular page:

```
wiki_content_new(uri: "<slug>", type: "<type>")
```

The page is scaffolded with frontmatter and a body template based on
the type (from `schemas/<type>.md`). Overwrite the body with
synthesized content:

```
wiki_content_write(uri: "<slug>", content: "<full markdown>")
```

For each page:
- Set the correct `type`
- Write all required fields for that type (the template shows them)
- Add `sources`, `concepts`, `tags`, `confidence`, `claims` as relevant;
  set `confidence` to `0.5` on new pages (single source, unreviewed) and
  raise it only as corroborating evidence accumulates
- Write a structured body — synthesize, do not copy verbatim
- Add links to related pages found in step 2c

Edge target types: each edge field (`sources`, `concepts`) declares
allowed target types via `x-graph-edges` / `target_types` in the
schema. Check the schema to confirm valid targets before writing:

```
wiki_schema(action: "show", type: "<type>")
```

**Updating an existing page (accumulation contract):**

1. Read the current page first with `wiki_content_read`
2. Preserve existing list values — do not drop `tags`, `read_when`,
   `sources`, `concepts`, or `claims` added by prior ingests
3. Add new values to lists, do not replace them
4. Update scalar fields (`summary`, `tldr`, `confidence`) only when
   there is a clear reason
5. Write the complete file

#### 2f. Validate and index

Pre-check the schema:

```
wiki_schema(action: "validate")
```

Dry-run to catch errors without committing:

```
wiki_ingest(path: "<path-relative-to-wiki-root>", dry_run: true)
```

Dry-run validates frontmatter against the type's JSON Schema and
reports edge target type mismatches. Fix any reported issues, then
ingest for real:

```
wiki_ingest(path: "<path-relative-to-wiki-root>")
```

**Redaction (opt-in):** when ingesting external content that may contain
secrets — web clips, session transcripts, raw notes — pass `redact: true`:

```
wiki_ingest(path: "<path>", redact: true)
```

The engine scans each file body for 6 built-in patterns (GitHub PAT,
OpenAI key, Anthropic key, AWS access key, Bearer token, email) and
replaces matches with `[REDACTED:pattern-name]` before commit. The
report includes a `redacted` field with the slug and line numbers of
each match. **Redaction is lossy** — original values are gone after
the file is written to disk. Do not use it on pages you have already
reviewed and committed.

Per-wiki, you can disable specific patterns or add custom ones in
`wiki.toml`:

```toml
[redact]
disable = ["email"]   # keep emails in a people/contacts wiki

[[redact.patterns]]
name        = "employee-id"
pattern     = "EMP-[0-9]{6}"
replacement = "[REDACTED:employee-id]"
```

The engine validates frontmatter, updates the tantivy search index,
and commits to git (if `ingest.auto_commit` is true). If validation
fails, the file is rejected with a clear error showing which fields
are missing or invalid.

After successful ingest, move the source file from `inbox/` to
`raw/` yourself:

```bash
mv <wiki-root>/inbox/<filename> <wiki-root>/raw/<filename>
```

The move is the record of completion — a file in `raw/` means it
was successfully ingested.

If validation passes but you want deeper checks (broken wikilinks,
orphan pages, style issues), follow the **lint** skill.

#### 2g. Record outcome

Track the result for this file:
- Pages created (slugs and types)
- Pages updated (what changed)
- Skipped (reason: unreadable, failed validation, etc.)

Then proceed to the next file in inbox/.

### Step 3 — Summary

After all files are processed, report to the user:

- Files processed with outcomes
- Pages created (with slugs and types)
- Pages updated (what changed)
- Files skipped with reasons
- Contradictions or confidence changes worth flagging
- Suggested follow-ups (e.g. run **lint**, check **graph** edges)

After ingest, use `wiki_suggest` to propose links for new pages,
and the **graph** skill to verify new pages are
connected as expected (edges, backlinks, section placement).

## Linking policy

When adding links between pages — in frontmatter (`sources`,
`concepts`) or body (`[[wikilinks]]`) — apply this test: would a
reader of this page benefit from navigating to the linked page?

If the connection is only surface-level (shared keyword, same broad
domain), omit the link. Prefer fewer meaningful links over many weak
ones.

## Key rules

1. **inbox/ is the queue** — ingest reads from inbox/ only; you
   move source files to raw/ after successful ingest; never delete
   from inbox/
2. **The move is your responsibility** — the engine does not move
   files; you do it after `wiki_ingest` succeeds; a file in raw/
   means it was successfully ingested
3. **Synthesize, do not copy** — wiki pages contain synthesized
   knowledge, not verbatim transcripts of the source
4. **One source can produce multiple pages** — a rich document may
   warrant a source page plus new concept pages; each page's
   `sources` field should reference the source page
5. **Process sequentially** — finish all sub-steps for one file
   before starting the next; do not batch writes across files
6. **Skip, do not block** — if a file is unreadable or fails
   validation, record the reason and continue with the next file
7. **Preserve on update** — never drop existing list values; read
   before write (accumulation contract in step 2e)
