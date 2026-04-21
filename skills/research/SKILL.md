---
name: research
description: >
  Search the wiki and synthesize an answer from existing knowledge.
  Use when the user asks a question that the wiki might answer,
  wants to know what the wiki says about a topic, or needs a
  summary of existing knowledge.
type: skill
status: active
last_updated: "2025-07-18"
tags: [research, search, synthesis]
owner: geronimo
---

# Research

Search the wiki, read relevant pages, and synthesize an answer from
existing knowledge. The wiki is the persistent knowledge base — use it
before generating from scratch.

## MCP tools used

- `wiki_search` — full-text BM25 search with optional type filter
- `wiki_content_read` — read full page content

## Steps

### 1. Search

```
wiki_search(query: "<user's question or topic>")
```

Use the user's natural language query. The BM25 engine matches against
`title`, `summary`, `read_when`, `tldr`, `tags`, and body text.

For targeted searches, add a type filter:

```
wiki_search(query: "<query>", type: "concept")
wiki_search(query: "<query>", type: "paper,article")
```

### 2. Read top results

```
wiki_content_read(uri: "<slug>")
```

Read the most relevant pages. Follow `sources` and `concepts` links
in frontmatter to find related pages that add context.

### 3. Synthesize

Compose an answer from the wiki's knowledge:

- Cite sources with `wiki://` URIs (e.g., `wiki://concepts/moe`)
- Distinguish between what concept pages say (synthesized knowledge)
  and what source pages claim (provenance)
- Note confidence levels where available

### 4. Note gaps

Report what the wiki does not cover yet. This helps the user decide
whether to ingest new sources or crystallize new knowledge.

If the wiki has no relevant pages, say so clearly rather than
generating an answer from general knowledge.
