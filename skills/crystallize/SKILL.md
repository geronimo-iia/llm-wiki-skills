---
name: crystallize
description: >
  Distil a session into durable wiki pages — extract decisions,
  findings, and open questions into concept or query-result pages.
type: skill
status: active
last_updated: "2025-07-21"
when_to_use: >
  Preserving session knowledge — decisions reached, patterns
  discovered, questions resolved, or design rationale established.
  Propose crystallization when a session produces durable knowledge;
  always confirm with the user before writing.
tags: [crystallize, session, knowledge-capture]
owner: jguibert@gmail.com
metadata:
  version: "0.2.0"
---

# Crystallize

Distil a session into durable wiki pages. Valuable knowledge emerges
from conversations — decisions reached, patterns discovered, questions
resolved. Without crystallization, this knowledge disappears when the
session ends.

## What to capture

**Keep:** decisions made, patterns established, lessons learned, open
questions, current understanding, key findings, agreed frameworks,
design rationale.

**Discard:** exploratory back-and-forth, dead ends, process chat,
superseded drafts, corrections already incorporated.

The output is always significantly shorter and more structured than
the input. Crystallize distils — it does not transcribe.

## When to crystallize

- A decision was reached → crystallize the decision and rationale
- New knowledge was absorbed → crystallize into a concept page
- A question was resolved → update the page that had the open question
- A design was settled → crystallize into a query-result or concept
- The chat is getting heavy → crystallize before context degrades
- Closing a long thread → crystallize everything worth keeping

## Search for an existing home

Before creating anything new, search the wiki:

```
wiki_search(query: "<topic>")
```

If a concept page, section index, or prior query-result already covers
this ground, prefer updating it over creating a new page.

Read candidates to check scope:

```
wiki_content_read(uri: "<candidate-slug>")
```

## Create a new page

When no existing page fits, use `type: query-result` for session
conclusions or `type: concept` for synthesized knowledge.

Get the frontmatter scaffold:

```
wiki_schema(action: "show", type: "query-result", template: true)
```

Create and write:

```
wiki_content_new(uri: "<slug>", type: "query-result")
wiki_content_write(uri: "<slug>", content: "<full markdown>")
```

Set `sources` to the source pages that contributed claims, `concepts`
to the concept pages discussed. These create typed graph edges
(`fed-by` and `depends-on`).

## Update an existing page

Respect the accumulation contract:

1. Read the current page: `wiki_content_read(uri: "<slug>")`
2. Preserve existing list values (`tags`, `read_when`, `sources`,
   `concepts`, `claims`) — add, do not replace
3. Update scalar fields (`summary`, `tldr`, `confidence`) only with
   clear reason
4. Write the complete file:

```
wiki_content_write(uri: "<slug>", content: "<updated markdown>")
```

## Validate and index

Dry-run to catch errors (including edge target type mismatches):

```
wiki_ingest(path: "<path>", dry_run: true)
```

Then ingest for real:

```
wiki_ingest(path: "<path>")
```

## Verify

Confirm the knowledge was captured correctly:

```
wiki_content_read(uri: "<slug>")
```

Check graph edges are connected as expected:

```
wiki_graph(root: "<slug>", depth: 1)
```

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
