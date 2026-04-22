---
name: frontmatter
description: >
  Reference for writing correct wiki frontmatter — required fields,
  field conventions, type-specific validation, and the accumulation
  contract.
type: skill
status: active
last_updated: "2025-07-21"
user-invocable: false
when_to_use: >
  Writing or updating wiki pages — loaded automatically as background
  reference for correct frontmatter fields and conventions.
tags: [frontmatter, reference, types]
owner: jguibert@gmail.com
metadata:
  version: "0.2.0"
---

# Frontmatter Reference

Background knowledge for writing correct frontmatter in wiki pages.
This skill is loaded automatically when writing wiki pages.

For type system management (listing, adding, removing types), see the
[schema](../schema/SKILL.md) skill. For the full type taxonomy, see
[references/type-taxonomy.md](references/type-taxonomy.md).

## Quick template

Get the exact frontmatter scaffold for any type:

```
wiki_schema(action: "show", type: "<type>", template: true)
```

## Required fields

Every wiki page must have:

| Field | Rule |
|-------|------|
| `title` | Concise, specific, unambiguous |
| `type` | Page type from the type registry |

Additional required fields depend on the type:

| Type | Extra required fields |
|------|----------------------|
| `concept`, `query-result` | `read_when` |
| `skill` | `name`, `description` (instead of `title`, `summary`) |

## Field conventions

### title

| Type | Convention | Example |
|------|-----------|---------| 
| `concept` | The concept name | "Mixture of Experts" |
| `paper` | "Paper Title (Year)" | "Switch Transformer (2021)" |
| `article` | "Article Title" | "Why MoE Models Are the Future" |
| `documentation` | "Product — Topic" | "vLLM — MoE Configuration" |
| `transcript` | "Event — Topic (Date)" | "Team Standup — MoE Decision (2025-07-15)" |
| `note` | Descriptive title | "Quick Notes on Routing Strategies" |
| `clipping` | Original title or descriptive | "Karpathy on LLM Wikis" |
| `book-chapter` | "Book Title — Chapter" | "Designing ML Systems — Ch. 8" |
| `thread` | "Forum — Topic" | "HN — MoE Scaling Discussion" |
| `data` | Descriptive title | "MoE Benchmark Results 2024" |
| `query-result` | "Topic — Aspect" | "MoE Routing — Design Decision" |
| `section` | The section name | "Scaling Research" |

Do not include the page type in the title ("Paper: Switch Transformer" ✗).

### summary vs tldr

- `summary` describes scope ("what is this page about?")
- `tldr` states the conclusion ("what's the bottom line?")

### read_when

Write as situations, not keywords:

```yaml
read_when:
  - "Reasoning about MoE architecture tradeoffs"
  - "Comparing sparse vs dense model scaling"
```

Not: `["MoE", "scaling", "routing"]` — that's what `tags` is for.

### tags

Flat list, lowercase, hyphenated:

```yaml
tags: [mixture-of-experts, scaling, transformers]
```

### sources

Slugs of source pages that actually contributed claims:

```yaml
sources: [sources/switch-transformer-2021]
```

### concepts

Slugs of concept pages this page directly discusses or depends on:

```yaml
concepts: [concepts/scaling-laws]
```

Apply the backlink quality test: would a reader benefit from navigating
there?

### confidence

| Value | When to use |
|-------|-------------|
| `high` | Multiple corroborating sources, well-established |
| `medium` | Single source, or sources with caveats |
| `low` | Preliminary, speculative, or contradicted |

Default to `medium`.

### claims

Structured claims extracted from sources:

```yaml
claims:
  - text: "Sparse MoE reduces effective compute 8x"
    confidence: high
    source: sources/switch-transformer-2021
    section: "Results"
```

### owner

Who is responsible — a person, team, or agent session ID.

### superseded_by

Slug of the page that replaces this one. Use when a page is
effectively replaced, not for minor updates. Creates a
`superseded-by` graph edge.

## Graph edges from frontmatter fields

Certain frontmatter fields create typed graph edges at ingest:

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

## Field aliasing

Skill pages use different field names. The engine aliases them at
ingest time so they index uniformly:

| Source field | Canonical field |
|-------------|----------------|
| `name` | `title` |
| `description` | `summary` |
| `when_to_use` | `read_when` |

Aliases affect indexing only — files on disk are never rewritten.

## Accumulation contract

When updating a page:

1. Read the current page first — `wiki_content_read`
2. Preserve existing list values — do not drop `tags`, `read_when`,
   `sources`, `concepts`, or `claims`
3. Add new values to lists, do not replace them
4. Update scalar fields only with clear reason
5. Write the complete file, then `wiki_ingest`

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Missing `title` | Engine rejects the file |
| Using `source-summary` as type | Pick specific source type |
| Missing `read_when` | Always include 2–5 retrieval conditions |
| Listing every related source | Only sources that contributed claims |
| Dropping existing tags on update | Read first, preserve existing values |
| Setting `confidence: high` without evidence | Default to `medium` |
| Classifying by topic instead of source nature | Blog about research → `article` |
