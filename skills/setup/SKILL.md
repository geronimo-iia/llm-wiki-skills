---
name: setup
description: >
  Install llm-wiki and create the first wiki. Use when llm-wiki is
  not yet installed or needs initial setup.
type: skill
status: active
last_updated: "2025-07-18"
disable-model-invocation: true
argument-hint: "[--name <name>] [--path <path>]"
when_to_use: >
  Installing llm-wiki for the first time, or creating the initial
  wiki.
tags: [setup, install]
owner: jguibert@gmail.com
metadata:
  version: "0.4.0"
---

# Setup

Install the llm-wiki engine and create the first wiki. All steps use
**CLI commands only** — MCP tools are not available until the engine
is installed and serving.

## Steps

### 1. Check installation

```bash
which llm-wiki && llm-wiki --version
```

If not installed, pick one method
([full guide](https://github.com/geronimo-iia/llm-wiki/blob/main/docs/guides/installation.md)):

| Method                      | Command                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Quick install (macOS/Linux) | `curl -fsSL https://raw.githubusercontent.com/geronimo-iia/llm-wiki/main/install.sh \| bash`                 |
| Quick install (Windows)     | `irm https://raw.githubusercontent.com/geronimo-iia/llm-wiki/main/install.ps1 \| iex`                        |
| Homebrew                    | `brew tap geronimo-iia/tap && brew install llm-wiki`                                                         |
| asdf                        | `asdf plugin add llm-wiki https://github.com/geronimo-iia/asdf-llm-wiki.git && asdf install llm-wiki latest` |
| Cargo (from source)         | `cargo install llm-wiki`                                                                                     |
| Cargo (pre-built)           | `cargo binstall llm-wiki`                                                                                    |

### 2. Create the first wiki

Determine the wiki name and description from the conversation context
(project name, topic, stated purpose). If unclear, ask the user for
a short name and one-line description.

```bash
llm-wiki spaces create <path> --name <name> --set-default
```

This initializes a git repo with the standard layout (`inbox/`,
`raw/`, `wiki/`, `schemas/`, `wiki.toml`) and registers it as the
default wiki.

### 3. Verify

```bash
llm-wiki spaces list
llm-wiki schema list
```

The MCP plugin (`.mcp.json`) starts `llm-wiki serve` automatically —
MCP tools become available in the next agent session.

To manage additional wikis later, see the [spaces](../spaces/SKILL.md) skill.
