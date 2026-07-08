# Claude Quality Gates

Three reusable, model-agnostic quality-control skills for anyone building
document-producing agents with Claude (or any other LLM). They are the layers
that stand between "the model produced something" and "it is safe to ship":
independent, adversarial, checklist-driven, and configurable to your own house
rules.

These are distilled from a production advisory workflow and rewritten as generic
building blocks. Nothing here is tied to a specific brand, dataset, or business:
you supply your own checklist rules, sources, fonts, and branding, and the
mechanism does the rest.

## The three gates

| Skill | What it does | Runs when |
|---|---|---|
| [`proofreader-gate`](skills/proofreader-gate/SKILL.md) | Final adversarial quality-and-house-style gate. Reviews a finished document against a configurable checklist in a fresh context and returns `APPROVED` / `RETURNED` / `REJECTED`. | After a document is built, before it ships. |
| [`fact-consistency-gate`](skills/fact-consistency-gate/SKILL.md) | Zero-fabrication error detection. Catches wrong numbers, misspelled names, inconsistent figures, stale data, and logic gaps; verifies every empirical claim against a source. Grounded in published error science. | Before any document goes external. |
| [`clean-doc-formatter`](skills/clean-doc-formatter/SKILL.md) | House-style formatting framework for DOCX/PDF/text output. Enforces one consistent institutional look, with a mandatory PDF font-embedding gate so builds never silently substitute the wrong font. | Read first, before any document-creation skill. |

The proofreader gate and the fact-consistency gate are complementary and best run
as a **pair**: one owns format and house style, the other owns data and factual
accuracy. A format pass is not a data pass, and vice versa. Together they form a
two-part gate that a deliverable must clear before it is done.

## Design ideas worth stealing

- **Independent, adversarial verification.** A gate never authors the content it
  reviews. The reviewer runs in a *fresh context* that contains only the finished
  artifact and the rubric, never the author's prompt or reasoning. This is the
  structural fix for a model grading its own work too generously.
- **Checklist over memory.** Every gate is checklist-driven with a logged result
  per item. Self-certification without the log is not a valid pass.
- **Zero fabrication.** Every empirical claim traces to a source or it does not
  ship. Unverifiable claims are removed, qualified, or flagged, never quietly
  asserted.
- **Binary blocking gates.** A small set of objective, machine-checkable rules
  (banned glyphs, required voice, embedded fonts) that block approval on any
  failure, removing reviewer discretion from the checks that matter most.
- **Error science, not vibes.** The fact-consistency gate is built on the Swiss
  Cheese Model (Reason), checklist methodology (Gawande), statistical process
  control (Shewhart/Deming), and root-cause analysis (Ohno).

## Using these as Claude Code skills

Each skill is a self-contained `SKILL.md` with a `name` and `description` in the
frontmatter, the standard Claude Code skill format. To use them:

1. Copy the skill folders under `skills/` into your project's or plugin's skills
   directory (for example `.claude/skills/`), or into a plugin you distribute.
2. Configure the placeholders. Each skill is generic by design: fill in your own
   checklist rules, staleness thresholds, verification sources, section order,
   fonts, and branding where the skill marks a `<PLACEHOLDER>` or a "configure
   this" section.
3. Invoke a gate after your document-producing step. The gates are written to run
   as a separate, independent pass, not inline with authoring.

They also work as plain prompts or system instructions with any LLM: the content
is model-agnostic.

## Configuring for your team

None of these gates ship with opinions about *your* house style. They ship with
the *mechanism* for enforcing whatever house style you define. Start by writing
down:

- Your checklist rules and which ones are binary/blocking (proofreader gate).
- Your staleness thresholds and your list of acceptable verification sources
  (fact-consistency gate).
- Your fonts, logo, section order, and writing-convention policies
  (clean-doc-formatter).

Keep that configuration under version control so the rules only ever grow more
precise.

## License

[MIT](LICENSE). Use them, fork them, adapt them.
