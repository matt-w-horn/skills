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

Each skill is activated by a symlink:

    ln -s ~/code/skills/<skill> ~/.claude/skills/<skill>

Claude Code reads the symlink, so edits here take effect immediately — no copy to
drift. Adding a new skill means adding its directory and its symlink.

## Checks

Two checks gate every change:

    python3 tools/validate_skills.py   # frontmatter + every referenced path resolves
    tools/run_tests.sh                 # every tests/ suite (skills and tools alike)

CI runs both on every push and pull request. To also run them on every local commit
(plus a gitleaks secret scan), install the git hook once:

    sh tools/install-hooks.sh

(Equivalent, if you use the pre-commit framework: `pre-commit install`.)
