"""Tests for the model-report / verify-before-claim check (HARD RULES #90/#92/#93,
Wayfinder model-drift episode 2026-07-27). Enrich-and-merge: this file was ADDED."""
from checks.model_report_check import report_active_state, verify_before_claim, run


def test_no_turn1_report_fails():
    r = report_active_state("", "claude-opus-5")
    assert r["ok"] is False and r["violation"] == "no_turn1_model_report", r


def test_drift_fails_and_surfaces():
    # The exact 2026-07-27 episode: session on Opus 4.8 after fleet moved to Opus 5.
    r = report_active_state("claude-opus-4-8", "claude-opus-5")
    assert r["ok"] is False and r["drift"] is True, r
    assert "DRIFT" in r["report_line"], r


def test_on_standard_passes():
    r = report_active_state("claude-opus-5", "claude-opus-5")
    assert r["ok"] is True and r["drift"] is False, r


def test_unverified_state_claim_flagged():
    r = verify_before_claim("The pipeline works now and the connector is free.")
    assert r["ok"] is False and r["unverified_state_claims"], r


def test_verified_state_claim_passes():
    r = verify_before_claim("Verified as of 2026-07-27 14:03: the pipeline works (source: run log).")
    assert r["ok"] is True, r


def test_name_based_model_claim_flagged():
    # The exact 2026-07-27 mischaracterization: "Fable 5 is cheap/fast for routing".
    r = verify_before_claim("Fable is cheap so use it for routing.")
    assert r["ok"] is False and r["name_based_model_claims"], r


def test_cited_model_claim_passes():
    r = verify_before_claim("Per the routing standard, Fable 5 is premium/apex.")
    assert r["ok"] is True, r


def test_run_combined_fails_on_drift_and_bad_claim():
    res = run("claude-opus-4-8", "claude-opus-5", "it works")
    assert res["ok"] is False, res
