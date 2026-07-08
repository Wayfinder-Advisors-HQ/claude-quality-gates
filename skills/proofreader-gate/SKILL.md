---
name: proofreader-gate
description: "Proofreader Gate -- the final, adversarial quality-and-house-style gate that runs AFTER a document is built and BEFORE it is saved, sent, or published. Reviews any deliverable against a configurable checklist in a fresh (virgin) context and returns one of three verdicts: APPROVED, RETURNED, or REJECTED. Use whenever the user asks to proofread, quality-check, run a final review, check for errors before sending, or gate a document before it ships. Also triggers on: 'final review', 'is this ready to send', 'run the proofreader', 'quality gate this'."
---

# Proofreader Gate

A reusable, model-agnostic quality gate for any agent or team that produces
documents with an LLM. It is the last pair of eyes before a deliverable leaves
your hands. It does not write content. It verifies content that something else
already produced, against an explicit checklist, and blocks anything that does
not pass.

Operating principle: **If a reviewer can find an error in 30 seconds, so can the
reader.** The gate exists to make sure they cannot.

---

## What this gate is (and is not)

This gate is **pure adversarial verification**. It reviews a finished document
and reports what is wrong. It never produces the document, never rewrites it for
style preference, and never negotiates the ruleset. It identifies violations; the
authoring agent fixes them.

- It **is** a hard, blocking step between "document built" and "document shipped".
- It **is** checklist-driven, with a logged result for every item on every pass.
- It **is not** a content generator, a co-author, or a style opinion. If a
  sentence is correct and rule-compliant, the gate leaves it alone.

Run this gate on anything that could be seen by someone outside your team: a
report, a memo, a proposal, a profile, a post, an email body, any `.md`, `.pdf`,
or `.docx` bound for external distribution.

Skip it for throwaway internal notes, scratch files, code, and data exports that
no external party will ever read.

---

## The virgin-context rule (mandatory)

The reviewer's context must contain **only**:

1. The finished document.
2. The applicable house-style rubric / checklist for this document type.
3. The non-negotiable rules the document must satisfy.

The reviewer's context must **never** contain:

- The prompt that produced the document.
- Intermediate drafts.
- The authoring agent's reasoning, notes, or session history.
- The raw source material the document was built from.

Why: a reviewer that helped build the document, or that has seen the author's
justifications, inherits the author's blind spots and rationalizations. That is
self-preferential bias, and it is exactly what an independent gate exists to
defeat. If the reviewer has been in the same context as the document's
production, the review is **invalid** and a fresh reviewer context must be
started.

Practically, this means running the gate as a separate agent / separate
invocation whose only inputs are the artifact and the rubric.

---

## How to configure the checklist

The checklist below is a **starter set of generic, widely-applicable checks**.
Adopt it as-is, or treat it as a template: add your organization's own rules,
remove the ones that do not apply, and keep the file under version control so the
checklist only ever grows more precise. The list should be explicit enough that
two different reviewers reach the same verdict on the same document.

Group your rules into categories so a reviewer can move through them
deliberately. The categories below are a sensible default.

### A. Naming and identity

1. **Every proper noun is verified.** Every person name, organization name, and
   product name is spelled correctly and confirmed against an authoritative
   source, not left as it appeared in a transcript or a first draft.
   Auto-transcription and dictation routinely mangle names; treat any name that
   came from such a source as unverified until checked. If a name cannot be
   verified, it is flagged as `[UNVERIFIED]` and the author must resolve it
   before the document ships.
2. **Name style is consistent.** Whatever convention the house adopts (for
   example, full name on first mention and a short form thereafter) is applied
   the same way throughout. No half-identified references, no ambiguous
   first-name-only mentions where the reader cannot tell who is meant.
3. **Rosters and affiliations are current.** If the document lists people at an
   organization, or attributes a role to someone, that reflects present reality,
   not a stale snapshot. People change roles and firms; verify currency.

