"""Tests for simcore. Run from the skill directory:
    python3 -m unittest discover tests

Deterministic where possible; the one statistical test is seeded. These
tests are also the pattern for bespoke run-code tests: a zero-volatility
analytic case, a conservation check, and direct exercises of any policy
logic.
"""

import math
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import simcore as sc  # noqa: E402


class TestRandomness(unittest.TestCase):
    def test_lognormal_params_moments(self):
        mean, std = 0.06, 0.13
        mu, sig = sc.lognormal_params(mean, std)
        implied_mean = math.exp(mu + sig * sig / 2.0) - 1.0
        implied_var = (math.exp(sig * sig) - 1.0) * math.exp(2 * mu + sig * sig)
        self.assertAlmostEqual(implied_mean, mean, places=10)
        self.assertAlmostEqual(math.sqrt(implied_var), std, places=10)

    def test_zero_std_is_deterministic(self):
        r = sc.rng(1)
        rets = sc.lognormal_returns(r, 0.05, 0.0, 10)
        for x in rets:
            self.assertAlmostEqual(x, 0.05, places=12)

    def test_statistical_mean_converges(self):
        r = sc.rng(42)
        rets = sc.lognormal_returns(r, 0.05, 0.13, 30000)
        self.assertAlmostEqual(sum(rets) / len(rets), 0.05, delta=0.005)


