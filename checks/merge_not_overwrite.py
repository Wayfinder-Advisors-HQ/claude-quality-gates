#!/usr/bin/env python3
"""merge-not-overwrite check — enrich and merge, never overwrite.

An additive-write gate for agent-produced artifacts. It flags destructive
overwrites of tracked text files so that an enriched record is never silently
replaced by a smaller or empty one:

  * a write that drops / truncates prior content,
  * a stub / skeleton that overwrites previously enriched content,
  * a blanket regeneration where a field-level (frontmatter-key) update was possible.

The principle: every write preserves prior content, adds or enriches, and only
supersedes a specific field with a cited, gated update — never blanket-replace,
never regenerate-from-stub.

Pure stdlib. Usable as a library (`check_merge_not_overwrite`) or a CLI:
  python checks/merge_not_overwrite.py OLD_FILE NEW_FILE
  python checks/merge_not_overwrite.py --staged [BASE]      # git index vs BASE (default HEAD)
  python checks/merge_not_overwrite.py --diff  BASE         # working tree vs BASE (CI/PR)
"""
from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass

_KEY_RE = re.compile(r"^([A-Za-z0-9_\-]+)\s*:")
_TEXT_RE = re.compile(r"\.(md|markdown|json|jsonl|txt|ya?ml)$", re.IGNORECASE)


@dataclass
class Result:
    ok: bool
    reason: str
    retained_ratio: float


def _nonblank(text: str):
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def _frontmatter_keys(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return set()
    keys = set()
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        m = _KEY_RE.match(ln)
        if m:
            keys.add(m.group(1))
    return keys


def check_merge_not_overwrite(old: str, new: str, *, shrink_tolerance: float = 0.5) -> Result:
    """Return a Result judging whether writing `new` over `old` is additive.

    shrink_tolerance=0.5 means at least 50% of prior non-blank lines must survive.
    Frontmatter keys present in `old` must still be present in `new`.
    """
    old_lines = _nonblank(old)
    if not old_lines:
        return Result(True, "new artifact (no prior content) — additive", 1.0)
    if not _nonblank(new):
        return Result(False, "blank/stub overwrite: prior non-empty content replaced by empty", 0.0)

    new_set = set(_nonblank(new))
    retained = sum(1 for ln in old_lines if ln in new_set)
    ratio = retained / len(old_lines)

    dropped_keys = _frontmatter_keys(old) - _frontmatter_keys(new)
    if dropped_keys:
        return Result(False, f"frontmatter keys dropped: {sorted(dropped_keys)}", ratio)

    floor = 1.0 - shrink_tolerance
    if ratio < floor:
        return Result(False, f"non-additive: only {ratio:.0%} of prior content retained (need >= {floor:.0%})", ratio)
    return Result(True, f"additive: {ratio:.0%} of prior content retained", ratio)


def _run(args):
    return subprocess.run(args, capture_output=True, text=True)


def _git_show(spec: str) -> str:
    r = _run(["git", "show", spec])
    return r.stdout if r.returncode == 0 else ""


def check_paths(base: str = "HEAD", cached: bool = True):
    """Judge every MODIFIED tracked text file. Returns list of (path, Result)."""
    cmd = ["git", "diff", "--name-status", "--diff-filter=M"]
    if cached:
        cmd.append("--cached")
    cmd.append(base)
    out = _run(cmd).stdout
    results = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        path = parts[-1].strip()
        if not _TEXT_RE.search(path):
            continue
        old = _git_show(f"{base}:{path}")
        try:
            with open(path, encoding="utf-8") as fh:
                new = fh.read()
        except OSError:
            continue
        results.append((path, check_merge_not_overwrite(old, new)))
    return results


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--staged":
        base = argv[1] if len(argv) > 1 else "HEAD"
        results = check_paths(base, cached=True)
    elif argv and argv[0] == "--diff":
        base = argv[1] if len(argv) > 1 else "HEAD"
        results = check_paths(base, cached=False)
    elif len(argv) == 2:
        with open(argv[0], encoding="utf-8") as fh:
            old = fh.read()
        with open(argv[1], encoding="utf-8") as fh:
            new = fh.read()
        r = check_merge_not_overwrite(old, new)
        print(f"{'PASS' if r.ok else 'FAIL'}: {r.reason}")
        return 0 if r.ok else 1
    else:
        print(__doc__)
        return 2

    violations = 0
    for path, r in results:
        print(f"{'PASS' if r.ok else 'FAIL'} {path}: {r.reason}")
        violations += 0 if r.ok else 1
    if violations:
        print(f"merge-not-overwrite: {violations} violation(s) — enrich and merge, never overwrite")
        return 1
    print("merge-not-overwrite: OK (all modified text files additive)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
