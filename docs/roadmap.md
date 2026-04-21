# Roadmap

## Current State

11 skills written for the initial engine (Phase 1+2). Skills need
updating to reflect Phase 3 (typed graph edges) and engine refactoring
(renamed tools, new features).

## Skills Inventory

| Skill | Status | Needs update? |
|-------|--------|---------------|
| `setup` | written | Yes — install methods changed (install.sh, homebrew, asdf) |
| `bootstrap` | written | Yes — tool names changed, `wiki_schema` tool added |
| `ingest` | written | Yes — edge target warnings, `wiki_schema validate` |
| `crystallize` | written | Review — may reference old tool names |
| `research` | written | Review — `--all` renamed to `--cross-wiki` |
| `lint` | written | Yes — add type constraint violation detection via graph edges |
| `graph` | written | Yes — relation-aware instructions (`--relation`, `x-graph-edges`) |
| `frontmatter` | written | Yes — update type taxonomy with `x-graph-edges` declarations |
| `skill` | written | Review — may reference old tool names |
| `write-page` | written | Yes — `wiki_schema show --template` may have changed |
| `configure-hugo` | written | Review — hugo-cms project now has its own docs |

## Phase 1 — Sync with Engine

Update all skills to match the current engine state.

- [ ] Audit each SKILL.md for stale tool names
- [ ] Update `setup` with new install methods
- [ ] Update `bootstrap` with `wiki_schema` tool
- [ ] Update `research` with `--cross-wiki` flag
- [ ] Update `graph` with relation filtering and `x-graph-edges`
- [ ] Update `lint` with edge target type validation
- [ ] Update `frontmatter` type taxonomy with edge declarations
- [ ] Update `ingest` with edge target warnings
- [ ] Test with `claude --plugin-dir ./llm-wiki-skills`

## Phase 2 — New Skills

Skills for new engine capabilities.

- [ ] `multi-wiki` — manage multiple wikis, cross-wiki workflows
- [ ] `custom-type` — guide for creating custom page types with schemas
- [ ] `ci-cd` — set up CI/CD validation and deployment

## Future

- Skill composition (`extends` field)
- Skill versioning (track which engine version a skill targets)
- Automated skill testing
