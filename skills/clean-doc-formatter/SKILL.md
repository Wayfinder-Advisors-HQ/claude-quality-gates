---
name: clean-doc-formatter
description: "Clean Doc Formatter -- a house-style formatting framework for LLM-generated documents (DOCX, PDF, formatted text). Enforces one consistent, restrained, institutional look across every deliverable, and MUST be read before any document-creation skill (docx, pdf, pptx) so the house style is applied at build time rather than patched afterward. Use whenever producing a formatted document output, or when the user says 'apply our house style', 'format this like our memos', or wants output that looks consistent and institutional. Configure the placeholders to your own brand; the mechanism is the reusable part."
---

# Clean Doc Formatter

A house-style formatting framework for any team that generates documents with an
LLM. It is the layer that makes every deliverable look like it came from the same
serious, consistent hand, regardless of which skill or model produced it.

**Read this skill FIRST, before the document-creation skill (docx, pdf, pptx).**
House style applied at build time is clean; house style patched on afterward is
not. The document-creation skill handles the technical mechanics; this skill
decides what the output should look like.

Everything in angle brackets, like `<HOUSE_FONT>` or `<LOGO_PATH>`, is a
**placeholder you configure** for your own brand. The framework is generic; the
values are yours.

---

## What good formatting is for

Formatting is not decoration. A restrained, consistent format reassures the reader
that the author is serious, careful, and worth trusting. The document should feel
calm, dense in substance, easy to scan, and consistent page to page. It should not
feel like a pitch deck, a slide pasted into a document, a marketing brochure, or a
raw model export.

### Three principles

1. **Clarity over style.** No decorative formatting, no visual noise. Everything
   on the page exists to make the content easier to read and evaluate.
2. **Institutional, not marketing.** Reads like an internal analytical memo, not a
   sales pitch. Confidence comes from structure, not from emphasis or hype.
3. **Consistency equals credibility.** Every document looks the same, so readers
   know instantly where to find what they need. Consistency becomes part of the
   brand.

---

## Configuration: define your house style once

Set these in your own copy of this skill. The rest of the framework enforces
whatever you set here.

| Element | Placeholder | Guidance |
|---|---|---|
| Body font | `<HOUSE_FONT>` | One family per document. Never mix. |
| Body size | `<BODY_PT>` | A single consistent size (commonly 10-11pt). |
| Heading size / weight | `<HEADING_PT>` | Larger, bold, left-aligned; one step above body. |
| Heading color | `<HEADING_COLOR>` | One color. Avoid multi-color heading systems. |
| Page size / margins | `<PAGE>`, `<MARGIN>` | Consistent on every page. |
| Logo file | `<LOGO_PATH>` | A single brand mark; see the logo rules below. |
| Logo locked ratio | `<LOGO_W>:<LOGO_H>` | Measure it once; always derive height from width. |
| Section order | `<SECTION_ORDER>` | Define the canonical order for each document type. |

Keep this configuration under version control. When it changes, every document
inherits the change from one place.

---

## Logo rules (mechanism, not a specific mark)

A logo is a signature, not a headline. The rules below prevent the two failure
modes that ship most often: a distorted logo, and text printing on top of it.

- **Position:** header, one consistent corner, on every page.
- **Size:** small enough to read as a signature, not a banner.
- **Lock the aspect ratio.** Measure your logo's true pixel ratio once
  (`<LOGO_W>:<LOGO_H>`) and **always derive height from width**:
  `height = width / (LOGO_W / LOGO_H)`. Never set width and height
  independently, never free-scale, never stretch to fill a cell. A visibly
  squished or stretched logo is a hard fail. In reportlab, pass
  `preserveAspectRatio=True` and the derived height; in Word, lock the picture's
  aspect ratio.
- **Clear the content frame below the logo band.** A correct ratio does not stop
  body text from riding up under the logo on continuation pages. Paint the logo in
  the page header (on every page) and start the text frame *beneath* the logo
  band, so body text can never overlap it. Verify this in QC, not by eye.
- **One image only.** Insert the logo and nothing else. Strip any images carried
  over from source documents. No watermarks, no tiling, no decorative graphics.

---

## Typography

- One font family per document. Bold is reserved for the title, section headers,
  and table headers, not sprayed through body prose. Italics are used sparingly
  (publication or product names, genuine emphasis). Underlining is avoided except
  for auto-applied hyperlinks.
- Body prose is set at one consistent size with comfortable line spacing and a
  little space after each paragraph. Headings are one clear step larger, bold, and
  left-aligned. No oversized or centered titles, no decorative rules.

---

## Structure and section hierarchy

- **Define a canonical section order per document type** (`<SECTION_ORDER>`) and
  apply it every time. A predictable order is itself part of the house identity:
  readers learn where things live. The framework enforces *consistency* of order;
  the specific order is yours to define.
- Section headers: bold, one consistent size, left-aligned, no numbering, no
  dividers, no all-caps, no decorative elements.
- If a section would contain only placeholders or dashes, omit it entirely rather
  than shipping an empty shell.
- Never strand a section heading at the bottom of a page. Turn on "keep with next"
  and widow/orphan control.

---

## Body content

- Prose does the work: full sentences and developed paragraphs, not slide
  fragments. Bullets are not the default mode; overusing them makes a document
  feel light and presentation-oriented.
- Controlled density. Dense in substance, but with enough white space to stay
  scannable. A little white space is useful; large random gaps are not.
- Minimal inline emphasis. Do not bold phrases inside every paragraph.

---

## Tables

Tables are analytical instruments, not decoration.

- Use **real** tables (actual Word/PDF tables), never screenshots or
  tab-aligned text pretending to be a table.
