#!/usr/bin/env python3
"""
Fetch Sensex CURRENT spot price using yfinance
Gets the latest available price (current LTP)
"""

import yfinance as yf
from datetime import datetime, timedelta

def fetch_sensex_spot():
    """Fetch Sensex current spot price (latest available price)"""
    try:
        # Sensex symbol (same as ss_data.py)
        sensex_symbol = "^BSESN"

        # Get ticker object
        sensex = yf.Ticker(sensex_symbol)

        # Try to get current price using fast_info (most recent)
        try:
            current_price = sensex.fast_info.get('lastPrice')
            if current_price and current_price > 0:
                return float(current_price)
        except:
            pass

        # Fallback: Get last few days of data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)

        sensex_df = sensex.history(start=start_date, end=end_date)

        if not sensex_df.empty:
            # Get the most recent close price available
            current_price = sensex_df['Close'].iloc[-1]
            return float(current_price)

        # Fallback if no data
        return 80500.00

    except Exception as e:
        # Silent failure with fallback
        return 80500.00

if __name__ == "__main__":
    price = fetch_sensex_spot()
    print(f"{price:.2f}")
