---
name: fact-consistency-gate
description: "Fact & Consistency Gate -- a zero-fabrication error-detection layer for LLM-produced documents. Catches wrong numbers, misspelled names, inconsistent figures, broken links, stale data, logic gaps, and unsupported claims by running a structured checklist and verifying every empirical claim against a source. Use whenever the user asks to fact-check, verify, cross-check, validate data, catch errors, sanity-check, or QA a document before it goes out. Also triggers on: 'is this right', 'double check this', 'verify the numbers', 'catch my mistakes', 'ready to send?', 'cross-reference this'."
---

# Fact & Consistency Gate

A model-agnostic error-detection layer for any pipeline that produces documents
with an LLM. It is the last resolution check before a deliverable goes external:
the layer that looks at the granular level where errors actually live -- a
transposed digit, a name that does not match its source, a total that does not
add up, a 2023 figure presented as current.

Its discipline is not intuition. It is built on published error science, and it
holds one non-negotiable line: **zero fabrication**. Every empirical claim traces
to a source, or it does not ship.

---

## I. Role

This gate does one thing: find the errors everyone else missed, because it is
looking at a different resolution than the reviewers focused on content, strategy,
or narrative. A wrong number, a misspelled name, or an inconsistent data point can
destroy credibility in a single reading. This gate is the defense against that.

It is diagnostic, not punitive. It reports errors as data points for system
improvement, never as indictments of the author. And it is fast: the checklist is
what makes it possible to be thorough and quick at the same time.

---

## II. Research foundation

The methods below are grounded in established error-science literature. This is
what makes the gate a discipline rather than a vibe.

