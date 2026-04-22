# Type Taxonomy

The `type` field carries the epistemic role. Classify by the source
material's nature, not its topic.

Get a frontmatter template for any type:

```
wiki_schema(action: "show", type: "<type>", template: true)
```

## Knowledge types

Pages the wiki synthesizes and maintains.

| Type | Schema | Description |
|------|--------|-------------|
| `concept` | `concept.json` | Synthesized knowledge — one concept per page |
| `query-result` | `concept.json` | Saved conclusion — crystallized sessions, comparisons |
| `section` | `section.json` | Section index page grouping related pages |

### concept / query-result

Additional fields: `read_when` (required), `tldr`, `sources`,
`concepts`, `confidence`, `claims`.

Graph edges:

| Field | Relation | Target types |
|-------|----------|--------------|
| `sources` | `fed-by` | All source types |
| `concepts` | `depends-on` | `concept` |
| `superseded_by` | `superseded-by` | Any |

### section

No additional fields beyond base. Excluded from search results by
default (`--include-sections` to include them).

## Source types

Pages that record what a specific source claims. One page per source.

| Type | Schema | Source nature |
|------|--------|-------------|
| `paper` | `paper.json` | Academic — research papers, preprints |
| `article` | `paper.json` | Editorial — blog posts, news, essays |
| `documentation` | `paper.json` | Reference — product docs, API references |
| `clipping` | `paper.json` | Web capture — browser clips, bookmarks |
| `transcript` | `paper.json` | Spoken — meeting transcripts, podcasts |
| `note` | `paper.json` | Informal — freeform drafts, quick captures |
| `data` | `paper.json` | Structured — CSV, JSON, datasets |
| `book-chapter` | `paper.json` | Published — book excerpts |
| `thread` | `paper.json` | Discussion — forum threads, social media |

Additional fields: `read_when`, `tldr`, `sources` (cites other
sources), `concepts` (informs), `confidence`, `claims`.

Graph edges:

| Field | Relation | Target types |
|-------|----------|--------------|
| `sources` | `cites` | All source types |
| `concepts` | `informs` | `concept` |
| `superseded_by` | `superseded-by` | Any |

## Doc type

Reference document — specifications, guides, standards.

| Type | Schema | Description |
|------|--------|-------------|
| `doc` | `doc.json` | Reference document with document authority |

Additional fields: `read_when`, `sources`.

Graph edges:

| Field | Relation | Target types |
|-------|----------|--------------|
| `sources` | `informed-by` | All source types |
| `superseded_by` | `superseded-by` | Any |

## Skill type

Agent skill with workflow instructions. Uses `name`/`description`
instead of `title`/`summary` (aliased at ingest).

| Type | Schema | Description |
|------|--------|-------------|
| `skill` | `skill.json` | Agent skill with workflow instructions |

Additional fields: `when_to_use`, `argument-hint`, `paths`,
`disable-model-invocation`, `user-invocable`, `allowed-tools`,
`context`, `agent`, `model`, `effort`, `document_refs`.

Graph edges:

| Field | Relation | Target types |
|-------|----------|--------------|
| `document_refs` | `documented-by` | `doc` |
| `superseded_by` | `superseded-by` | Any |

## Base type

| Type | Schema | Description |
|------|--------|-------------|
| `default` | `base.json` | Fallback for unrecognized or missing types |

No graph edges beyond `superseded_by`.

## Choosing a type

- Synthesized knowledge? → `concept`
- Conclusion from a session? → `query-result`
- Summary of a specific source? → pick the source type matching
  the material's nature
- Section index? → `section`
- Reference document? → `doc`
- Agent workflow? → `skill`