class TestHistorical(unittest.TestCase):
    def test_windows(self):
        w = sc.historical_windows([0.1, 0.2, 0.3, 0.4], 2)
        self.assertEqual(w, [[0.1, 0.2], [0.2, 0.3], [0.3, 0.4]])
        with self.assertRaises(ValueError):
            sc.historical_windows([0.1], 2)

    def test_block_bootstrap(self):
        src = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]
        out = sc.block_bootstrap(sc.rng(3), src, 17, block=4)
        self.assertEqual(len(out), 17)
        self.assertTrue(all(x in src for x in out))

    def test_block_bootstrap_empty_series_raises(self):
        with self.assertRaises(ValueError):
            sc.block_bootstrap(sc.rng(3), [], 5)

    def test_blend(self):
        self.assertEqual(sc.blend([0.1, 0.2], [0.0, 0.0], 0.8),
                         [0.08000000000000002, 0.16000000000000003])
        with self.assertRaises(ValueError):
            sc.blend([0.1], [0.1, 0.2], 0.5)

    def test_load_returns_csv(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write("year,real_return\n1966,-0.132\n1967,0.201\n")
            path = f.name
        try:
            self.assertEqual(sc.load_returns_csv(path), [-0.132, 0.201])
        finally:
            os.unlink(path)

    def test_load_returns_csv_skips_short_rows_and_rejects_empty(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write("year,real_return\n1966\n1967,0.05\n")  # ragged row skipped
            path = f.name
        try:
            self.assertEqual(sc.load_returns_csv(path), [0.05])
        finally:
            os.unlink(path)
        for content in ("", "year,real_return\n"):  # empty / header-only
            with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
                f.write(content)
                path = f.name
            try:
                with self.assertRaises(ValueError):
                    sc.load_returns_csv(path)
            finally:
                os.unlink(path)


class TestLedger(unittest.TestCase):
    def test_zero_return_annuity_depletes_exactly(self):
        # Hand math: 100 wealth, withdraw 10/yr, zero return -> zero at year 10.
        returns = [0.0] * 12
        path, flows = sc.simulate_ledger(100, returns, lambda t, w: -10.0)
        self.assertEqual(path[:10], [90, 80, 70, 60, 50, 40, 30, 20, 10, 0])
        self.assertEqual(path[10:], [0, 0])
        self.assertEqual(flows[9], -10.0)   # exact final withdrawal
        self.assertEqual(flows[10], 0.0)    # nothing left to withdraw

    def test_depletion_truncates_realized_flow(self):
        path, flows = sc.simulate_ledger(5, [0.0], lambda t, w: -10.0)
        self.assertEqual(path, [0.0])
        self.assertEqual(flows, [-5.0])     # only what existed was withdrawn

    def test_conservation_random(self):
        r = sc.rng(7)
        returns = sc.lognormal_returns(r, 0.05, 0.15, 40)
        policy = lambda t, w: 20.0 if t < 10 else -15.0  # noqa: E731
        path, flows = sc.simulate_ledger(100, returns, policy)
        self.assertTrue(sc.check_conservation(100, returns, flows, path))

    def test_growth_with_contribution(self):
        # 100 * 1.10 + 10 = 120; 120 * 1.10 + 10 = 142.
        path, _ = sc.simulate_ledger(100, [0.10, 0.10], lambda t, w: 10.0)
        self.assertAlmostEqual(path[0], 120.0, places=9)
        self.assertAlmostEqual(path[1], 142.0, places=9)


class TestGuardrailPolicy(unittest.TestCase):
    def test_initial_wr_and_no_adjust_at_t0(self):
        p = sc.GuardrailPolicy(spending=10)
        flow = p(0, 100.0)
        self.assertAlmostEqual(p.initial_wr, 0.10)
        self.assertEqual(flow, -10.0)

    def test_cut_trigger(self):
        p = sc.GuardrailPolicy(spending=10, adjust_pct=0.10)
        p(0, 100.0)              # initial WR 10%
        p(1, 50.0)               # WR 20% > 1.2 * 10% -> cut 10%
        self.assertAlmostEqual(p.spending, 9.0)

    def test_raise_trigger(self):
        p = sc.GuardrailPolicy(spending=10, adjust_pct=0.10)
        p(0, 100.0)
        p(1, 200.0)              # WR 5% < 0.8 * 10% -> raise 10%
        self.assertAlmostEqual(p.spending, 11.0)

    def test_floor_holds(self):
        p = sc.GuardrailPolicy(spending=10, adjust_pct=0.50, floor=9.5)
        p(0, 100.0)
        p(1, 50.0)               # 50% cut would give 5; floor lifts to 9.5
        self.assertAlmostEqual(p.spending, 9.5)

    def test_income_offsets_withdrawal(self):
        p = sc.GuardrailPolicy(spending=10, income=[0, 4])
        self.assertEqual(p(0, 100.0), -10.0)
        self.assertEqual(p(1, 100.0), -6.0)

    def test_inactive_after_window(self):
        p = sc.GuardrailPolicy(spending=10, active_years=2)
        p(0, 100.0)
        p(2, 10.0)               # t >= active_years: no adjustment
        self.assertAlmostEqual(p.spending, 10.0)

    def test_empty_income_list_means_no_income(self):
        p = sc.GuardrailPolicy(spending=10, income=[])
        self.assertEqual(p(0, 100.0), -10.0)

    def test_reuse_across_runs_resets_state(self):
        # One policy object, two identical ledger runs: t == 0 resets state,
        # so the second run must reproduce the first exactly.
        p = sc.GuardrailPolicy(spending=10, adjust_pct=0.10)
        returns = [-0.5, 0.0, 0.0]
        first_path, _ = sc.simulate_ledger(100, returns, p)
        first_spends = list(p.realized_spending)
        second_path, _ = sc.simulate_ledger(100, returns, p)
        self.assertEqual(second_path, first_path)
        self.assertEqual(p.realized_spending, first_spends)


class TestPhasePolicy(unittest.TestCase):
    def test_constant_phases_and_tail(self):
        policy = sc.phase_policy([(2, 10.0), (2, -5.0)])
        flows = [policy(t, 100.0) for t in range(5)]
        self.assertEqual(flows, [10.0, 10.0, -5.0, -5.0, -5.0])

    def test_callable_phase_gets_relative_t(self):
        seen = []
        def probe(t, w):
            seen.append(t)
            return 0.0
        policy = sc.phase_policy([(3, 1.0), (2, probe)])
        for t in range(5):
            policy(t, 100.0)
        self.assertEqual(seen, [0, 1])   # phase-relative, not absolute

    def test_accumulate_then_guardrail_end_to_end(self):
        gr = sc.GuardrailPolicy(spending=10)
        policy = sc.phase_policy([(2, 10.0), (30, gr)])
        returns = [0.0] * 12
        path, flows = sc.simulate_ledger(100, returns, policy)
        self.assertEqual(path[1], 120.0)                 # two contributions
        self.assertAlmostEqual(gr.initial_wr, 10 / 120)  # set at drawdown start
        self.assertEqual(path[2], 110.0)                 # first withdrawal
        self.assertTrue(sc.check_conservation(100, returns, flows, path))


class TestSummaries(unittest.TestCase):
    def test_percentile(self):
        vals = [1, 2, 3, 4, 5]
        self.assertEqual(sc.percentile(vals, 50), 3)
        self.assertEqual(sc.percentile(vals, 100), 5)
        self.assertAlmostEqual(sc.percentile(vals, 25), 2.0)

    def test_summarize_checkpoints(self):
        paths = [[100] * 11, [200] * 11]
        out = sc.summarize(paths, start_age=60, every=5)
        self.assertEqual(sorted(out.keys()), [60, 65, 70])
        self.assertEqual(out[65][50], 150)

    def test_spending_summary(self):
        out = sc.spending_summary([[10, 10], [20, 20]])
        self.assertEqual(out["first_year"][50], 15)
        self.assertEqual(out["lifetime_avg"][50], 15)

    def test_percentiles_batch_matches_singles(self):
        vals = [5, 1, 4, 2, 3]
        batch = sc.percentiles(vals, sc.PCTS)
        for p in sc.PCTS:
            self.assertEqual(batch[p], sc.percentile(vals, p))

    def test_empty_and_degenerate_inputs_raise(self):
        with self.assertRaises(ValueError):
            sc.percentile([], 50)
        with self.assertRaises(ValueError):
            sc.summarize([], start_age=60)
        with self.assertRaises(ValueError):
            sc.summarize([[100.0] * 5], start_age=60, every=0)
        with self.assertRaises(ValueError):
            sc.spending_summary([[], []])


if __name__ == "__main__":
    unittest.main()