- Borders: thin, single-line, consistent. Shading: little to none, at most a
  light neutral fill on the header row. No heavy boxes, no zebra striping, no
  brand-color fills.
- Alignment: text left-aligned, numbers right-aligned, dates consistent. Same font
  family as the body.
- Header row: bold, and repeated on each page if the table spans pages. Never
  strand a header row at the bottom of a page.

### Data integrity (critical)

- Reproduce every number **exactly** as sourced. Never round, estimate, or
  reinterpret a figure while formatting it.
- Map every column against its source before export. No column drift from
  half-structured source text.
- Keep number formats consistent (one convention for currency, one for
  percentages, one for multiples/ratios). No mixed-metric cells.

---

## House-style policies (configurable)

Most teams standardize a few writing conventions so every document reads the same.
These are **choices you configure**, not universal rules. Decide each one, write it
down, and enforce it the same way every time. Common categories:

- **Number policy:** e.g. numerals vs. spelled-out numbers, and how percentages,
  currency, and ratios are written.
- **Punctuation policy:** e.g. which dashes or glyphs are allowed, quotation
  conventions.
- **Name policy:** e.g. full name on first mention and a short form thereafter;
  whether first-name-only references are allowed; whether to omit a person whose
  full identity cannot be confirmed rather than guess.
- **Voice policy:** e.g. institutional third-person vs. first-person; whether
  judgments are attributed to the organization or to a named individual.
- **Emphasis policy:** how sparingly bold/italic are used.

Whatever you choose, record it in your configuration so the proofreader gate can
enforce it as a binary check.

---

## DOCX generation

- If building from HTML, use only simple tags (`<p>`, `<strong>`, `<table>`,
  `<tr>`, `<td>`, `<th>`). Avoid CSS classes and complex nested structures.
- Strip all images from source documents automatically; insert only your own
  configured logo.
- Define a small set of named paragraph/table styles programmatically (a body
  style, a heading style, a title style, a table-header style, a table-body style,
  a footer style) so formatting is applied by style, not ad hoc per element.

---

## PDF generation: mandatory font embedding

This is the single most valuable portable lesson in this skill.

**The failure mode:** PDFs are often generated in a sandbox or CI environment that
does **not** have your house font installed. If you do not explicitly register and
embed the font, the PDF engine silently substitutes a default (a generic serif or
Helvetica/Times), and an off-brand PDF ships without anyone noticing.

**The rule:** every PDF must explicitly register and embed the house font from a
font file you ship with the build, then **verify** the embedded font before the
document is considered done. Never rely on the engine's default, and never accept
a silent substitution.

Pattern (reportlab shown; the principle applies to any engine):

```python
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Point this at the folder holding YOUR licensed house font files.
# Use an env var so CI and local builds resolve it the same way.
FONTS_DIR = os.environ.get("HOUSE_FONTS_DIR", "./fonts")
HOUSE_FONT = "<HOUSE_FONT>"   # e.g. the family name you register below

def register_house_fonts():
    pdfmetrics.registerFont(TTFont(HOUSE_FONT, os.path.join(FONTS_DIR, "<HOUSE_FONT>-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(HOUSE_FONT + "-Bold", os.path.join(FONTS_DIR, "<HOUSE_FONT>-Bold.ttf")))

def assert_house_font(pdf_path):
    """QC gate: raise unless every embedded font in the PDF is the house font.
    Inspect embedded fonts with pypdf or the `pdffonts` utility and compare
    against HOUSE_FONT. An off-font PDF must FAIL the build and regenerate."""
    ...

register_house_fonts()   # REQUIRED before building the document
# ... build the PDF using HOUSE_FONT for body and HOUSE_FONT + "-Bold" for headings ...
assert_house_font("output.pdf")   # MANDATORY -- fail and rebuild if it does not pass
```

Notes:

- **Ship your own font files** with the build, and only fonts you are licensed to
  redistribute. This framework does not include any font; supply your own under
  `HOUSE_FONTS_DIR`.
- If the environment cannot reach the fonts folder, fix the path. **Never** resolve
  a missing-font error by allowing substitution.
- The build must fail on the font-verification check and regenerate. An off-font
  PDF cannot pass sign-off.

---

## Quick QC checklist

Before any document is considered done:

- [ ] Logo present, correct corner, small, no other images, no repetition.
- [ ] Logo at its locked aspect ratio (height derived from width) -- not stretched
      or squished. Verify the rendered ratio.
- [ ] No text overlaps the logo on any page (content frame starts below the logo
      band). Verify programmatically; a correct ratio alone is not enough.
- [ ] PDF embeds the genuine house font -- not a silent substitute. Run the
      font-verification gate.
- [ ] One font family only; body and headings at their configured sizes.
- [ ] Sections in the configured order; headings attached to the content below
      them; no stranded headings; no empty placeholder sections.
- [ ] Tables are real tables, header row repeated across pages, columns mapped to
      source, numbers reproduced exactly, alignment and units consistent.
- [ ] No broken page breaks, no awkwardly split table rows.
- [ ] Footer consistent (e.g. page number only, if used).
- [ ] Configured house-style policies (numbers, punctuation, names, voice)
      applied consistently throughout.
- [ ] No images or residue carried over from source documents; no raw markdown
      artifacts (stray pipes, asterisks) and no raw URLs in body text.

---

*Generic, model-agnostic formatting framework. Configure the placeholders to your
own brand and supply your own logo and licensed fonts; the framework, the
aspect-ratio and overlap rules, the real-tables discipline, and the mandatory
font-embedding gate are the reusable core.*
