---
name: bootstrap
description: >
  Orient to a wiki space — read configuration, understand types and
  structure, review hub pages.
type: skill
status: active
last_updated: "2026-08-20"
when_to_use: >
  At the start of a session, when switching wikis, or when
  orientation to a wiki's structure and content is needed.
tags: [bootstrap, session, orientation]
owner: jguibert@gmail.com
compatibility: "llm-wiki >= 1.0.0"
---

# Bootstrap

Bring the agent from zero to oriented using the wiki itself.

## Steps

### 0. Check server identity and index health

```
wiki_info()
```

Returns server version, registered spaces, default wiki, and index
health. `index_status` is either `"ok"` (all wikis healthy) or an
object keyed by wiki name when any wiki is degraded:

```json
{
  "research": {"status": "ok"},
  "notes": {"status": "degraded", "reason": "..."}
}
```

If `index_status` is not the string `"ok"`, warn the user before
proceeding: the affected wiki's index may be incomplete or stale, so
stats and search results could be unreliable. Call
`wiki_index_status(wiki: "<name>")` for details, then
`wiki_index_rebuild(wiki: "<name>")` to recover.

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
  for page counts per type (`type`, `status`, `tags` are keyword
  FAST fields; counts come at no extra cost)
- Any recent activity (check `last_updated` on hub pages)
