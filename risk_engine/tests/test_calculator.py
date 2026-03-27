"""Tests for the core risk calculator."""

import math
import unittest

from risk_engine.calculator import RiskCalculator


class TestRiskCalculator(unittest.TestCase):

    def setUp(self):
        """Default calculator matching the HTML defaults."""
        self.calc = RiskCalculator(
            capital=13600000,
            risk_percent=0.5,
            stop_loss_percent=50,
            lot_size=100,
        )

    def test_total_risk(self):
        self.assertAlmostEqual(self.calc.total_risk, 68000.0)

    def test_base_risk_per_tranche(self):
        self.assertAlmostEqual(self.calc.base_risk_per_tranche, 17000.0)

    def test_all_four_tranches_filled(self):
        result = self.calc.calculate([150, 120, 100, 80])

        self.assertEqual(len(result.tranches), 4)
        for t in result.tranches:
            self.assertTrue(t.completed)
            self.assertGreater(t.lots, 0)

        # Verify cascading: each tranche's available risk includes prior leftover
        for i in range(1, 4):
            prev_leftover = result.tranches[i - 1].leftover_risk
            expected_available = self.calc.base_risk_per_tranche + prev_leftover
            self.assertAlmostEqual(
                result.tranches[i].available_risk, expected_available
            )

        # Total utilized should be <= total risk
        self.assertLessEqual(result.total_risk_utilized, self.calc.total_risk + 0.01)

    def test_single_tranche_filled(self):
        result = self.calc.calculate([150, None, None, None])

        self.assertTrue(result.tranches[0].completed)
        for t in result.tranches[1:]:
            self.assertFalse(t.completed)

        # Pending tranches accumulate available risk
        self.assertAlmostEqual(
            result.tranches[1].available_risk,
            self.calc.base_risk_per_tranche + result.tranches[0].leftover_risk,
        )

    def test_no_tranches_filled(self):
        result = self.calc.calculate([None, None, None, None])

        self.assertEqual(result.total_lots, 0)
        self.assertEqual(result.total_quantity, 0)
        self.assertAlmostEqual(result.total_risk_utilized, 0.0)

    def test_lot_calculation_correctness(self):
        """Verify the exact lot calculation for tranche 1."""
        result = self.calc.calculate([150, None, None, None])
        t1 = result.tranches[0]

        expected_risk_per_lot = 150 * 100 * (50 / 100)  # 7500
        expected_lots = math.floor(17000 / 7500)  # 2
        expected_utilized = 2 * 7500  # 15000
        expected_leftover = 17000 - 15000  # 2000

        self.assertAlmostEqual(t1.risk_per_lot, expected_risk_per_lot)
        self.assertEqual(t1.lots, expected_lots)
        self.assertAlmostEqual(t1.utilized_risk, expected_utilized)
        self.assertAlmostEqual(t1.leftover_risk, expected_leftover)
        self.assertEqual(t1.quantity, expected_lots * 100)

    def test_cascading_leftover(self):
        """Verify leftover from T1 adds to T2's available risk."""
        result = self.calc.calculate([150, 150, None, None])
        t1 = result.tranches[0]
        t2 = result.tranches[1]

        # T2 available = base_risk + T1 leftover
        self.assertAlmostEqual(
            t2.available_risk,
            self.calc.base_risk_per_tranche + t1.leftover_risk,
        )

    def test_100_percent_stop_loss(self):
        calc = RiskCalculator(
            capital=13600000,
            risk_percent=0.5,
            stop_loss_percent=100,
            lot_size=100,
        )
        result = calc.calculate([150, None, None, None])
        t1 = result.tranches[0]

        # With 100% SL, risk_per_lot = premium * lot_size * 1.0
        self.assertAlmostEqual(t1.risk_per_lot, 150 * 100 * 1.0)

    def test_natural_gas_lot_size(self):
        calc = RiskCalculator(
            capital=13600000,
            risk_percent=0.5,
            stop_loss_percent=50,
            lot_size=1250,
        )
        result = calc.calculate([5, None, None, None])
        t1 = result.tranches[0]

        risk_per_lot = 5 * 1250 * 0.5  # 3125
        expected_lots = math.floor(17000 / 3125)  # 5
        self.assertEqual(t1.lots, expected_lots)
        self.assertEqual(t1.quantity, expected_lots * 1250)

    def test_invalid_capital(self):
        with self.assertRaises(ValueError):
            RiskCalculator(capital=0, risk_percent=0.5, stop_loss_percent=50, lot_size=100)

    def test_invalid_risk_percent(self):
        with self.assertRaises(ValueError):
            RiskCalculator(capital=100000, risk_percent=0, stop_loss_percent=50, lot_size=100)

    def test_wrong_number_of_premiums(self):
        with self.assertRaises(ValueError):
            self.calc.calculate([150, 120])  # Only 2, need 4

    def test_summary_aggregation(self):
        result = self.calc.calculate([150, 120, 100, 80])

        # Verify totals match sum of tranches
        self.assertEqual(
            result.total_lots,
            sum(t.lots for t in result.tranches),
        )
        self.assertEqual(
            result.total_quantity,
            sum(t.quantity for t in result.tranches),
        )
        self.assertAlmostEqual(
            result.total_risk_utilized,
            sum(t.utilized_risk for t in result.tranches),
        )


class TestRiskCalculatorCustomTranches(unittest.TestCase):

    def test_two_tranches(self):
        calc = RiskCalculator(
            capital=1000000,
            risk_percent=1.0,
            stop_loss_percent=50,
            lot_size=100,
            num_tranches=2,
        )
        result = calc.calculate([50, 50])
        self.assertEqual(len(result.tranches), 2)
        self.assertAlmostEqual(calc.base_risk_per_tranche, 5000.0)


if __name__ == "__main__":
    unittest.main()