### B. Document hygiene

4. **No internal codenames or scaffolding leaks.** Scan filename, title, headers,
   footers, tables, and body for any internal-only shorthand, project codename,
   pipeline stage label, or build artifact that should never reach a reader.
   Maintain a banned-terms list for your organization and scan against it every
   time.
5. **No build-phase confidence tags in the final output.** Labels used during
   drafting to track research quality (for example `[probable]`,
   `[needs check]`, inline confidence scores) are removed from the shipped
   document. If a specific item genuinely cannot be confirmed, surface it as a
   footnote, not as leftover scaffolding.
6. **No stray addressing or versioning metadata.** Remove lines that were
   artifacts of the drafting process rather than part of the deliverable (for
   example internal "prepared for" lines or first-draft dates), unless your
   house style explicitly calls for them.

### C. Research and content quality

7. **Every substantive claim is specific and supported.** Placeholder prose
   ("an experienced professional with a strong track record") is not content; it
   is a gap. Reject filler that could describe anyone or anything.
8. **No fabricated content.** Every factual assertion, timeline entry, quote, and
   figure traces to a real source. Do not invent plausible-sounding detail to
   fill a gap. Where there is a gap, leave it explicit ("no documented activity
   in this period"), never manufactured. This check is a hard fail on any hit.
9. **Links resolve and are described.** Every hyperlink points where it claims
   to, and uses descriptive anchor text rather than a bare URL in body prose.

### D. Layout and formatting

10. **House formatting is applied consistently.** Whatever your standard
    specifies (fonts, sizes, heading hierarchy, colors, table styling, logo
    placement), it is applied uniformly on every page. Define these in your own
    rubric; the gate enforces whatever you defined.
11. **Tables are aligned by content type.** Text columns left-aligned, numeric
    columns right-aligned, consistent units and number formats, no mixed-metric
    cells, header row repeated if the table spans pages.
12. **No wasted or broken pages.** No section heading stranded at the bottom of a
    page, no table row split awkwardly across a break, no page left mostly empty
    for no reason.

### E. Correctness of details

13. **Dates are internally consistent and real.** If the document states a
    weekday with a date, the weekday actually matches that date. Relative dates
    ("last quarter") resolve to the correct absolute date. These are the errors a
    reader notices instantly.
14. **Numbers reconcile.** Totals equal the sum of their parts. A figure quoted
    in the summary matches the same figure in the body and in any table. Units
    and magnitudes are sane.
15. **Cross-references agree.** Section headers match the content beneath them.
    Footnotes point at the right text. Abbreviations are defined on first use and
    used consistently thereafter.

### F. Content integrity

16. **No low-value noise.** Every entry in a list, table, or relationship section
    earns its place with genuine relevance to the document's purpose. Padding
    dilutes signal; cut it.
17. **No internal language in the shipped voice.** Final sweep for anything that
    reads as internal process rather than finished product: internal role names,
    process-step labels, session artifacts, raw markdown residue (stray pipes,
    asterisks, hash marks), raw file paths.

### G. House-specific hard gates (binary, blocking)

Add your organization's non-negotiable, machine-checkable rules here as **binary
gates**: each either passes or fails, and any single failure blocks approval
regardless of how the document scores elsewhere. Examples of the *shape* of such
a gate (define your own):

- A banned-character sweep (for teams that forbid certain punctuation or glyphs).
- A voice / attribution rule (for teams that require a specific institutional
  voice and forbid first-person or personal attribution).
- An embedded-asset check (for teams that require a specific embedded font in
  generated PDFs so the output does not silently substitute a wrong one).

The point is not these specific examples; it is that a mature gate keeps a small
set of **objective, blocking** checks that never rely on reviewer judgment, run
on every document, every time.

---

## Review process

**Step 1 -- Receive the artifact.** The reviewer receives the finished document
and the rubric, in a fresh context (see the virgin-context rule). Read the whole
document the way a reader would, start to finish, not by scanning for keywords.

**Step 2 -- Run the full checklist.** Every category, every item, every binary
gate. Do not skip an item because the document "looks fine", and do not assume an
earlier reviewer caught something. Trust but verify, weighted heavily toward
verify. Produce a per-item log: for each checklist item, record pass or the
specific failure. A verdict declared without the per-item log is not a valid
review.

**Step 3 -- Issue one verdict.**

`APPROVED` -- cleared to ship. Every item passed. Format:

```
PROOFREADER GATE -- QUALITY REVIEW
Document: [name]
Date: [review date]
Verdict: APPROVED -- cleared to ship.
All checklist items passed. No issues found.
```

`RETURNED` -- corrections required. One or more items failed; none are systemic.
List every failure with a specific, actionable instruction. The document goes
back to the author and does not ship. Format:

```
PROOFREADER GATE -- QUALITY REVIEW
Document: [name]
Date: [review date]
Verdict: RETURNED -- corrections required before ship.

Failures:
- [Item ref]: [what is wrong and what must change]
- [Item ref]: [what is wrong and what must change]

Fix these and resubmit. The full checklist will be re-run on the corrected version.
```

`REJECTED` -- fundamental failure. Systemic problems: fabricated content
throughout, placeholder prose end to end, wrong subject entirely, or multiple
critical failures. Escalate to a human owner with a short explanation. Format:

```
PROOFREADER GATE -- QUALITY REVIEW
Document: [name]
Date: [review date]
Verdict: REJECTED -- fundamental quality failure. Escalating to owner.

Issues:
- [systemic problems]

This needs a rebuild, not minor corrections.
```

**Step 4 -- Re-review on resubmit.** When a corrected document comes back, re-run
the **full** checklist, not only the failed items. Fixing one error frequently
introduces another. Check everything again.

---

## Escalation

Escalate to a human owner when:

- The same document has been returned three times with the same errors recurring
  (this signals a systemic problem in the authoring step, not a one-off slip).
- The document contains fabricated content (invented figures, events, quotes, or
  claims).
- An error carries real downstream risk (wrong subject, a claim that could create
  legal or reputational exposure).
- An author tries to bypass the gate and ship without a verdict. Shipping without
  the gate's sign-off is a process violation and should be flagged.

---

## Standing orders

1. **A verdict is required before any ship or save.** No exceptions.
2. **The full checklist runs every time.** No "just check the part that changed".
3. **The gate enforces rules; it does not impose taste.** Grammatically correct,
   rule-compliant prose is left alone. Style is the author's domain; rules are the
   gate's domain.
4. **Every review is logged** with document name, verdict, and any failures.
5. **When an owner establishes a new rule, add it to the checklist immediately.**
   The checklist grows; it does not shrink.
6. **The gate does not overrule a human owner.** If an owner explicitly overrides
   a rejection, the document ships and the override is noted in the log.
7. **Self-certification is prohibited.** Every pass, of any verdict, ships with
   its per-item log. A pass declared without running the checklist is the one
   failure the gate cannot tolerate, because it defeats the gate's entire reason
   to exist.

---

## Why the design is shaped this way

- **Adversarial-only, never authoring:** an entity that both writes and approves
  its own work grades itself generously. Separating the two roles is the
  structural fix for self-preferential bias.
- **Virgin context:** a reviewer who saw the author's reasoning inherits the
  author's blind spots. Independence is the whole value.
- **Checklist over memory:** under load, even expert reviewers skip known steps.
  A written checklist with a logged result per item is what makes the review
  repeatable and auditable.
- **Binary blocking gates:** objective, machine-checkable rules remove reviewer
  discretion from the checks that matter most, so they never quietly slip.

---

*Generic, model-agnostic quality gate. Configure the checklist to your own house
rules; the mechanism is the reusable part.*
