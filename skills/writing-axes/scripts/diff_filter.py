#!/usr/bin/env python3
"""Filter linter findings down to lines changed in a unified diff.

Lint the whole file, then intersect: the style rules need full-file context
(sentence segmentation, masking, consistency), so findings are produced for
the entire manuscript and this filter keeps only those on added or modified
lines.

Usage:
    vale --output=line main.tex | diff_filter.py CHANGES.diff
    check_tex.py main.tex       | diff_filter.py CHANGES.diff

CHANGES.diff is any unified diff (any context size) whose new side matches
the text the linter ran on, e.g.:

    git diff -U0 HEAD~1 -- main.tex > CHANGES.diff
    vale --output=line main.tex | diff_filter.py <(git diff HEAD~1)

Findings are `path:line:...` lines (Vale's line output and check_tex.py
both emit this); paths are matched by trailing components, so `main.tex`
findings match a `paper/main.tex` diff entry. Lines that do not parse as
findings are dropped. Exits 1 if any finding survives, 0 otherwise.
"""
import re
import sys
from pathlib import Path

FILE_HEADER = re.compile(r"^\+\+\+ (?:b/)?(.*)$")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def changed_lines(diff_text: str) -> dict:
    """Map diff path -> set of new-side line numbers added or modified."""
    out = {}
    path = None
    lineno = None
    for line in diff_text.splitlines():
        if line.startswith("diff "):
            path, lineno = None, None
            continue
        m = FILE_HEADER.match(line)
        if m:
            # `diff -u` (unlike `git diff`) appends "\t<timestamp>".
            header_path = m.group(1).split("\t")[0]
            path = None if header_path == "/dev/null" else header_path
            lineno = None
            continue
        m = HUNK.match(line)
        if m and path is not None:
            lineno = int(m.group(1))
            continue
        if path is None or lineno is None:
            continue
        if line.startswith("+"):
            out.setdefault(path, set()).add(lineno)
            lineno += 1
        elif line.startswith("-") or line.startswith("\\"):
            pass  # old-side line / "\\ No newline": no new-side number
        else:
            lineno += 1  # context line
    return out


def same_file(finding_path: str, diff_path: str) -> bool:
    """True when the paths agree on their trailing components."""
    fa = [p for p in finding_path.replace("\\", "/").split("/") if p not in ("", ".")]
    fb = [p for p in diff_path.split("/") if p not in ("", ".")]
    n = min(len(fa), len(fb))
    return n > 0 and fa[-n:] == fb[-n:]


def filter_findings(findings, changed: dict) -> list:
    """Keep `path:line:...` finding lines that land on a changed line."""
    kept = []
    for raw in findings:
        raw = raw.rstrip("\n")
        parts = raw.split(":", 2)
        if len(parts) < 3 or not parts[1].isdigit():
            continue
        path, line = parts[0], int(parts[1])
        if any(
            line in lines and same_file(path, dpath)
            for dpath, lines in changed.items()
        ):
            kept.append(raw)
    return kept


def main(argv: list) -> int:
    if len(argv) != 1:
        raise ValueError("usage: diff_filter.py DIFF_FILE < findings")
    diff_path = Path(argv[0])
    try:
        diff_text = diff_path.read_text()
    except OSError as exc:
        raise ValueError(f"cannot read diff file: {diff_path}") from exc
    kept = filter_findings(sys.stdin, changed_lines(diff_text))
    for line in kept:
        print(line)
    return 1 if kept else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
