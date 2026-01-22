# Performance Dashboard - Local Folder Setup

## 🚀 Quick Start

### Step 1: Start the CORS-enabled Server

```bash
cd Performance_Data
./start_server.sh
```

Or manually:
```bash
python3 cors_server.py
```

### Step 2: Access the Dashboard

1. Open `performance_dashboard.html` in your browser
2. Click **"Local Folder"** button
3. Enter: `http://localhost:8080`
4. Click **"Connect"**

---

## 📋 File Structure

```
Performance_Data/
├── cors_server.py          # CORS-enabled HTTP server
├── start_server.sh         # Quick start script
├── files.json              # List of data files to load
├── performance_dashboard.html
├── Pnl_Dec25.xlsx
├── PnL_Nov25.xlsx
└── PnL_Oct25.xlsx
```

---

## 📄 files.json Format

Create a `files.json` file listing all your trading data files.

### New Format (Recommended):
Segregate strategy files and final P&L files:

```json
{
  "strategy_files": [
    "Pnl_Dec25.xlsx",
    "PnL_Nov25.xlsx",
    "PnL_Oct25.xlsx"
  ],
  "final_files": [
    "Final_PnL_Dec25.xlsx"
  ]
}
```

**File Types:**
- **strategy_files** - Individual strategy P&L (before costs)
  - Shows with 🟡 STRATEGY badge (gold)
- **final_files** - Consolidated P&L after all costs
  - Shows with 🟢 FINAL badge (green)

### Old Format (Still Supported):
Simple array of files (all treated as strategy files):

```json
["Pnl_Dec25.xlsx", "PnL_Nov25.xlsx", "PnL_Oct25.xlsx"]
```

**Supported formats:**
- `.xlsx` - Excel files
- `.xls` - Legacy Excel
- `.csv` - CSV files

---

## 🔀 Strategy vs Final Files

### When to use Strategy Files:
- Individual strategy performance tracking
- Pre-cost analysis
- Strategy-wise breakdowns
- Comparing different trading approaches

**Example:**
- `Crude_Straddle_Dec25.xlsx` - Single strategy data
- `BankNifty_Spreads_Dec25.xlsx` - Another strategy
- `Gold_Scalping_Dec25.xlsx` - Yet another strategy

### When to use Final Files:
- Consolidated P&L after all costs (brokerage, taxes, etc.)
- Overall account performance
- Net profit/loss tracking
- Month-end summaries

**Example:**
- `Final_PnL_Dec25.xlsx` - All strategies combined + costs deducted
- `Account_Statement_Dec25.xlsx` - Net account P&L

### Visual Indicators:
The dashboard shows different badges:
- 🟡 **STRATEGY** badge (Gold border) - Strategy files
- 🟢 **FINAL** badge (Green border) - Final P&L files

This helps you quickly identify which data you're analyzing.

---

## ⚠️ Troubleshooting

### Error: "Failed to fetch"

**Cause:** CORS (Cross-Origin Resource Sharing) restriction

**Solution:**
1. Stop any running server (`Ctrl+C`)
2. Use the CORS-enabled server:
   ```bash
   python3 cors_server.py
   ```
3. Do NOT use: `python3 -m http.server 8080` (it doesn't support CORS)

### Error: "Port 8080 already in use"

**Solution:**
```bash
# Find and kill the process using port 8080
lsof -ti:8080 | xargs kill -9

# Or change the port in cors_server.py:
PORT = 8081  # Use a different port
```

### Files not loading

**Check:**
1. `files.json` exists and is valid JSON
2. File names in `files.json` match actual files (case-sensitive)
3. Server is running (check terminal output)
4. URL in dashboard is `http://localhost:8080` (no trailing slash)

---

## 🔄 Auto-refresh Feature

Enable **"Auto-refresh on page load"** to automatically reload data when you:
- Refresh the dashboard page
- Open the dashboard in a new tab
- Come back to the dashboard tab

This is useful for live trading data updates.

---

## 🛡️ Security Notes

- Server only accepts connections from localhost
- No external network access
- Files are served read-only
- No authentication required (local only)

---

## 💡 Tips

### Multiple Folders
To serve different folders, change directory:
```bash
cd ~/Documents/TradesQ1
python3 /path/to/cors_server.py
```

### Background Server
Run server in background:
```bash
./start_server.sh &
```

Kill background server:
```bash
pkill -f cors_server.py
```

### Custom Port
Edit `cors_server.py` and change:
```python
PORT = 8080  # Change to your desired port
```

---

## 📊 Data File Requirements

Your Excel/CSV files should have columns:
- `Date` or `Trade Date` - Trade date
- `Strategy` - Strategy name
- `P&L` or `Profit/Loss` - Daily P&L amount
- Optional: `Instrument`, `Qty`, `Entry`, `Exit`, etc.

---

## 🎯 Example Workflow

1. **Morning:** Start server
   ```bash
   cd Performance_Data && ./start_server.sh
   ```

2. **Trading Day:** Update Excel files as you trade

3. **Dashboard:** Refresh to see latest data (if auto-refresh enabled)

4. **End of Day:** Server auto-stops when you close terminal, or:
   ```bash
   # Press Ctrl+C in the terminal where server is running
   ```

---

## 📞 Common Commands

```bash
# Start server
./start_server.sh

# Check if server is running
lsof -i :8080

# Stop server
# Press Ctrl+C in the terminal, or:
pkill -f cors_server.py

# Test server manually
curl http://localhost:8080/files.json
```

---

**Version:** 1.0
**Last Updated:** January 22, 2026
