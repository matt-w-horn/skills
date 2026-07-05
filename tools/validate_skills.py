#!/usr/bin/env python3
"""Validate the structure of every skill in this repo.

A "skill" is any directory (any depth) containing a SKILL.md. For each one:

  1. SKILL.md has YAML frontmatter with a non-empty `name` and `description`,
     and `name` matches the directory name (how Claude Code resolves the
     skill). Multi-line values (plain or `>`/`|` block scalars) are handled.
  2. Every local path referenced from a Markdown file in the skill resolves:
     - Markdown links `](path)` outside fenced code blocks (links inside
       fences are treated as illustrative examples, not dependencies).
     - Any path-like token `dir/...` — in prose, backticks, or fenced
       commands — whose first segment is a real subdirectory of the skill.
       This validates `scripts/fi_model.py` in a fenced command while
       ignoring runtime artifacts like `finances/config.json` (no such dir
       in the repo). It follows that a token under a real dir is a claim
       about this repo and must resolve.
  3. (warning only) files under references/ or scripts/ that no Markdown
     mentions — likely renamed or dead.

Exits non-zero if any check fails. Run from anywhere:  python3 tools/validate_skills.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MD_LINK = re.compile(r"\]\(([^)]+)\)")
FENCE = re.compile(r"^```.*?^```[ \t]*$", re.M | re.S)
FM_LINE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
# first path segment / rest; the lookbehind keeps this off URLs and
# already-matched longer paths.
PATH_TOKEN = re.compile(r"(?<![\w./@-])([A-Za-z0-9_-]+)/([A-Za-z0-9_][\w./-]*)")
BLOCK_SCALARS = {">", "|", ">-", "|-", ">+", "|+"}


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def frontmatter(text):
    """Dict of the leading `--- ... ---` YAML block, or None if absent.

    Values may continue onto indented lines (plain multi-line scalars and
    `>`/`|` block scalars); continuations are folded with single spaces.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    data, key = {}, None
    for line in text[3:end].splitlines():
        m = FM_LINE.match(line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            data[key] = "" if val in BLOCK_SCALARS else val
        elif key and line[:1] in (" ", "\t") and line.strip():
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def is_local(target):
    target = target.strip()
    if not target:
        return False
    return re.match(r"^[a-z][a-z0-9+.-]*:", target) is None  # skip http:, mailto:, ...


def referenced_paths(md_path, subdirs):
    """(claimed_path, description) pairs a Markdown file asserts exist."""
    text = read(md_path)
    out = []
    # Markdown links: prose only — a link inside a fence is an example.
    for m in MD_LINK.finditer(FENCE.sub("", text)):
        t = m.group(1).split("#", 1)[0].split(" ", 1)[0]
        if is_local(t):
            out.append(t)
    # dir/... tokens anywhere (incl. fences), gated on the dir being real.
    for m in PATH_TOKEN.finditer(text):
        if m.group(1) in subdirs:
            out.append(f"{m.group(1)}/{m.group(2)}".rstrip("."))
    return out


def find_skills(root):
    """Directories containing a SKILL.md, at any depth, hidden dirs pruned."""
    skills = []
    for dp, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        if "SKILL.md" in files:
            skills.append(dp)
    return skills


def validate(root):
    """Validate every skill under root; returns (errors, warnings)."""
    errors, warnings = [], []
    skills = find_skills(root)
    if not skills:
        errors.append("no skills found (expected <dir>/SKILL.md)")
        return errors, warnings

    for sdir in skills:
        skill = os.path.relpath(sdir, root)
        subdirs = {d for d in os.listdir(sdir) if os.path.isdir(os.path.join(sdir, d))}

        fm = frontmatter(read(os.path.join(sdir, "SKILL.md")))
        if fm is None:
            errors.append(f"{skill}/SKILL.md: missing or malformed YAML frontmatter")
        else:
            name = fm.get("name", "")
            if not name:
                errors.append(f"{skill}/SKILL.md: frontmatter missing `name`")
            elif name != os.path.basename(sdir):
                errors.append(
                    f"{skill}/SKILL.md: name `{name}` != directory `{os.path.basename(sdir)}`"
                )
            if not fm.get("description"):
                errors.append(f"{skill}/SKILL.md: frontmatter missing `description`")

        md_files = [
            os.path.join(dp, f)
            for dp, _dirs, files in os.walk(sdir)
            for f in files
            if f.endswith(".md")
        ]

        referenced = set()
        for md in md_files:
            for target in referenced_paths(md, subdirs):
                cands = [
                    os.path.normpath(os.path.join(sdir, target)),
                    os.path.normpath(os.path.join(os.path.dirname(md), target)),
                ]
                hit = next((c for c in cands if os.path.exists(c)), None)
                if hit:
                    referenced.add(hit)
                else:
                    errors.append(
                        f"{os.path.relpath(md, root)}: broken reference -> `{target}`"
                    )

        # Orphans: docs and scripts should be reachable from some Markdown.
        for sub in ("references", "scripts"):
            subpath = os.path.join(sdir, sub)
            for dp, dirs, files in os.walk(subpath):
                dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
                for f in sorted(files):
                    if f.startswith(".") or f.endswith((".pyc", ".pyo")):
                        continue
                    fp = os.path.normpath(os.path.join(dp, f))
                    if fp not in referenced:
                        warnings.append(
                            f"{os.path.relpath(fp, root)}: not referenced by any markdown"
                        )

    return errors, warnings


def main():
    errors, warnings = validate(ROOT)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    skills = len(find_skills(ROOT))
    print(f"\nchecked {skills} skill(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
