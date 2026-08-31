---
name: config
description: >
  Read, write, and understand wiki configuration — global defaults,
  per-wiki overrides, and resolution order.
type: skill
status: active
last_updated: "2026-07-23"
when_to_use: >
  Reading or changing configuration, understanding what settings
  are available, or troubleshooting unexpected behavior caused by
  config values.
tags: [config, settings, configuration]
owner: jguibert@gmail.com
compatibility: "llm-wiki >= 1.0.0"
---

# Config

Two configuration files control llm-wiki behavior:

- `~/.llm-wiki/config.toml` — global engine config (local to the
  machine, never committed). Override the path with `--config <path>`
  or the `LLM_WIKI_CONFIG` environment variable.
- `<wiki>/wiki.toml` — per-wiki config (committed to git, shared)

## Config file location

```
1. --config <path> CLI flag        (highest)
2. LLM_WIKI_CONFIG env var
3. ~/.llm-wiki/config.toml         (default)
```

The `--config` flag is global — it works on every subcommand including
`serve`. Use it in `.mcp.json` to run isolated environments:

```json
{
  "llm-wiki": {
    "command": "llm-wiki",
    "args": ["--config", "/path/to/config.toml", "serve"]
  }
}
```

Or via `env`:

```json
{
  "llm-wiki": {
    "command": "llm-wiki",
    "args": ["serve"],
    "env": { "LLM_WIKI_CONFIG": "/path/to/config.toml" }
  }
}
```

## Resolution order (settings within the config)

```
1. CLI flag / MCP parameter
2. Per-wiki config   (wiki.toml)
3. Global config     (config.toml)
4. Built-in default
```

Per-wiki wins over global. CLI flags win over everything.

## wiki.toml

Lives at the wiki repository root. Contains wiki identity and
optional per-wiki overrides.

```toml
name        = "research"
description = "ML research knowledge base"

[ingest]
auto_commit = true

[validation]
type_strictness = "loose"
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Wiki name — used in `wiki://` URIs |
| `description` | no | One-line description |

Type overrides (`[types.*]`) are also declared here but managed
through the [schema](../schema/SKILL.md) skill.

## List current config

```
wiki_config(action: "list")
```

Returns all resolved config values for the default wiki.

```json
{
  "defaults.search_top_k": 10,
  "defaults.page_mode": "flat",
  "ingest.auto_commit": true,
  "validation.type_strictness": "loose"
}
```

## Read a config value

```
wiki_config(action: "get", key: "defaults.search_top_k")
```

## Set a config value

Per-wiki (writes to `wiki.toml`):

```
wiki_config(action: "set", key: "ingest.auto_commit", value: "false")
```

Global (writes to `config.toml`):

```
wiki_config(action: "set", key: "defaults.search_top_k", value: "15", global: true)
```

Global-only keys reject per-wiki writes with an error.

## Overridable settings

These keys can appear in both `config.toml` and `wiki.toml`.

| Key | Default | Description |
|-----|---------|-------------|
| `defaults.search_top_k` | `10` | Default result count for search |
| `defaults.search_excerpt` | `true` | Include excerpts in search results |
| `defaults.search_sections` | `false` | Include section pages in search |
| `defaults.page_mode` | `flat` | Default page creation mode: `flat` or `bundle` |
| `defaults.list_page_size` | `20` | Default page size for list |
| `defaults.output_format` | `text` | Default output format: `text` or `json` |
| `read.no_frontmatter` | `false` | Strip frontmatter from read output |
| `ingest.auto_commit` | `true` | Commit to git after ingest |
| `validation.type_strictness` | `loose` | `strict`: unknown type is error; `loose`: warning |
| `graph.format` | `mermaid` | Graph output format: `mermaid`, `dot`, `json`, or `llms` |
| `graph.depth` | `3` | Default hop limit for graph traversal |
| `graph.type` | `[]` | Page types to include; empty = all |
| `graph.output` | `""` | Default output path; empty = stdout |
| `graph.snapshot` | `true` | Persist graph to disk for warm-start across restarts |
| `graph.snapshot_format` | `bincode+lz4` | Snapshot serialization format: `bincode+lz4` or `bincode+zstd` |
| `graph.structural_algorithms` | `true` | Enable diameter/radius/center in `wiki_stats`; `false` skips O(n²) |
| `graph.max_nodes_for_diameter` | `2000` | Skip structural algorithms when local node count exceeds this |
| `graph.min_nodes_for_communities` | `30` | Minimum pages before Louvain community detection runs |
| `search.status.<key>` | — | Override search weight for a status value; key is a status slug (e.g. `active`, `draft`), value is a float |
| `index.memory_budget_mb` | `50` | Tantivy writer memory budget in MB |
| `index.tokenizer` | `en_stem` | Tantivy tokenizer for text fields |

## Search status weights

Control how much each status value contributes to search ranking.
Higher weight = pages with that status rank higher in results.

```
wiki_config(action: "set", key: "search.status.active", value: "1.2")
wiki_config(action: "set", key: "search.status.draft", value: "0.3")
wiki_config(action: "set", key: "search.status.archived", value: "0.1")
```

Custom status values defined in your schemas work the same way:

```
wiki_config(action: "set", key: "search.status.accepted", value: "1.5")
```

Per-wiki overrides take precedence over global values — use them when a
wiki has a domain-specific status taxonomy (e.g. ADR `accepted`/`superseded`).

## Global-only settings

These keys can only appear in `config.toml`. Setting them in
`wiki.toml` is rejected.

| Key | Default | Description |
|-----|---------|-------------|
| `index.auto_rebuild` | `false` | Rebuild stale index before search/list |
| `index.auto_recovery` | `true` | Rebuild corrupt index on open failure |
| `serve.http` | `false` | Enable HTTP transport |
| `serve.http_port` | `8080` | HTTP port |
| `serve.http_allowed_hosts` | `localhost,127.0.0.1,::1` | Allowed Host headers |
| `serve.acp` | `false` | Enable ACP transport |
| `serve.max_restarts` | `10` | Max transport restarts; `0` = no restart |
| `serve.restart_backoff` | `1` | Initial backoff seconds; doubles, cap 30s |
| `serve.heartbeat_secs` | `60` | Heartbeat interval; `0` = disabled |
| `serve.acp_max_sessions` | `20` | Max concurrent ACP sessions; `NewSession` returns error when exceeded |
| `logging.log_path` | `~/.llm-wiki/logs` | Log file directory; empty = stderr only |
| `logging.log_rotation` | `daily` | `daily`, `hourly`, `never` |
| `logging.log_max_files` | `7` | Max rotated files; `0` = unlimited |
| `logging.log_format` | `text` | `text` or `json` |
| `watch.debounce_ms` | `500` | Filesystem watcher debounce interval in ms |
