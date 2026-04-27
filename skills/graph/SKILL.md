---
name: graph
description: >
  Generate and interpret the wiki's concept graph — typed nodes,
  labeled edges, relation filtering, and subgraph extraction.
type: skill
status: active
last_updated: "2026-04-27"
disable-model-invocation: false
argument-hint: "[--type concept] [--root slug] [--depth N] [--relation fed-by]"
when_to_use: >
  Visualizing wiki structure, exploring relationships between pages,
  identifying orphans or gaps, or verifying graph integrity after
  content changes.
tags: [graph, visualization, structure, edges]
owner: jguibert@gmail.com
metadata:
  version: "0.4.0"
---

# Graph

The concept graph is built from the tantivy index — no file reads.
Nodes are typed (by page `type`), edges are labeled (by `x-graph-edges`
relation declarations in type schemas).

Edges come from two sources:
- Frontmatter fields (`sources`, `concepts`, `document_refs`,
  `superseded_by`) — typed edges with relation labels
- Body `[[wikilinks]]` — generic `links-to` edges

Only pages that exist in the index are included. Broken references
are silently skipped.

## Edge system

The same frontmatter field has different relation labels depending on
the page type. The engine reads `x-graph-edges` from the type's JSON
Schema to determine the label.

| Page type | Field | Relation | Target types |
|-----------|-------|----------|--------------|
| concept | `sources` | `fed-by` | All source types |
| concept | `concepts` | `depends-on` | `concept` |
| source types | `sources` | `cites` | All source types |
| source types | `concepts` | `informs` | `concept` |
| doc | `sources` | `informed-by` | All source types |
| skill | `document_refs` | `documented-by` | `doc` |
| any | `superseded_by` | `superseded-by` | Any |
| any | `[[wikilinks]]` | `links-to` | Any |

Edge target type constraints are declared in `x-graph-edges` via
`target_types`. The engine warns at ingest when an edge target has
the wrong type.

## Generate the graph

```
wiki_graph()
```

Output format is `mermaid` (default), `dot`, or `llms`:

```
wiki_graph(format: "mermaid")
wiki_graph(format: "dot")
wiki_graph(format: "llms")
```

Mermaid output can be rendered directly in Markdown code blocks.
Relation labels appear on edges. Node types map to CSS classes.

`format: "llms"` produces a natural language description of the graph
structure: node counts by type, top hubs by degree, edge relation
counts, and isolated nodes — directly readable without a renderer.
Use it when the goal is interpretation, not visualization.

## Filter the graph

Filters compose — combine any of them:

```
wiki_graph(type: "concept")
wiki_graph(relation: "fed-by")
wiki_graph(root: "<slug>", depth: 2)
wiki_graph(type: "concept", relation: "depends-on", root: "concepts/moe", depth: 2)
```

| Filter | Effect |
|--------|--------|
| `type` | Include only nodes of these types (comma-separated) |
| `relation` | Include only edges with this relation label |
| `root` | Subgraph starting from this node |
| `depth` | Hop limit from root (default from config) |

| `root` | `depth` | Behavior |
|--------|---------|----------|
| not set | not set | Full graph, all nodes |
| not set | N | Full graph, edges within N hops of any node |
| set | not set | Subgraph from root, default depth from config |
| set | N | Subgraph from root, N hops |

**Unified cross-wiki graph:**
```
wiki_graph(cross_wiki: true)
```
Merges all mounted wikis into a single graph. Each node is prefixed with its
wiki name for disambiguation. Cross-wiki edges appear as resolved connections.

**Single-wiki with cross-wiki targets:**
Without `cross_wiki: true`, pages linking to other wikis produce external
placeholder nodes — visually distinct (dashed border in Mermaid/DOT) — showing
that the link exists but the target lives in another space.

## Interpret the graph

For structural interpretation, use `format: "llms"` to get a natural
language summary of the graph without requiring you to parse Mermaid:

```
wiki_graph(format: "llms")
```

The output surfaces clusters (nodes grouped by type), key hubs (by
degree), edge relation counts, and isolated nodes directly. Use it
when the goal is analysis rather than visualization.

For a renderable diagram (Mermaid, DOT), use the default format:

```
wiki_graph()
```

Analyze the graph structure for:

- **Clusters** — groups of tightly connected pages (knowledge domains)
- **Isolated nodes** — pages with no connections (potential orphans)
- **Key hubs** — pages with high degree (important concepts)
- **Bridge nodes** — pages connecting otherwise separate clusters
- **Missing edges** — concepts that should be linked but aren't

## Suggest improvements

Based on the analysis:

- Missing links between related concepts
- Orphan pages that should connect to the main graph
- Overly connected hub pages that might need splitting
- Clusters that lack a section index page
- Edge target type mismatches (concept linking to wrong type)
