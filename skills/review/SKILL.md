---
name: review
description: >
  Build a prioritized review queue from lint findings, draft pages, and
  low-confidence knowledge; process items one at a time with guided decisions.
type: skill
status: active
last_updated: "2026-04-27"
disable-model-invocation: true
argument-hint: "[max-items]"
when_to_use: >
  Reviewing draft pages, verifying low-confidence knowledge, resolving
  flagged contradictions, or doing a periodic wiki quality pass.
tags: [review, quality, audit]
owner: jguibert@gmail.com
metadata:
  version: "0.1.0"
---

# Review

Process wiki pages that need human attention: structural errors, unverified
drafts, and low-confidence active pages. The queue is rebuilt from existing
fields each session — no dedicated state required.

## Step 1 — Discover the wiki root

```
wiki_spaces_list()
```

## Step 2 — Build the review queue

Assemble from three sources, then merge and deduplicate:

**Source 1 — lint errors and warnings (highest priority):**
```
wiki_lint()
```
Pages with `Error` findings (broken links, missing fields, unknown type) rank
first — they are structurally broken, not just unreviewed.

**Source 2 — draft pages:**
```
wiki_list(status: "draft")
```

**Source 3 — low-confidence active pages:**
```
wiki_list(status: "active")
```
Filter to pages where `confidence < 0.4`.

**Priority order:**

| Priority | Condition |
|---|---|
| 1 — Error | `wiki_lint` `Error` finding |
| 2 — Warning | `wiki_lint` `Warning` finding |
| 3 — Draft | `status: draft`, no lint finding |
| 4 — Low confidence | `status: active`, `confidence < 0.4` |

Within each tier: sort by `confidence` ascending (least certain first), then
`last_updated` ascending (oldest first).

If the user provided a `max-items` argument, cap the queue at that count.

## Step 3 — Review loop

Process items one at a time. For each page:

### 3a. Read the page

```
wiki_content_read(slug: "<slug>", backlinks: true)
wiki_history(slug: "<slug>", limit: 3)
```

### 3b. Show context

Present:
- What triggered the flag (lint finding type, draft status, or confidence value)
- Backlinks — who links to this page (load-bearing vs. orphaned)
- Last 3 commits — how recently and how often this page was touched

### 3c. Guide the review decision

| Decision | When | Action |
|---|---|---|
| **Promote** | Content is correct and complete | Set `status: active`, raise `confidence` to 0.7–0.9, commit |
| **Update** | Content is partially correct | Edit claims, update `confidence`, keep `status: draft` if still incomplete, commit |
| **Resolve contradiction** | Page has open question from ingest | Verify conflicting claims, update `claims[]`, remove open question, adjust `confidence`, commit |
| **Defer** | Cannot verify now | Leave as-is, add a dated note in body; skip for this session |
| **Flag for deletion** | Page is redundant or wrong | Set `status: archived`, lower `confidence` to 0.1, add `superseded_by` if applicable, commit |

### 3d. Resolve contradictions (when applicable)

When a page has an open question flagged during ingest:
1. Read the source page cited in the open question (`wiki_content_read`)
2. Compare the conflicting claims side by side
3. Determine which is more authoritative (recency, source type, confidence)
4. Update `claims[]` — add an entry for the resolved claim with the winning source
5. Remove the open question from the body
6. Set `confidence` to reflect the resolved state (raise if resolved, leave low if uncertain)
7. Write and commit

### 3e. Write and commit

```
wiki_content_write(slug: "<slug>", content: "<updated content>")
wiki_ingest(path: "<slug-path>")
```

### 3f. Move to the next item

## Step 4 — Report

After the session ends (queue exhausted or user stops):

```
Review session complete.

Processed: N pages
  Promoted (draft → active): N
  Updated (confidence raised): N
  Contradictions resolved: N
  Deferred: N
  Flagged for deletion: N

Remaining in queue: N pages
  Errors: N
  Warnings: N
  Drafts: N
  Low confidence: N

Suggested next session: start with the N Error findings.
```

## Key rules

1. **Never delete** — use `status: archived` + `superseded_by`; deletion
   removes the page from backlinks and breaks graph edges
2. **Preserve claim history** — add to `claims[]`, do not replace existing
   entries; both the old and new versions should be visible
3. **Defer is valid** — add a dated reason, move on; the queue rebuilds next
   session from current field values
4. **One page at a time** — finish each review decision before starting the
   next; do not batch writes
5. **Confirm borderline promotions** — if `confidence` would jump from < 0.4
   to ≥ 0.7, confirm with the user before writing
