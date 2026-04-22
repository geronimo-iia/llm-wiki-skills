---
name: spaces
description: >
  Manage wiki spaces — create, list, inspect, remove, and switch
  the default wiki.
type: skill
status: active
last_updated: "2025-07-21"
when_to_use: >
  Creating an additional wiki, listing registered wikis, inspecting
  a wiki, removing a wiki, or changing the default wiki.
tags: [spaces, multi-wiki]
owner: jguibert@gmail.com
metadata:
  version: "0.1.0"
---

# Spaces

A space is a registered wiki repository. Each space has a name (used
in `wiki://` URIs), a local path, and an optional description. One
space is marked as the default — all commands target it unless
`--wiki <name>` is specified.

Use this skill to manage spaces after the initial setup.
When called from a running server, create, remove, and set-default
take effect immediately — no restart needed.

## Repository layout

Each space is a git repository with a fixed structure:

```
<path>/                     ← repository root
├── wiki.toml               ← wiki identity + config
├── schemas/                ← JSON Schema per page type
├── inbox/                  ← drop zone for files to process
├── raw/                    ← immutable archive of originals
└── wiki/                   ← compiled knowledge (wiki root)
```

Page slugs are relative to `<path>/wiki/`.

## List all wikis

```
wiki_spaces_list()
```

Returns all registered wikis with their paths and which is the
current default.

```json
[
  {
    "name": "research",
    "path": "/path/to/research",
    "description": "ML research knowledge base",
    "default": true
  }
]
```

## Inspect a specific wiki

```
wiki_spaces_list(name: "<name>")
```

Returns the same structure filtered to the requested wiki.
If the name is not found, returns an empty list.

```json
{
  "name": "research",
  "path": "/path/to/research",
  "description": "ML research knowledge base",
  "default": true
}
```

## Create a wiki

Ask the user for a name, path, and optional description.

```
wiki_spaces_create(path: "<path>", name: "<name>")
```

Add `set_default: true` only if the user wants to switch to it.

## Switch default wiki

```
wiki_spaces_set_default(name: "<name>")
```

## Remove a wiki

A wiki cannot be removed if it is the current default — switch
default first if needed.

```
wiki_spaces_remove(name: "<name>")
```

Add `delete: true` only if the user explicitly wants to delete the
local directory.
