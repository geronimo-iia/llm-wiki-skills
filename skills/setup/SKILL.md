---
name: setup
description: >
  Install llm-wiki and manage wiki spaces. Create new wikis, set
  defaults, list and remove spaces. Use when the user says "set up",
  "install", "create a wiki", "add a wiki", "remove a wiki",
  "list wikis", or when llm-wiki is not yet installed.
type: skill
status: active
last_updated: "2025-07-18"
disable-model-invocation: true
argument-hint: "[create|list|remove] [--name <name>] [--path <path>]"
tags: [setup, install, spaces, configuration]
owner: geronimo
---

# Setup

Install the llm-wiki engine and manage wiki spaces.

## MCP tools used

- `wiki_spaces_create` — initialize a new wiki repo + register space
- `wiki_spaces_list` — list all registered wikis
- `wiki_spaces_remove` — remove a wiki from the registry
- `wiki_spaces_set_default` — set the default wiki
- `wiki_config` — read/write configuration values

## Steps

### 1. Check installation

Run `which llm-wiki` or `llm-wiki --help` to verify the binary is
available.

If not installed, guide the user:

- From source: `cargo install llm-wiki`
- From GitHub releases: download the binary for the user's platform

### 2. Create a wiki

```
wiki_spaces_create(path: "<path>", name: "<name>")
```

This initializes a git repository at `<path>` with the standard
directory structure (`inbox/`, `raw/`, `wiki/`, `schemas/`,
`wiki.toml`) and registers it in the global config.

Optional parameters:
- `description` — one-line description of the wiki's purpose
- `force` — update the space entry if the name already exists
- `set_default` — set this wiki as the default

### 3. Set as default

If this is the first wiki or the user wants it as default:

```
wiki_spaces_set_default(name: "<name>")
```

### 4. Verify

```
wiki_config(action: "list")
```

Confirm the wiki is registered and configuration is correct.

### 5. List existing wikis

```
wiki_spaces_list()
```

### 6. Remove a wiki

```
wiki_spaces_remove(name: "<name>")
```

Add `delete: true` to also delete the wiki directory from disk.

## Additional operations

- **Add a second wiki** — repeat step 2 with a different name and path.
- **Rename a wiki** — use `wiki_spaces_create` with `force: true` on
  the same path with the new name.
- **Directory structure** — every wiki has:
  - `inbox/` — drop zone for files to process
  - `raw/` — immutable archive of original sources
  - `wiki/` — compiled knowledge (where pages live)
  - `schemas/` — JSON Schema files for type validation
  - `wiki.toml` — per-wiki configuration and type registry
