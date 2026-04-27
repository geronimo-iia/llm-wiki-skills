---
name: lint
description: >
  Audit wiki quality — orphan pages, broken links, empty sections,
  edge target type mismatches, and schema integrity.
type: skill
status: active
last_updated: "2026-04-27"
disable-model-invocation: false
when_to_use: >
  Auditing wiki structure, checking for broken links or orphan pages,
  validating schemas, or verifying graph integrity after content
  changes.
tags: [lint, audit, quality, structure]
owner: jguibert@gmail.com
metadata:
  version: "0.4.0"
---

# Lint

Structural audit of the wiki. Find quality issues, report them, and
offer fixes.

## Deterministic checks (engine)

Start every audit by running the engine lint tool. These checks are
index-based, deterministic, and fast:

```
wiki_lint()
```

This returns a JSON report with `findings` grouped by rule:

| Rule | Severity | What it checks |
|------|----------|----------------|
| `orphan` | warning | Pages with no incoming links (excluding sections) |
| `broken-link` | error | Slugs in `body_links` or frontmatter edge fields that don't exist |
| `missing-fields` | error | Required frontmatter fields absent per type schema |
| `stale` | warning | Old `last_updated` AND low `confidence` (both must hold) |
| `unknown-type` | error | `type` field not registered in the type registry |

Run a subset of rules:

```
wiki_lint(rules: "orphan,broken-link")
```

Filter to errors only (CI-suitable):

```
wiki_lint(severity: "error")
```

Target a specific wiki:

```
wiki_lint(wiki: "research")
```

An empty `findings` array means the wiki is clean for these rules.
`error` findings block CI (`llm-wiki lint --severity error` exits non-zero).

## Schema integrity

Validate all schema files for correctness and index compatibility:

```
wiki_schema(action: "validate")
```

Checks: valid JSON Schema, `x-wiki-types` presence, alias resolution,
base schema invariant (`default` type requires `title` and `type`),
and full index compatibility.

Validate a single type:

```
wiki_schema(action: "validate", type: "<type>")
```

## Edge target type validation

Use dry-run ingest to check for edge target type mismatches without
modifying the index:

```
wiki_ingest(path: "<path>", dry_run: true)
```

The engine reads `x-graph-edges` from the type's schema and warns
when an edge target has the wrong type.

## Judgment-based checks (skill layer)

These require reasoning and stay in the skill — they cannot be reduced
to an index query.

### Structural orientation

For a full-wiki structural overview before gap analysis, use
`format: "llms"` to get all pages grouped by type with summaries:

```
wiki_list(format: "llms")
```

This replaces paginated listing for broad enumeration — one call
covers the full wiki, grouped and annotated, without needing multiple
`page_size: 100` calls.

### Empty sections

```
wiki_list(type: "section", page_size: 50)
```

For each section, check if any pages exist under that slug prefix.

### Missing stubs

Referenced slugs that don't exist and have not been caught by
`broken-link` (e.g. intentional forward references). These are
candidates for new pages — create stubs or remove the dead reference.

### Untyped sources

Pages with a generic or missing type that appear to be source
summaries should use a specific source type (`paper`, `article`,
`documentation`, etc.). Requires judgment: is this page *acting* as
a source?

### Draft audit

```
wiki_stats()
```

The `status` facet shows the distribution (e.g. `active: 40, draft: 3`).
Review draft pages: are they progressing, abandoned, or placeholders?

### Under-linked pages

```
wiki_suggest(slug: "<slug>", limit: 10)
```

Pages with many high-score suggestions are likely under-linked.
Requires relevance judgment — don't link for graph density.

## Report findings

Present findings grouped by category, leading with `wiki_lint` output:

- **Engine findings** — orphans, broken links, missing fields, stale, unknown types
- **Schema issues** — invalid schemas, field conflicts
- **Edge type mismatches** — wrong target types on graph edges
- **Empty sections** — sections with no children
- **Missing stubs** — referenced pages that don't exist
- **Untyped sources** — source pages without specific types

## Fix issues

For each category:

- **Broken links** — remove dead references or create the missing pages
- **Orphan pages** — add a `[[slug]]` reference from a related page, or link from a section or index page
- **Missing fields** — open the page and add the required frontmatter field for its type; use `wiki_schema(action: "show", type: "<type>")` to see what is required
- **Stale pages** — review and update content, set `last_updated` to today, and raise `confidence` to reflect current certainty; a page with `confidence: 0.9` is not stale even if old
- **Unknown type** — correct the typo in the `type:` field, or register the new type with `wiki_schema(action: "add")`; run `wiki_schema(action: "list")` to see registered types
- **Schema issues** — fix the schema file, then `wiki_schema(action: "validate")`
- **Edge type mismatches** — fix the frontmatter field, then `wiki_ingest`
- **Missing stubs** — `wiki_content_new(uri: "<slug>", type: "<type>")`
- **Empty sections** — create or move pages under the section

After each fix:

```
wiki_content_write(uri: "<slug>", content: "<fixed content>")
wiki_ingest(path: "<path>")
```
