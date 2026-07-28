#!/usr/bin/env python3
"""
model_report_check.py -- enforceable startup check for HARD RULES #90 / #93
(Wayfinder model-drift episode, 2026-07-27). Model-agnostic, stdlib-only.

Two gates, both fail-closed:

  (1) REPORT-ACTIVE-STATE (#90): every session/surface/loop must declare the model
      it is ACTUALLY running on turn 1, and that reported model must be reconciled
      against the fleet's current required model. An empty/undetected running model
      FAILS. A running-model != required-model mismatch is DRIFT and FAILS (surface
      it, never swallow it). This mirrors and composes with the fleet drift flag
      (wayfinder-os lib/session_model_guard.py + router_live.current_session_model()).

  (2) VERIFY-BEFORE-CLAIM / SURFACE-DON'T-DEFAULT (#93): a state/capability/cost claim
      ("it works", "it's done", "X is cheap/free/blocked/needed/available") is UNVERIFIED
      unless it carries an evidence token (a timestamped "as of ...", "verified", a source
      citation, or an explicit [UNVERIFIED] label). Name-based model-tier claims
      ("fable is cheap/fast") are flagged for #92.

Exit code 0 = pass, 1 = fail. Intended to run at session start and in CI on a claim log.
"""
from __future__ import annotations
import argparse, json, os, re, sys

# Claims that assert current state/capability/cost and therefore need evidence (#93).
_CLAIM_PAT = re.compile(
    r"\b(it works|works now|is done|it's done|already done|"
    r"is (?:cheap|free|fast|expensive|premium|blocked|unblocked|needed|not needed|available|unavailable|impossible)|"
    r"can't be done|cannot be done|no longer needed)\b",
    re.I,
)
# Evidence tokens that discharge the verify-before-claim requirement.
_EVIDENCE_PAT = re.compile(
    r"(as of\s+\d|verified|confirmed via|per (?:the )?(?:doc|docs|pricing|routing standard|"
    r"router|api|outlook|granola|listing|registry)|\[unverified\]|\[model claim unverified\]|"
    r"source:|https?://)",
    re.I,
)
# Name-based model claims (#92): a model name adjacent to a tier/cost word, no citation.
_NAME_TIER_PAT = re.compile(
    r"\b(fable|opus|sonnet|haiku)\b[^.\n]{0,40}\b(cheap|expensive|fast|slow|premium|"
    r"cheapest|light(?:weight)?|budget|top[- ]?tier|best|routing)\b",
    re.I,
)


def running_model(explicit: str | None = None) -> str:
    """The model the session is ACTUALLY on. Explicit arg wins; else env; else ''."""
    if explicit:
        return explicit.strip()
    for k in ("WF_SESSION_MODEL", "CLAUDE_MODEL", "ANTHROPIC_MODEL", "MODEL_ID"):
        v = os.environ.get(k)
        if v:
            return v.strip()
    return ""  # undetected -> fails #90 (report-active-state)


def report_active_state(reported: str, required: str) -> dict:
    """#90 gate. reported = model the session says/observes it is running;
    required = fleet current required model (the standard)."""
    reported = (reported or "").strip()
    required = (required or "").strip()
    if not reported:
        return {"gate": "report_active_state", "ok": False,
                "violation": "no_turn1_model_report",
                "reason": "running model not reported/detected on turn 1 (#90); empty actual fails",
                "report_line": None}
    drift = bool(required) and (reported != required)
    return {
        "gate": "report_active_state",
        "ok": not drift,
        "reported_model": reported,
        "required_model": required or None,
        "drift": drift,
        "violation": "model_drift" if drift else None,
        "reason": (f"DRIFT: running '{reported}' != required '{required}' -- raise drift flag (#90/#91)"
                   if drift else "running model reported and matches required standard"),
        "report_line": f"[turn-1 model report] running={reported}"
                       + (f" required={required} {'DRIFT' if drift else 'OK'}" if required else " (no required standard supplied)"),
    }


def verify_before_claim(text: str) -> dict:
    """#93 gate over a chunk of claim text; also flags #92 name-based model claims."""
    text = text or ""
    unverified = [m.group(0) for m in _CLAIM_PAT.finditer(text)] if not _EVIDENCE_PAT.search(text) else []
    name_tier = [f"{m.group(1)} {m.group(2)}" for m in _NAME_TIER_PAT.finditer(text)]
    name_tier = [] if _EVIDENCE_PAT.search(text) else name_tier
    ok = not unverified and not name_tier
    return {
        "gate": "verify_before_claim",
        "ok": ok,
        "unverified_state_claims": unverified,     # #93
        "name_based_model_claims": name_tier,       # #92
        "reason": ("state/capability claim without a fresh, timestamped/cited read (#93) "
                   "or a model tier/cost claim from the name (#92)" if not ok
                   else "no unverified state or name-based model claim found"),
    }


def run(reported: str, required: str, claim_text: str = "") -> dict:
    g1 = report_active_state(reported, required)
    g2 = verify_before_claim(claim_text) if claim_text else {"gate": "verify_before_claim", "ok": True, "skipped": True}
    return {"ok": g1["ok"] and g2["ok"], "checks": [g1, g2]}


def main() -> int:
    ap = argparse.ArgumentParser(description="HARD RULE #90/#92/#93 model-report + verify-before-claim check")
    ap.add_argument("--reported-model", default=None, help="model the session is actually running (else env)")
    ap.add_argument("--required-model", default=os.environ.get("WF_REQUIRED_MODEL", ""),
                    help="fleet current required model / standard")
    ap.add_argument("--claim-text", default="", help="claim text (or a claim log) to scan for #92/#93")
    ap.add_argument("--claim-file", default=None, help="path to a file of claim text to scan")
    args = ap.parse_args()
    claim = args.claim_text
    if args.claim_file and os.path.isfile(args.claim_file):
        claim += "\n" + open(args.claim_file, encoding="utf-8").read()
    res = run(running_model(args.reported_model), args.required_model, claim)
    print(json.dumps(res, indent=2))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
