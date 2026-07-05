# skills

Personal [Claude Code](https://claude.com/claude-code) skills, kept in one repo and
symlinked into `~/.claude/skills/` so they load in every project.

Each top-level directory is one skill:

| Skill | What it does |
|---|---|
| `writing/` | Style guide for prose humans will read, plus a catalog of AI writing tells to avoid. |
| `apps-script-deploy/` | Push-first deploy ritual for Google Apps Script projects (clasp). |
| `life-paths/` | Maps realistic long-term life and career paths, grounded in a person's record and finances. |
| `financial-planning/` | Builds and stress-tests a long-horizon financial plan: accumulation, FI timing, drawdown. |

A skill is a directory with a `SKILL.md` (YAML frontmatter: `name`, `description`) and,
optionally, `references/` (deeper docs pulled in on demand), `scripts/` (code the skill
runs), and `tests/`.

## Activation

The skills load globally through symlinks:

    ~/.claude/skills/<skill> -> ~/code/skills/<skill>

Add a new one the same way:

    ln -s ~/code/skills/<skill> ~/.claude/skills/<skill>

## Checks

Two checks run on every commit (pre-commit) and every push (GitHub Actions):

    python3 tools/validate_skills.py   # frontmatter + every referenced path resolves
    tools/run_tests.sh                 # each skill's unittest suite

To run the pre-commit hooks locally, install them once with `pre-commit install`.
