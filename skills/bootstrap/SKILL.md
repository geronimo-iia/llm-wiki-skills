---
name: bootstrap
description: >
  Orient to a wiki space — read configuration, understand types and
  structure, review hub pages.
type: skill
status: active
last_updated: "2026-04-26"
when_to_use: >
  At the start of a session, when switching wikis, or when
  orientation to a wiki's structure and content is needed.
tags: [bootstrap, session, orientation]
owner: jguibert@gmail.com
metadata:
  version: "0.3.0"
---

# Bootstrap

Bring the agent from zero to oriented using the wiki itself.

## Steps

### 1. Read configuration

```
wiki_config(action: "list")
```

Learn the wiki name, description, and key settings.

### 2. Discover types

```
wiki_schema(action: "list")
```

Learn what page types are registered. This tells you what kinds of
pages the wiki contains.

### 3. Get wiki composition

```
wiki_stats()
```

Returns page counts per type and status, orphan count, graph
connectivity, staleness distribution, and index health — all in
one call.

### 4. Get the section structure

```
wiki_list(type: "section", page_size: 50)
```

If no sections exist, the wiki is empty — report this to the user
and suggest using the ingest or write-page skills to start building
content.

### 5. Read hub pages

For each key section (up to 5), read its index page:

```
wiki_content_read(uri: "<section-slug>")
```

Prioritize sections with the most children or the most inbound links.
Skip this step if the wiki has no sections.

### 6. Report to the user

Present a brief orientation:

- The wiki's scope and purpose
- What knowledge domains exist (from sections)
- The current state (empty, sparse, well-developed) — use facets
  for page counts per type
- Any recent activity (check `last_updated` on hub pages)
