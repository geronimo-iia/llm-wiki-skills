# llm-wiki-skills

Skills for the [llm-wiki](https://github.com/geronimo-iia/llm-wiki) engine.

A Claude Code plugin that teaches agents how to use llm-wiki — ingest
sources, crystallize sessions, search knowledge, audit structure, and
more. Also usable by any agent platform that reads SKILL.md files.

## Prerequisites

The `llm-wiki` binary must be installed. The plugin starts the MCP
server (`llm-wiki serve`); the skills call the engine's tools.

```bash
cargo install llm-wiki
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

| Skill            | Invocation                 | Description                                             |
| ---------------- | -------------------------- | ------------------------------------------------------- |
| `setup`          | `/llm-wiki:setup`          | Install llm-wiki and manage wiki spaces                 |
| `bootstrap`      | Auto (session start)       | Orient to a wiki — read config, types, hub pages        |
| `ingest`         | `/llm-wiki:ingest`         | Process source files into synthesized wiki pages        |
| `crystallize`    | `/llm-wiki:crystallize`    | Distil the current session into durable wiki pages      |
| `research`       | Auto + manual              | Search the wiki and synthesize an answer                |
| `lint`           | `/llm-wiki:lint`           | Structural audit — orphans, stubs, broken links         |
| `graph`          | `/llm-wiki:graph`          | Generate and interpret the concept graph                |
| `frontmatter`    | Auto (background)          | Reference for writing correct frontmatter               |
| `skill`          | Auto + manual              | Find and activate skills stored in the wiki             |
| `write-page`     | `/llm-wiki:write-page`     | Create a wiki page of any type with correct frontmatter |
| `configure-hugo` | `/llm-wiki:configure-hugo` | Configure a wiki for Hugo rendering                     |

## How Skills Relate to MCP Tools

The engine exposes 15 MCP tools — stateful primitives for space
management, content operations, search, and graph traversal. Skills
orchestrate these tools into multi-step workflows.

| Tool group       | Tools                                                                                              | Used by skills                                            |
| ---------------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Space management | `wiki_spaces_create`, `wiki_spaces_list`, `wiki_spaces_remove`, `wiki_spaces_set_default`          | setup, bootstrap                                          |
| Configuration    | `wiki_config`                                                                                      | setup, bootstrap, frontmatter, write-page, configure-hugo |
| Content          | `wiki_content_read`, `wiki_content_write`, `wiki_content_new`, `wiki_content_commit`               | ingest, crystallize, lint, write-page                     |
| Search & index   | `wiki_search`, `wiki_list`, `wiki_ingest`, `wiki_graph`, `wiki_index_rebuild`, `wiki_index_status` | All skills                                                |

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

[MIT](http://opensource.org/licenses/MIT) OR
[Apache-2.0](http://www.apache.org/licenses/LICENSE-2.0)


## Futur improvement

- transform the layout as a llm-wiki
- create knowledge about llm-wiki, epistemologic model, etc
- extend skill with automatic usage of the search engine
