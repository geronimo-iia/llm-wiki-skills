# llm-wiki-skills

Skills for the [llm-wiki](https://github.com/geronimo-iia/llm-wiki) engine.

A Claude Code plugin that teaches agents how to use llm-wiki — manage
spaces, ingest sources, crystallize sessions, search knowledge, audit
structure, and more. Also usable by any agent platform that reads
SKILL.md files.

## Prerequisites

The `llm-wiki` binary must be installed. The plugin starts the MCP
server (`llm-wiki serve`); the skills call the engine's tools.

```bash
cargo install llm-wiki-engine
```

Or download a binary from
[GitHub releases](https://github.com/geronimo-iia/llm-wiki/releases).

## Installation

### Claude marketplace

```bash
claude plugin add llm-wiki-skills
```

### Direct from GitHub

```bash
claude plugin add https://github.com/geronimo-iia/llm-wiki-skills
```

### Local development

```bash
claude --plugin-dir ./llm-wiki-skills
```

## Skill Inventory

| Skill             | Invocation                 | Description                                             |
| ----------------- | -------------------------- | ------------------------------------------------------- |
| `setup`           | `/llm-wiki:setup`          | Install llm-wiki and create the first wiki              |
| `spaces`          | `/llm-wiki:spaces`         | Manage wiki spaces — create, list, inspect, remove      |
| `config`          | `/llm-wiki:config`         | Read, write, and understand wiki configuration          |
| `schema`          | `/llm-wiki:schema`         | Understand and manage the type system                   |
| `bootstrap`       | Auto (session start)       | Orient to a wiki — read config, types, hub pages        |
| `content`         | `/llm-wiki:content`        | Read, create, update pages and sections                 |
| `ingest`          | `/llm-wiki:ingest`         | Process source files into synthesized wiki pages        |
| `crystallize`     | Auto + manual              | Distil the current session into durable wiki pages      |
| `research`        | Auto + manual              | Search the wiki and synthesize an answer                |
| `lint`            | `/llm-wiki:lint`           | Audit quality — orphans, broken links, schema integrity |
| `graph`           | `/llm-wiki:graph`          | Generate and interpret the concept graph                |
| `frontmatter`     | Auto (background)          | Reference for writing correct frontmatter               |
| `configure-hugo`  | `/llm-wiki:configure-hugo` | Configure a wiki for Hugo rendering                     |
| `stats`           | `/llm-wiki:stats`          | Wiki health dashboard — interpret metrics and triage    |
| `export`          | `/llm-wiki:export`         | Export wiki to llms.txt, llms-full, or JSON             |

## How Skills Relate to MCP Tools

The engine exposes MCP tools — stateful primitives for space
management, content operations, search, and graph traversal. Skills
orchestrate these tools into workflows.

| Tool group       | Tools                                                                                                          | Used by skills                             |
| ---------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Space management | `wiki_spaces_create`, `wiki_spaces_list`, `wiki_spaces_remove`, `wiki_spaces_set_default`, `wiki_spaces_register` | setup, spaces, ingest                      |
| Configuration    | `wiki_config`                                                                                                     | config, bootstrap, configure-hugo          |
| Schema           | `wiki_schema`                                                                                                     | schema, frontmatter, content, ingest, lint |
| Content          | `wiki_content_read`, `wiki_content_write`, `wiki_content_new`, `wiki_content_commit`                              | content, ingest, crystallize, lint         |
| Search & index   | `wiki_search`, `wiki_list`, `wiki_ingest`, `wiki_index_rebuild`, `wiki_index_status`                              | research, content, ingest, lint            |
| Graph            | `wiki_graph`                                                                                                      | graph, research, lint, crystallize         |
| Knowledge        | `wiki_stats` (health + structural topology), `wiki_suggest`, `wiki_history`                                       | content, research, bootstrap, lint, stats  |
| Resolve          | `wiki_resolve`                                                                                                    | content, ingest                            |
| Export           | `wiki_export`                                                                                                     | export                                     |

The engine is a dumb pipe. Skills are the brain.

## Non-Claude Agents

Clone this repo and read `skills/*/SKILL.md` directly. The skills
follow the [agentskills.io](https://agentskills.io) compatible format
and work with any agent platform that reads Markdown skill files.

| Agent platform    | How to use                                      |
| ----------------- | ----------------------------------------------- |
| Claude Code       | Install as plugin (see above)                   |
| Cursor / Windsurf | MCP tools + read SKILL.md files as prompts      |
| Custom agents     | MCP tools + parse SKILL.md frontmatter and body |
| CLI scripts       | `llm-wiki` CLI commands directly                |

## License

[MIT](LICENSE-MIT) OR [Apache-2.0](LICENSE-APACHE)

## Future improvements

See [docs/roadmap.md](docs/roadmap.md).

