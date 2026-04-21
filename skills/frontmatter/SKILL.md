---
name: frontmatter
description: >
  Reference for writing correct wiki frontmatter. Covers required
  fields, type conventions, per-type templates, and the accumulation
  contract. Use when writing or updating wiki pages.
type: skill
status: active
last_updated: "2025-07-18"
user-invocable: false
tags: [frontmatter, reference, types]
owner: geronimo
---

# Frontmatter Reference

Background knowledge for writing correct frontmatter in wiki pages.
This skill is loaded automatically when writing wiki pages.

## Required fields

Every wiki page must have:

```yaml
---
title: "Page Title"
summary: "One sentence describing the page's scope."
read_when:
  - "Situation when this page should be retrieved"
status: active
last_updated: "2025-07-18"
type: concept
---
```

| Field | Rule |
|-------|------|
| `title` | Concise, specific, unambiguous |
| `summary` | One sentence: what this page is about |
| `read_when` | 2–5 retrieval conditions (situations, not keywords) |
| `status` | `active` for new pages, `draft` for incomplete work |
| `last_updated` | Today's ISO 8601 date |
| `type` | Page type from the type registry (see type-taxonomy.md) |

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
effectively replaced, not for minor updates.

## Type-specific validation

The engine validates frontmatter against JSON Schema per type on
`wiki_ingest`. Each type has required fields beyond the base:

| Type | Required fields | Schema |
|------|----------------|--------|
| `concept`, `query-result` | `title`, `type`, `read_when` | `concept.json` |
| `skill` | `name`, `description`, `type` | `skill.json` |
| All source types | `title`, `type` | `paper.json` |
| `doc` | `title`, `type` | `doc.json` |
| `section` | `title`, `type` | `section.json` |

Use `wiki_schema show <type> --template` to get the exact frontmatter
scaffold for any type. Use `wiki_schema list` to see all registered
types.

Skill pages use `name`/`description` instead of `title`/`summary`.
The engine aliases them at ingest time (`name` → `title`,
`description` → `summary`, `when_to_use` → `read_when`).

## Per-type templates

Get a template for any type:

```
wiki_schema(action: "show", type: "<type>", template: true)
```

See also `references/type-taxonomy.md` for the full type taxonomy.

## Accumulation contract

When updating a page:

1. **Read the current page first** — `wiki_content_read`
2. **Preserve existing list values** — do not drop `tags`, `read_when`,
   `sources`, `concepts`, or `claims`
3. **Add new values** to lists, do not replace them
4. **Update scalar fields** only with clear reason
5. **Write the complete file**, then `wiki_ingest`

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
