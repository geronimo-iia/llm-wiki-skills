# Phase 4 — Skill Registry

Transform `llm-wiki-skills` into a llm-wiki itself. The skills repo
becomes a wiki that the engine can index, search, and serve — skills
are discoverable through the same tools as any other wiki content.

## Context

Today, `llm-wiki-skills` is a flat git repo with `skills/*/SKILL.md`
files. Agents discover skills through the Claude plugin system or by
reading files directly. This works but doesn't leverage the engine:

- No search — agents can't `wiki_search(type: "skill")` against
  this repo
- No graph — skill relationships (`document_refs`, `superseded_by`)
  aren't indexed
- No cross-wiki — skills live outside the wiki ecosystem

## Goal

Make `llm-wiki-skills` a valid llm-wiki repository so that:

1. `llm-wiki spaces register` can register it as a wiki space
2. All skills are indexable and searchable via `wiki_search`
3. Skill relationships are visible in `wiki_graph`
4. Cross-wiki search (`cross_wiki: true`) finds skills alongside
   wiki content
5. The Claude plugin still works without any path changes

## Prerequisite: configurable wiki_root (engine v0.x)

This phase requires `wiki_root` support in the engine
(`spaces register --wiki-root`, `wiki.toml` `wiki_root` field).
See `llm-wiki/docs/prompts/design-configurable-wiki-root.md`.

Until that lands, Phase 4 cannot be executed without restructuring
the repo layout.

## Repository Layout

No restructuring needed. `skills/` stays at the repo root.
`wiki_root = "skills"` tells the engine where content lives:

```
llm-wiki-skills/
├── wiki.toml          ← NEW: wiki identity + wiki_root
├── skills/            ← KEEP: becomes the wiki content root
│   ├── bootstrap/SKILL.md
│   ├── content/SKILL.md
│   └── ...
├── docs/              ← KEEP
└── .claude/           ← KEEP: plugin path unchanged
```

`inbox/` and `raw/` are omitted — this repo doesn't use the DKR ingest
flow and the engine does not require their existence.
Schemas are managed by the engine — no `schemas/` directory needed.

## Steps

### 0. Create a branch

```bash
git checkout -b feat/wiki-layout
```

### 1. Add wiki.toml

```toml
name        = "llm-wiki-skills"
description = "Skills for the llm-wiki engine"
wiki_root   = "skills"
```

### 2. Verify skill frontmatter

Run `wiki_schema(action: "validate")` against all skills. Current
skills use the agentskills.io format (`name`/`description` aliased to
`title`/`summary`) — the engine already supports this via
`x-index-aliases` in `skill.json`.

### 4. Register and test

```bash
llm-wiki spaces register . --name llm-wiki-skills
wiki_ingest(path: "skills/")
wiki_search(query: "ingest", type: "skill")
wiki_graph(type: "skill")
```

Verify:
- All skills are indexed and searchable
- `document_refs` edges appear in the graph
- Cross-wiki search from another wiki finds these skills
- Claude plugin still discovers skills at `skills/*/SKILL.md` (unchanged)

### 5. Add knowledge pages

Source material lives in `llm-wiki/docs/` — use it to create concept
pages rather than writing from scratch:

| Source | Candidate concept pages |
|--------|------------------------|
| `docs/overview.md` | epistemic model, DKR model, type system, accumulation contract |
| `docs/guides/getting-started.md` | wiki repository layout, write+ingest pattern |
| `docs/guides/multi-wiki.md` | cross-wiki search, space registry |
| `docs/specifications/` | tool surface, graph edges, field aliasing |

Pages go into `skills/concepts/` (inside `wiki_root`). Each page
should have `type: concept` frontmatter and reference skills via
`concepts` fields where relevant.

### 6. Commit

```bash
git add wiki.toml
git commit -m "feat: register llm-wiki-skills as a wiki space"
```

## Success Criteria

- `wiki_search(query: "ingest", type: "skill")` returns the ingest
  skill from this repo
- `wiki_graph(type: "skill")` shows skill→doc edges
- Cross-wiki search finds skills alongside regular wiki content
- Claude plugin still works without changes
- All existing skills pass `wiki_schema validate`
