# Update: lint Skill

## Changes

- Add edge target type validation: use `wiki_ingest --dry-run` to check
  for type constraint warnings (e.g., concept with `sources` pointing to
  another concept instead of a source type)
- `wiki_schema validate` checks schema integrity
- Tool names: `wiki_content_read` (not `wiki_read`)
