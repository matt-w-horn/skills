"""Tests for tools/eval/harness.py. Run from the tools/eval directory:
    python3 -m unittest discover tests

The scanner is the whole measurement. If it fails to recognise a trigger, every
row reads zero and the corpus looks like a description problem, which is
exactly how the previous tooling failed, silently and confidently. So the
recognition cases are pinned against recorded event shapes, and so is the
stopping rule that made it fail: a run must never be called a no-trigger just
because some other tool was used first.
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import harness  # noqa: E402

SKILLS = ["financial-planning", "life-paths"]


def init_event(skills=("skills:financial-planning", "skills:life-paths")):
    return json.dumps({"type": "system", "subtype": "init",
                       "skills": list(skills), "tools": ["Read", "Bash"]})


def tool_event(name, **inp):
    return json.dumps({"type": "assistant", "message": {
        "content": [{"type": "tool_use", "name": name, "input": inp}]}})


def text_event(text):
    return json.dumps({"type": "assistant", "message": {
        "content": [{"type": "text", "text": text}]}})


class Scanner(unittest.TestCase):
    def scan(self, lines, max_tool_calls=6):
        s = harness.StreamScanner(SKILLS, max_tool_calls=max_tool_calls)
        settled_at = None
        for i, line in enumerate(lines):
            if s.feed(line) and settled_at is None:
                settled_at = i
        return s, settled_at

    def test_detects_plugin_namespaced_skill(self):
        s, at = self.scan([init_event(), tool_event("Skill",
                                                    skill="skills:life-paths")])
        self.assertEqual(s.invoked, ["life-paths"])
        self.assertEqual(s.outcome(), harness.TRIGGERED)
        self.assertEqual(at, 1, "a match should settle the run immediately")

    def test_detects_bare_skill_name(self):
        s, _ = self.scan([init_event(), tool_event("Skill",
                                                   skill="financial-planning")])
        self.assertEqual(s.invoked, ["financial-planning"])

    def test_detects_skill_named_in_command_field(self):
        s, _ = self.scan([init_event(),
                          tool_event("Skill", command="/skills:life-paths")])
        self.assertEqual(s.invoked, ["life-paths"])

    def test_detects_reading_the_skill_file(self):
        path = "/x/skills/financial-planning/SKILL.md"
        s, _ = self.scan([init_event(), tool_event("Read", file_path=path)])
        self.assertEqual(s.invoked, ["financial-planning"])

    def test_unrelated_skill_is_not_counted(self):
        s, _ = self.scan([init_event(),
                          tool_event("Skill", skill="superpowers:brainstorming")])
        self.assertEqual(s.invoked, [])
        self.assertEqual(s.outcome(), harness.NO_TRIGGER)

    def test_other_tools_do_not_settle_the_run(self):
        """The bug that made the previous harness report 0/N for everything."""
        lines = [init_event(), text_event("Let me look around."),
                 tool_event("Bash", command="ls"),
                 tool_event("Glob", pattern="*.csv"),
                 tool_event("Skill", skill="skills:financial-planning")]
        s, at = self.scan(lines, max_tool_calls=6)
        self.assertEqual(s.invoked, ["financial-planning"],
                         "a skill invoked after other tools must still count")
        self.assertEqual(at, 4)

    def test_budget_stops_a_run_that_never_fires(self):
        lines = [init_event()] + [tool_event("Bash", command=f"echo {i}")
                                  for i in range(6)]
        s, at = self.scan(lines, max_tool_calls=3)
        self.assertEqual(s.invoked, [])
        self.assertEqual(at, 3, "should stop once the tool-call budget is spent")
        self.assertEqual(s.outcome(), harness.NO_TRIGGER)

    def test_timeout_is_not_a_no_trigger(self):
        s, _ = self.scan([init_event(), tool_event("Bash", command="sleep")])
        self.assertEqual(s.outcome(timed_out=True), harness.TIMEOUT)

    def test_malformed_lines_are_survived(self):
        s, _ = self.scan([init_event(), "not json at all\n", "[]",
                          tool_event("Skill", skill="skills:life-paths")])
        self.assertEqual(s.invoked, ["life-paths"])

    def test_init_event_skill_listing_is_captured(self):
        s, _ = self.scan([init_event(["skills:life-paths"])])
        self.assertEqual(s.listed_skills, ["skills:life-paths"])

    def test_result_event_marks_the_turn_as_finished(self):
        result = json.dumps({"type": "result", "result": "done"})
        s, _ = self.scan([init_event(), result])
        self.assertTrue(s.saw_result)

    def test_a_stream_without_a_result_event_is_unfinished(self):
        """How a run killed at the deadline is told from one that finished.

        A run that invoked the skill and was then killed still reports
        `triggered`, because firing is what a trigger eval measures. For an
        execution eval it means the deliverable is however far it got, and
        only the missing end-of-turn event distinguishes the two.
        """
        s, _ = self.scan([init_event(), tool_event("Bash", command="sleep")])
        self.assertFalse(s.saw_result)
        self.assertEqual(s.outcome(timed_out=True), harness.TIMEOUT)

    def test_a_killed_run_that_fired_still_reports_triggered(self):
        s, _ = self.scan([init_event(),
                          tool_event("Skill", skill="skills:life-paths")])
        self.assertEqual(s.outcome(timed_out=True), harness.TRIGGERED,
                         "firing is the trigger measurement even if cut off")
        self.assertFalse(s.saw_result, "but the turn never finished")


class Commands(unittest.TestCase):
    def test_configurations_differ_only_by_the_plugin_flag(self):
        with_skill = harness.build_command("q", harness.WITH_SKILL, repo_root="/r")
        without = harness.build_command("q", harness.WITHOUT_SKILL, repo_root="/r")
        self.assertEqual(set(with_skill) - set(without), {"--plugin-dir", "/r"})
        self.assertEqual(set(without) - set(with_skill), set())

    def test_settings_are_scoped_to_the_project(self):
        """Without this the user's own installed skills leak into the baseline."""
        cmd = harness.build_command("q", harness.WITHOUT_SKILL)
        self.assertIn("--setting-sources", cmd)
        self.assertEqual(cmd[cmd.index("--setting-sources") + 1], "project")

    def test_unknown_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            harness.build_command("q", "sort-of-with-the-skill")


