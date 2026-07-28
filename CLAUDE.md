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


<!-- ADDITIVE APPEND 2026-07-27 -- model-drift episode best practices. Do not rewrite content above this line. -->
## House Rules addendum -- Model & Verification discipline (2026-07-27, Dave; binding)

Added from the 2026-07-27 model-drift episode (the Dispatch orchestrator ran on Opus 4.8 after the fleet moved to Opus 5, undetected until a provider error; and a model was mischaracterized from its name -- "Fable 5 is cheap/fast" -- when Fable 5 is the premium apex tier). These are firmwide HARD RULES #90-#94 (see the marketplace plugin `gates/HARD_RULES.md`) and lessons L-0010..L-0014 in the fleet `LESSONS_REGISTER.md`. Owners: **Wendy** (behavioral/coaching), **Adam** (model facts + verify + drift flag), **Mafee** (infra/CTO sign-off); Ben Kim gates.

- **#90 Report active state on the first turn.** Every session, surface, loop, and job declares its RUNNING MODEL and key config (surface, account, standard/version) at STEP 0, observed not assumed, and reconciles it against the current fleet standard; a mismatch raises the drift flag. Never assume a running session inherited a standard that changed mid-session.
- **#91 A global change sweeps every surface.** Any model flip / standard change ships with a coverage checklist (harness `models.json`, plugin agents, EACH seat, the orchestrator/session, memory + every repo `CLAUDE.md`, running loops) and is not "done" until every surface is verified -- app-controlled surfaces (e.g. a live session's bound model) are explicitly flagged with the manual action, never assumed resolved.
- **#92 Never assert a model's capability/cost/tier from its name.** Verify against the routing standard / Anthropic docs / current pricing and cite it, or label `[MODEL CLAIM UNVERIFIED]`. Charter: Fable 5 = apex/orchestrator (premium), Opus 5 = hard judgment + sensitivity floor, Sonnet 5 = workers, Haiku = basic mechanical only.
- **#93 Verify before claiming; surface state, don't silently default.** No "it works / it's done / X is needed/blocked/cheap" without a fresh, timestamped read of the actual state; report a default AS a default rather than adopting it silently. Generalizes #76/#77 to model/cost/capability/config claims.
- **#94 When corrected, fix every downstream artifact.** A correction propagates to memory/register, the standard, running tasks, and repo house-rules -- additively (#89), not just the chat sentence -- then re-verify and report what changed where.

Enforceable check: the `model-report / verify-before-claim` startup check in `claude-quality-gates` (composes with the `session_model_guard` drift flag). This section is APPENDED and additive; nothing above it was modified.
