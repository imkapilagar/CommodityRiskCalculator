"""Tests for the premium coverage calculator."""

import unittest

from risk_engine.premium import PremiumCalculator, PREMIUM_PERCENTAGES


class TestPremiumCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = PremiumCalculator()

    def test_nifty_0dte(self):
        result = self.calc.calculate("nifty", dte=0, spot_price=26013.45)
        self.assertAlmostEqual(result.premium_percent, 0.63)
        expected = 26013.45 * 0.63 / 100
        self.assertAlmostEqual(result.premium_amount, round(expected, 2))

    def test_sensex_2dte(self):
        result = self.calc.calculate("sensex", dte=2, spot_price=85186.47)
        self.assertAlmostEqual(result.premium_percent, 1.17)
        expected = 85186.47 * 1.17 / 100
        self.assertAlmostEqual(result.premium_amount, round(expected, 2))

    def test_banknifty_4dte(self):
        result = self.calc.calculate("banknifty", dte=4, spot_price=59216.05)
        self.assertAlmostEqual(result.premium_percent, 1.72)

    def test_case_insensitive(self):
        result = self.calc.calculate("NIFTY", dte=0, spot_price=25000)
        self.assertAlmostEqual(result.premium_percent, 0.63)

    def test_default_spot_price(self):
        result = self.calc.calculate("nifty", dte=0)
        self.assertEqual(result.spot_price, 24500.00)

    def test_unknown_index_raises(self):
        with self.assertRaises(KeyError):
            self.calc.calculate("dowjones", dte=0)

    def test_unknown_dte_raises(self):
        with self.assertRaises(KeyError):
            self.calc.calculate("nifty", dte=10)

    def test_all_dte(self):
        results = self.calc.calculate_all_dte("nifty", spot_price=25000)
        self.assertEqual(len(results), 5)
        for r in results:
            self.assertEqual(r.index, "nifty")
            self.assertGreater(r.premium_amount, 0)

    def test_all_premium_percentages_present(self):
        """Verify all expected index/DTE combinations exist."""
        for index in ["nifty", "sensex", "banknifty"]:
            for dte in range(5):
                pct = self.calc.get_premium_percent(index, dte)
                self.assertGreater(pct, 0)

    def test_custom_percentages(self):
        custom = {"myindex": {0: 1.5, 1: 2.0}}
        calc = PremiumCalculator(custom_percentages=custom)
        result = calc.calculate("myindex", dte=0, spot_price=10000)
        self.assertAlmostEqual(result.premium_amount, 150.0)


class TestPremiumPercentages(unittest.TestCase):

    def test_premium_increases_with_dte(self):
        """Premium % should generally increase with more DTE."""
        for index, dte_map in PREMIUM_PERCENTAGES.items():
            dtes = sorted(dte_map.keys())
            for i in range(1, len(dtes)):
                self.assertGreaterEqual(
                    dte_map[dtes[i]],
                    dte_map[dtes[i - 1]],
                    f"{index} DTE {dtes[i]} should be >= DTE {dtes[i-1]}",
                )


if __name__ == "__main__":
    unittest.main()
