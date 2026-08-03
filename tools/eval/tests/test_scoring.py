"""Tests for the trigger scorer in tools/eval/run_trigger.py. Run from
tools/eval:
    python3 -m unittest discover tests

Scoring is where a sweep turns into a claim, and every one of its judgment
calls is silent: a threshold that rounds the wrong way, an errored run counted
as a non-trigger, an "either" label that passes when nothing fired. None of
those raise. They just produce a number that looks like the others.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import run_trigger  # noqa: E402

SKILLS = ["financial-planning", "life-paths"]
FP, LP = SKILLS


def query(qid, expect, owner=FP, split="train"):
    return {"id": qid, "query": "a long enough question about the future",
            "expect": expect, "why": "test", "split": split, "owner": owner}


def runs(qid, fired_per_run, void=None):
    """One record per run; `fired_per_run` lists the skills fired each time."""
    return [{"query_id": qid, "index": i, "skills_invoked": list(fired),
             "void": void, "outcome": "triggered" if fired else "no_trigger"}
            for i, fired in enumerate(fired_per_run)]


class Positives(unittest.TestCase):
    def row(self, fired_per_run, expect=None):
        q = query("q1", expect or {FP: True, LP: False})
        summary = run_trigger.score([q], runs("q1", fired_per_run), SKILLS)
        return summary["rows"][0]

    def test_always_firing_passes(self):
        row = self.row([[FP], [FP], [FP]])
        self.assertTrue(row["passed"])
        self.assertEqual(row["rates"][FP], 1.0)

    def test_two_of_three_passes_at_the_threshold(self):
        row = self.row([[FP], [FP], []])
        self.assertAlmostEqual(row["rates"][FP], 2 / 3)
        self.assertTrue(row["passed"])

    def test_one_of_three_fails(self):
        row = self.row([[FP], [], []])
        self.assertAlmostEqual(row["rates"][FP], 1 / 3)
        self.assertFalse(row["passed"])

    def test_never_firing_fails(self):
        self.assertFalse(self.row([[], [], []])["passed"])

    def test_the_wrong_skill_firing_fails_the_query(self):
        """Routing to the neighbour is a miss, not a pass on a technicality."""
        row = self.row([[LP], [LP], [LP]])
        self.assertEqual(row["rates"][FP], 0.0)
        self.assertEqual(row["rates"][LP], 1.0)
        self.assertFalse(row["passed"])


class Negatives(unittest.TestCase):
    def row(self, fired_per_run):
        q = query("q1", {FP: False, LP: False})
        return run_trigger.score([q], runs("q1", fired_per_run), SKILLS)["rows"][0]

    def test_silence_passes(self):
        self.assertTrue(self.row([[], [], []])["passed"])

    def test_firing_twice_fails(self):
        self.assertFalse(self.row([[FP], [FP], []])["passed"])

    def test_firing_once_still_passes(self):
        """One run in three is below the threshold; report the rate, not a veto."""
        row = self.row([[FP], [], []])
        self.assertAlmostEqual(row["rates"][FP], 1 / 3)
        self.assertTrue(row["passed"])


class CrossSkill(unittest.TestCase):
    def test_both_expectations_must_hold(self):
        q = query("q1", {FP: False, LP: True})
        rows = run_trigger.score([q], runs("q1", [[LP], [LP], [LP]]), SKILLS)["rows"]
        self.assertTrue(rows[0]["passed"])
        self.assertEqual(rows[0]["class"], "cross")

    def test_right_answer_absent_fails_even_if_the_wrong_one_is_silent(self):
        q = query("q1", {FP: False, LP: True})
        rows = run_trigger.score([q], runs("q1", [[], [], []]), SKILLS)["rows"]
        self.assertFalse(rows[0]["passed"])


class MixedEither(unittest.TestCase):
    """One skill required, the other merely permitted.

    This shape is most of the "either" corpus: a query that must reach one
    skill, where reaching the neighbour too would also be defensible. The
    permissive label constrains nothing on its own skill, so the query stands
    or falls on the definite expectation. Scoring it as though the permitted
    skill were required fails queries that routed exactly as intended.
    """

    def row(self, expect, fired_per_run):
        q = query("q1", expect)
        return run_trigger.score([q], runs("q1", fired_per_run), SKILLS)["rows"][0]

    def test_required_skill_fires_and_permitted_one_does_not(self):
        row = self.row({FP: True, LP: run_trigger.corpus.EITHER},
                       [[FP], [FP], [FP]])
        self.assertTrue(row["passed"],
                        "fp was required and fired; lp was optional and silent")

    def test_required_skill_fires_and_permitted_one_also_would(self):
        row = self.row({FP: True, LP: run_trigger.corpus.EITHER},
                       [[LP], [FP], [FP]])
        self.assertTrue(row["passed"])

    def test_required_skill_silent_fails_even_if_permitted_one_fires(self):
        row = self.row({FP: True, LP: run_trigger.corpus.EITHER},
                       [[LP], [LP], [LP]])
        self.assertFalse(row["passed"], "the required skill never fired")

    def test_required_skill_must_not_fire_when_labelled_false(self):
        row = self.row({FP: False, LP: run_trigger.corpus.EITHER},
                       [[FP], [FP], [FP]])
        self.assertFalse(row["passed"])


class Either(unittest.TestCase):
    """With no definite expectation, `either` must not pass on a total miss."""

    def row(self, fired_per_run):
        q = query("q1", {FP: run_trigger.corpus.EITHER,
                         LP: run_trigger.corpus.EITHER})
        return run_trigger.score([q], runs("q1", fired_per_run), SKILLS)["rows"][0]

    def test_one_skill_firing_passes(self):
        self.assertTrue(self.row([[FP], [FP], [FP]])["passed"])

    def test_the_other_skill_firing_also_passes(self):
        self.assertTrue(self.row([[LP], [LP], [LP]])["passed"])

    def test_nothing_firing_fails(self):
        self.assertFalse(self.row([[], [], []])["passed"])

    def test_below_threshold_fails(self):
        """Fired once in three is not "either skill is fine", it is a miss."""
        self.assertFalse(self.row([[FP], [], []])["passed"])


class Threshold(unittest.TestCase):
    """Exactly on the line decides nothing, whichever label the query carries.

    Reachable because voiding a run leaves an even denominator, and it must
    not be read as a pass for a positive and a fail for a negative: that would
    make one firing in two mean opposite things depending on the label.
    """

    def row(self, expect, fired_per_run, void_last=False):
        q = query("q1", expect)
        records = runs("q1", fired_per_run)
        if void_last:
            records[-1]["void"] = "run errored"
        return run_trigger.score([q], records, SKILLS)["rows"][0]

    def test_positive_at_exactly_half_is_ungraded(self):
        row = self.row({FP: True, LP: False}, [[FP], [], []], void_last=True)
        self.assertEqual(row["runs"], 2)
        self.assertAlmostEqual(row["rates"][FP], 0.5)
        self.assertIsNone(row["passed"])

    def test_negative_at_exactly_half_is_ungraded(self):
        row = self.row({FP: False, LP: False}, [[FP], [], []], void_last=True)
        self.assertAlmostEqual(row["rates"][FP], 0.5)
        self.assertIsNone(row["passed"])

    def test_above_half_still_passes_a_positive(self):
        self.assertTrue(self.row({FP: True, LP: False}, [[FP], [FP], []])["passed"])

    def test_below_half_still_passes_a_negative(self):
        self.assertTrue(self.row({FP: False, LP: False}, [[FP], [], []])["passed"])


class VoidedRuns(unittest.TestCase):
    def test_voided_runs_leave_the_denominator(self):
        """An unreachable model is not evidence about a description."""
        q = query("q1", {FP: True, LP: False})
        records = runs("q1", [[FP], [FP]]) + runs("q1", [[]], void="run errored")
        records[-1]["index"] = 2
        row = run_trigger.score([q], records, SKILLS)["rows"][0]
        self.assertEqual(row["runs"], 2)
        self.assertEqual(row["excluded"], 1)
        self.assertEqual(row["rates"][FP], 1.0, "2 usable runs, both fired")
        self.assertTrue(row["passed"])

    def test_a_query_whose_runs_all_failed_is_ungraded(self):
        q = query("q1", {FP: True, LP: False})
        records = runs("q1", [[], [], []], void="claude did not start")
        summary = run_trigger.score([q], records, SKILLS)
        self.assertIsNone(summary["rows"][0]["passed"])
        self.assertEqual(summary["ungraded"], 1)
        self.assertEqual(summary["graded"], 0)
        self.assertEqual(summary["passed"], 0,
                         "an ungraded query must not be counted as a pass")


class Aggregate(unittest.TestCase):
    def test_totals_and_confusion_matrix(self):
        queries = [query("hit", {FP: True, LP: False}),
                   query("miss", {FP: True, LP: False}),
                   query("quiet", {FP: False, LP: False})]
        records = (runs("hit", [[FP], [FP], [FP]])
                   + runs("miss", [[], [], []])
                   + runs("quiet", [[], [], []]))
        summary = run_trigger.score(queries, records, SKILLS)
        self.assertEqual(summary["queries"], 3)
        self.assertEqual(summary["graded"], 3)
        self.assertEqual(summary["passed"], 2)
        self.assertEqual(summary["failed"], 1)
        counted = sum(cell["count"] for cell in summary["confusion"])
        self.assertEqual(counted, 9, "every usable run lands in exactly one cell")


if __name__ == "__main__":
    unittest.main()
