---
name: graph
description: >
  Generate and interpret the wiki's concept graph. Show
  relationships between pages, identify clusters and gaps.
  Use when the user says "graph", "show connections",
  "visualize", or "map the wiki".
type: skill
status: active
last_updated: "2025-07-18"
disable-model-invocation: true
argument-hint: "[--type concept] [--root slug] [--depth N]"
tags: [graph, visualization, structure]
owner: geronimo
---

# Graph

Generate and interpret the wiki's concept graph. The graph is built
from frontmatter link fields (`sources`, `concepts`, `superseded_by`)
and body `[[wikilinks]]`, with typed edges from the schema's
`x-graph-edges` declarations.

## MCP tools used

- `wiki_graph` — generate the graph in Mermaid or DOT format
- `wiki_content_read` — read specific pages for context

## Steps

### 1. Generate the graph

```
wiki_graph()
```

Optional filters:

```
wiki_graph(format: "mermaid")
wiki_graph(type: "concept")
wiki_graph(root: "<slug>", depth: 2)
wiki_graph(relation: "fed-by")
```

Parameters:
- `format` — `mermaid` (default) or `dot`
- `root` — start from a specific node (slug)
- `depth` — hop limit from root
- `type` — comma-separated page types to include
- `relation` — filter edges by relation label
- `output` — file path for output

### 2. Present the output

Show the Mermaid or DOT output. For Mermaid, the output can be
rendered directly in Markdown code blocks.

### 3. Interpret the graph

Analyze the graph structure:

- **Clusters** — groups of tightly connected pages (knowledge domains)
- **Isolated nodes** — pages with no connections (potential orphans)
- **Key hubs** — pages with high degree (important concepts)
- **Bridge nodes** — pages connecting otherwise separate clusters
- **Missing edges** — concepts that should be linked but aren't

### 4. Suggest improvements

Based on the analysis:

- Missing links between related concepts
- Orphan concepts that should connect to the main graph
- Overly connected hub pages that might need splitting
- Clusters that lack a section index page

## Edge types

The graph uses typed edges from `x-graph-edges` in type schemas:

| Relation | Meaning |
|----------|---------|
| `fed-by` | Concept ← Source (source contributed claims) |
| `depends-on` | Concept → Concept (prerequisite knowledge) |
| `informs` | Source → Concept (source informs a concept) |
| `cites` | Source → Source (citation) |
| `informed-by` | Doc ← Source (doc informed by source) |
| `documented-by` | Skill → Doc (skill documented by doc) |
| `superseded-by` | Any → Any (page replaced by another) |
| `links-to` | Any → Any (body `[[wikilink]]`) |
