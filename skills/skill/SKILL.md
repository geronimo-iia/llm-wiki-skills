---
name: skill
description: >
  Find and activate skills stored in the wiki. Search for skills
  by capability, read their instructions, and follow them. Use
  when the user needs a workflow the wiki might have a skill for,
  or says "find a skill for", "how do I", or "is there a skill".
type: skill
status: active
last_updated: "2025-07-18"
tags: [skill, discovery, activation]
owner: geronimo
---

# Skill

Find, read, and activate skills stored in the wiki. The wiki is a
skill registry — `type: skill` pages contain workflow instructions
that any agent can discover and follow.

## MCP tools used

- `wiki_search` — find skills by capability (with type filter)
- `wiki_list` — list all skills
- `wiki_content_read` — read full skill instructions

## Steps

### 1. Search for skills

```
wiki_search(query: "<what the user wants to do>", type: "skill")
```

The BM25 engine matches against the skill's `name` (indexed as
`title`), `description` (indexed as `summary`), `when_to_use`
(indexed as `read_when`), `tags`, and body text.

### 2. Present results

Show the matching skills with name, description, and tags. Let the
user choose which skill to activate.

To list all available skills:

```
wiki_list(type: "skill")
```

### 3. Read the skill

```
wiki_content_read(uri: "<skill-slug>")
```

Get the full skill content — frontmatter and body with instructions.

### 4. Follow the instructions

Parse the skill's body and follow its workflow steps. The skill may
reference MCP tools, other wiki pages, or external commands.

If the skill has `concepts` in its frontmatter, read those concept
pages for supporting knowledge before executing.

## Plugin skills vs wiki skills

| Aspect | Plugin skills (this repo) | Wiki skills (`type: skill` pages) |
|--------|--------------------------|-----------------------------------|
| Source | `llm-wiki-skills` git repo | Written into the wiki tree |
| Scope | Engine-level — how to use the tools | Domain-level — how to do domain tasks |
| Discovery | `/llm-wiki:<skill>` namespace | `wiki_search --type skill` |
| Mutable | Via PRs to the repo | Editable in the wiki |

Both coexist. Bootstrap with plugin skills (how to use the engine),
then discover wiki skills (how to do domain work).
