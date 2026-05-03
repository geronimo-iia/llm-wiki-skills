---
name: export
description: >
  Export the full wiki to a file — llms.txt for publishing, llms-full
  for deep offline analysis, or JSON for batch processing.
type: skill
status: active
last_updated: "2026-05-04"
disable-model-invocation: false
when_to_use: >
  Publishing the wiki as llms.txt, handing off wiki content to an
  external tool or pipeline, generating a snapshot for offline use,
  or auditing all pages without pagination.
tags: [export, publishing, llms-txt, batch]
owner: jguibert@gmail.com
metadata:
  version: "0.1.0"
---

# Export

Write the full wiki to a file — no pagination. Response is a report,
not the content itself.

```
wiki_export(wiki: "research")
```

Default output: `llms.txt` at the wiki repository root, `llms-txt` format,
`active` pages only.

## Choosing a format

| Format | Content | When to use |
|--------|---------|-------------|
| `llms-txt` (default) | One line per page with summary, grouped by type | Publishing via `llms.txt` ecosystem; orientation for a new LLM session |
| `llms-full` | Summary + full body per page separated by `---` | Deep offline analysis; passing full wiki content to a long-context model |
| `json` | JSON array — metadata + body per page | CI pipelines, batch scripts, external tooling |

## Publishing workflow (llms.txt ecosystem)

Export after every significant ingest or content session:

```
wiki_export(wiki: "research", format: "llms-txt", path: "llms.txt")
```

The default path `llms.txt` lands at the wiki root. This file:
- Is picked up by `llms.txt`-aware tools automatically
- Is served by the Hugo scaffold at `/<wiki>/llms.txt` when committed
- Can be committed to git as a snapshot: `wiki_content_commit`

Include drafts when the export is for internal review only:

```
wiki_export(wiki: "research", status: "all")
```

## Handoff to external tool

For passing full content to a long-context model or analysis pipeline:

```
wiki_export(wiki: "research", format: "llms-full", path: "export/full.md")
```

This differs from `wiki_list(format: "llms")` — that produces a tool
response for the current session. `wiki_export` writes a file for
persistent use outside the session.

## Batch processing / JSON pipeline

```
wiki_export(wiki: "research", format: "json", path: "export/pages.json")
```

Each JSON object includes `slug`, `uri`, `title`, `type`, `status`,
`confidence`, `summary`, and `body`.

## Response

```json
{
  "path": "/home/user/wiki/llms.txt",
  "pages_written": 42,
  "bytes": 18340,
  "format": "llms-txt"
}
```

`path` is always absolute — use it for follow-up file operations without
needing to resolve the wiki root.

## When to re-export

- After `wiki_ingest` if the wiki is published via `llms.txt`
- Before a research session with an external tool that reads the file
- Before publishing Hugo site (ensure `llms.txt` is up to date)
- After a crystallize session that added or updated many pages

## Path notes

`path` is resolved relative to the wiki root when not absolute.
Avoid paths outside the wiki root for files meant to be committed —
`wiki_content_commit` only commits files within the wiki repository.
