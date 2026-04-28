# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com),
and this project adheres to [Semantic Versioning](https://semver.org).

## [0.4.0] — Unreleased

### Added

- **Crystallize two-step extraction** — explicit analysis step added before writes; extraction plan format with `What/Type/Action/Confidence` per item; user confirmation required before any page is created or updated
- **Confidence calibration table** — 7-row table mapping session knowledge types (decision, pattern, finding, hypothesis, open-question, speculation) to suggested `confidence` ranges; adjustment guidance; default 0.5 rule
- **Post-ingest lint step** — `wiki_lint(rules: "broken-link,orphan")` added after ingest in crystallize; catches dead references and orphan pages introduced by new session pages
- **Redaction in ingest skill** — `wiki_ingest(redact: true)` documented in step 2f; when to use it (external content, session transcripts, raw notes); built-in patterns listed; per-wiki `wiki.toml` disable/extend example; lossy-by-design warning
- **`wiki_lint` in lint skill** — `wiki_lint()` is now the first step in every audit; manual orphan/broken-link detection replaced with `wiki_lint(rules: "orphan")` and `wiki_lint(rules: "broken-link")`; judgment-based checks (empty sections, draft audit, under-linked pages) retained
- **Backlinks discovery** — `backlinks: true` on `wiki_content_read` documented in content skill; example JSON response with `backlinks` array shown
- **Backlinks as research technique** — research skill documents backlinks as a way to trace what depends on or cites a page
- **`format: "llms"` orientation pattern** — `wiki_list(format: "llms")` added as first step in crystallize (before searches), first-file orientation in ingest step 2c, and optional broad-query orientation in research; replaces multi-call paginated listing for full-wiki orientation
- **Lint structural orientation** — `wiki_list(format: "llms")` documented in lint skill for structural gap analysis before judgment-based checks
- **Graph `format: "llms"`** — graph skill documents `wiki_graph(format: "llms")` as the primary interpretation call; produces natural language description (clusters, hubs, isolated nodes, relation counts) without requiring Mermaid parsing; Mermaid/DOT retained for visualization
- **Lint fix guidance completed** — fix instructions added for all 5 engine rules (`stale`, `unknown-type`, `missing-fields` were previously missing); `wiki_lint(wiki: "name")` parameter documented
- `.mcp.json.example` — template for local development with a custom binary path and config; use when testing against a local build or non-default config path

### Changed

- **`claims[].confidence` aligned to float** — was string enum `high/medium/low`; now `0.0–1.0` matching page-level confidence in frontmatter, ingest, and research skills
- **Confidence guidance updated** — frontmatter skill rewrites the `### confidence` section with float scale table and conventional values (`0.9` well-corroborated, `0.5` single source, `0.2` speculative); anti-pattern row updated from `confidence: high` → `confidence: 0.9`
- **Ingest skill** — confidence guidance for new pages notes `0.5` as the scaffold default
- **Research skill** — confidence interpretation updated for float values in search results
- `.gitignore` — added `mcp-config.json` and `.mcp.json.testing` (machine-specific local dev overrides)

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
