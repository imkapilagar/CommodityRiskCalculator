"""
Pre-configured commodity instruments with their lot sizes.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    """A tradeable commodity instrument."""
    name: str
    symbol: str
    lot_size: int

    def __str__(self):
        return f"{self.name} (lot size: {self.lot_size})"


# Pre-configured instruments matching the HTML calculator
INSTRUMENTS = {
    "crude": Instrument(name="Crude Oil", symbol="crude", lot_size=100),
    "ng": Instrument(name="Natural Gas", symbol="ng", lot_size=1250),
    "goldm": Instrument(name="Gold M", symbol="goldm", lot_size=10),
    "gold": Instrument(name="Gold", symbol="gold", lot_size=100),
}


def get_instrument(symbol: str) -> Instrument:
    """Look up an instrument by symbol. Raises KeyError if not found."""
    if symbol not in INSTRUMENTS:
        available = ", ".join(INSTRUMENTS.keys())
        raise KeyError(f"Unknown instrument '{symbol}'. Available: {available}")
    return INSTRUMENTS[symbol]


def custom_instrument(name: str, lot_size: int) -> Instrument:
    """Create a custom instrument with a user-defined lot size."""
    return Instrument(name=name, symbol="custom", lot_size=lot_size)
