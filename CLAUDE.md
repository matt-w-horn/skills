# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this is

Personal Claude skills, one per directory under `skills/`. The repo is also a
Claude Code plugin marketplace (`.claude-plugin/marketplace.json` +
`plugin.json`), so others can `/plugin marketplace add matt-w-horn/skills`; I
load them myself by symlinking each into `~/.claude/skills/`. A skill is a
directory with a `SKILL.md` (frontmatter: `name` matching the directory,
`description`) plus optional `references/`, `scripts/`, and `tests/`. The
simulation scripts (`skills/life-paths/scripts/fi_model.py`,
`skills/financial-planning/scripts/simcore.py`) are pure standard library;
keep them that way, since CI installs nothing.

## Commands

```bash
python3 tools/validate_skills.py   # structure + path-reference validation
tools/run_tests.sh                 # every tests/ suite (skills and tools)
sh tools/install-hooks.sh          # git pre-commit hook: both checks + gitleaks
```

Both checks run on commit (hook) and on push/PR (CI). Keep them green.

Evals (see `tools/eval/README.md`; only the first is gated by CI, via
`tools/eval/tests/`):

```bash
python3 tools/eval/lint_evals.py          # corpus quality gate, stdlib only
python3 tools/eval/grade.py --calibrate   # judge must separate good.md from bad.md
python3 tools/eval/run_trigger.py --split graded    # ~144 `claude -p` runs
python3 tools/eval/run_exec.py --runs 2             # 32 long runs; hours
```

## Conventions & gotchas

- **Adding a skill**: create `skills/<skill>/` with a `SKILL.md`, then activate
  it from the repo root with `ln -s "$PWD/skills/<skill>" ~/.claude/skills/<skill>`.
  Nothing else to wire up: the marketplace auto-discovers everything under
  `skills/` (no manifest edit), and the validator finds skills at any depth by
  their `SKILL.md`.
- **Path references are validated.** Any `dir/file` token in a skill's
  Markdown whose first segment is a real subdirectory of that skill must
  resolve, fenced commands included; runtime artifacts (dirs that don't exist
  in the repo, like `finances/config.json`) are ignored. Files under
  `references/` or `scripts/` that no Markdown mentions draw a warning.
- **Scripts must ship with tests** (`tests/test_*.py`, `unittest`, run from
  the skill directory). Degenerate inputs should raise `ValueError` with a
  clear message, never crash deep in the math — see the guards in `simcore.py`
  and `fi_model.py` for the pattern.
- **Eval corpora live in `skills/<skill>/evals/`** and are authored blind: a
  trigger query or rubric assertion must not paraphrase the SKILL.md body, and
  `lint_evals.py` rule 5 fails the corpus if one shares a five-word phrase with
  the body that is absent from the description. When editing evals, work from
  the description and domain knowledge, not the skill's own instructions.
  Trigger queries must also be self-contained: runs happen in an empty
  directory, so a query naming a file misfires for a fixture reason that reads
  like a description failure.
- **Never put a `SKILL.md` under `evals/`.** `validate_skills.py` treats any
  `SKILL.md` at any depth as a skill and would try to validate the fixture.
  Same trap for `scripts/`-, `references/`-, `tests/`- or `evals/`-prefixed
  path tokens in eval prose: the validator resolves them against the real
  directories. Both are linted.
- **This repo is public, so it may not depend on anything outside itself.** A
  skill here must stand alone: no references to system-wide skills, to
  `~/.claude`, or to a project that isn't public. Skills needing any of those
  live as real directories under `~/.claude/skills/` instead, which is where
  `apps-script-deploy` went on 2026-07-26. The `~/.claude/skills/`
  paths below are install instructions for a reader, not a dependency.
- No secrets belong here, ever; gitleaks runs in the hook and CI as a backstop.
