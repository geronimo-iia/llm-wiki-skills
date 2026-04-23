---
name: lint
description: >
  Audit wiki quality — orphan pages, broken links, empty sections,
  edge target type mismatches, and schema integrity.
type: skill
status: active
last_updated: "2025-07-21"
disable-model-invocation: true
when_to_use: >
  Auditing wiki structure, checking for broken links or orphan pages,
  validating schemas, or verifying graph integrity after content
  changes.
tags: [lint, audit, quality, structure]
owner: jguibert@gmail.com
metadata:
  version: "0.2.0"
---

# Lint

Structural audit of the wiki. Find quality issues, report them, and
offer fixes.

## Schema integrity

Validate all schema files for correctness and index compatibility:

```
wiki_schema(action: "validate")
```

Checks: valid JSON Schema, `x-wiki-types` presence, alias resolution,
base schema invariant (`default` type requires `title` and `type`),
and full index compatibility (no field conflicts across schemas).

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
when an edge target has the wrong type. For example:

- A concept with `sources` pointing to another concept instead of a
  source type (`fed-by` expects source types)
- A source page with `concepts` pointing to a paper instead of a
  concept (`informs` expects `concept`)

## Orphan detection

Pages with no inbound links from `sources`, `concepts`, or body
`[[wikilinks]]` are orphans.

Generate the graph and look for isolated nodes:

```
wiki_graph()
```

## Broken links

Frontmatter fields (`sources`, `concepts`, `document_refs`,
`superseded_by`) and body `[[wikilinks]]` may reference slugs that
don't exist in the index.

Read each page and check referenced slugs against the page list:

```
wiki_list(page_size: 100)
wiki_content_read(uri: "<slug>")
```

## Empty sections

Sections with no child pages underneath:

```
wiki_list(type: "section", page_size: 50)
```

For each section, check if any pages exist under that slug prefix.

## Missing stubs

Referenced slugs that don't exist. These are candidates for new pages
— create stubs with minimal frontmatter or remove the dead reference.

## Untyped sources

Pages with a generic or missing type that appear to be source
summaries should use a specific source type (`paper`, `article`,
`documentation`, etc.).

## Draft audit

Use the `status` facet from `wiki_list` or `wiki_stats` to find how
many pages are in draft status:

```
wiki_stats()
```

The `status` facet shows the distribution (e.g. `active: 40, draft: 3`).

## Report findings

Present findings grouped by category:

- **Schema issues** — invalid schemas, field conflicts
- **Edge type mismatches** — wrong target types on graph edges
- **Orphan pages** — no inbound links
- **Broken links** — references to non-existent slugs
- **Empty sections** — sections with no children
- **Missing stubs** — referenced pages that don't exist
- **Untyped sources** — source pages without specific types

## Fix issues

For each category:

- **Schema issues** — fix the schema file, then
  `wiki_schema(action: "validate")`
- **Edge type mismatches** — fix the frontmatter field, then
  `wiki_ingest(path: "<path>")`
- **Missing stubs** — create stub pages with
  `wiki_content_new(uri: "<slug>", type: "<type>")`
- **Broken links** — remove dead references or create the missing
  pages
- **Orphan pages** — add links from related pages
- **Empty sections** — create or move pages under the section

After each fix, write and ingest:

```
wiki_content_write(uri: "<slug>", content: "<fixed content>")
wiki_ingest(path: "<path>")
```

## Under-linked pages

Use `wiki_suggest` to find pages that should be linked but aren't:

```
wiki_suggest(slug: "<slug>", limit: 10)
```

Pages with many high-score suggestions are likely under-linked.

## Linking policy

When suggesting new links, apply the backlink quality test: would a
reader of page A genuinely benefit from knowing about page B? Do not
link for graph density — link for navigation quality.
