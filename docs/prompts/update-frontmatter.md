# Update: frontmatter Skill

## Changes

- Add `x-graph-edges` to the type taxonomy reference:
  - concept: `sources` (fed-by), `concepts` (depends-on), `superseded_by` (superseded-by)
  - paper/article/etc: `sources` (cites), `concepts` (informs), `superseded_by` (superseded-by)
  - skill: `document_refs` (documented-by), `superseded_by` (superseded-by)
  - doc: `sources` (informed-by), `superseded_by` (superseded-by)
- Update `references/type-taxonomy.md` with edge declarations
- `wiki_schema show <type> --template` for quick frontmatter reference
