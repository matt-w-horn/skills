#!/usr/bin/env python3
"""Drive `claude -p` runs and read what happened out of the event stream.

Every eval run is a headless `claude -p` subprocess in its own empty directory.
That buys three things a subagent-based harness doesn't: each trial genuinely
starts from a clean environment, the run survives the parent session going away,
and the result is on disk the moment it lands, so a sweep resumes rather than
restarts.

The two configurations differ by exactly one flag:

    without_skill   --setting-sources project
    with_skill      --setting-sources project --plugin-dir <repo>

`--setting-sources project` drops the user's own `~/.claude/skills`, and an
empty working directory has no project settings to load, so the only skills in
play are Claude Code's built-ins. Adding the repo as a plugin puts the two
skills under test back, under their plugin-namespaced names, e.g.
`skills:life-paths`. One probe, recorded here so nobody re-derives it: a run in
the without_skill configuration made no Skill call across 226 seconds of work on
a query that fires the skill in 5 seconds with the plugin loaded.

The scanner is deliberately asymmetric about how it concludes. Seeing the skill
invoked settles the question, so it stops. *Not* seeing it settles nothing until
the budget runs out, because a model may read a file or two before deciding.
A harness that concluded "no" at the first Bash call would report zero triggers
for every realistic prompt and look, from the outside, exactly like a skill that
never fires.
"""
import json
import os
import shutil
import signal
import subprocess
import threading
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

WITH_SKILL = "with_skill"
WITHOUT_SKILL = "without_skill"
CONFIGURATIONS = (WITH_SKILL, WITHOUT_SKILL)

# Outcomes. `no_trigger` is a measurement; `error` and `timeout` are the absence
# of one. Collapsing them is how a broken harness reports a confident zero.
TRIGGERED = "triggered"
NO_TRIGGER = "no_trigger"
ERROR = "error"
TIMEOUT = "timeout"

BASE_FLAGS = (
    "-p",
    "--output-format", "stream-json",
    "--verbose",
    "--strict-mcp-config",
    "--no-session-persistence",
    "--setting-sources", "project",
)


def build_command(prompt, configuration, repo_root=REPO_ROOT,
                  permission_mode="acceptEdits", model=None):
    """The argv for one run. The two configurations differ by one flag."""
    if configuration not in CONFIGURATIONS:
        raise ValueError(f"unknown configuration {configuration!r}")
    cmd = ["claude", *BASE_FLAGS, "--permission-mode", permission_mode]
    if model:
        cmd += ["--model", model]
    if configuration == WITH_SKILL:
        cmd += ["--plugin-dir", repo_root]
    cmd.append(prompt)
    return cmd


def skill_aliases(skill):
    """Names one skill can appear under, depending on how it was installed.

    A plugin install namespaces it (`skills:life-paths`); a symlink into the
    user skills directory doesn't. Matching both keeps the harness honest if
    the install route ever changes.
    """
    return {skill, f"skills:{skill}", f"/{skill}", f"/skills:{skill}"}


class StreamScanner:
    """Reads stream-json events and decides whether a skill was invoked.

    Kept free of subprocess handling so it can be tested against recorded
    events, which is the only way to know it recognises a trigger at all.
    """

    def __init__(self, skills, max_tool_calls=6):
        self.skills = list(skills)
        self.aliases = {s: skill_aliases(s) for s in self.skills}
        self.max_tool_calls = max_tool_calls
        self.invoked = []       # skills seen, in order
        self.tool_calls = []    # every tool name seen, in order
        self.saw_init = False
        self.saw_result = False
        self.listed_skills = None

    def feed(self, line):
        """Consume one line. Returns True when the answer is settled."""
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            return False
        if not isinstance(event, dict):
            return False

        if event.get("type") == "system" and event.get("subtype") == "init":
            self.saw_init = True
            listed = event.get("skills")
            if isinstance(listed, list):
                self.listed_skills = listed

        # The CLI emits a result event when its turn ends. Its absence in a
        # run read to completion means the run was cut off, which is a more
        # direct signal than comparing elapsed time against the deadline.
        if event.get("type") == "result":
            self.saw_result = True

        for block in self._tool_uses(event):
            name = block.get("name")
            self.tool_calls.append(name)
            hit = self._skill_for(block)
            if hit and hit not in self.invoked:
                self.invoked.append(hit)

        # A positive settles it. A negative never does on its own; only the
        # tool-call budget or the wall clock can end a run that hasn't fired.
        if self.invoked:
            return True
        return len(self.tool_calls) >= self.max_tool_calls

    @staticmethod
    def _tool_uses(event):
        content = (event.get("message") or {}).get("content")
        if not isinstance(content, list):
            return []
        return [b for b in content
                if isinstance(b, dict) and b.get("type") == "tool_use"]

    def _skill_for(self, block):
        """Which skill under test this tool_use invokes, if any."""
        inp = block.get("input") or {}
        if block.get("name") == "Skill":
            named = str(inp.get("skill") or inp.get("command") or "").strip()
            for skill, aliases in self.aliases.items():
                if named in aliases:
                    return skill
        if block.get("name") == "Read":
            path = str(inp.get("file_path") or "")
            if path.endswith("SKILL.md"):
                for skill in self.skills:
                    if f"{os.sep}{skill}{os.sep}" in path:
                        return skill
        return None

    def outcome(self, timed_out=False):
        if self.invoked:
            return TRIGGERED
        if timed_out:
            return TIMEOUT
        return NO_TRIGGER


