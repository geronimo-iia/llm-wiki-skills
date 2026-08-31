---
name: migrate
description: >
  Guided migration to remove redundant stock schema copies from registered
  wikis after upgrading to 1.0.0. Runs dry-run preview, explains kept custom
  files, confirms before deletion, and commits changes per wiki.
type: skill
status: active
last_updated: "2026-08-26"
when_to_use: >
  After upgrading llm-wiki to 1.0.0, when a wiki was created with a previous
  version and has stock schema copies in its schemas/ directory that are now
  redundant under the overlay model.
tags: [migrate, schemas, upgrade]
owner: jguibert@gmail.com
compatibility: "llm-wiki >= 1.0.0"
---

## migrate

Remove redundant stock schema copies left by pre-1.0.0 wiki creation.
Since 1.0.0, the overlay model serves embedded schemas as defaults; on-disk
copies in `schemas/` are only needed for genuine user customisations.

### Step 1 — Determine scope

If the user provided a wiki name when invoking the skill, use that name for
all subsequent calls (`wiki=<name>`). Otherwise ask:

> "Migrate all registered wikis, or a specific one? (Reply with a wiki name
> or 'all'.)"

Wait for the answer. Use `wiki=<name>` for a specific wiki, or omit `wiki`
(targeting all) for 'all'.

### Step 2 — Dry-run preview

Call `wiki_migrate` with `dry_run=true` and the scope from Step 1.

Parse the JSON result. Categorise the response:

- **All already clean** (`already_clean=true` for every wiki): inform the user
  — nothing to do — and stop here.
- **Deletions pending**: one or more wikis have non-empty `deleted`.
- **Custom overrides present**: one or more wikis have non-empty `kept_custom`.

### Step 3 — Get wiki paths

Call `wiki_spaces_list` (no arguments if scope is all; pass `name=<name>` if
scoped). Parse the result into a name→path map. You will need these paths for
git commits in Step 7.

### Step 4 — Present the report

Show a clear summary for each wiki. Example format:

```
Wiki: research
  Would delete (stock copies):  concept.json, base.json
  Kept (custom overrides):      mytype.json
  already_clean: false

Wiki: notes
  already_clean: true  — nothing to do
```

If `kept_custom` is non-empty for any wiki, add this explanation:

> "Files listed under 'Kept (custom overrides)' differ from every known stock
> version. They are genuine customisations and will NOT be touched. After
> migration they continue to work as overrides on top of the embedded defaults."

Then, for each kept custom schema file, open it and check whether it defines
any of the following fields. If so, verify the field includes `"x-keyword": true`:

| Field | Present in stock schema |
|---|---|
| `type` | `base.json`, `concept.json`, `doc.json`, `paper.json`, `section.json` |
| `last_updated` | `base.json` |
| `tags` | `base.json` |
| `aliases` | `concept.json` |

In 1.0.0, `base.json` added `"x-keyword": true` to `type`, `last_updated`,
and `tags`; derived schemas (`concept`, `doc`, `paper`, `section`) added it
to `type`. Custom schemas are standalone overlays — they do **not** inherit
annotations from base automatically. A custom schema that defines `type`
without `"x-keyword": true` will not be keyword-indexed.

For each missing annotation, apply the fix inline:

```json
"type": {
  "type": "string",
  "x-keyword": true,
  "description": "Page type from registry"
}
```

After patching, ask the user to confirm the changes look correct, then commit
the updated custom schemas with:
```bash
git -C "<wiki-path>" add schemas/
git -C "<wiki-path>" commit -m "fix: add x-keyword annotations to custom schemas for 1.0.0 compatibility"
```

Then call `wiki_index_rebuild` for the affected wiki (pass `name=<wiki-name>`).
The index must be rebuilt so keyword fields take effect — without this, pages
already ingested will not be searchable by the newly annotated fields.

### Step 5 — Confirm before proceeding

Ask:

> "Delete the stock schema copies listed above? These files are identical to
> the embedded defaults and are safe to remove. The overlay model will serve
> the embedded versions automatically. (yes/no)"

If the user answers anything other than 'yes', abort and inform them no
changes were made.

### Step 6 — Live migration

Call `wiki_migrate` with `dry_run=false` and the same scope as Step 1.

Verify the result against the dry-run: for each wiki, `deleted` should match
what the dry-run reported. If the live result has fewer deletions than the
dry-run (a file vanished between dry-run and live run), report the discrepancy
clearly — state which files were expected, which were actually deleted, and
that the remaining stock files were not removed. Do not stop silently; the
filesystem state has already changed for the files that were deleted.

### Step 7 — Commit per wiki

For each wiki where `deleted` is non-empty:

1. Look up the wiki's filesystem path from the name→path map built in Step 3.
2. Run both commands with `-C "<path>"` so they execute inside the wiki repo,
   not the llm-wiki engine repo:
   ```bash
   git -C "<path>" add schemas/
   git -C "<path>" commit -m "chore: remove redundant stock schema copies"
   ```
3. Report the commit hash.

Skip wikis where `deleted` was empty (nothing to commit).

### Step 8 — Summary

Report the final outcome:

```
Migration complete.
  research:  deleted 2 files, committed <hash>
  notes:     already clean — no changes
```
