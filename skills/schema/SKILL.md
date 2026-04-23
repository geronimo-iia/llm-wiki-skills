---
name: schema
description: >
  Understand and manage the type system — built-in types, type
  discovery, field aliasing, graph edges, and schema operations.
type: skill
status: active
last_updated: "2025-07-21"
when_to_use: >
  Understanding the type system, listing registered types, inspecting
  a type's schema or template, adding a custom type, removing a type,
  or validating schemas.
tags: [schema, types, validation, type-system]
owner: jguibert@gmail.com
metadata:
  version: "0.1.0"
---

# Schema

Every wiki page has a `type` field. The type determines which JSON
Schema validates the frontmatter, how fields are indexed, and what
graph edges are declared.

For frontmatter field conventions, see the
[frontmatter](../frontmatter/SKILL.md) skill.

## Epistemic roles

The type field carries epistemic distinctions:

| Role | Types | Question answered |
|------|-------|-------------------|
| Synthesized knowledge | `concept` | What do we know? |
| Source provenance | `paper`, `article`, `documentation`, ... | What does this source claim? |
| Reasoning output | `query-result` | What did we conclude? |
| Structure | `section` | How is knowledge organized? |
| Agent workflow | `skill` | How to perform a task? |
| Reference | `doc` | What are the specifications? |

Classify by the source material's nature, not its topic. A blog post
about academic research is `article`, not `paper`.

## Built-in types

Shipped by `llm-wiki spaces create`:

| Type | Schema | Description |
|------|--------|-------------|
| `default` | `base.json` | Fallback for unrecognized types |
| `concept`, `query-result` | `concept.json` | Synthesized knowledge and saved conclusions |
| `paper`, `article`, `documentation`, `clipping`, `transcript`, `note`, `data`, `book-chapter`, `thread` | `paper.json` | Source types — one page per source document |
| `skill` | `skill.json` | Agent skill with workflow instructions |
| `doc` | `doc.json` | Reference document |
| `section` | `section.json` | Section index grouping related pages |

One schema can serve multiple types (e.g. `paper.json` serves all 9
source types).

## Type discovery

Types are discovered automatically from `schemas/*.json` files. Each
schema declares which types it serves via `x-wiki-types`:

```json
"x-wiki-types": {
  "paper": "Academic source — research papers, preprints",
  "article": "Editorial source — blog posts, news, essays"
}
```

Resolution order:
1. Scan `schemas/*.json` → collect `x-wiki-types` entries
2. Read `[types.*]` from `wiki.toml` (if any)
3. `wiki.toml` entry wins over discovered entry

Common case: no `[types.*]` in `wiki.toml` — types are fully
discovered from schema files.

## Field aliasing

Different types use different field names for the same role. The
engine maps them via `x-index-aliases` in the schema:

```json
"x-index-aliases": {
  "name": "title",
  "description": "summary",
  "when_to_use": "read_when"
}
```

Aliases affect indexing only — files on disk are never rewritten.

## Graph edges

Each schema declares outgoing edges via `x-graph-edges`:

| Type | Field | Relation | Target types |
|------|-------|----------|--------------|
| concept | `sources` | `fed-by` | All source types |
| concept | `concepts` | `depends-on` | `concept` |
| source types | `sources` | `cites` | All source types |
| source types | `concepts` | `informs` | `concept` |
| doc | `sources` | `informed-by` | All source types |
| skill | `document_refs` | `documented-by` | `doc` |
| any | `superseded_by` | `superseded-by` | Any |

Body `[[wiki-links]]` get a generic `links-to` relation.

## Constraints

- A `default` type must always exist in the registry. If no schema
  declares it, the embedded `base.json` is used as fallback.
- A custom `base.json` must declare `default` in `x-wiki-types`.
- A custom `base.json` must require at least `title` and `type`
  fields (superset is fine, but cannot drop them).
- Pages without a `type` field default to `type: page`, validated
  against `default`.
- Pages with an unregistered type are validated against `default`.
- The `default` type cannot be removed.

## List registered types

```
wiki_schema(action: "list")
```

```json
[
  {
    "name": "concept",
    "description": "Synthesized knowledge — one concept per page",
    "schema_path": "schemas/concept.json"
  }
]
```

## Inspect a type schema

```
wiki_schema(action: "show", type: "<type>")
```

Returns the full JSON Schema for the given type.

## Get a frontmatter template

```
wiki_schema(action: "show", type: "<type>", template: true)
```

Returns a YAML frontmatter block with required fields filled with
placeholder values.

## Add a custom type

Drop a schema file into `schemas/` with `x-wiki-types` for automatic
discovery, or register explicitly:

```
wiki_schema(action: "add", type: "<type>", schema_path: "<path>")
```

A custom schema must be valid JSON Schema (Draft 2020-12) and should
include `x-wiki-types`. The engine validates, copies it into
`schemas/`, and confirms index resolution works.

Optionally add a body template at `schemas/<type>.md` — it will be
used by `wiki_content_new` when creating pages of this type.

## Remove a type

```
wiki_schema(action: "remove", type: "<type>")
```

The `default` type cannot be removed. Add `delete: true` to also
modify/delete the schema file. Add `delete_pages: true` to delete
page files from disk. Use `dry_run: true` to preview.

## Validate schemas

```
wiki_schema(action: "validate")
```

Validates all schema files. Pass `type: "<type>"` to validate a
single type. Checks: valid JSON Schema, `x-wiki-types` presence,
alias resolution, base schema invariant (`default` type requires
`title` and `type`), and full index compatibility.