def run_once(prompt, configuration, skills, cwd, stream_path=None,
             timeout=120, max_tool_calls=6, repo_root=REPO_ROOT,
             permission_mode="acceptEdits", model=None, run_to_completion=False):
    """One `claude -p` run. Returns a record; never raises for a failed run.

    `run_to_completion` disables the early stops. It costs far more time and
    exists for one reason: to check, on a sample, that the cheap stopping rule
    isn't hiding late skill invocations. Until that check runs, the shortcut is an
    assumption rather than an optimisation.
    """
    os.makedirs(cwd, exist_ok=True)
    cmd = build_command(prompt, configuration, repo_root, permission_mode, model)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    scanner = StreamScanner(skills, max_tool_calls=10**9 if run_to_completion
                            else max_tool_calls)
    started = time.time()
    stream = open(stream_path, "w", encoding="utf-8") if stream_path else None
    proc, timed_out, failure = None, False, None

    # A watchdog rather than a deadline check inside the read loop: iterating
    # proc.stdout blocks, so a run that goes quiet (thinking for a long time,
    # or wedged) would never reach an in-loop check. Long execution runs go
    # quiet routinely, so this is the difference between a bounded sweep and
    # one that hangs overnight on a single row.
    #
    # The whole process group gets killed, not just the child. These runs have
    # a shell and spawn subagents, so a grandchild holding the pipe's write end
    # keeps the read loop blocked long after the child is dead, and any
    # background process the model started would otherwise outlive the sweep.
    fired = threading.Event()
    state = {"proc": None}

    def expire():
        fired.set()
        victim = state["proc"]
        if victim is None:
            return
        try:
            os.killpg(os.getpgid(victim.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            victim.kill()

    deadline = threading.Timer(timeout, expire)
    deadline.daemon = True

    try:
        proc = subprocess.Popen(
            cmd, cwd=cwd, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, bufsize=1,
            errors="replace",            # a stray byte must not kill the run
            start_new_session=True,      # its own group, so killpg reaches all
        )
        state["proc"] = proc
        deadline.start()
        if fired.is_set():               # timer beat the assignment
            expire()
        for line in proc.stdout:
            if stream:
                stream.write(line)
            settled = scanner.feed(line)
            if settled and not run_to_completion:
                break
        else:
            # Ran out of output rather than breaking out. Only the watchdog
            # having fired makes that a timeout; a run finishing just before
            # the deadline is a completed run, not a truncated one.
            timed_out = fired.is_set()
    except OSError as exc:          # claude missing, cwd unusable, pipe died
        failure = f"{type(exc).__name__}: {exc}"
    finally:
        deadline.cancel()
        if proc:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                proc.kill()
            proc.wait()
            if proc.stdout:
                proc.stdout.close()
        if stream:
            stream.close()

    if failure:
        outcome = ERROR
    elif not scanner.saw_init and not scanner.invoked:
        # No init event means the CLI never really started, which is an
        # environment failure, not a negative result.
        outcome = ERROR
        failure = "no init event in stream; claude did not start cleanly"
    else:
        outcome = scanner.outcome(timed_out=timed_out)

    return {
        "configuration": configuration,
        "outcome": outcome,
        # Separate from `outcome` on purpose. A run that invoked the skill and
        # was then killed at the deadline reports `triggered`, which is the
        # right answer for a trigger eval (it fired) and the wrong one for an
        # execution eval (its deliverable is however far it got).
        "timed_out": timed_out,
        "completed": scanner.saw_result if run_to_completion else None,
        "skills_invoked": scanner.invoked,
        "tool_calls": scanner.tool_calls,
        "listed_skills": scanner.listed_skills,
        "seconds": round(time.time() - started, 1),
        "error": failure,
        "cwd": cwd,
        "stream": stream_path,
    }


def void_reason(record, skills_under_test):
    """Why this record must not be counted, or None if it may be.

    The load-bearing case is a without_skill run that invoked a skill under
    test. That means isolation leaked, and every baseline number from that
    sweep is describing something other than a baseline.
    """
    if record["outcome"] == ERROR:
        return record.get("error") or "run errored"
    if record["configuration"] == WITHOUT_SKILL:
        leaked = [s for s in record["skills_invoked"] if s in skills_under_test]
        if leaked:
            return f"isolation leak: baseline run invoked {leaked}"
        if record.get("listed_skills") is not None:
            visible = set(record["listed_skills"])
            seen = [s for s in skills_under_test if skill_aliases(s) & visible]
            if seen:
                # Listed but not invoked is still contamination: the model read
                # those descriptions before deciding, so this is not a baseline.
                return f"isolation leak: baseline run could see {seen}"
    if record["configuration"] == WITH_SKILL and record["listed_skills"] is not None:
        visible = set(record["listed_skills"])
        missing = [s for s in skills_under_test
                   if not (skill_aliases(s) & visible)]
        if missing:
            return f"skills not loaded in with_skill run: {missing}"
    return None


def write_json(path, payload):
    """Write via a temporary file and rename, so a cache entry is never partial.

    These files are the resume points for a sweep that takes hours. A direct
    dump interrupted by a laptop sleeping leaves truncated JSON that the next
    run reads back, fails to parse, and records as a permanently voided row:
    the run never re-executes, because the file exists.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def read_json(path):
    """Read a cache entry, treating a corrupt one as absent rather than fatal."""
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, ValueError, OSError):
        return None


def prepare_cwd(cwd, fixture_dir=None):
    """A clean directory per run, with the fixture copied in if there is one."""
    if os.path.exists(cwd):
        shutil.rmtree(cwd)
    os.makedirs(cwd)
    if fixture_dir and os.path.isdir(fixture_dir):
        for name in sorted(os.listdir(fixture_dir)):
            src = os.path.join(fixture_dir, name)
            dst = os.path.join(cwd, name)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    return cwd


def collect_outputs(cwd, fixture_dir=None, limit_bytes=400_000):
    """Text files the run produced, plus any fixture file it edited.

    Comparing content rather than filenames matters for the finish-the-job
    shape, where correcting the document the user brought is a natural way to
    deliver. Excluding fixture paths outright would hide that work, so a run
    that edited the file in place would fail assertions that a run pasting the
    same content into chat would pass.
    """
    seeded = {}
    if fixture_dir and os.path.isdir(fixture_dir):
        for dp, _dirs, files in os.walk(fixture_dir):
            for f in files:
                path = os.path.join(dp, f)
                rel = os.path.relpath(path, fixture_dir)
                try:
                    with open(path, encoding="utf-8") as fh:
                        seeded[rel] = fh.read()
                except (OSError, UnicodeDecodeError):
                    seeded[rel] = None      # unreadable: treat as untouched

    produced = {}
    for dp, dirs, files in os.walk(cwd):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(dp, f), cwd)
            if f.startswith("."):
                continue
            path = os.path.join(dp, f)
            if rel in seeded:
                if seeded[rel] is None:
                    continue
                try:
                    with open(path, encoding="utf-8") as fh:
                        if fh.read() == seeded[rel]:
                            continue        # untouched fixture file
                except (OSError, UnicodeDecodeError):
                    continue
            try:
                if os.path.getsize(path) > limit_bytes:
                    produced[rel] = f"<{os.path.getsize(path)} bytes, truncated>"
                    continue
                with open(path, encoding="utf-8") as fh:
                    produced[rel] = fh.read()
            except (OSError, UnicodeDecodeError):
                continue          # binary or unreadable: not gradeable text
    return produced


def final_text(stream_path):
    """The assistant's last message: the response a user would have read."""
    if not stream_path or not os.path.exists(stream_path):
        return ""
    chunks = []
    with open(stream_path, encoding="utf-8") as fh:
        for line in fh:
            try:
                event = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            if not isinstance(event, dict):
                continue
            if event.get("type") == "result" and isinstance(event.get("result"), str):
                chunks.append(event["result"])
                continue
            if event.get("type") != "assistant":
                continue
            for block in (event.get("message") or {}).get("content") or []:
                if isinstance(block, dict) and block.get("type") == "text":
                    chunks.append(block.get("text", ""))
    return "\n".join(c for c in chunks if c).strip()
