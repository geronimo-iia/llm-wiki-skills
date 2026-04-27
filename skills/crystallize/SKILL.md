---
name: crystallize
description: >
  Distil a session into durable wiki pages — extract decisions,
  findings, and open questions into concept or query-result pages.
type: skill
status: active
last_updated: "2026-04-27"
when_to_use: >
  Preserving session knowledge — decisions reached, patterns
  discovered, questions resolved, or design rationale established.
  Propose crystallization when a session produces durable knowledge;
  always confirm with the user before writing.
tags: [crystallize, session, knowledge-capture]
owner: jguibert@gmail.com
metadata:
  version: "0.3.0"
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

## Analyse before writing

Before creating or updating any page, produce a concise extraction plan.

For each item of durable knowledge in the session, note:
- **What** — one sentence describing the knowledge
- **Type** — `decision`, `finding`, `pattern`, `open-question`
- **Action** — `create <type> <slug>`, `update <slug>`, or `discard`
- **Confidence** — estimated score (see calibration table below)

Example plan output:

```
1. tantivy fast fields require f64 not f32 (finding) → create concept tantivy-fast-field-types [0.85]
2. tweak_score replaces post-retrieval sort (decision) → create query-result search-ranking-tweak-score [0.9]
3. design-03 needs to depend on design-04 (decision) → update query-result improvements-ordering [0.8]
4. explored renaming ops module (dead end) → discard
```

Present the plan to the user and confirm before writing. This keeps the
user in control and prevents the session from producing redundant or
misclassified pages.

## Confidence calibration for session knowledge

| Knowledge type | Suggested `confidence` |
|---|---|
| Decision explicitly reached, agreed by all parties | 0.85–0.95 |
| Pattern observed, confirmed by evidence in session | 0.70–0.85 |
| Finding confirmed and cross-referenced with existing pages | 0.80–0.95 |
| Pattern observed, not yet tested broadly | 0.50–0.65 |
| Hypothesis raised, plausible but unvalidated | 0.30–0.50 |
| Open question noted, no resolution | 0.20–0.35 |
| Speculation or brainstorm output | 0.10–0.25 |

These ranges are starting points. Adjust up when the session provided
strong evidence (code confirmed to work, multiple independent sources);
adjust down when the conclusion was tentative or context-specific.

The default when no calibration applies is `0.5` (neutral — present but
unreviewed). Never leave `confidence` absent on session-derived pages:
the lint rule will flag them as stale if they stay at default for long.

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

### Check structural quality

After ingest, run the engine lint for the pages just written:

```
wiki_lint(rules: "broken-link,orphan")
```

This catches:
- Dead references in `sources`, `concepts`, or body wikilinks introduced
  by the new pages
- Orphan pages if the new page was not linked from anywhere

Fix any `Error` findings before closing the session. `Warning` findings
(orphan on a newly created standalone page) can be deferred.

> **Note:** `wiki_lint` ships with engine v0.2.0. If the command is not
> recognized, skip this step and follow the **lint** skill manually for
> broken-link and orphan checks.

## Verify

Confirm the knowledge was captured correctly:

```
wiki_content_read(uri: "<slug>")
```

Check graph edges are connected as expected:

```
wiki_graph(root: "<slug>", depth: 1)
```

Suggest links for the new page:

```
wiki_suggest(slug: "<slug>")
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
