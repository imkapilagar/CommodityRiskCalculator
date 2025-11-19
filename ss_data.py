"""
Simple Stock Market Data Fetcher
Fetches last 5 days: Date, Open, Close, %Change
Separate tables for Nifty, Bank Nifty and Sensex
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_index_data(days=5):
    """Fetch Nifty, Bank Nifty and Sensex data"""
    
    # Index symbols
    nifty_symbol = "^NSEI"
    banknifty_symbol = "^NSEBANK"
    sensex_symbol = "^BSESN"
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days+5)
    
    try:
        # Fetch Nifty data
        nifty = yf.Ticker(nifty_symbol)
        nifty_df = nifty.history(start=start_date, end=end_date).tail(days)
        
        # Fetch Bank Nifty data
        banknifty = yf.Ticker(banknifty_symbol)
        banknifty_df = banknifty.history(start=start_date, end=end_date).tail(days)
        
        # Fetch Sensex data
        sensex = yf.Ticker(sensex_symbol)
        sensex_df = sensex.history(start=start_date, end=end_date).tail(days)
        
        # Format Nifty data
        nifty_result = pd.DataFrame({
            'Date': nifty_df.index.strftime('%Y-%m-%d'),
            'Open': nifty_df['Open'].round(2),
            'Close': nifty_df['Close'].round(2),
            'Change_%': ((nifty_df['Close'] - nifty_df['Open']) / nifty_df['Open'] * 100).round(2)
        })
        
        # Format Bank Nifty data
        banknifty_result = pd.DataFrame({
            'Date': banknifty_df.index.strftime('%Y-%m-%d'),
            'Open': banknifty_df['Open'].round(2),
            'Close': banknifty_df['Close'].round(2),
            'Change_%': ((banknifty_df['Close'] - banknifty_df['Open']) / banknifty_df['Open'] * 100).round(2)
        })
        
        # Format Sensex data
        sensex_result = pd.DataFrame({
            'Date': sensex_df.index.strftime('%Y-%m-%d'),
            'Open': sensex_df['Open'].round(2),
            'Close': sensex_df['Close'].round(2),
            'Change_%': ((sensex_df['Close'] - sensex_df['Open']) / sensex_df['Open'] * 100).round(2)
        })
        
        return nifty_result, banknifty_result, sensex_result
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None


def save_to_csv(nifty_data, banknifty_data, sensex_data):
    """Save data to CSV with 3 separate tables"""
    
    with open('ss_data.csv', 'w') as f:
        # Nifty table
        f.write("NIFTY\n")
        nifty_data.to_csv(f, index=False)
        f.write("\n")
        
        # Bank Nifty table
        f.write("BANK NIFTY\n")
        banknifty_data.to_csv(f, index=False)
        f.write("\n")
        
        # Sensex table
        f.write("SENSEX\n")
        sensex_data.to_csv(f, index=False)
    
    print("Data saved to ss_data.csv (3 separate tables)")


if __name__ == "__main__":
    print("Fetching data...\n")
    
    nifty_data, banknifty_data, sensex_data = fetch_index_data(days=5)
    
    if nifty_data is not None and banknifty_data is not None and sensex_data is not None:
        # Display Nifty table
        print("=" * 60)
        print("NIFTY")
        print("=" * 60)
        print(nifty_data.to_string(index=False))
        
        print("\n")
        
        # Display Bank Nifty table
        print("=" * 60)
        print("BANK NIFTY")
        print("=" * 60)
        print(banknifty_data.to_string(index=False))
        
        print("\n")
        
        # Display Sensex table
        print("=" * 60)
        print("SENSEX")
        print("=" * 60)
        print(sensex_data.to_string(index=False))
        
        print("\n")
        
        # Save to CSV
        save_to_csv(nifty_data, banknifty_data, sensex_data)
    else:
        print("Failed to fetch data")
