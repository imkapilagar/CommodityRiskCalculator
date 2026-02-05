"""
Market data fetching for Indian indices using yfinance.

Provides spot prices and historical data for Nifty, Bank Nifty, and Sensex.
Includes fallback logic when APIs are unavailable.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Index symbol mapping for Yahoo Finance
INDEX_SYMBOLS: Dict[str, str] = {
    "nifty": "^NSEI",
    "banknifty": "^NSEBANK",
    "sensex": "^BSESN",
}

# Fallback prices when APIs fail
FALLBACK_PRICES: Dict[str, float] = {
    "nifty": 24500.00,
    "sensex": 80500.00,
    "banknifty": 52000.00,
}


@dataclass
class IndexPrice:
    """Current spot price for an index."""
    index: str
    symbol: str
    price: float
    is_fallback: bool


@dataclass
class HistoricalDay:
    """Single day of historical index data."""
    date: str
    open_price: float
    close_price: float
    change_percent: float


def fetch_spot_price(index: str) -> IndexPrice:
    """
    Fetch current spot price for an index.

    Uses yfinance with fallback to hardcoded defaults.

    Args:
        index: Index name (nifty, sensex, banknifty)

    Returns:
        IndexPrice with the current or fallback price.
    """
    index_lower = index.lower()
    if index_lower not in INDEX_SYMBOLS:
        available = ", ".join(INDEX_SYMBOLS.keys())
        raise KeyError(f"Unknown index '{index}'. Available: {available}")

    symbol = INDEX_SYMBOLS[index_lower]
    fallback = FALLBACK_PRICES[index_lower]

    try:
        import yfinance as yf

        ticker = yf.Ticker(symbol)

        # Try fast_info first
        try:
            price = ticker.fast_info.get("lastPrice")
            if price and price > 0:
                return IndexPrice(
                    index=index_lower,
                    symbol=symbol,
                    price=float(price),
                    is_fallback=False,
                )
        except Exception:
            pass

        # Fallback: last 5 days of history
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)
        df = ticker.history(start=start_date, end=end_date)
        if not df.empty:
            return IndexPrice(
                index=index_lower,
                symbol=symbol,
                price=float(df["Close"].iloc[-1]),
                is_fallback=False,
            )
    except ImportError:
        pass  # yfinance not installed
    except Exception:
        pass

    return IndexPrice(
        index=index_lower,
        symbol=symbol,
        price=fallback,
        is_fallback=True,
    )


def fetch_historical(index: str, days: int = 5) -> List[HistoricalDay]:
    """
    Fetch recent historical data for an index.

    Args:
        index: Index name (nifty, sensex, banknifty)
        days: Number of trading days to fetch (default 5)

    Returns:
        List of HistoricalDay records.
    """
    index_lower = index.lower()
    if index_lower not in INDEX_SYMBOLS:
        available = ", ".join(INDEX_SYMBOLS.keys())
        raise KeyError(f"Unknown index '{index}'. Available: {available}")

    symbol = INDEX_SYMBOLS[index_lower]

    try:
        import yfinance as yf

        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days + 5)
        df = ticker.history(start=start_date, end=end_date).tail(days)

        results = []
        for idx, row in df.iterrows():
            change_pct = ((row["Close"] - row["Open"]) / row["Open"]) * 100
            results.append(HistoricalDay(
                date=idx.strftime("%Y-%m-%d"),
                open_price=round(row["Open"], 2),
                close_price=round(row["Close"], 2),
                change_percent=round(change_pct, 2),
            ))
        return results
    except ImportError:
        raise ImportError("yfinance is required for market data. Install: pip install yfinance")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch historical data for {index}: {e}")
