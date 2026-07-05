# skills

[![skills.sh](https://skills.sh/b/matt-w-horn/skills)](https://skills.sh/matt-w-horn/skills)

Skills I use with [Claude](https://claude.ai) and
[Claude Code](https://www.anthropic.com/claude-code). A skill is a folder of instructions
(plus optional scripts and reference docs) that the model loads only when a task calls for
it, so specialized know-how stays out of the prompt until it's needed. The format is an open
standard; see [agentskills.io](https://agentskills.io), or Claude's
[What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills) and
[Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills).
These are built around how I work, but the layout and the checks transfer to any skill repo.

Each folder under [`skills/`](skills) is one skill:

| Skill | What it does |
|---|---|
| [`writing`](skills/writing) | A style guide for prose humans read, with a catalog of AI writing tells to avoid. |
| [`apps-script-deploy`](skills/apps-script-deploy) | The push-first ritual for deploying Google Apps Script projects with clasp. |
| [`life-paths`](skills/life-paths) | Maps realistic long-term life and career paths from a person's actual record and finances. |
| [`financial-planning`](skills/financial-planning) | Builds and stress-tests a long-horizon financial plan: saving schedule, retirement timing, drawdown. |

## Layout

A skill is a directory with a `SKILL.md`: YAML frontmatter (`name`, `description`) followed
by the instructions Claude reads. When a skill needs more, it adds:

- `references/` for background docs the skill opens only when relevant
- `scripts/` for code the skill runs (here, standard-library Python simulators)
- `tests/` for those scripts' tests

Claude decides when to load a skill by matching a request against the `description`, so
each one spells out its trigger cases.

## Install

### Claude Code plugin (easiest)

This repo is a plugin marketplace. In Claude Code:

```
/plugin marketplace add matt-w-horn/skills
/plugin install skills@matt-horn-skills
```

A new session loads the skills automatically; in a running session, run `/reload-plugins`.
Claude picks a skill when your request matches its description (say, "check my retirement
math" for `financial-planning`), and the skills also appear as `/skills:<name>`.

### Claude Code manual (symlink or copy)

Prefer a symlink or a copy? Clone the repo and link a skill into your Claude skills
directory. Linking into `~/.claude/skills/` makes it available in every project:

```bash
git clone https://github.com/matt-w-horn/skills.git
cd skills
ln -s "$PWD/skills/writing" ~/.claude/skills/writing   # one per skill you want
```

Edits to the repo take effect the next time Claude loads the skill, with no copy to keep in
sync. To scope a skill to a single project, link it into that project's `.claude/skills/`
instead.

### Claude apps (claude.ai and desktop)

Upload a skill as a ZIP. Zip the folder:

```bash
cd skills && zip -r writing.zip writing
```

Then in Claude go to **Customize → Skills**, click **+ Create skill**, choose **Upload a
skill**, and upload the ZIP. This needs "Code execution and file creation" turned on, and
uploaded skills stay private to your account. The general skills (`writing`, `life-paths`,
`financial-planning`) fit the Claude apps; `apps-script-deploy` is written for a terminal, so
it belongs in Claude Code.

## Developing

Two checks run in CI and gate every change:

```bash
python3 tools/validate_skills.py   # frontmatter parses and every referenced path exists
tools/run_tests.sh                 # each skill's test suite
```

Install the git hook once to run both (plus a gitleaks secret scan) on every commit:
`sh tools/install-hooks.sh`, or `pre-commit install` if you use pre-commit.

## License

MIT; see [LICENSE](LICENSE). The AI-writing-tells catalog in
[`skills/writing/references/tropes.md`](skills/writing/references/tropes.md) is adapted from
[tropes.fyi](https://tropes.fyi); see [NOTICE](NOTICE).
