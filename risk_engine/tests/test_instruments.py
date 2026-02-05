"""Tests for instrument definitions."""

import unittest

from risk_engine.instruments import (
    Instrument,
    INSTRUMENTS,
    get_instrument,
    custom_instrument,
)


class TestInstruments(unittest.TestCase):

    def test_known_instruments(self):
        self.assertIn("crude", INSTRUMENTS)
        self.assertIn("ng", INSTRUMENTS)
        self.assertIn("goldm", INSTRUMENTS)
        self.assertIn("gold", INSTRUMENTS)

    def test_crude_lot_size(self):
        crude = get_instrument("crude")
        self.assertEqual(crude.lot_size, 100)
        self.assertEqual(crude.name, "Crude Oil")

    def test_ng_lot_size(self):
        ng = get_instrument("ng")
        self.assertEqual(ng.lot_size, 1250)

    def test_goldm_lot_size(self):
        goldm = get_instrument("goldm")
        self.assertEqual(goldm.lot_size, 10)

    def test_gold_lot_size(self):
        gold = get_instrument("gold")
        self.assertEqual(gold.lot_size, 100)

    def test_unknown_instrument_raises(self):
        with self.assertRaises(KeyError):
            get_instrument("unknown")

    def test_custom_instrument(self):
        inst = custom_instrument("Silver", 30)
        self.assertEqual(inst.name, "Silver")
        self.assertEqual(inst.lot_size, 30)
        self.assertEqual(inst.symbol, "custom")

    def test_instrument_frozen(self):
        crude = get_instrument("crude")
        with self.assertRaises(AttributeError):
            crude.lot_size = 200


if __name__ == "__main__":
    unittest.main()
