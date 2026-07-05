#!/usr/bin/env python3
"""Validate the structure of every skill in this repo.

A "skill" is any top-level directory containing a SKILL.md. For each one this checks:

  1. SKILL.md has YAML frontmatter with a non-empty `name` and `description`, and
     `name` matches the directory name (how Claude Code resolves the skill).
  2. Every local path referenced from a Markdown file in the skill resolves to a file
     that exists — both Markdown links `](path)` and backtick spans naming a
     `references/`, `scripts/`, or `tests/` file. This catches a reference renamed or
     dropped without updating SKILL.md.
  3. (warning only) no file under `references/` is left unreferenced.

Exits non-zero if any check fails. Run from anywhere:  python3 tools/validate_skills.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MD_LINK = re.compile(r"\]\(([^)]+)\)")
BACKTICK_PATH = re.compile(r"`((?:references|scripts|tests)/[\w./-]+)`")
FM_LINE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def frontmatter(text):
    """Return a dict of the leading `--- ... ---` YAML block, or None if absent."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    data = {}
    for line in text[3:end].splitlines():
        m = FM_LINE.match(line)
        if m:
            data[m.group(1)] = m.group(2).strip()
    return data


def is_local(target):
    target = target.strip()
    if not target or target.startswith("#"):
        return False
    return re.match(r"^[a-z][a-z0-9+.-]*:", target) is None  # skip http:, mailto:, ...


def referenced_paths(md_path):
    text = read(md_path)
    out = []
    for m in MD_LINK.finditer(text):
        t = m.group(1).split("#", 1)[0].split(" ", 1)[0]
        if is_local(t):
            out.append(t)
    out += BACKTICK_PATH.findall(text)
    return out


def main():
    errors, warnings = [], []
    skills = sorted(
        d for d in os.listdir(ROOT)
        if os.path.isfile(os.path.join(ROOT, d, "SKILL.md"))
    )
    if not skills:
        print("ERROR no skills found (expected <dir>/SKILL.md)", file=sys.stderr)
        return 1

    for skill in skills:
        sdir = os.path.join(ROOT, skill)

        fm = frontmatter(read(os.path.join(sdir, "SKILL.md")))
        if fm is None:
            errors.append(f"{skill}/SKILL.md: missing or malformed YAML frontmatter")
        else:
            name = fm.get("name", "")
            if not name:
                errors.append(f"{skill}/SKILL.md: frontmatter missing `name`")
            elif name != skill:
                errors.append(f"{skill}/SKILL.md: name `{name}` != directory `{skill}`")
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
            for target in referenced_paths(md):
                cands = [
                    os.path.normpath(os.path.join(os.path.dirname(md), target)),
                    os.path.normpath(os.path.join(sdir, target)),
                ]
                hit = next((c for c in cands if os.path.exists(c)), None)
                if hit:
                    referenced.add(hit)
                else:
                    errors.append(f"{os.path.relpath(md, ROOT)}: broken reference -> `{target}`")

        refdir = os.path.join(sdir, "references")
        if os.path.isdir(refdir):
            for f in sorted(os.listdir(refdir)):
                fp = os.path.normpath(os.path.join(refdir, f))
                if os.path.isfile(fp) and fp not in referenced:
                    warnings.append(f"{skill}/references/{f}: not referenced by any markdown")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\nchecked {len(skills)} skill(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
