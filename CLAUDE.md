# CLAUDE.md — house rules

Repo-specific house rules for agents working in this repository. Created 2026-07-27
(additive; no prior file modified).

## Additive, never rewrite (enrich and merge, never overwrite)

A write path preserves prior content, adds or enriches, and only supersedes a specific
field with a cited, verifiable update — never blanket-replace, never regenerate-from-stub.

Merge-vs-overwrite contract:

1. **Read before write** — load the existing artifact; if it exists you are enriching it, not authoring it fresh.
2. **Preserve prior content** — nothing already present is dropped, truncated, or blank-replaced.
3. **Supersede one field at a time, with a citation** — update a field only on a cited, verifiable basis; record source + as-of.
4. **Never blanket-replace** — no wholesale overwrite of a record with a new generation of it.
5. **Never regenerate-from-stub** — a stub/skeleton must never win over enriched content.
6. **Move-not-delete; label-in-place** — retire/reclassify by labeling in place or archiving with a manifest.
7. **Back up with known vintage** before any destructive-looking step, and verify a snapshot's vintage before restoring.

This principle is made **enforceable, not just documented**, in this repo:
`checks/merge_not_overwrite.py` (the check), `tests/test_merge_not_overwrite.py` (unit tests,
required in CI), and `.github/workflows/merge-not-overwrite.yml` (runs the tests on every PR and
advisory-scans the diff for destructive overwrites).
