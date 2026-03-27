"""
Commodity Risk Engine - Reusable risk calculation library.

Extracted from the CommodityRiskCalculator project.
Provides multi-tranche position sizing with cascading leftover risk,
premium coverage calculations, and market data fetching.
"""

from .calculator import RiskCalculator, TrancheResult, RiskSummary
from .premium import PremiumCalculator
from .instruments import Instrument, INSTRUMENTS

__version__ = "1.0.0"
__all__ = [
    "RiskCalculator",
    "TrancheResult",
    "RiskSummary",
    "PremiumCalculator",
    "Instrument",
    "INSTRUMENTS",
]
