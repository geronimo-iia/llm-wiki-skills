---
name: research
description: >
  Search the wiki and synthesize an answer from existing knowledge —
  full-text search, type filtering, cross-wiki search, graph
  exploration, and gap identification.
type: skill
status: active
last_updated: "2025-07-21"
when_to_use: >
  Answering a question from wiki knowledge, exploring what the wiki
  knows about a topic, or identifying knowledge gaps.
tags: [research, search, synthesis]
owner: jguibert@gmail.com
metadata:
  version: "0.2.0"
---

# Research

Search the wiki, read relevant pages, and synthesize an answer from
existing knowledge. The wiki is the persistent knowledge base — use it
before generating from scratch.

## Search

BM25 full-text search across `title`, `summary`, `read_when`, `tldr`,
`tags`, and body text:

```
wiki_search(query: "<topic>")
```

Filter by page type:

```
wiki_search(query: "<topic>", type: "concept")
wiki_search(query: "<topic>", type: "paper,article")
```

Search across all registered wikis:

```
wiki_search(query: "<topic>", cross_wiki: true)
```

Include section index pages (excluded by default):

```
wiki_search(query: "<topic>", include_sections: true)
```

## Read results

Read the most relevant pages:

```
wiki_content_read(uri: "<slug>")
```

Follow `sources` and `concepts` links in frontmatter to find related
pages that add context. A concept's `sources` field points to the
source pages that contributed claims. A source's `concepts` field
points to the concepts it informs.

## Explore relationships

Use the graph to explore how pages connect:

```
wiki_graph(root: "<slug>", depth: 2)
```

Filter by relation to trace specific edge types:

```
wiki_graph(root: "<slug>", relation: "fed-by")
wiki_graph(root: "<slug>", relation: "depends-on")
wiki_graph(type: "concept", relation: "depends-on")
```

This is useful for:
- Tracing which sources fed a concept (`fed-by`)
- Finding prerequisite concepts (`depends-on`)
- Seeing what a source informs (`informs`)

## Synthesize

Compose an answer from the wiki's knowledge:

- Cite sources with `wiki://` URIs (e.g. `wiki://concepts/moe`)
- Distinguish between what concept pages say (synthesized knowledge)
  and what source pages claim (provenance)
- Note confidence levels where available

## Identify gaps

Report what the wiki does not cover yet. This helps decide whether
to ingest new sources or crystallize new knowledge.

If the wiki has no relevant pages, say so clearly rather than
generating an answer from general knowledge.
