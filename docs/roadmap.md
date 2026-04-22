# Roadmap

## Current State

14 skills covering the full engine surface. All skills updated to
reflect Phase 3 (typed graph edges), engine refactoring (renamed
tools, new features), and consistent goal-oriented style.

## Skills Inventory

| Skill             | Status  | Notes                                                                       |
| ----------------- | ------- | --------------------------------------------------------------------------- |
| `setup`           | updated | First-time install, neutral tone                                            |
| `spaces`          | updated | Space management with repository layout                                     |
| `schema`          | updated | Full type system — epistemic roles, edges, aliasing                         |
| `config`          | new     | Config operations, key reference, resolution order                          |
| `bootstrap`       | updated | Session orientation, neutral tone                                           |
| `content`         | updated | Renamed from `write-page` — read, create, update, sections, bundles, assets |
| `ingest`          | updated | Inbox→raw workflow, neutral tone                                            |
| `crystallize`     | updated | Session→page, LLM can propose                                               |
| `research`        | updated | Search, graph exploration, cross-wiki                                       |
| `lint`            | updated | Schema validation, edge type checks                                         |
| `graph`           | updated | Edge system, relation filtering, composable filters                         |
| `frontmatter`     | updated | Field conventions, graph edges, aliasing                                    |
| `skill-discovery` | updated | Renamed from `skill` — proactive discovery                                  |
| `configure-hugo`  | written | Review — hugo-cms project now has its own docs                              |

## Phase 1 — Sync with Engine ✓

All skills updated to match the current engine state.

### Completed

- [x] Consistent goal-oriented style across all skills (not sequential steps)
- [x] Neutral tone in frontmatter (`description`, `when_to_use`) — works for both users and LLMs
- [x] Tool names: `wiki_content_read`, `wiki_content_write`, `wiki_content_new`, `wiki_content_commit`
- [x] `--cross-wiki` flag (not `--all`) for cross-wiki search
- [x] `wiki_graph --relation <label>` for relation filtering
- [x] `x-graph-edges` documented per type (concept, source, doc, skill)
- [x] Composable graph filters: `--type`, `--relation`, `--root`, `--depth`
- [x] Edge target type validation via `wiki_ingest --dry-run`
- [x] `wiki_schema validate` for schema integrity
- [x] `wiki_schema show <type> --template` for frontmatter scaffolding
- [x] Page anatomy: flat vs bundle, assets, slug resolution
- [x] Accumulation contract in content and crystallize skills
- [x] `write-page` → `content` (broader scope: read, create, update, sections)
- [x] `skill` → `skill-discovery` (clearer name)
- [x] `crystallize` allows LLM-initiated proposals
- [x] `skill-discovery` allows proactive search
- [x] New `config` skill with full key reference
- [x] New `spaces` skill with repository layout

## Phase 2 — New Skills

Skills for new engine capabilities.

- [ ] `custom-type` — guide for creating custom page types with schemas
- [ ] `ci-cd` — set up CI/CD validation and deployment

## Future

- Skill composition (`extends` field)
- Skill versioning (track which engine version a skill targets)
- Automated skill testing
- Review `configure-hugo` — may be obsolete or need its own repo
