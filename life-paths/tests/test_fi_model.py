"""Tests for scripts/fi_model.py. Run from the skill directory:
    python3 -m unittest discover tests
"""

import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import fi_model as fm  # noqa: E402


def base_cfg(**over):
    cfg = {
        "current_age": 60, "retire_age": 60, "horizon_age": 62,
        "current_assets": 100, "annual_savings": 0,
        "retirement_spending": 10,
        "real_return_mean": 0.0, "real_return_std": 0.0,
        "sims": 3, "seed": 1,
    }
    cfg.update(over)
    return cfg


class TestParams(unittest.TestCase):
    def test_lognormal_params_moments(self):
        mu, sig = fm.lognormal_params(0.06, 0.13)
        implied_mean = math.exp(mu + sig * sig / 2.0) - 1.0
        self.assertAlmostEqual(implied_mean, 0.06, places=10)

    def test_pct_interpolation(self):
        self.assertEqual(fm.pct([1, 2, 3, 4, 5], 50), 3)
        self.assertAlmostEqual(fm.pct([1, 2, 3, 4, 5], 25), 2.0)

    def test_pct_empty_raises(self):
        with self.assertRaises(ValueError):
            fm.pct([], 50)

    def test_validate_config(self):
        fm.validate_config(base_cfg())  # a good config passes
        bad = [
            base_cfg(retire_age=99),            # retirement beyond horizon
            base_cfg(horizon_age=55),           # horizon before current age
            base_cfg(sims=0),                   # nothing to simulate
            {k: v for k, v in base_cfg().items() if k != "retire_age"},
        ]
        for cfg in bad:
            with self.assertRaises(ValueError):
                fm.validate_config(cfg)

    def test_savings_schedule_scalar_and_list(self):
        cfg = base_cfg(current_age=60, retire_age=63, annual_savings=10)
        self.assertEqual(fm.savings_schedule(cfg), [10.0, 10.0, 10.0])
        cfg = base_cfg(current_age=60, retire_age=63, annual_savings=[5, 6])
        self.assertEqual(fm.savings_schedule(cfg), [5, 6, 0.0])  # padded


class TestDeterministicRuns(unittest.TestCase):
    """With std=0 the lognormal draw is exactly the mean, so every path is
    hand-checkable arithmetic."""

    def test_pure_drawdown(self):
        # Zero return: 100 -> 90 -> 80 -> 70 over ages 60,61,62.
        ages, paths, spends, depleted, n = fm.run_sims(base_cfg(), random.Random(1))
        self.assertEqual(ages, [60, 61, 62])
        for wp in paths:
            self.assertEqual([round(w) for w in wp], [90, 80, 70])
        self.assertEqual(depleted, 0)
        for s in spends:
            self.assertEqual(s, [10.0, 10.0, 10.0])

    def test_accumulation_then_retirement(self):
        # Save 10 at 60 and 61, retire at 62: 110, 120, then 120 - 5 = 115.
        cfg = base_cfg(retire_age=62, annual_savings=10, retirement_spending=5)
        _, paths, _, depleted, _ = fm.run_sims(cfg, random.Random(1))
        for wp in paths:
            self.assertEqual([round(w) for w in wp], [110, 120, 115])
        self.assertEqual(depleted, 0)

    def test_income_stream_offsets_withdrawal(self):
        cfg = base_cfg(income_streams=[{"start_age": 61, "annual": 10}])
        _, paths, _, _, _ = fm.run_sims(cfg, random.Random(1))
        # Age 60: 100-10=90; ages 61-62: net withdrawal 0 -> flat 90.
        for wp in paths:
            self.assertEqual([round(w) for w in wp], [90, 90, 90])

    def test_income_stream_pays_during_accumulation(self):
        # Rent from 60 while retiring at 62: it accrues alongside savings,
        # not only after retirement. 0+10, 10+10, then retirement covers
        # the 10 withdrawal exactly: 20+10-10 = 20.
        cfg = base_cfg(retire_age=62, current_assets=0,
                       income_streams=[{"start_age": 60, "annual": 10}])
        _, paths, _, _, _ = fm.run_sims(cfg, random.Random(1))
        for wp in paths:
            self.assertEqual([round(w) for w in wp], [10, 20, 20])

    def test_depletion_counts(self):
        cfg = base_cfg(current_assets=15, horizon_age=63)
        _, paths, _, depleted, n = fm.run_sims(cfg, random.Random(1))
        self.assertEqual(depleted, n)  # 15 cannot fund 4 years of 10

    def test_guardrail_cut_fires(self):
        # Retire at 100 with spending 10 (initial WR 10%). A -50% return
        # year pushes WR far past 1.2x; spending must fall below 10.
        cfg = base_cfg(horizon_age=64, real_return_mean=-0.5,
                       guardrails={"enabled": True, "cut_trigger": 1.2,
                                   "raise_trigger": 0.8, "adjust_pct": 0.10,
                                   "active_years": 30})
        _, _, spends, _, _ = fm.run_sims(cfg, random.Random(1))
        for s in spends:
            self.assertEqual(s[0], 10.0)
            self.assertLess(s[1], 10.0)


class TestSummary(unittest.TestCase):
    def test_summary_shapes(self):
        cfg = base_cfg(sims=50, real_return_std=0.10)
        rng = random.Random(cfg["seed"])
        res = fm.summarize(cfg, *fm.run_sims(cfg, rng))
        self.assertIn("survival_rate", res)
        self.assertIn(60, res["wealth_percentiles"])
        for p in fm.PCTS:
            self.assertIn(p, res["lifetime_spending_percentiles"])


if __name__ == "__main__":
    unittest.main()
