---
name: skill-discovery
description: >
  Find and activate skills stored in the wiki — search by capability,
  read instructions, and follow workflows.
type: skill
status: draft
last_updated: "2025-07-21"
when_to_use: >
  Looking for a workflow the wiki might have a skill for, listing
  available skills, or activating a discovered skill. Proactively
  search for relevant wiki skills when a task could benefit from
  an existing workflow.
tags: [skill, discovery, activation]
owner: jguibert@gmail.com
metadata:
  version: "0.2.0"
---

# Skill Discovery

The wiki is a skill registry — `type: skill` pages contain workflow
instructions that any agent can discover and follow. Skill pages use
`name`/`description` instead of `title`/`summary` (aliased at ingest
for uniform indexing).

## Plugin skills vs wiki skills

| Aspect | Plugin skills (this repo) | Wiki skills (`type: skill` pages) |
|--------|--------------------------|-----------------------------------|
| Source | `llm-wiki-skills` git repo | Written into the wiki tree |
| Scope | Engine-level — how to use the tools | Domain-level — how to do domain tasks |
| Discovery | `/llm-wiki:<skill>` namespace | `wiki_search(type: "skill")` |
| Mutable | Via PRs to the repo | Editable in the wiki |

Both coexist. Bootstrap with plugin skills (how to use the engine),
then discover wiki skills (how to do domain work).

## List all skills

```
wiki_list(type: "skill")
```

## Search for a skill

```
wiki_search(query: "<what needs to be done>", type: "skill")
```

BM25 matches against `name` (indexed as `title`), `description`
(indexed as `summary`), `when_to_use` (indexed as `read_when`),
`tags`, and body text.

## Read a skill

```
wiki_content_read(uri: "<skill-slug>")
```

Returns the full skill content — frontmatter and body with
instructions.

If the skill has `concepts` in its frontmatter, read those concept
pages for supporting knowledge before executing.

If the skill has `document_refs`, read those doc pages for
specifications and reference material.

## Activate a skill

Parse the skill's body and follow its workflow. The skill may
reference MCP tools, other wiki pages, or external commands.

## Explore skill relationships

```
wiki_graph(root: "<skill-slug>", depth: 1)
```

Shows `documented-by` edges to doc pages and any `superseded-by`
replacements.
