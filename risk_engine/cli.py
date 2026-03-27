"""
Command-line interface for the commodity risk engine.

Usage:
    python -m risk_engine risk --capital 13600000 --risk-pct 0.5 --sl 50 --lot-size 100 --premiums 150 120
    python -m risk_engine premium --index nifty --dte 0 --spot 26000
    python -m risk_engine premium --index nifty --all-dte --spot 26000
"""

import argparse
import sys


def format_inr(amount: float) -> str:
    """Format amount in Indian Rupee style."""
    return f"\u20b9{amount:,.2f}"


def cmd_risk(args):
    """Run the multi-tranche risk calculator."""
    from .calculator import RiskCalculator

    premiums = []
    for p in (args.premiums or []):
        premiums.append(float(p) if p.lower() != "none" else None)

    # Pad with None up to num_tranches
    while len(premiums) < args.tranches:
        premiums.append(None)

    calc = RiskCalculator(
        capital=args.capital,
        risk_percent=args.risk_pct,
        stop_loss_percent=args.sl,
        lot_size=args.lot_size,
        num_tranches=args.tranches,
    )
    result = calc.calculate(premiums)

    print(f"\n{'=' * 55}")
    print(f"  Commodity Risk Calculation")
    print(f"{'=' * 55}")
    print(f"  Capital:           {format_inr(result.capital)}")
    print(f"  Risk:              {result.risk_percent}% = {format_inr(result.total_risk)}")
    print(f"  Stop Loss:         {result.stop_loss_percent}%")
    print(f"  Lot Size:          {result.lot_size}")
    print(f"  Base Risk/Tranche: {format_inr(result.base_risk_per_tranche)}")
    print(f"{'=' * 55}")

    for t in result.tranches:
        status = "FILLED" if t.completed else "PENDING"
        print(f"\n  Tranche {t.tranche_num} [{status}]")
        print(f"  {'─' * 40}")
        if t.completed:
            print(f"    Premium:        {format_inr(t.premium)}")
            print(f"    Risk/Lot:       {format_inr(t.risk_per_lot)}")
            print(f"    Available Risk: {format_inr(t.available_risk)}")
            print(f"    Lots:           {t.lots}")
            print(f"    Quantity:       {t.quantity:,}")
            print(f"    Utilized:       {format_inr(t.utilized_risk)}")
            print(f"    Leftover:       {format_inr(t.leftover_risk)}")
        else:
            print(f"    Available Risk: {format_inr(t.available_risk)}")

    print(f"\n{'=' * 55}")
    print(f"  TOTALS")
    print(f"  {'─' * 40}")
    print(f"    Total Lots:     {result.total_lots}")
    print(f"    Total Quantity: {result.total_quantity:,}")
    print(f"    Risk Utilized:  {format_inr(result.total_risk_utilized)}")
    print(f"    Leftover:       {format_inr(result.final_leftover)}")
    print(f"{'=' * 55}\n")


def cmd_premium(args):
    """Run the premium coverage calculator."""
    from .premium import PremiumCalculator

    calc = PremiumCalculator()

    if args.all_dte:
        results = calc.calculate_all_dte(args.index, args.spot)
        print(f"\n{'=' * 60}")
        print(f"  Premium Coverage: {args.index.upper()}")
        if args.spot:
            print(f"  Spot Price: {format_inr(args.spot)}")
        print(f"{'=' * 60}")
        print(f"  {'DTE':<6} {'Premium %':<14} {'Premium Amount':<20}")
        print(f"  {'─' * 45}")
        for r in results:
            print(f"  {r.dte:<6} {r.premium_percent:<14.2f} {format_inr(r.premium_amount):<20}")
        print(f"{'=' * 60}\n")
    else:
        result = calc.calculate(args.index, args.dte, args.spot)
        print(f"\n  {result.index.upper()} | DTE {result.dte}")
        print(f"  Spot:    {format_inr(result.spot_price)}")
        print(f"  Premium: {result.premium_percent}% = {format_inr(result.premium_amount)}\n")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="risk_engine",
        description="Commodity Risk Engine - position sizing and premium calculator",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Risk calculator subcommand
    risk_parser = subparsers.add_parser("risk", help="Multi-tranche risk calculator")
    risk_parser.add_argument("--capital", type=float, required=True, help="Total capital amount")
    risk_parser.add_argument("--risk-pct", type=float, required=True, help="Risk as %% of capital")
    risk_parser.add_argument("--sl", type=float, required=True, help="Stop loss percentage")
    risk_parser.add_argument("--lot-size", type=int, required=True, help="Lot size for the instrument")
    risk_parser.add_argument("--premiums", nargs="*", help="Premium values per tranche (use 'none' for pending)")
    risk_parser.add_argument("--tranches", type=int, default=4, help="Number of tranches (default: 4)")

    # Premium calculator subcommand
    prem_parser = subparsers.add_parser("premium", help="Index premium coverage calculator")
    prem_parser.add_argument("--index", required=True, help="Index name (nifty, sensex, banknifty)")
    prem_parser.add_argument("--dte", type=int, help="Days to expiry (0-4)")
    prem_parser.add_argument("--spot", type=float, help="Spot price (uses default if omitted)")
    prem_parser.add_argument("--all-dte", action="store_true", help="Show all DTEs")

    args = parser.parse_args(argv)

    if args.command == "risk":
        cmd_risk(args)
    elif args.command == "premium":
        if not args.all_dte and args.dte is None:
            prem_parser.error("Either --dte or --all-dte is required")
        cmd_premium(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
