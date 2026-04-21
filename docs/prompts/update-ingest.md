# Update: ingest Skill

## Changes

- Edge target type warnings: ingest now warns when `sources` points to
  a non-source type (or similar mismatches per `x-graph-edges` `target_types`)
- `wiki_schema validate` can pre-check schemas before ingest
- Tool name: `wiki_content_write` (not `wiki_write`)
- Mention `wiki_ingest --dry-run` for validation without commit
