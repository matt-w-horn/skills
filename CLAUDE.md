# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this is

Personal Claude Code skills, one per top-level directory, symlinked into
`~/.claude/skills/` so they load in every project. A skill is a directory with
a `SKILL.md` (frontmatter: `name` matching the directory, `description`) plus
optional `references/`, `scripts/`, and `tests/`. The simulation scripts
(`life-paths/scripts/fi_model.py`, `financial-planning/scripts/simcore.py`)
are pure standard library — keep them that way; CI installs nothing.

## Commands

```bash
python3 tools/validate_skills.py   # structure + path-reference validation
tools/run_tests.sh                 # every tests/ suite (skills and tools)
sh tools/install-hooks.sh          # git pre-commit hook: both checks + gitleaks
```

Both checks run on commit (hook) and on push/PR (CI). Keep them green.

## Conventions & gotchas

- **Adding a skill**: create the directory, write `SKILL.md`, then activate it
  from the repo root with `ln -s "$PWD/<skill>" ~/.claude/skills/<skill>`. The
  validator discovers skills at any depth by finding `SKILL.md`.
- **Path references are validated.** Any `dir/file` token in a skill's
  Markdown whose first segment is a real subdirectory of that skill must
  resolve, fenced commands included; runtime artifacts (dirs that don't exist
  in the repo, like `finances/config.json`) are ignored. Files under
  `references/` or `scripts/` that no Markdown mentions draw a warning.
- **Scripts must ship with tests** (`tests/test_*.py`, `unittest`, run from
  the skill directory). Degenerate inputs should raise `ValueError` with a
  clear message, never crash deep in the math — see the guards in `simcore.py`
  and `fi_model.py` for the pattern.
- The `writing` and `apps-script-deploy` skills were consolidated here from
  the nudge and receipt-printer repos; the generic deploy skill defers
  per-repo specifics to each repo's own CLAUDE.md.
- No secrets belong here, ever; gitleaks runs in the hook and CI as a backstop.
