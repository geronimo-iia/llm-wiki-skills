---
name: configure-hugo
description: >
  Configure a wiki for Hugo rendering. Read the wiki's registered
  types, generate Hugo configuration with type-specific cascades
  and layouts, set up frontmatter mapping. Use when the user says
  "set up Hugo", "configure Hugo", "make this wiki publishable",
  or "add Hugo to this wiki". Requires the llm-wiki-hugo-cms
  scaffold to be present in the wiki repo.
type: skill
status: active
last_updated: "2025-07-18"
disable-model-invocation: true
when_to_use: >
  The user says "configure Hugo", "set up Hugo", "make this wiki
  publishable", or wants to render the wiki as a static site.
tags: [hugo, publishing, configuration]
owner: jguibert@gmail.com
metadata:
  version: "0.1.0"
---

# Configure Hugo

Configure a wiki for Hugo rendering using the llm-wiki-hugo-cms
scaffold. This skill reads the wiki's registered types and generates
matching Hugo configuration.

## Prerequisites

The [llm-wiki-hugo-cms](https://github.com/geronimo-iia/llm-wiki-hugo-cms)
scaffold must be present in the wiki repo. If not, instruct the user
to clone or copy it first.

## Steps

### 1. Read wiki configuration

```
wiki_config(action: "list")
```

Collect the wiki name, description, and all registered types with
their schemas.

### 2. Check for Hugo scaffold

Verify that `hugo.toml` (or `hugo.yaml`/`hugo.json`) and `layouts/`
exist in the wiki repo. If not present, instruct the user:

> The llm-wiki-hugo-cms scaffold is required. Clone it into your wiki
> repo first:
> ```
> git clone https://github.com/geronimo-iia/llm-wiki-hugo-cms .hugo
> ```

### 3. Generate hugo.toml

Generate `hugo.toml` with:

- `contentDir` pointing to `wiki/`
- `title` from wiki name
- `[[cascade]]` rules for each registered type
- Taxonomy mappings for `tags`, `owner`, `type`
- `ignoreFiles` for `inbox/`, `raw/`, `schemas/`

### 4. Generate type-specific layouts

For each registered type, check if a layout exists at
`layouts/<section>/single.html`. If not, generate one based on the
type's fields.

### 5. Generate frontmatter mapping

Map type-specific fields to Hugo template variables. Handle aliases:

- Skill: `name` → `title`, `description` → `summary`
- All types: `read_when` → displayed as retrieval conditions
- Source types: `claims` → rendered as structured data

### 6. Validate (if Hugo is installed)

```bash
hugo --printUnusedTemplates
```

### 7. Report

Report what was generated:

- Hugo configuration file
- Layout files created or updated
- Frontmatter mappings applied
- Any issues or manual steps needed
