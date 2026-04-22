# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com),
and this project adheres to [Semantic Versioning](https://semver.org).

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