1. **Aviation safety -- James Reason (Swiss Cheese Model).** Every defense layer
   has holes. Accidents, and document errors, occur only when the holes across
   multiple layers happen to align. Reason distinguishes *active failures* (slips
   and mistakes at the point of action) from *latent conditions* (systemic
   weaknesses that persist undetected). Non-punitive, confidential error reporting
   (as in NASA's Aviation Safety Reporting System) improves safety more than
   blame ever does.
2. **Medical error prevention -- Atul Gawande (The Checklist Manifesto).**
   Structured pause-point checklists prevent "errors of ineptitude", where the
   operator knows the right thing to do but skips it under cognitive load. The WHO
   Surgical Safety Checklist (three pause points: Sign In, Time Out, Sign Out)
   materially reduced surgical mortality in trials. Checklists are a tool for
   experts under load, not a crutch for novices.
3. **Software quality assurance -- code-review practice.** Every change needs an
   independent approval before merge. Static analysis catches errors without
   execution; dynamic analysis catches them during execution. "Shift left"
   (testing earlier) reduces the cost of fixing a defect by orders of magnitude.
4. **Editorial QA -- Chicago Manual of Style / New Yorker fact-checking.** Three
   distinct disciplines that must not be conflated: line editing (flow and
   structure), copy editing (grammar, spelling, internal consistency), and
   fact-checking (verifying every empirical claim against a primary source). The
   New Yorker's checkers place a dot over every empirical claim and clear each dot
   against a source. No claim passes undotted.
5. **Statistical process control -- Shewhart / Deming.** Control charts separate
   *common-cause* variation (inherent, stable, within tolerance) from
   *special-cause* variation (assignable, unstable, needs intervention). Deming's
   Point 3: "Cease dependence on inspection to achieve quality. Build quality into
   the product in the first place."
6. **Root cause analysis -- Ohno (Toyota Production System).** The Five Whys: when
   an error is found, ask "why" until you reach the systemic root rather than the
   proximate cause. Ishikawa fishbone diagrams map causes across categories
   (people, process, data, template, system, environment).

---

## III. The Swiss Cheese Model applied to document production

No single defense layer is perfect. Each layer -- author self-review, this gate,
a senior editorial review, periodic batch audits -- has holes. An error reaches
the reader only when the holes in every layer line up.

This gate's job is not to be the only defense. It is to make sure its own holes
never overlap with the holes in adjacent layers.

| Reason's category | Document-production equivalent |
|---|---|
| Organizational influences | Unclear templates, missing style guide, ambiguous sources |
| Unsafe supervision | No editorial review scheduled, batch audit skipped |
| Preconditions for unsafe acts | Author working from stale or conflicting source data |
| Active failures | Wrong name typed, number transposed, date not updated |

Common latent conditions worth reporting upstream:

- Source records not updated after a change (personnel, figures, status).
- Conflicting versions of a source document in shared storage.
- Author templates not updated after a standard changed.
- Enrichment / lookup data that has gone stale.

The gate does not just catch errors. It names the latent conditions that produced
them, so they can be fixed at the source (Deming's Point 3 in practice).

---

## IV. Error taxonomy

Classify every finding. Severity drives the document's status.

### Type A -- Critical (active failures)

Errors that directly mislead the reader. Never acceptable. A single Type A error
halts distribution.

- Wrong names (person, organization, product).
- Wrong numbers (any quantitative figure: amounts, rates, sizes, counts).
- Fabricated data (any figure or fact not traceable to a verified source).
- Wrong entity relationships (misclassifying what something is or how two things
  relate).
- Misattributed quotes or statements.
- Wrong dates on consequential events.
- Incorrect regulatory, legal, or compliance claims.

**Threshold: zero tolerance. Status = HOLD.**

### Type B -- Significant (latent conditions)

Systemic weaknesses that do not directly mislead but undermine credibility and
can enable future Type A errors.

- Inconsistencies between documents about the same subject.
- Stale data presented without a staleness disclosure.
- Conclusions unsupported by the evidence presented.
- Missing sections required by the template.
- Cross-reference failures (one document says X, another says Y).
- Source-quality degradation (citing retracted or defunct sources).
- Logic gaps (a risk flagged in the analysis but absent from the summary).
- Single-source characterization of something important, where the standard
  requires corroboration across multiple independent sources.

**Threshold: must be corrected before external distribution. Status = REVISE.**

### Type C -- Minor (common-cause variation)

Errors within the normal operating range of the system.

- Formatting inconsistencies (spacing, alignment, size).
- Minor deviations from house style.
- Spelling errors in non-critical text.
- Inconsistent capitalization or hyphenation.

**Threshold: correct if time permits, log for coaching. Status = CLEAR with notes.**

### Type D -- Cosmetic (within-tolerance drift)

Variation that does not affect readability or credibility. Logged only when it
recurs across three or more documents, as a recurrence may signal a latent
condition.

---

## V. What the gate catches

### 1. Factual errors

- **Numbers:** figures that do not match across documents or against the source;
  calculations that do not add up; sizes or counts that changed but were not
  updated; totals that do not equal the sum of their rows.
- **Names:** misspellings; wrong titles (people change roles); wrong affiliations
  (people change organizations); entity confusion (two different things with a
  similar name treated as one); ambiguous first-name-only references.
- **Entities:** wrong or outdated names; misstated parent/subsidiary or
  membership relationships; wrong classification of what something is.

### 2. Consistency errors

- **Cross-document:** does the profile match the later memo? Does the tracker
  match the summary? Are the same facts presented the same way everywhere? Do
  names taken from a transcript match the authoritative record?
- **Internal:** does the executive summary match the detailed body? Do table
  totals match their rows? Do footnotes reference the correct text? Are
  abbreviations defined on first use and used consistently after?

### 3. Formatting errors

- House-style compliance (as defined by your own standard): consistent tables,
  headings, alignment, hyphenation of compound modifiers, name conventions,
  filename conventions.
- Structural: missing or misordered sections, broken internal links, missing page
  breaks, incomplete tables.

### 4. Data currency (staleness detection)

Define staleness thresholds for each class of data you handle, and flag anything
older than its threshold. The table below is a **template** -- set the thresholds
and categories that fit your domain.

| Data class | Example threshold | Action on breach |
|---|---|---|
| Key quantitative figures | > 2 quarters old | Flag, request current source |
| Personnel / roster | > 1 quarter old | Verify against authoritative record |
| Contact information | > 1 quarter old | Verify against most recent source |
| Market / benchmark data | > 1 month old | Flag with as-of date |
| Official filings / records | > 1 year old | Request current filing |

Source-quality checks: is the data from a primary source or secondhand? Is it
cited with a date? Is the source still valid (not retracted, not defunct)?

### 5. Logic errors

- **Reasoning:** conclusions unsupported by evidence; recommendations that
  contradict the analysis; risk flags present in the analysis but missing from the
  summary; positive spin on negative data; cherry-picked comparison periods.
- **Completeness:** are all required sections present? Are all questions answered?
  Are all sources cited? Are the hard questions asked, not just the easy ones?

---

## VI. The checklist protocol (pause points)

Modeled on the WHO Surgical Safety Checklist's pause-point architecture. Each
pause forces a deliberate stop. No step is skipped because a previous reviewer
"probably caught it".

### A. Pre-external review (full protocol)

**Pause 1 -- Identity verification (Sign In)**

1. **Name check:** every proper noun verified against an authoritative record for
   correct spelling, current title, and current affiliation.
2. **Entity check:** every organization/product name verified; its type and any
   parent/membership relationships confirmed; no entity confusion.

**Pause 2 -- Data verification (Time Out)**

3. **Number check:** every figure traced to a source; calculations re-performed;
   table totals re-summed.
4. **Date check:** every date verified for accuracy and currency; staleness
   thresholds applied; anything past threshold flagged with an as-of date.
5. **Consistency check:** cross-referenced against other recent documents about
   the same subject; internal summary-vs-body consistency confirmed.

**Pause 3 -- Presentation verification (Sign Out)**

6. **Format check:** full house-style compliance per your standard.
7. **Logic check:** conclusions match evidence; recommendations supported; risk
   flags propagate to the summary; no positive spin on negative data.
8. **Link and tone check:** hyperlinks resolve; internal references resolve; tone
   is consistent and appropriate throughout.
9. **Sentence-completeness sweep:** scan for fragments, missing predicates, and
   truncated constructions that leave a thought unfinished. Any fragment is a
   HOLD until corrected.

**All nine must pass. A failure in Pause 1 or 2 = HOLD. A failure in Pause 3 = REVISE.**

### B. Internal review (abbreviated)

For documents that circulate internally only: (1) name/number spot check on
headers, tables, and summary; (2) currency check; (3) consistency check against
the latest version of referenced subjects; (4) basic format check.

### C. Batch review (periodic sampling)

Periodically sample several outputs across different authors and run the full
pre-external protocol on them. Purpose: catch systemic errors that individual
reviews miss, and detect latent conditions before their holes align. Prioritize
document types not covered in the previous sample, and any internal-only item that
could later become external.

---

## VII. Statistical process control

Track quality over time rather than heroically catching one error at a time.

Maintain a rolling error-rate chart per author or per document type: counts of
Type A / B / C per period, normalized per page. Compute a center line and control
limits. A point signals **special cause** (investigate) when it falls outside the
3-sigma limits, or when a run of consecutive points sits on one side of the
center line, or trends steadily in one direction.

- **Common-cause variation** (in control, no pattern): the system is stable.
  Improving it means changing the system (better templates, better sources,
  better prompts), not scolding an individual.
- **Special-cause variation** (a signal fired): something specific changed.
  Investigate with root cause analysis.

When a metric is out of control, work the DMAIC loop: **D**efine the specific
error type and where it concentrates, **M**easure the current rate, **A**nalyze
the root cause, **I**mprove (fix the assignable cause for special-cause; change
the system for common-cause), **C**ontrol (monitor until the improvement holds
for several periods).

Reacting to common-cause noise as if it were a signal ("tampering") makes the
system less stable, not more. Distinguish the two before acting.

---

## VIII. Fact-checking protocol (the dot method)

Adapted from the New Yorker. Place a dot over every empirical claim, and clear
each dot against a source before the document ships.

Dot every: number, name, attributed statement, factual assertion (founding date,
description, status), and comparison ("largest", "top-quartile").

Clear each dot by one of:

| Verification method | Acceptable for |
|---|---|
| Authoritative internal record | Names, titles, affiliations, contact info |
| Official filing / registry | Structural facts, status, key figures |
| Primary source (the organization's own materials) | Descriptions, composition |
| Primary conversation / transcript | Attributed statements, meeting detail |
| System-of-record data | Quantitative figures |
| Dated, named publication | Events, announcements, market data |

An unverifiable claim must be **removed**, **qualified** with explicit uncertainty
("unverified", "as of [date], per [source]"), or **flagged Type A** if it is
presented as fact without qualification. Never mark a dot cleared that was not
actually verified. Fabricated verification is itself a Type A failure.

Names taken from auto-transcription deserve special suspicion: cross-reference
every one against the authoritative record before using it. A name that appears
in a transcript but not in your records is either new (add it) or wrong (fix it).

---

## IX. Root cause analysis

Catching an error fixes one document. Finding its root cause fixes every future
document.

**Five Whys** -- worked example:

```
Error: A report listed an outdated figure for subject X.
Why 1: The author used an outdated source figure.
Why 2: The source record had not been updated.
Why 3: The periodic data-refresh task did not include subject X.
Why 4: Subject X was added to coverage after the refresh task was defined.
Why 5: There is no process to auto-enroll new coverage items in the refresh cycle.
Root cause: new coverage items are not automatically added to the refresh schedule.
Systemic fix: auto-enroll new coverage items in the refresh cycle; assign an owner to track it.
```

**Ishikawa** -- when a pattern spans multiple authors or document types, map the
causes across people, process, data, template, system, and environment to find
the shared origin.

Feed the pattern data (error frequency, recurring error types, root-cause
findings) to whoever owns coaching and to whoever owns accountability. This gate
diagnoses; it does not coach. The handoff is clean: diagnose, then someone else
coaches, then someone else tracks the fix to completion.

---

## X. Defense layers

Four layers, each with its own scope. An error reaches the reader only if it slips
through holes in all four.

1. **Author self-review** at the point of production. Cheapest, first line.
   Typical holes: content focus misses formatting; stale data used unchecked.
2. **This gate** -- full checklist verification. The primary error-catching layer.
   Typical holes: time pressure shortens the review; familiarity breeds attention
   drift. Mitigation: use the checklist, do not rely on memory.
3. **Senior editorial review** -- asks "is this the right analysis?" while this
   gate asks "are the facts correct?". Different lens, same document.
4. **Batch review** -- system-level surveillance that catches what layers 1-3
   missed and surfaces latent conditions. Any Type A found in batch review
   triggers a full review of that author's output for the period.

Multiple layers with different hole patterns is the design. This gate catching an
error in senior-approved work is not a failure of that review; it is the Swiss
Cheese Model working as intended.

---

## XI. Output format

```
# Quality Review -- [document title]

Author: [who produced it]
Document type: [type]
Date reviewed: [date]      Date produced: [date]
Review type: [Pre-external / Internal / Batch]

## Errors found

### Type A (Critical)
- Location: [section / line]
  Error: [what is wrong]
  Correction: [what is correct]
  Source: [primary source for the correction]
  Root cause: [brief]

### Type B (Significant)
- [location, error, correction]

### Type C (Minor)
- [by category: formatting, spelling, style]

### Type D (Cosmetic)
- [only if a recurring pattern is detected]

## Error summary
| Type | Count | Details |
|------|-------|---------|
| A | [n] | [brief] |
| B | [n] | [brief] |
| C | [n] | [brief] |
| D | [n] | [brief] |
| Total | [n] | in [pages] pages ([n/pages] per page) |

## Staleness flags
| Data point | As-of date | Age | Threshold | Status |
|---|---|---|---|---|

## Fact-check dots
Total empirical claims: [n]
Verified (primary): [n]   Verified (secondary): [n]   Unverifiable / flagged: [n]

## Pattern notes
[recurring patterns for coaching; latent conditions for systemic fix; Five Whys if a Type A was found]

## Verdict
[CLEAR -- approved for distribution]
[REVISE -- corrections required before distribution; list items]
[HOLD -- critical errors; fix and re-review before distribution]
```

---

## XII. Principles

1. **The error you catch saves the reputation.** One wrong name and the author
   looks careless; one wrong figure and the author looks uninformed. Detection is
   cheap; an undetected error is not.
2. **Check the check.** Do not assume previous reviewers caught everything. That
   is why multiple layers exist.
3. **Patterns beat catches.** Catching one misspelling fixes one document.
   Noticing that the same name is misspelled every time fixes every future one.
4. **Silent precision.** The best outcome is that no errors are found because the
   process was improved upstream. Build quality in; do not depend on inspection.
5. **Currency is credibility.** Stale data undermines everything around it, even
   when everything else is perfect. Date-check everything.
6. **Cross-reference, always.** Never assume one source is right. Verify every
   claim against a primary source.
7. **Non-punitive reporting.** Error reports are diagnostic, not accusatory. The
   goal is a better system, not blame.
8. **The checklist is not optional.** Experts under load skip known steps. The
   checklist is the step that catches what memory would have missed.
9. **Distinguish variation types before acting.** Treating common-cause noise as a
   signal makes the process worse.
10. **The Five Whys stop at five for a reason.** Deep enough to reach the systemic
    root, shallow enough to stay actionable.

---

## XIII. What this gate never does

- Approve a document with a Type A error, under any time pressure.
- Skip the checklist because "it is probably fine".
- Let a stale figure pass because finding the current one takes effort.
- Miss a formatting violation because the content was good.
- Assume a prior reviewer already caught it.
- Produce false positives (flagging correct information as wrong); false alarms
  erode trust in the review and cause alert fatigue.
- Slow distribution unnecessarily; the checklist makes fast-and-thorough possible.
- Coach the author directly; it diagnoses, someone else coaches.
- Blame an individual for a systemic failure.
- React to common-cause noise as if it were a special-cause signal.
- Skip batch review because "it was a quiet week"; latent conditions accumulate
  silently.
- Fabricate verification; an unverifiable claim is flagged, never marked verified
  to close the dot.

---

*Generic, model-agnostic fact-and-consistency gate. Set your own staleness
thresholds, verification sources, and house-style rules; the error science and the
protocol are the reusable core.*
