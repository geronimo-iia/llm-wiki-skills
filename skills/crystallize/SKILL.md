---
name: crystallize
description: >
  Distil the current session into durable wiki pages. Extract
  decisions, findings, and open questions. Update existing pages
  or create new ones. Use when the user says "crystallize",
  "save this", "write this up", or at the end of a productive session.
type: skill
status: active
last_updated: "2025-07-18"
disable-model-invocation: true
tags: [crystallize, session, knowledge-capture]
owner: geronimo
---

# Crystallize

Distil the current session into durable wiki pages. Valuable knowledge
emerges from conversations — decisions reached, patterns discovered,
questions resolved. Without crystallize, this knowledge disappears when
the session ends.

## MCP tools used

- `wiki_search` — find existing pages that should be updated
- `wiki_content_read` — read existing pages before updating
- `wiki_content_write` — write pages into the wiki tree
- `wiki_ingest` — validate, index, commit
- `wiki_content_commit` — commit if auto_commit is off

## What to capture

**Keep:** decisions made, patterns established, lessons learned, open
questions, current understanding, key findings, agreed frameworks,
design rationale.

**Discard:** exploratory back-and-forth, dead ends, process chat,
superseded drafts, corrections already incorporated.

The output is always significantly shorter and more structured than the
input. Crystallize distils — it does not transcribe.

## Steps

### 1. Search for an existing home

Before creating anything new, search the wiki:

```
wiki_search(query: "<topic>")
```

If a concept page, section index, or prior query-result already covers
this ground, prefer updating it over creating a new page.

### 2. Read existing pages

```
wiki_content_read(uri: "<candidate-slug>")
```

Check if the update fits the existing page's scope.

### 3. Write the page

For a **new page** (no existing home found), use `type: query-result`:

```yaml
---
title: "Topic — Aspect"
summary: "One sentence describing what was established."
tldr: "The bottom line conclusion."
read_when:
  - "Reviewing decisions about <topic>"
status: active
last_updated: "2025-07-18"
type: query-result
tags: [relevant, tags]
sources: [slugs/of/sources/used]
concepts: [slugs/of/concepts/discussed]
confidence: medium
---
```

For an **update** to an existing page:
1. Read the current page with `wiki_content_read`
2. Merge new knowledge — preserve existing frontmatter values, add new
   tags/sources/claims, update body sections
3. Write the complete updated file

```
wiki_content_write(uri: "<slug>", content: "<full markdown>")
```

### 4. Ingest

```
wiki_ingest(path: "<path-relative-to-wiki-root>")
```

### 5. Verify

```
wiki_content_read(uri: "<slug>")
```

Confirm the knowledge was captured correctly.

## Suggested body structure

Adapt to the content — not every section is needed:

| Section | When to include |
|---------|----------------|
| Summary | Always — 2–4 sentences of what was established |
| Decisions | When decisions were made |
| Findings | When new knowledge was discovered |
| Current Understanding | When the session advanced understanding |
| Open Questions | When questions remain unresolved |
| Related Pages | When connections to other wiki pages are worth noting |

## When to crystallize

Use crystallize liberally:

- A decision was reached → crystallize the decision and rationale
- New knowledge was absorbed → crystallize into a concept page
- A question was resolved → update the page that had the open question
- A design was settled → crystallize into a query-result or concept page
- The chat is getting heavy → crystallize before context degrades
- Closing a long thread → crystallize everything worth keeping
