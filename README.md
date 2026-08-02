# skills

[![skills.sh](https://skills.sh/b/matt-w-horn/skills)](https://skills.sh/matt-w-horn/skills)
[![ci](https://github.com/matt-w-horn/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/matt-w-horn/skills/actions/workflows/ci.yml)
![license: MIT](https://img.shields.io/badge/license-MIT-blue)

Two skills I use with [Claude](https://claude.ai) and
[Claude Code](https://www.anthropic.com/claude-code): one maps realistic long-term life and
career paths, one builds and stress-tests a long-horizon financial plan. Around them sit
the validator, tests, and CI that keep the repo honest, and that scaffolding transfers to
any skill repo. A skill is a folder of instructions the model loads only when a task calls
for it, so specialized know-how stays out of the prompt until it's needed. The format is
documented at [agentskills.io](https://agentskills.io).

Each folder under [`skills/`](skills) is one skill:

| Skill | What it does |
|---|---|
| [`life-paths`](skills/life-paths) | Maps realistic long-term life and career paths from a person's actual record and finances. |
| [`financial-planning`](skills/financial-planning) | Builds and stress-tests a long-horizon financial plan: saving schedule, retirement timing, drawdown. |

The financial-planning skill produces analysis for you to check, not financial advice.

## Layout

A skill is a directory with a `SKILL.md`: YAML frontmatter (`name`, `description`) followed
by the instructions Claude reads (Claude's docs:
[What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills) and
[Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)).
When a skill needs more, it adds:

- `references/` for background docs the skill opens only when relevant
- `scripts/` for code the skill runs (here, standard-library Python simulators)
- `tests/` for those scripts' tests

Claude decides when to load a skill by matching a request against the `description`, so
each one spells out its trigger cases.

`values/` at the repo root is not a skill: it holds the operating-values text my global
`CLAUDE.md` starts with.

## Install

All three routes below work for both skills.

### Claude Code plugin (easiest)

This repo is installable as a Claude Code plugin; it carries the marketplace metadata
Claude Code needs. In Claude Code:

```
/plugin marketplace add matt-w-horn/skills
/plugin install skills@matt-horn-skills
```

A new session loads the skills automatically; in a running session, run `/reload-plugins`.
Claude picks a skill when your request matches its description (say, "check my retirement
math" for `financial-planning`), and the skills also appear as `/skills:<name>`.

### Claude Code manual (symlink)

To track the repo directly instead, clone it and link a skill into your Claude skills
directory. Linking into `~/.claude/skills/` makes it available in every project:

```bash
git clone https://github.com/matt-w-horn/skills.git
cd skills
ln -s "$PWD/skills/life-paths" ~/.claude/skills/life-paths   # one per skill you want
```

Edits to the repo take effect the next time Claude loads the skill, with no copy to keep in
sync. To scope a skill to a single project, link it into that project's `.claude/skills/`
instead.

### Claude apps (claude.ai and desktop)

Upload a skill as a ZIP. Zip the folder with
`cd skills && zip -r life-paths.zip life-paths`. Then in Claude go to **Customize → Skills**, click **+ Create skill**, choose **Upload a
skill**, and upload the ZIP. This needs "Code execution and file creation" turned on, and
uploaded skills stay private to your account.

## Developing

Two checks run in CI and gate every change:

```bash
python3 tools/validate_skills.py   # frontmatter parses and every referenced path exists
tools/run_tests.sh                 # each skill's test suite, and the eval corpus linter
```

Install the git hook once to run both (plus a gitleaks secret scan) on every commit:
`sh tools/install-hooks.sh`, or `pre-commit install` if you use pre-commit.

## Evals

Each skill ships an eval corpus in `evals/`, and [`tools/eval/`](tools/eval) has the
harness that runs it. Two questions get measured separately: does Claude reach for the
skill when it should, and is the deliverable worth having.

```bash
python3 tools/eval/lint_evals.py          # corpus quality gate, also run by the tests
python3 tools/eval/grade.py --calibrate   # check the judge separates good from bad
python3 tools/eval/run_trigger.py --split graded
python3 tools/eval/run_exec.py --runs 2
```

The linter and its tests need nothing but the standard library, so CI gates them. The
sweeps shell out to the `claude` CLI and cost time and money, so they are run by
hand.
[`tools/eval/README.md`](tools/eval/README.md) covers how the two configurations are kept
apart, what the numbers do and don't support, and where the design came from.

## License

MIT; see [LICENSE](LICENSE) and [NOTICE](NOTICE).
