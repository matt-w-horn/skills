"""Tests for tools/eval/lint_evals.py. Run from the tools/eval directory:
    python3 -m unittest discover tests

Every test builds a throwaway corpus and perturbs exactly one thing. Each detector here has been
observed to fire on input built to trip it. A detector nobody has watched fail cannot be
distinguished from a detector that returns green unconditionally, and green is
the direction broken instruments fail in.

`test_clean_corpus_passes` is the other half of that: it pins that the rules
don't fire on good input, so a passing corpus means something.
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import lint_evals as le  # noqa: E402

ALPHA_DESC = (
    "Build a long-horizon financial plan covering retirement timing, savings "
    "and drawdown for a person. Use whenever someone asks when they can retire "
    "or whether their money supports leaving work."
)
BETA_DESC = (
    "Map realistic long-term career paths for a person grounded in their record. "
    "Use whenever someone asks what to do with their career or is weighing a "
    "job offer against going independent."
)
ALPHA_BODY = "Distinctive alpha guidance about verified registers and floors.\n"
BETA_BODY = "Distinctive beta guidance about falsifiers and evidence ledgers.\n"

# Queries are assembled from independent pools so that no two share enough
# vocabulary to look like duplicates. Templated fixtures trip the duplicates
# rule, which is the rule doing its job, but it makes the clean baseline
# untestable, so the fixture has to be as varied as a real corpus.
WHO = ["a district nurse in Leeds", "a warehouse supervisor near Rotherham",
       "a freelance cellist", "a dental hygienist", "a lorry mechanic",
       "a primary school caretaker", "a pharmacist in Swansea",
       "a scaffolder", "a bakery owner", "a probation officer",
       "a marine surveyor", "a piano tuner", "a farrier", "a locksmith"]
# Pool lengths are deliberately coprime-ish and unequal: indexing each by
# `seed % len(pool)` then makes every seed in range produce a distinct
# combination in all four slots. Equal-length pools collide every cycle, which
# is how the first version of this fixture generated real duplicates.
SITUATION = ["the mill closed last spring", "my mother moved in with us",
             "the lease on the unit ends soon", "our youngest starts college",
             "the union negotiated a new shift pattern", "we sold the caravan",
             "my back gave out in February", "the franchise changed hands",
             "we finally cleared the credit cards", "the allotment flooded",
             "my brother offered me a partnership", "the depot relocated",
             "our tenant left without notice"]                       # 13
CONCERN = ["whether the sums actually hold up over decades",
           "if stepping back to four days breaks anything long term",
           "how much cushion we genuinely need before I stop earning",
           "whether the numbers survive a bad decade early on",
           "what happens to the money once the wages stop",
           "if we can afford for me to go part time from spring",
           "whether leaving at sixty is remotely realistic",
           "how thin things get if markets disappoint",
           "what the drawdown side of this actually looks like",
           "whether our savings rate is anywhere near enough",
           "if the pension gap between us matters"]                  # 11
DETAIL = ["we keep about eleven thousand in an emergency fund",
          "the mortgage has nine years left on it",
          "there is a small inheritance coming, maybe",
          "neither of us has a defined benefit scheme",
          "my partner earns roughly half what I do",
          "the shop turns over less than it did",
          "I have a frozen scheme from two jobs ago",
          "we bought the flat outright in 2011",
          "our outgoings jumped when the childcare started"]         # 9
NEAR_MISS_TOPIC = [
    "the provider wants a form for moving savings between two funds and I "
    "cannot tell which box covers a straight transfer",
    "I need to understand why my retirement account statement shows two "
    "different balances on the same page",
    "can you explain how the tax relief is actually credited on a workplace "
    "pension contribution each month",
    "the mortgage lender wants a redemption figure and I want to check their "
    "arithmetic on the early repayment charge",
    "what is the difference between an accumulation and an income unit in a "
    "tracker fund, plainly",
    "my payslip deductions changed this month and I want to work out which "
    "line item moved and why",
    "help me fix the broken formula in the savings column of a budget sheet I "
    "have been keeping",
    "which of these two index funds has the lower ongoing charge once you "
    "account for the platform fee",
    "explain how salary sacrifice interacts with statutory maternity pay in "
    "practical terms",
    "I want to know whether a cash ISA transfer resets the annual allowance "
    "for the rest of the year",
]
CROSS_TOPIC = [
    "there is an offer on the table from a smaller firm that pays less but the "
    "work looks better, and I keep circling what the next decade looks like",
    "I have been asked to take over the department and I genuinely do not know "
    "whether that is the direction I want the rest of this to go",
    "after the redundancy I could retrain, go independent, or take the safe "
    "role, and I cannot see which version of me is at the end of each",
    "my partner has been offered a post abroad and it forces a question about "
    "what I actually want the working part of my life to be",
]


def _query(qid, owner, expect, split, text):
    return {"id": qid, "query": text, "expect": expect, "why": "test label",
            "split": split}


def _pick(pool, seed):
    return pool[seed % len(pool)]


def _varied(seed, tail=""):
    """A sentence assembled so that different seeds share little vocabulary."""
    return (
        f"I am {_pick(WHO, seed)}, {_pick(SITUATION, seed)}, and I want to work "
        f"out {_pick(CONCERN, seed)}. For context {_pick(DETAIL, seed)}.{tail}"
    )


def build_queries(owner, other):
    """A balanced, stratified, lint-clean query set for one skill.

    Seeds are globally unique across skills so no two queries anywhere in the
    fixture can collide.
    """
    base = 0 if owner.startswith("alpha") else 200
    out = []
    for i in range(12):
        split = "train" if i < 7 else "validation"
        out.append(_query(f"{owner[0]}-p{i:02d}", owner,
                          {owner: True, other: False}, split,
                          _varied(base + i)))
    for i in range(9):
        seed = base + 40 + i
        split = "train" if i < 5 else "validation"
        out.append(_query(f"{owner[0]}-n{i:02d}", owner,
                          {owner: False, other: False}, split,
                          f"I am {_pick(WHO, seed)} with a quick question about "
                          f"my savings and retirement paperwork: "
                          f"{_pick(NEAR_MISS_TOPIC, seed)}. For context "
                          f"{_pick(DETAIL, seed)}."))
    for i in range(3):
        seed = base + 70 + i
        split = "train" if i < 2 else "validation"
        out.append(_query(f"{owner[0]}-x{i:02d}", owner,
                          {owner: False, other: True}, split,
                          f"{_pick(CROSS_TOPIC, seed)}. I am {_pick(WHO, seed)}, "
                          f"{_pick(SITUATION, seed)}, and {_pick(DETAIL, seed)}."))
    for i in range(4):
        out.append(_query(f"{owner[0]}-s{i:02d}", owner,
                          {owner: True, other: False}, "sealed",
                          _varied(base + 100 + i,
                                  tail=" It has been on my mind for a while.")))
    return out


def make_skill(root, name, description, body):
    sdir = os.path.join(root, name)
    os.makedirs(sdir, exist_ok=True)
    with open(os.path.join(sdir, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(f"---\nname: {name}\ndescription: {description}\n---\n\n{body}")
    return sdir


def write_trigger(sdir, skill, queries):
    edir = os.path.join(sdir, "evals")
    os.makedirs(edir, exist_ok=True)
    with open(os.path.join(edir, "trigger.json"), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "skill": skill, "queries": queries}, fh)


def write_execution(sdir, skill, eval_id="probe-eval", shape="seeded-defect",
                    assertions=None, defects=None, fixture_text=None):
    edir = os.path.join(sdir, "evals", "execution", eval_id)
    os.makedirs(os.path.join(edir, "fixture"), exist_ok=True)
    os.makedirs(os.path.join(edir, "reference"), exist_ok=True)

    assertions = assertions or [
        {"id": "a1", "text": "The response states the planning horizon ends "
                             "before age ninety.", "good_expect": True,
         "bad_expect": False},
        {"id": "a2", "text": "The response names the return assumption used.",
         "good_expect": True, "bad_expect": True},
    ]
    defects = defects if defects is not None else [
        {"id": "d1", "summary": "Horizon truncated at 85", "assertion": "a1"}]

    with open(os.path.join(edir, "eval.json"), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "id": eval_id, "skill": skill, "shape": shape,
                   "prompt_file": "prompt.md", "fixture_dir": "fixture",
                   "planted_defects": defects}, fh)
    with open(os.path.join(edir, "prompt.md"), "w", encoding="utf-8") as fh:
        fh.write("Please look over the numbers I put together and tell me what is wrong.\n")
    with open(os.path.join(edir, "rubric.json"), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "assertions": assertions}, fh)
    for name in ("good.md", "bad.md"):
        with open(os.path.join(edir, "reference", name), "w", encoding="utf-8") as fh:
            fh.write(f"# {name}\n\nA reference response.\n")
    with open(os.path.join(edir, "fixture", "model.md"), "w", encoding="utf-8") as fh:
        fh.write(fixture_text if fixture_text is not None
                 else "Synthetic test data - not a real person.\n\nHorizon: age 85.\n")
    return edir


class LintCase(unittest.TestCase):
    """Builds a clean two-skill corpus, then lets each test break one thing."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

        self.alpha = make_skill(self.root, "alpha-skill", ALPHA_DESC, ALPHA_BODY)
        self.beta = make_skill(self.root, "beta-skill", BETA_DESC, BETA_BODY)
        write_trigger(self.alpha, "alpha-skill",
                      build_queries("alpha-skill", "beta-skill"))
        write_trigger(self.beta, "beta-skill",
                      build_queries("beta-skill", "alpha-skill"))
        write_execution(self.alpha, "alpha-skill")

    def lint(self):
        return le.lint(self.root)

    def rules_fired(self, rep):
        joined = rep.errors + rep.warnings
        return {line.split("]")[0].lstrip("[") for line in joined}

    def assertFires(self, rule, rep, where="errors"):
        pool = rep.errors if where == "errors" else rep.warnings
        self.assertTrue(
            any(line.startswith(f"[{rule}]") for line in pool),
            f"expected rule {rule!r} to fire in {where}; got "
            f"errors={rep.errors} warnings={rep.warnings}")

    # -- the baseline -----------------------------------------------------

    def test_clean_corpus_passes(self):
        rep = self.lint()
        self.assertEqual(rep.errors, [], f"clean corpus reported errors: {rep.errors}")

    # -- one test per detector -------------------------------------------

    def test_balance_fires_when_negatives_are_dropped(self):
        queries = [q for q in build_queries("alpha-skill", "beta-skill")
                   if "-n" not in q["id"] and "-x" not in q["id"]]
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("balance", self.lint())

    def test_balance_fires_on_too_many_either_labels(self):
        """The cap must fire on its own, not because the corpus went lopsided.

        The first version of this test relabelled 9 positives, which dropped
        the positive count under the class minimum; `[balance]` then fired for
        that reason and the cap branch was never exercised. Take the `either`
        labels from both classes so the corpus stays balanced.
        """
        queries = build_queries("alpha-skill", "beta-skill")
        picked = ([q for q in queries if "-p" in q["id"]][:5]
                  + [q for q in queries if "-n" in q["id"]][:5])
        for q in picked:
            q["expect"] = {"alpha-skill": "either", "beta-skill": "either"}
        write_trigger(self.alpha, "alpha-skill", queries)
        rep = self.lint()
        self.assertTrue(
            any("either" in e for e in rep.errors),
            f"expected the either-cap to fire specifically; got {rep.errors}")

    def test_splits_fires_when_a_split_is_single_class(self):
        queries = build_queries("alpha-skill", "beta-skill")
        for q in queries:
            if q["split"] == "validation":
                q["expect"] = {"alpha-skill": True, "beta-skill": False}
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("splits", self.lint())

    def test_splits_fires_when_validation_is_empty(self):
        queries = build_queries("alpha-skill", "beta-skill")
        for q in queries:
            if q["split"] == "validation":
                q["split"] = "train"
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("splits", self.lint())

    def test_duplicates_fires_on_near_identical_queries(self):
        queries = build_queries("alpha-skill", "beta-skill")
        queries[1]["query"] = queries[0]["query"]
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("duplicates", self.lint())

    def test_substance_fires_on_a_trivial_query(self):
        queries = build_queries("alpha-skill", "beta-skill")
        queries[0]["query"] = "when can i retire"
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("substance", self.lint())

    def test_self_contained_fires_on_a_file_path(self):
        queries = build_queries("alpha-skill", "beta-skill")
        queries[0]["query"] += " the numbers are in ~/Downloads/retirement.xlsx"
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("self-contained", self.lint())

    def test_self_contained_fires_on_a_bare_filename(self):
        queries = build_queries("alpha-skill", "beta-skill")
        queries[0]["query"] += " see budget.csv for the detail"
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("self-contained", self.lint())

    def test_self_contained_warns_on_an_artifact_it_is_asked_to_open(self):
        queries = build_queries("alpha-skill", "beta-skill")
        queries[0]["query"] += " Can you review my spreadsheet and tell me?"
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("self-contained", self.lint(), where="warnings")

    def test_self_contained_allows_an_artifact_merely_mentioned(self):
        """Background colour is not a dependency; only a demand to open one is."""
        queries = build_queries("alpha-skill", "beta-skill")
        queries[0]["query"] += " I have kept a spreadsheet since 2019."
        write_trigger(self.alpha, "alpha-skill", queries)
        rep = self.lint()
        self.assertNotIn("self-contained", self.rules_fired(rep))

    def test_near_miss_warns_on_an_unrelated_negative(self):
        queries = build_queries("alpha-skill", "beta-skill")
        for q in queries:
            if "-n" in q["id"]:
                q["query"] = ("please write me a python function that returns "
                              "the fibonacci sequence up to a given integer "
                              "limit using an iterative approach")
                break
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("near-miss", self.lint(), where="warnings")

    def test_leakage_fires_when_a_query_echoes_the_skill_body(self):
        body = ("The floor is the risk metric and every plan reports the tenth "
                "percentile lifetime spending against actual lifestyle.\n")
        make_skill(self.root, "alpha-skill", ALPHA_DESC, body)
        queries = build_queries("alpha-skill", "beta-skill")
        queries[0]["query"] = (
            "i want a plan where the floor is the risk metric and every plan "
            "reports the tenth percentile lifetime spending, can you do that "
            "for our situation over the next few decades")
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("leakage", self.lint())

    def test_leakage_fires_when_an_assertion_echoes_the_skill_body(self):
        body = ("Any bespoke module gets its own tests before its outputs are "
                "trusted, at minimum a zero volatility analytic case.\n")
        make_skill(self.root, "alpha-skill", ALPHA_DESC, body)
        write_execution(self.alpha, "alpha-skill", assertions=[
            {"id": "a1",
             "text": "Any bespoke module gets its own tests before its outputs "
                     "are trusted in the response.",
             "good_expect": True, "bad_expect": False}])
        self.assertFires("leakage", self.lint())

    def test_leakage_ignores_ordinary_english(self):
        """A shared stopword-heavy phrase is not evidence of paraphrase."""
        body = "It is one of the things that you would want to do here.\n"
        make_skill(self.root, "alpha-skill", ALPHA_DESC, body)
        queries = build_queries("alpha-skill", "beta-skill")
        queries[0]["query"] = (
            "it is one of the things that you would want to do here, so please "
            "help me think about when i could stop working entirely")
        write_trigger(self.alpha, "alpha-skill", queries)
        rep = self.lint()
        self.assertNotIn("leakage", self.rules_fired(rep))

    def test_assertions_fires_on_a_judgment_word(self):
        write_execution(self.alpha, "alpha-skill", assertions=[
            {"id": "a1", "text": "The response is comprehensive about horizons.",
             "good_expect": True, "bad_expect": False}])
        self.assertFires("assertions", self.lint())

    def test_assertions_warns_on_two_claims_joined_by_and(self):
        write_execution(self.alpha, "alpha-skill", assertions=[
            {"id": "a1",
             "text": "The response states the horizon is too short and names "
                     "the return assumption used in the projection.",
             "good_expect": True, "bad_expect": False}])
        self.assertFires("assertions", self.lint(), where="warnings")

    def test_calibration_fires_when_nothing_can_fail(self):
        write_execution(self.alpha, "alpha-skill", assertions=[
            {"id": "a1", "text": "The response names the return assumption.",
             "good_expect": True, "bad_expect": True}],
            defects=[])
        self.assertFires("calibration", self.lint())

    def test_calibration_fires_on_a_missing_reference(self):
        edir = write_execution(self.alpha, "alpha-skill")
        os.remove(os.path.join(edir, "reference", "bad.md"))
        self.assertFires("calibration", self.lint())

    def test_calibration_fires_when_seeded_eval_plants_nothing(self):
        write_execution(self.alpha, "alpha-skill", shape="seeded-defect",
                        defects=[])
        self.assertFires("calibration", self.lint())

    def test_fixtures_fires_on_a_skill_md_under_evals(self):
        stray = os.path.join(self.alpha, "evals", "execution", "probe-eval",
                             "fixture", "SKILL.md")
        with open(stray, "w", encoding="utf-8") as fh:
            fh.write("---\nname: nope\ndescription: x\n---\n")
        self.assertFires("fixtures", self.lint())

    def test_fixtures_fires_on_an_unmarked_fixture(self):
        write_execution(self.alpha, "alpha-skill",
                        fixture_text="Horizon: age 85. Returns: 7 percent.\n")
        self.assertFires("fixtures", self.lint())

    def test_fixtures_fires_on_a_reserved_path_token(self):
        os.makedirs(os.path.join(self.alpha, "scripts"), exist_ok=True)
        with open(os.path.join(self.alpha, "scripts", "real.py"), "w",
                  encoding="utf-8") as fh:
            fh.write("pass\n")
        edir = os.path.join(self.alpha, "evals", "execution", "probe-eval")
        with open(os.path.join(edir, "prompt.md"), "a", encoding="utf-8") as fh:
            fh.write("\nI ran scripts/missing_model.py against it last week.\n")
        self.assertFires("fixtures", self.lint())

    def test_schema_fires_on_malformed_json(self):
        with open(os.path.join(self.alpha, "evals", "trigger.json"), "w",
                  encoding="utf-8") as fh:
            fh.write("{not json")
        self.assertFires("schema", self.lint())

    def test_schema_fires_on_a_missing_expect_key(self):
        queries = build_queries("alpha-skill", "beta-skill")
        queries[0]["expect"] = {"alpha-skill": True}       # beta-skill missing
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("schema", self.lint())

    def test_schema_fires_on_a_duplicate_query_id(self):
        queries = build_queries("alpha-skill", "beta-skill")
        queries[1]["id"] = queries[0]["id"]
        write_trigger(self.alpha, "alpha-skill", queries)
        self.assertFires("schema", self.lint())


class RealCorpus(unittest.TestCase):
    """The committed corpus lints with no errors and no unexpected warnings.

    Warnings are not pinned to zero, unlike the repo validator's own real-tree
    test. The corpus carries a handful on purpose: each bad reference is built
    to catch one or two of the easy planted defects, so that it fools a skim
    rather than failing everything, and the assertions for those defects are
    legitimately expected to pass on it. Pinning warnings to zero would force
    that design out. Pinning the *kinds* still catches a new class appearing.
    """

    ACCEPTED = {"calibration"}

    def test_repo_corpus_lints(self):
        import corpus as c
        skills = c.skill_names()
        if not skills or not all(
            os.path.exists(os.path.join(c.SKILLS_DIR, s, "evals", "trigger.json"))
            for s in skills
        ):
            self.skipTest("trigger corpus not complete for every skill yet")
        rep = le.lint()
        self.assertEqual(rep.errors, [])
        unexpected = [w for w in rep.warnings
                      if w.split("]")[0].lstrip("[") not in self.ACCEPTED]
        self.assertEqual(unexpected, [],
                         "a warning of a kind the corpus does not knowingly carry")


if __name__ == "__main__":
    unittest.main()
