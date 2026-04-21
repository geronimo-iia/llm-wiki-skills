# Update: graph Skill

## Changes

- Relation filtering: `wiki_graph --relation fed-by` shows only those edges
- `x-graph-edges` declarations in schemas define edge labels per type
- The same field (`sources`) has different relations depending on page type:
  - concept: `sources` → `fed-by`
  - paper: `sources` → `cites`
  - doc: `sources` → `informed-by`
- Composable filters: `--type concept --relation depends-on --root concepts/moe --depth 2`
- Edge target type warnings on ingest (graph integrity)
