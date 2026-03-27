"""
Premium coverage calculator for Indian index options.

Calculates expected coverage premiums based on:
- Index (Nifty, Sensex, Bank Nifty)
- Days to Expiry (DTE: 0-4)
- Spot price

Premium percentages are backtested historical averages.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

# Backtested average premium coverage percentages by index and DTE
PREMIUM_PERCENTAGES: Dict[str, Dict[int, float]] = {
    "nifty": {0: 0.63, 1: 1.02, 2: 1.31, 3: 1.53, 4: 1.74},
    "sensex": {0: 0.60, 1: 0.95, 2: 1.17, 3: 1.29, 4: 1.55},
    "banknifty": {0: 0.63, 1: 1.02, 2: 1.31, 3: 1.53, 4: 1.72},
}

# Default fallback spot prices when APIs are unavailable
DEFAULT_SPOT_PRICES: Dict[str, float] = {
    "nifty": 24500.00,
    "sensex": 80500.00,
    "banknifty": 52000.00,
}


@dataclass
class PremiumResult:
    """Result of a premium coverage calculation."""
    index: str
    dte: int
    premium_percent: float
    spot_price: float
    premium_amount: float


class PremiumCalculator:
    """
    Calculate expected option premiums based on index, DTE, and spot price.

    Coverage Premium = Spot Price * (Premium% / 100)

    Usage:
        calc = PremiumCalculator()
        result = calc.calculate("nifty", dte=0, spot_price=26013.45)
        # result.premium_amount ~= 163.88
    """

    def __init__(
        self,
        custom_percentages: Optional[Dict[str, Dict[int, float]]] = None,
    ):
        """
        Args:
            custom_percentages: Override default premium percentages.
                Format: {"index_name": {dte: percent, ...}, ...}
        """
        self.percentages = custom_percentages or PREMIUM_PERCENTAGES

    def get_premium_percent(self, index: str, dte: int) -> float:
        """
        Get the backtested premium coverage percentage.

        Args:
            index: Index name (nifty, sensex, banknifty)
            dte: Days to expiry (0-4)

        Returns:
            Premium percentage as a float.

        Raises:
            KeyError: If index or DTE is not found.
        """
        index_lower = index.lower()
        if index_lower not in self.percentages:
            available = ", ".join(self.percentages.keys())
            raise KeyError(f"Unknown index '{index}'. Available: {available}")
        dte_map = self.percentages[index_lower]
        if dte not in dte_map:
            available = ", ".join(str(d) for d in sorted(dte_map.keys()))
            raise KeyError(f"Unknown DTE {dte} for {index}. Available: {available}")
        return dte_map[dte]

    def calculate(
        self,
        index: str,
        dte: int,
        spot_price: Optional[float] = None,
    ) -> PremiumResult:
        """
        Calculate the expected coverage premium amount.

        Args:
            index: Index name (nifty, sensex, banknifty)
            dte: Days to expiry (0-4)
            spot_price: Current spot price. Uses default if None.

        Returns:
            PremiumResult with the calculated premium.
        """
        index_lower = index.lower()
        pct = self.get_premium_percent(index_lower, dte)

        if spot_price is None:
            spot_price = DEFAULT_SPOT_PRICES.get(index_lower)
            if spot_price is None:
                raise ValueError(
                    f"No default spot price for '{index}'. Provide spot_price."
                )

        premium_amount = spot_price * (pct / 100)

        return PremiumResult(
            index=index_lower,
            dte=dte,
            premium_percent=pct,
            spot_price=spot_price,
            premium_amount=round(premium_amount, 2),
        )

    def calculate_all_dte(
        self,
        index: str,
        spot_price: Optional[float] = None,
    ) -> list:
        """Calculate premiums for all DTEs of a given index."""
        index_lower = index.lower()
        if index_lower not in self.percentages:
            raise KeyError(f"Unknown index '{index}'")
        results = []
        for dte in sorted(self.percentages[index_lower].keys()):
            results.append(self.calculate(index_lower, dte, spot_price))
        return results
