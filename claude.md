# Data Generators - Trading Tools Documentation

## 📋 Project Overview

This repository contains automated trading data generation and risk calculation tools for Indian equity indices (Nifty, Sensex, Bank Nifty) and commodity options (Crude Oil, Natural Gas, Gold).

---

## 🛠️ Tools Available

### 1. **Premium Coverage Calculator** (`premium_calculator.sh`)

A bash script that calculates option premium coverage based on spot prices and DTE (Days to Expiry).

#### Features:
- Fetches **live spot prices** from NSE/BSE APIs
- Calculates coverage premium for 0-4 DTE
- Supports Nifty, Sensex, and Bank Nifty
- Beautiful colored table output
- Auto-saves to CSV with timestamp

#### Usage:
```bash
# Single index
./premium_calculator.sh nifty0

# Multiple indices
./premium_calculator.sh nifty0 sensex2 banknifty1

# All indices (default)
./premium_calculator.sh
```

#### Premium Percentages:
| Index      | 0 DTE | 1 DTE | 2 DTE | 3 DTE | 4 DTE |
|------------|-------|-------|-------|-------|-------|
| Nifty      | 0.63% | 1.02% | 1.31% | 1.53% | 1.74% |
| Sensex     | 0.60% | 0.95% | 1.17% | 1.29% | 1.55% |
| Bank Nifty | 0.63% | 1.02% | 1.31% | 1.53% | 1.72% |

#### Output Example:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          COVERAGE PREMIUM DETAILS                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Index           DTE        Premium %       Spot Price           Premium Amount
───────────── ──────── ───────────── ────────────────── ──────────────────
Nifty           0          0.63%           ₹26,013.45         ₹163.88
Sensex          2          1.17%           ₹84,950.95         ₹993.92
```

---

### 2. **Sixth Sense Data Table** (`ss_data.py`)

Python script that fetches last 5 trading days' data for all major indices.

#### Features:
- Fetches from Yahoo Finance
- Shows Date, Open, Close, Change%
- Separate tables for Nifty, Bank Nifty, Sensex
- Auto-saves to CSV

#### Usage:
```bash
python3 ss_data.py
```

#### Output:
```
============================================================
SENSEX
============================================================
      Date     Open    Close  Change_%
2025-11-12 84238.86 84466.51      0.27
2025-11-13 84525.89 84478.67     -0.06
2025-11-14 84060.14 84562.78      0.60
2025-11-17 84700.50 84950.95      0.30
2025-11-18 85042.37 84673.02     -0.43
```

---

### 3. **Options Risk Calculator** (`options_risk_calculator.html`)

Mobile-friendly HTML calculator for options trading risk management with tranche-based lot calculation.

#### Features:
✅ **Progressive Entry** - Fill premiums as you take trades
✅ **4 Tranche System** - Automatic risk distribution across 4 entries
✅ **Cascading Leftover** - Unused risk flows to next tranche
✅ **Capital-based Risk** - Calculate risk as % of capital
✅ **SL Presets** - Quick select 50%, 100%, or custom
✅ **Offline-capable** - Works without internet
✅ **Mobile-optimized** - Responsive design for phones

#### Pre-configured Instruments:
- **Crude Oil**: Lot Size 100
- **Natural Gas**: Lot Size 1250
- **Gold M**: Lot Size 100
- **Custom**: Enter your own

#### Risk Calculation Formula:
```
Base Risk per Tranche = (Capital × Risk%) ÷ 4
Risk per Lot = Premium × Lot Size × (SL% ÷ 100)
Lots to Trade = Available Risk ÷ Risk per Lot
```

#### Cascading Logic:
```
Tranche 1: Gets base risk (Total ÷ 4)
  → Leftover goes to Tranche 2

Tranche 2: Gets base risk + Tranche 1 leftover
  → Leftover goes to Tranche 3

Tranche 3: Gets base risk + Tranche 2 leftover
  → Leftover goes to Tranche 4

Tranche 4: Gets base risk + Tranche 3 leftover
  → Shows final leftover
```

#### Example Workflow:
**Trade 1 (3:00 PM):**
```
Capital: ₹100,000
Risk%: 5%
Total Risk: ₹5,000
SL: 50%
Lot Size: 100
Premium 1: ₹50

Result:
- Tranche 1: 20 lots
- Tranche 2: Shows "⏳ Pending" with available risk
```

**Trade 2 (3:30 PM):**
```
Premium 2: ₹45 (add to form)

Result:
- Tranche 1: 20 lots ✅
- Tranche 2: 22 lots
- Tranche 3: Shows available risk
```

#### How to Use on Phone:
1. Transfer `options_risk_calculator.html` to phone
2. Open in any browser (Chrome/Safari)
3. Bookmark for quick access
4. Use offline anytime

---

## 📦 Supporting Files

### `fetch_sensex.py`
Helper script for fetching current Sensex spot price using yfinance.

### `premium_config.conf`
Configuration file for premium calculator (optional overrides).

---

## 📊 Data Outputs

All tools save data with timestamps:

1. **Premium Coverage**: `premium_coverage_YYYYMMDD_HHMMSS.csv`
2. **Sixth Sense**: `ss_data.csv`

---

## 🔧 Setup & Requirements

### Bash Scripts:
```bash
# Make executable
chmod +x premium_calculator.sh

# Run
./premium_calculator.sh
```

### Python Scripts:
```bash
# Install dependencies
pip3 install yfinance pandas

# Run
python3 ss_data.py
```

### HTML Calculator:
- No installation needed
- Just open in browser
- Works on any device

---

## 📱 Mobile Usage

### Premium Calculator:
Use SSH/Termux on Android or shortcuts on iOS:
```bash
ssh user@your-machine './premium_calculator.sh nifty0'
```

### Risk Calculator:
1. Transfer HTML file to phone
2. Save in Files/Downloads
3. Open with browser
4. Add to home screen for quick access

---

## 🎯 Use Cases

### Daily Trading:
1. Run `ss_data.py` to check market trend
2. Use `premium_calculator.sh` to get coverage premiums
3. Use `options_risk_calculator.html` to calculate lot sizes

### Risk Management:
- Capital-based risk allocation
- Multi-tranche position building
- Leftover risk optimization

### Premium Analysis:
- Historical price patterns
- DTE-based premium decay
- Index comparison

---

## 📈 Data Sources

- **Nifty/Bank Nifty**: NSE India API
- **Sensex**: Yahoo Finance (^BSESN)
- **Premium %**: Historical backtested averages

---

## 🔐 Security Notes

- All calculations done locally
- No data sent to external servers
- API calls are read-only
- No login/credentials required

---

## 🚀 Future Enhancements

- [ ] Save trade history in calculator
- [ ] Add Finnifty and Midcap Nifty
- [ ] Export calculator results to CSV
- [ ] Add profit/loss tracking
- [ ] Integration with broker APIs

---

## 📞 Quick Commands Reference

```bash
# Show Nifty 0 DTE premium
./premium_calculator.sh nifty0

# Show Sensex historical data
python3 ss_data.py

# Calculate lots (open HTML in browser)
open options_risk_calculator.html

# Show all indices, all DTEs
./premium_calculator.sh
```

---

## 📝 Notes

- Spot prices update in real-time during market hours
- Premium percentages are based on historical averages
- Always verify calculations before placing trades
- Risk management formulas are indicative, not advisory

---

**Last Updated**: November 18, 2025
**Version**: 1.0
**Tools**: 3 (Bash, Python, HTML)
