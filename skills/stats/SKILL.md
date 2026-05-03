---
name: stats
description: >
  Assess wiki health — page counts, orphans, graph connectivity,
  staleness, community clusters, and structural topology. Interpret
  metrics and decide what to fix next.
type: skill
status: active
last_updated: "2026-05-04"
disable-model-invocation: false
when_to_use: >
  Getting a quick health overview before a work session, deciding
  whether to lint or ingest next, checking index freshness, or
  assessing structural quality of the knowledge graph.
tags: [stats, health, graph, quality]
owner: jguibert@gmail.com
metadata:
  version: "0.1.0"
---

# Stats

Wiki health dashboard. One call returns all metrics — page counts,
graph shape, staleness buckets, community clusters, structural topology,
and index health.

```
wiki_stats()
```

Target a specific wiki:

```
wiki_stats(wiki: "research")
```

## Reading the output

### Page counts

`pages` — total indexed pages. If lower than expected, the index may be
stale: check `index.stale`. Rebuild with `wiki_index_rebuild` if needed.

`sections` — section index pages. Excluded from most metrics (orphan
check, staleness, structural rules) to avoid noise.

`types` / `status` — facet distributions. High `draft` count → run
`wiki_lint(rules: "stale")` or audit drafts manually.

### Orphans and connectivity

`orphans` — pages with zero inbound edges. Any orphan is a candidate
for a new link or deletion. Run `wiki_lint(rules: "orphan")` for the
full list with paths.

`avg_connections` — mean edges per node. Below ~1.5 on a wiki with
many pages signals sparse linking. Run `wiki_suggest` on isolated pages.

`graph_density` — edges / (n·(n-1)). Low density is expected on large
wikis. Only concerning when combined with high orphan count and low
`avg_connections`.

**Triage rule:** `orphans / pages > 0.2` → link audit needed.

### Staleness

```
"staleness": { "fresh": 30, "stale_7d": 8, "stale_30d": 4 }
```

- `fresh` — updated within 7 days
- `stale_7d` — updated 7–30 days ago
- `stale_30d` — older than 30 days or no date

High `stale_30d` alone is not a problem — stable knowledge doesn't need
frequent updates. It becomes a problem when combined with low `confidence`
on those pages. Run `wiki_lint(rules: "stale")` to find pages that are
both old AND low-confidence.

### Index health

```
"index": { "stale": false, "built": "2026-05-04T10:00:00Z" }
```

`stale: true` means wiki files have changed since the last index build.
Rebuild before relying on any other metric:

```
wiki_index_rebuild(wiki: "research")
```

### Community clusters

`communities` is `null` when the wiki has fewer than
`graph.min_nodes_for_communities` pages (default 30).

```json
{
  "count": 7,
  "largest": 34,
  "smallest": 3,
  "isolated": ["concepts/orphan-draft", "sources/tangent-2023"]
}
```

| Signal | Interpretation |
|--------|---------------|
| High `count`, low `largest` | Fragmented wiki — many small disconnected clusters |
| Low `count`, very high `largest` | Monolithic — one dominant cluster, poor separation of concerns |
| Non-empty `isolated` | Weakly connected pages — prime link candidates |

For each `isolated` slug, run `wiki_suggest` to find connection candidates:

```
wiki_suggest(slug: "concepts/orphan-draft")
```

### Structural topology

`diameter`, `radius`, `center`, `structural_note` — present when
`graph.structural_algorithms = true` (default) and wiki is below
`graph.max_nodes_for_diameter` (default 2000 nodes).

```json
{
  "diameter": 6.0,
  "radius": 3.0,
  "center": ["concepts/core-concept"],
  "structural_note": null
}
```

| Field | Interpretation |
|-------|---------------|
| `diameter` | Longest shortest path. High value (>8 on a 50-page wiki) = elongated chain graph |
| `radius` | Minimum eccentricity. Close to `diameter` = no strong center |
| `center` | Most central hub pages — linking sparse nodes through these shortens paths |
| `structural_note` | Non-null = O(n²) algorithms skipped due to graph size |

`diameter ≈ radius` (within 1–2) on a well-connected wiki. Large gap
means the graph has a tight core and a long tail of peripheral pages.
Run `wiki_lint(rules: "periphery")` to identify those tail pages.

When `structural_note` is set, disable-or-raise `max_nodes_for_diameter`
in config, or accept that topology fields are unavailable at that scale.

## Triage decision tree

```
index.stale = true          → wiki_index_rebuild first, then re-run stats
orphans / pages > 0.2       → wiki_lint(rules: "orphan")
stale_30d / pages > 0.3     → wiki_lint(rules: "stale")
isolated communities        → wiki_suggest per isolated slug
diameter >> radius          → wiki_lint(rules: "periphery")
articulation points likely  → wiki_lint(rules: "articulation-point,bridge")
```

## CI health gate pattern

Exit non-zero when the index is stale or orphan ratio is high:

```bash
llm-wiki stats --wiki research --format json \
  | jq 'if .index.stale or (.orphans / .pages > 0.2) then error else . end'
```
