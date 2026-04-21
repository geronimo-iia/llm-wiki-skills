---
name: bootstrap
description: >
  Orient to a wiki space. Read configuration, understand types and
  structure, review hub pages. Use at the start of every session or
  when switching wikis.
type: skill
status: active
last_updated: "2025-07-18"
tags: [bootstrap, session, orientation]
owner: geronimo
---

# Bootstrap

Session orientation — bring the agent from zero to oriented using the
wiki itself. Run at the start of every session or when switching wikis.

## MCP tools used

- `wiki_config` — read wiki name, description, settings
- `wiki_schema` — list registered types and their descriptions
- `wiki_list` — get the section structure
- `wiki_content_read` — read hub pages for context

## Steps

### 1. Read configuration

```
wiki_config(action: "list")
```

Learn the wiki name, description, and key settings
(`ingest.auto_commit`, `search.top_k`).

### 2. Discover types

```
wiki_schema(action: "list")
```

Learn what page types are registered, their descriptions, and which
schema files they use. This tells you what kinds of pages the wiki
contains.

### 2. Get the section structure

```
wiki_list(type: "section", page_size: 50)
```

Sections are the wiki's organizational skeleton. Understanding them
reveals what knowledge domains exist.

### 3. Read hub pages

For each key section, read its index page:

```
wiki_content_read(uri: "<section-slug>")
```

Hub pages summarize an entire area of knowledge. They are the most
valuable bootstrap targets because they provide context for everything
underneath.

Prioritize sections with the most children or the most inbound links.

### 4. Summarize

After reading config and hub pages, summarize:

- The wiki's scope and purpose
- What knowledge domains exist
- The current state of each domain (active, sparse, well-developed)
- Any recent activity (check `last_updated` on hub pages)

## The bootstrap loop

Each session starts from a richer baseline than the last. The
crystallize skill feeds back into bootstrap — every crystallized
session updates hub pages, making the next bootstrap richer.

```
Session N:   bootstrap → work → crystallize → hub pages updated
Session N+1: bootstrap → richer starting context → ...
```

The wiki is the accumulator. The agent is stateless — the wiki is not.
