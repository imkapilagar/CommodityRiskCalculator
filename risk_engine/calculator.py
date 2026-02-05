"""
Core commodity risk calculation engine.

Implements the 4-tranche progressive entry system with cascading leftover risk.

Algorithm:
    Total Risk = Capital * (Risk% / 100)
    Base Risk per Tranche = Total Risk / num_tranches

    For each tranche:
        Available Risk = Base Risk + Leftover from previous tranche
        Risk per Lot = Premium * Lot Size * (Stop Loss% / 100)
        Lots = floor(Available Risk / Risk per Lot)
        Utilized Risk = Lots * Risk per Lot
        Leftover = Available Risk - Utilized Risk  (cascades to next tranche)
"""

import math
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TrancheResult:
    """Result for a single tranche calculation."""
    tranche_num: int
    completed: bool
    premium: Optional[float]
    risk_per_lot: Optional[float]
    available_risk: float
    lots: int
    quantity: int
    utilized_risk: float
    leftover_risk: float


@dataclass
class RiskSummary:
    """Aggregated results across all tranches."""
    capital: float
    risk_percent: float
    total_risk: float
    stop_loss_percent: float
    lot_size: int
    base_risk_per_tranche: float
    tranches: List[TrancheResult]
    total_lots: int
    total_quantity: int
    total_risk_utilized: float
    final_leftover: float


class RiskCalculator:
    """
    Multi-tranche commodity risk calculator with cascading leftover logic.

    The system divides total risk equally across N tranches (default 4).
    Unused risk from each tranche cascades to the next, maximizing
    capital utilization.

    Usage:
        calc = RiskCalculator(
            capital=13600000,
            risk_percent=0.5,
            stop_loss_percent=50,
            lot_size=100,
        )
        result = calc.calculate(premiums=[150, 120, None, None])
    """

    def __init__(
        self,
        capital: float,
        risk_percent: float,
        stop_loss_percent: float,
        lot_size: int,
        num_tranches: int = 4,
    ):
        if capital <= 0:
            raise ValueError("Capital must be positive")
        if risk_percent <= 0 or risk_percent > 100:
            raise ValueError("Risk percent must be between 0 and 100")
        if stop_loss_percent <= 0 or stop_loss_percent > 100:
            raise ValueError("Stop loss percent must be between 0 and 100")
        if lot_size <= 0:
            raise ValueError("Lot size must be positive")
        if num_tranches <= 0:
            raise ValueError("Number of tranches must be positive")

        self.capital = capital
        self.risk_percent = risk_percent
        self.stop_loss_percent = stop_loss_percent
        self.lot_size = lot_size
        self.num_tranches = num_tranches

    @property
    def total_risk(self) -> float:
        """Total risk amount = Capital * (Risk% / 100)."""
        return self.capital * (self.risk_percent / 100)

    @property
    def base_risk_per_tranche(self) -> float:
        """Base risk allocated to each tranche before cascading."""
        return self.total_risk / self.num_tranches

    def calculate(self, premiums: List[Optional[float]]) -> RiskSummary:
        """
        Calculate lot sizes for each tranche with cascading leftover risk.

        Args:
            premiums: List of premium values per tranche. Use None for
                      tranches that haven't been entered yet.

        Returns:
            RiskSummary with per-tranche and aggregate results.
        """
        if len(premiums) != self.num_tranches:
            raise ValueError(
                f"Expected {self.num_tranches} premiums, got {len(premiums)}"
            )

        leftover = 0.0
        total_lots = 0
        total_quantity = 0
        total_utilized = 0.0
        tranches: List[TrancheResult] = []

        for i, premium in enumerate(premiums):
            available_risk = self.base_risk_per_tranche + leftover

            if premium is not None and premium > 0:
                risk_per_lot = premium * self.lot_size * (self.stop_loss_percent / 100)
                lots = math.floor(available_risk / risk_per_lot)
                utilized = lots * risk_per_lot
                leftover = available_risk - utilized
                quantity = lots * self.lot_size

                tranches.append(TrancheResult(
                    tranche_num=i + 1,
                    completed=True,
                    premium=premium,
                    risk_per_lot=risk_per_lot,
                    available_risk=available_risk,
                    lots=lots,
                    quantity=quantity,
                    utilized_risk=utilized,
                    leftover_risk=leftover,
                ))

                total_lots += lots
                total_quantity += quantity
                total_utilized += utilized
            else:
                tranches.append(TrancheResult(
                    tranche_num=i + 1,
                    completed=False,
                    premium=None,
                    risk_per_lot=None,
                    available_risk=available_risk,
                    lots=0,
                    quantity=0,
                    utilized_risk=0.0,
                    leftover_risk=available_risk,
                ))
                # Leftover carries the full available_risk for pending tranches
                leftover = available_risk

        return RiskSummary(
            capital=self.capital,
            risk_percent=self.risk_percent,
            total_risk=self.total_risk,
            stop_loss_percent=self.stop_loss_percent,
            lot_size=self.lot_size,
            base_risk_per_tranche=self.base_risk_per_tranche,
            tranches=tranches,
            total_lots=total_lots,
            total_quantity=total_quantity,
            total_risk_utilized=total_utilized,
            final_leftover=tranches[-1].leftover_risk if tranches else 0.0,
        )
