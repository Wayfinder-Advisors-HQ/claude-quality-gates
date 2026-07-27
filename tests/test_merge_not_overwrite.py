"""Tests for the merge-not-overwrite check (enrich and merge, never overwrite)."""
from checks.merge_not_overwrite import check_merge_not_overwrite


def test_new_artifact_is_additive():
    assert check_merge_not_overwrite("", "brand new content\nline two\n").ok


def test_blank_overwrite_fails():
    assert not check_merge_not_overwrite("alpha\nbeta\ngamma\n", "   \n").ok


def test_stub_regression_over_enriched_fails():
    old = (
        "---\ntype: profile\nname: Acme\nowner: alice\n---\n\n"
        "enriched body line one\nenriched body line two\nenriched body line three\n"
    )
    new = "---\n---\n"
    assert not check_merge_not_overwrite(old, new).ok


def test_frontmatter_key_drop_fails():
    old = "---\ntype: x\nowner: alice\nas_of: 2026-07-27\n---\nbody line\n"
    new = "---\ntype: x\n---\nbody line\n"
    assert not check_merge_not_overwrite(old, new).ok


def test_enrich_append_passes():
    old = "line1\nline2\nline3\n"
    new = "line1\nline2\nline3\nline4 (enriched, cited)\n"
    r = check_merge_not_overwrite(old, new)
    assert r.ok and r.retained_ratio == 1.0


def test_field_level_supersede_passes():
    old = "\n".join(f"fact {i}" for i in range(10)) + "\nprice: 100 (2026-01)\n"
    new = "\n".join(f"fact {i}" for i in range(10)) + "\nprice: 120 (2026-07, cited)\n"
    assert check_merge_not_overwrite(old, new).ok


def test_blanket_replace_fails():
    old = "\n".join(f"line{i}" for i in range(10)) + "\n"
    new = "line0\nline1\n"
    assert not check_merge_not_overwrite(old, new).ok
