# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com),
and this project adheres to [Semantic Versioning](https://semver.org).

## [0.4.0] — Unreleased

### Added

- **Backlinks discovery** — `backlinks: true` on `wiki_content_read` documented in content skill; example JSON response with `backlinks` array shown
- **Backlinks as research technique** — research skill documents backlinks as a way to trace what depends on or cites a page

### Changed

- **`claims[].confidence` aligned to float** — was string enum `high/medium/low`; now `0.0–1.0` matching page-level confidence in frontmatter, ingest, and research skills
- **Confidence guidance updated** — frontmatter skill rewrites the `### confidence` section with float scale table and conventional values (`0.9` well-corroborated, `0.5` single source, `0.2` speculative); anti-pattern row updated from `confidence: high` → `confidence: 0.9`
- **Ingest skill** — confidence guidance for new pages notes `0.5` as the scaffold default
- **Research skill** — confidence interpretation updated for float values in search results

## [0.3.1] — 2026-04-26

### Fixed

- Updated `cargo install llm-wiki` → `cargo install llm-wiki-engine`
  in setup skill and README (crate renamed on crates.io)

## [0.3.0] — 2026-04-26

### Fixed

- `wiki_content_commit`: `slugs` is a comma-separated string, not an array;
  removed non-existent `all` parameter — omit `slugs` to commit all changes
- `wiki_list`: replaced non-existent `path` parameter in ingest skill with
  `wiki_ingest(path:..., dry_run: true)` for inbox scanning

## [0.2.0] — 2025-07-21

### Added

- `spaces` skill — manage wiki spaces (create, list, inspect, remove)
- `config` skill — read, write, and understand wiki configuration
- `schema` skill — understand and manage the type system
- `content` skill — read, create, update pages and sections
- Graph edge system documentation in schema, frontmatter, and graph skills
- Edge target type validation via `wiki_ingest --dry-run`
- Schema validation via `wiki_schema validate`
- Page anatomy: flat vs bundle, assets, slug resolution in content skill
- Field aliasing documentation in frontmatter skill
- Composable graph filters: type, relation, root, depth
- Cross-wiki search (`cross_wiki` parameter)
- Repository layout section in spaces skill

### Changed

- All skills rewritten in goal-oriented style (not sequential steps)
- Neutral tone in frontmatter — works for both users and LLMs
- `write-page` renamed to `content` (broader scope)
- `skill` renamed to `skill-discovery` (clearer intent)
- `crystallize` now LLM-proactive (removed `disable-model-invocation`)
- `skill-discovery` now proactively searches for relevant wiki skills
- Correct tool names: `wiki_content_read`, `wiki_content_write`,
  `wiki_content_new`, `wiki_content_commit`
- Type taxonomy restructured with edge declarations per type category
- Updated README, plugin.json, roadmap

### Removed

- Phase 1 update prompts (`docs/prompts/update-*.md`) — completed

## [0.1.0] — 2025-07-18

### Added

- Initial release with 11 skills: setup, bootstrap, ingest,
  crystallize, research, lint, graph, frontmatter, skill, write-page,
  configure-hugo
