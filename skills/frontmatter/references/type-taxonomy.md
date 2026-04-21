# Type Taxonomy

The `type` field carries both the epistemic role and the source nature.
Classify by the source material's nature, not its topic.

## Knowledge types

Pages the wiki synthesizes and maintains.

| Type | Schema | Description |
|------|--------|-------------|
| `concept` | `concept.json` | Synthesized knowledge — one concept per page |
| `query-result` | `concept.json` | Saved conclusion — crystallized sessions, comparisons |
| `section` | `section.json` | Section index page grouping related pages |

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

## Other types

| Type | Schema | Description |
|------|--------|-------------|
| `doc` | `doc.json` | Reference document — specifications, guides, standards |
| `skill` | `skill.json` | Agent skill with workflow instructions |
| `base` | `base.json` | Default fallback for unrecognized types |

## Per-type templates

### concept

```yaml
---
title: "Mixture of Experts"
summary: "Sparse routing of tokens to expert subnetworks."
tldr: "MoE reduces compute 8x at pre-training scale."
read_when:
  - "Reasoning about MoE architecture tradeoffs"
status: active
last_updated: "2025-07-18"
type: concept
tags: [mixture-of-experts, scaling, transformers]
sources: [sources/switch-transformer-2021]
concepts: [concepts/scaling-laws]
confidence: high
claims:
  - text: "Sparse MoE reduces effective compute 8x"
    confidence: high
    section: "Results"
---
```

Additional fields: `read_when` (required), `tldr`, `sources`,
`concepts`, `confidence`, `claims`.

### query-result

```yaml
---
title: "MoE Routing — Design Decision"
summary: "Expert-choice routing selected for inference pipeline."
tldr: "Expert-choice gives best quality/efficiency tradeoff above 10B."
read_when:
  - "Reviewing MoE routing decisions"
status: active
last_updated: "2025-07-18"
type: query-result
tags: [moe, routing, inference]
sources: [sources/switch-transformer-2021]
concepts: [concepts/mixture-of-experts]
confidence: medium
---
```

Same additional fields as concept.

### section

```yaml
---
title: "Scaling Research"
summary: "Papers and concepts related to model scaling."
type: section
status: active
last_updated: "2025-07-18"
---
```

No additional fields beyond base.

### paper

```yaml
---
title: "Switch Transformer (2021)"
summary: "Fedus et al. on scaling MoE to trillion parameters."
tldr: "Switch routing achieves 4x speedup over dense baselines."
read_when:
  - "Looking for MoE benchmark results"
status: active
last_updated: "2025-07-18"
type: paper
tags: [mixture-of-experts, switch-transformer, scaling]
concepts: [concepts/mixture-of-experts, concepts/scaling-laws]
confidence: high
claims:
  - text: "Switch routing achieves 4x speedup"
    confidence: high
    section: "Abstract"
---
```

Additional fields: `read_when`, `tldr`, `sources` (cites other
sources), `concepts` (informs), `confidence`, `claims`.

### article

```yaml
---
title: "Why MoE Models Are the Future"
summary: "Industry perspective on MoE adoption trends."
tldr: "MoE is becoming the default architecture for large-scale inference."
read_when:
  - "Understanding MoE industry adoption"
status: active
last_updated: "2025-07-18"
type: article
tags: [mixture-of-experts, industry, inference]
concepts: [concepts/mixture-of-experts]
confidence: medium
---
```

### documentation

```yaml
---
title: "vLLM — MoE Configuration"
summary: "Official vLLM docs on configuring MoE model serving."
read_when:
  - "Setting up MoE inference with vLLM"
status: active
last_updated: "2025-07-18"
type: documentation
tags: [vllm, moe, inference, configuration]
concepts: [concepts/mixture-of-experts]
confidence: high
---
```

### doc

```yaml
---
title: "Payment API Reference"
summary: "Endpoints, auth, error codes for the Payment API."
type: doc
status: active
last_updated: "2025-07-18"
tags: [api, payment]
sources: [sources/payment-rfc-2024]
---
```

Additional fields: `read_when`, `sources` (informed-by).

### skill

```yaml
---
name: ingest
description: >
  Process source files into synthesized wiki pages.
type: skill
status: active
last_updated: "2025-07-18"
disable-model-invocation: true
tags: [ingest, workflow]
owner: geronimo
---
```

Skill pages use `name`/`description` instead of `title`/`summary`.
The engine aliases them at ingest time (`name` → `title`,
`description` → `summary`, `when_to_use` → `read_when`).

Additional fields: `when_to_use`, `argument-hint`, `paths`,
`disable-model-invocation`, `user-invocable`, `allowed-tools`,
`context`, `agent`, `model`, `effort`, `document_refs`.

### Other source types

`clipping`, `transcript`, `note`, `data`, `book-chapter`, `thread`
all use the same schema as `paper`. Follow the paper template, changing
only the `type` field and adapting the title convention.

## Choosing a type

- **Synthesized knowledge?** → `concept`
- **Conclusion from a session?** → `query-result`
- **Summary of a specific source?** → pick the source type matching
  the material's nature
- **Section index?** → `section`
- **Reference document?** → `doc`
- **Agent workflow?** → `skill`

## Edge declarations by type

| Type | Field | Relation | Target types |
|------|-------|----------|-------------|
| concept | `sources` | `fed-by` | All source types |
| concept | `concepts` | `depends-on` | `concept` |
| source types | `sources` | `cites` | All source types |
| source types | `concepts` | `informs` | `concept` |
| doc | `sources` | `informed-by` | All source types |
| skill | `document_refs` | `documented-by` | `doc` |
| any | `superseded_by` | `superseded-by` | Any |
