# Contributing to llm-wiki-skills

## What lives here

Each skill is a single `SKILL.md` file in `skills/<name>/`. The file
has YAML frontmatter and a Markdown body — no code, no build step.

Draft skills (waiting on engine features) go in `docs/draft-skills/`
with `status: draft` in the frontmatter.

## Prerequisites

- A working [llm-wiki](https://github.com/geronimo-iia/llm-wiki)
  installation to test tool calls
- Familiarity with the engine's MCP tool signatures — check
  `src/mcp/tools.rs` in the engine repo for the authoritative list

## Editing a skill

1. Open `skills/<name>/SKILL.md`
2. Update `last_updated` in the frontmatter to today's date
3. Verify all tool calls match the engine's current parameter names
   and types — the most common mistakes are wrong parameter types
   and non-existent parameters
4. Test the workflow end-to-end in a real wiki session

## Adding a skill

1. Create `skills/<name>/SKILL.md` with the standard frontmatter:

```yaml
---
name: <name>
description: >
  One or two sentences — what this skill does and when to use it.
type: skill
status: active
last_updated: "YYYY-MM-DD"
when_to_use: >
  Situations where an agent should activate this skill.
tags: [tag1, tag2]
owner: <your-email>
metadata:
  version: "0.1.0"
---
```

2. Write the body in goal-oriented style — describe outcomes and
   tools, not sequential steps unless order truly matters
3. Only reference MCP tools that exist in the current engine release
4. Add the skill to the inventory table in `README.md`

## Skill quality checklist

- [ ] Tool names and parameter types match the engine exactly
- [ ] No parameters that don't exist in the engine
- [ ] `slugs` in `wiki_content_commit` is a comma-separated string,
      not an array — omit to commit all
- [ ] `wiki_list` does not accept a `path` parameter
- [ ] `last_updated` is set to today
- [ ] Skill is listed in `README.md` inventory

## Updating the version

Bump `plugin.json` version and add a `CHANGELOG.md` entry for any
change that affects skill behaviour — wrong tool calls, new skills,
removed skills, or workflow corrections.

## Release

1. Bump `version` in `.claude-plugin/plugin.json`
2. Add a `## [x.y.z] — YYYY-MM-DD` entry to `CHANGELOG.md`
3. Commit: `chore: bump version to x.y.z`
4. Tag and push:
   ```bash
   git tag vx.y.z && git push origin vx.y.z
   ```

Pushing the tag triggers the release workflow — it creates a GitHub
release and extracts the matching CHANGELOG section as release notes.
No build step. The plugin is used directly from the repo.