class Voiding(unittest.TestCase):
    def record(self, **kw):
        base = {"configuration": harness.WITH_SKILL, "outcome": harness.TRIGGERED,
                "skills_invoked": [], "listed_skills": None, "error": None}
        base.update(kw)
        return base

    def test_baseline_that_invoked_the_skill_is_void(self):
        rec = self.record(configuration=harness.WITHOUT_SKILL,
                          skills_invoked=["life-paths"])
        self.assertIn("isolation leak", harness.void_reason(rec, SKILLS))

    def test_with_skill_run_missing_the_skill_is_void(self):
        rec = self.record(listed_skills=["dataviz", "code-review"])
        self.assertIn("not loaded", harness.void_reason(rec, SKILLS))

    def test_errored_run_is_void(self):
        rec = self.record(outcome=harness.ERROR, error="claude did not start")
        self.assertEqual(harness.void_reason(rec, SKILLS), "claude did not start")

    def test_clean_runs_are_kept(self):
        good = self.record(skills_invoked=["life-paths"],
                           listed_skills=["skills:life-paths",
                                          "skills:financial-planning"])
        self.assertIsNone(harness.void_reason(good, SKILLS))
        baseline = self.record(configuration=harness.WITHOUT_SKILL,
                               outcome=harness.NO_TRIGGER)
        self.assertIsNone(harness.void_reason(baseline, SKILLS))


class Outputs(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def test_fixture_files_are_not_reported_as_output(self):
        fixture = os.path.join(self.root, "fixture")
        os.makedirs(fixture)
        with open(os.path.join(fixture, "notes.md"), "w", encoding="utf-8") as fh:
            fh.write("brought by the user\n")

        cwd = harness.prepare_cwd(os.path.join(self.root, "run"), fixture)
        self.assertTrue(os.path.exists(os.path.join(cwd, "notes.md")))
        with open(os.path.join(cwd, "PLAN.md"), "w", encoding="utf-8") as fh:
            fh.write("the deliverable\n")

        produced = harness.collect_outputs(cwd, fixture)
        self.assertEqual(sorted(produced), ["PLAN.md"])
        self.assertIn("deliverable", produced["PLAN.md"])

    def test_prepare_cwd_clears_a_previous_run(self):
        cwd = os.path.join(self.root, "run")
        os.makedirs(cwd)
        with open(os.path.join(cwd, "stale.md"), "w", encoding="utf-8") as fh:
            fh.write("from last time\n")
        harness.prepare_cwd(cwd)
        self.assertEqual(os.listdir(cwd), [],
                         "each trial must start from a clean environment")

    def test_final_text_reads_the_answer_the_user_would_see(self):
        path = os.path.join(self.root, "stream.jsonl")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(init_event() + "\n")
            fh.write(text_event("Working on it.") + "\n")
            fh.write(tool_event("Bash", command="ls") + "\n")
            fh.write(text_event("Here is the plan.") + "\n")
        text = harness.final_text(path)
        self.assertIn("Here is the plan.", text)
        self.assertIn("Working on it.", text)

    def test_final_text_tolerates_a_missing_stream(self):
        self.assertEqual(harness.final_text(os.path.join(self.root, "nope")), "")


if __name__ == "__main__":
    unittest.main()
