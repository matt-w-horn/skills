# skills

[![skills.sh](https://skills.sh/b/matt-w-horn/skills)](https://skills.sh/matt-w-horn/skills)
[![ci](https://github.com/matt-w-horn/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/matt-w-horn/skills/actions/workflows/ci.yml)
![license: MIT](https://img.shields.io/badge/license-MIT-blue)

Skills I use with [Claude](https://claude.ai) and
[Claude Code](https://www.anthropic.com/claude-code), plus the validator, tests, and
CI around them — scaffolding that transfers to any skill repo. The format is
documented at [agentskills.io](https://agentskills.io).

Two of these ask for real numbers about your life. Those numbers go into the Claude
conversation you are already having, and nowhere else: the bundled simulators are
standard-library Python with no network imports, so they compute locally and send
nothing anywhere.

Each folder under [`skills/`](skills) is one skill:

| Skill | What it does |
|---|---|
| [`life-paths`](skills/life-paths) | Maps realistic long-term life and career paths from a person's actual record and finances. |
| [`financial-planning`](skills/financial-planning) | Builds and stress-tests a long-horizon financial plan: saving schedule, retirement timing, drawdown. |
| [`writing-axes`](skills/writing-axes) | Routes any writing or review task through reader, goal, and axis before drafting, then applies that axis's rules. |

The financial-planning skill produces analysis for you to check, not financial advice.
Its checks target a measured failure: asked about retirement, LLMs herd to the 4% rule.
Choukhmane, de Silva, Lin, and Akuzawa found 98.3% of withdrawal recommendations sat at
or below 4% of assets, where a life-cycle model puts almost none — so the advice tells
retirees to spend down too slowly. Their 2026 paper is distilled in
[`references/llm-advice.md`](skills/financial-planning/references/llm-advice.md).

## What a skill contains

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

The plugin route installs every skill at once. The symlink and ZIP routes are
per-skill — repeat them for each one you want.

### Claude Code plugin

This repo is installable as a Claude Code plugin; it carries the marketplace metadata
Claude Code needs. In Claude Code:

```
/plugin marketplace add matt-w-horn/skills
/plugin install skills@matt-horn-skills
```

The `owner/repo` shorthand clones over SSH, so the first command needs a GitHub key
loaded in `ssh-agent`. Without one, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` to clone over
HTTPS instead, or pass the URL: `/plugin marketplace add https://github.com/matt-w-horn/skills.git`.

Pull later changes with `/plugin marketplace update`, then `/plugin update`. The plugin
declares no pinned `version`, so it is versioned by commit and every push is picked up; a
pinned version would freeze existing installs until the string changed.

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

### Operating values

[`values/CLAUDE.md`](values/CLAUDE.md) is not a skill and the plugin cannot carry it: a
`CLAUDE.md` inside a plugin is never loaded as context, by design. It installs by hand
instead. Linking it into `~/.claude/rules/` applies it to every project, and a rule with no
`paths` frontmatter loads at launch like a `CLAUDE.md` would:

```bash
ln -s "$PWD/values/CLAUDE.md" ~/.claude/rules/values.md
```

That directory takes symlinks, so a `git pull` is again the whole update. If you would
rather keep it visible in one file, import it from your own `~/.claude/CLAUDE.md` with
`@~/path/to/values/CLAUDE.md` — user-scope imports load without the approval prompt an
external import in a project file would raise.

Either way it is 124 lines in every session, on top of whatever you already load, so read
it before you wire it in. They are principles for a coding agent rather than rules, and
they are opinionated: skills are the useful part of this repo, and this is the part worth
arguing with.

## Developing

Two checks run in CI and gate every change:

```bash
python3 tools/validate_skills.py   # frontmatter parses and every referenced path exists
tools/run_tests.sh                 # each skill's test suite, and the eval corpus linter
```

Install the git hook once to run both (plus a gitleaks secret scan) on every commit:
`sh tools/install-hooks.sh`, or `pre-commit install` if you use pre-commit.

## Evals

`life-paths` and `financial-planning` each ship an eval corpus in `evals/`, and
[`tools/eval/`](tools/eval) has the harness that runs it. Two questions get measured
separately: does Claude reach for the skill when it should, and is the deliverable
worth having.

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
