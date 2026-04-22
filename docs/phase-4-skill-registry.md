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

1. `llm-wiki spaces create` can register it as a wiki space
2. All skills are indexable and searchable via `wiki_search`
3. Skill relationships are visible in `wiki_graph`
4. Cross-wiki search (`cross_wiki: true`) finds skills alongside
   wiki content
5. The Claude plugin still works (backward compatible)

## Steps

### 1. Add wiki structure

Add the standard wiki repository layout to the repo root:

```
llm-wiki-skills/
├── wiki.toml                    ← NEW: wiki identity
├── schemas/                     ← NEW: at minimum skill.json + base.json
├── skills/                      ← KEEP: becomes wiki/ equivalent
│   ├── bootstrap/SKILL.md
│   ├── content/SKILL.md
│   └── ...
├── docs/                        ← KEEP
├── .claude-plugin/              ← KEEP: backward compat
└── README.md
```

Decision needed: should `skills/` be renamed to `wiki/` or should
`wiki.toml` point to `skills/` as the wiki root? Renaming breaks
the Claude plugin path convention. Keeping `skills/` requires the
engine to support a configurable wiki root.

### 2. Create wiki.toml

```toml
name = "llm-wiki-skills"
description = "Skills for the llm-wiki engine"
```

### 3. Add schemas

Copy `skill.json` and `base.json` from the engine's default schemas.
Skills already have valid skill-type frontmatter — they should pass
validation as-is.

### 4. Verify skill frontmatter

Run `wiki_schema(action: "validate")` against all skills. Fix any
validation errors. Current skills use the agentskills.io format
(`name`/`description` aliased to `title`/`summary`) which the engine
already supports.

### 5. Index and test

```
llm-wiki spaces create . --name llm-wiki-skills
wiki_ingest(path: "skills/")
wiki_search(query: "ingest", type: "skill")
wiki_graph(type: "skill")
```

Verify:
- All skills are indexed and searchable
- `document_refs` edges appear in the graph
- Cross-wiki search from another wiki finds these skills

### 6. Add knowledge pages

Create concept pages about llm-wiki itself:

- `wiki/concepts/epistemic-model.md` — why type carries epistemic
  distinctions (source vs concept vs query-result)
- `wiki/concepts/dkr-model.md` — the three-layer flow
  (inbox→raw→wiki)
- `wiki/concepts/type-system.md` — type discovery, aliasing, graph
  edges
- `wiki/concepts/accumulation-contract.md` — read-before-write,
  preserve lists

These pages make the engine's design philosophy searchable and
linkable from skills via `concepts` frontmatter fields.

### 7. Backward compatibility

Ensure the Claude plugin still works:
- `.claude-plugin/plugin.json` unchanged
- `skills/*/SKILL.md` paths unchanged
- Plugin discovery reads `skills/` directory as before

## Open questions

- Should the wiki root be `skills/` or `wiki/`? If `wiki/`, skills
  move to `wiki/skills/` and knowledge pages go to `wiki/concepts/`.
  If `skills/`, knowledge pages need a different location.
- Should knowledge pages live in this repo or in a separate
  `llm-wiki-docs` wiki?
- Does the engine need a configurable wiki root (`wiki_root` in
  `wiki.toml`) to support non-standard layouts?

## Success criteria

- `wiki_search(query: "ingest", type: "skill")` returns the ingest
  skill from this repo
- `wiki_graph(type: "skill")` shows skill→doc edges
- Cross-wiki search finds skills alongside regular wiki content
- Claude plugin still works without changes
- All existing skills pass `wiki_schema validate`
