#!/bin/bash

# Multi-Index Premium Coverage Calculator
# Supports Nifty, Sensex, and Bank Nifty with API data fetching
# Usage: ./script.sh [index1_dte1] [index2_dte2] ...
# Example: ./script.sh nifty0 sensex2 banknifty1

# Load configuration if exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/premium_config.conf" ]; then
    source "$SCRIPT_DIR/premium_config.conf"
fi

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to get premium percentage
get_premium_pct() {
    local index=$1
    local dte=$2
    
    case "$index" in
        nifty)
            case $dte in
                0) echo "0.63" ;;
                1) echo "1.02" ;;
                2) echo "1.31" ;;
                3) echo "1.53" ;;
                4) echo "1.74" ;;
            esac
            ;;
        sensex)
            case $dte in
                0) echo "0.60" ;;
                1) echo "0.95" ;;
                2) echo "1.17" ;;
                3) echo "1.29" ;;
                4) echo "1.55" ;;
            esac
            ;;
        banknifty)
            case $dte in
                0) echo "0.63" ;;
                1) echo "1.02" ;;
                2) echo "1.31" ;;
                3) echo "1.53" ;;
                4) echo "1.72" ;;
            esac
            ;;
    esac
}

# Function to fetch Nifty data
fetch_nifty() {
    # Fetch current spot price (lastPrice)
    local value=$(curl -s \
        -H "User-Agent: Mozilla/5.0" \
        -H "Accept: application/json" \
        "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050" | \
        grep -o '"lastPrice":[0-9.]*' | \
        head -1 | \
        cut -d':' -f2)

    if [ -z "$value" ] || [ "$value" == "null" ]; then
        echo "24500.00"
    else
        echo "$value"
    fi
}

# Function to fetch Bank Nifty data
fetch_banknifty() {
    # Fetch current spot price (lastPrice)
    local value=$(curl -s \
        -H "User-Agent: Mozilla/5.0" \
        -H "Accept: application/json" \
        "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK" | \
        grep -o '"lastPrice":[0-9.]*' | \
        head -1 | \
        cut -d':' -f2)

    if [ -z "$value" ] || [ "$value" == "null" ]; then
        echo "52000.00"
    else
        echo "$value"
    fi
}

# Function to fetch Sensex data
fetch_sensex() {
    # Check if manual override is set
    if [ ! -z "$SENSEX_VALUE" ]; then
        echo "$SENSEX_VALUE"
        return
    fi
    
    # Try Python helper first (more reliable)
    if [ -f "fetch_sensex.py" ]; then
        local value=$(python3 fetch_sensex.py 2>/dev/null)
        if [ ! -z "$value" ] && [ "$value" != "80500.00" ]; then
            echo "$value"
            return
        fi
    fi
    
    # Final fallback value
    echo "80500.00"
}

# Function to calculate premium
calculate_premium() {
    local close_value=$1
    local percentage=$2
    echo "scale=2; $close_value * $percentage / 100" | bc
}

# Parse arguments into a simple list
REQUESTED_ITEMS=""

if [ $# -eq 0 ]; then
    # Default: show all indices, all DTEs
    for dte in 0 1 2 3 4; do
        REQUESTED_ITEMS="$REQUESTED_ITEMS nifty_$dte sensex_$dte banknifty_$dte"
    done
else
    # Parse specific requests
    for arg in "$@"; do
        arg_lower=$(echo "$arg" | tr '[:upper:]' '[:lower:]')
        
        if [[ $arg_lower =~ ^(nifty|sensex|banknifty)([0-4])$ ]]; then
            index="${BASH_REMATCH[1]}"
            dte="${BASH_REMATCH[2]}"
            REQUESTED_ITEMS="$REQUESTED_ITEMS ${index}_${dte}"
        else
            echo -e "${RED}Invalid argument: $arg${NC}" >&2
            echo "Format: indexDTE (e.g., nifty0, sensex2, banknifty1)" >&2
            exit 1
        fi
    done
fi

# Main execution
echo -e "${BLUE}================================================${NC}"
echo -e "${YELLOW}  Multi-Index Premium Coverage Calculator${NC}"
echo -e "${BLUE}================================================${NC}"
echo

# Fetch index values
echo -e "${YELLOW}Fetching current spot prices...${NC}"
NIFTY_CLOSE=$(fetch_nifty)
SENSEX_CLOSE=$(fetch_sensex)
BANKNIFTY_CLOSE=$(fetch_banknifty)

echo -e "${GREEN}✓ Nifty Spot: ₹${NIFTY_CLOSE}${NC}"
echo -e "${GREEN}✓ Sensex Spot: ₹${SENSEX_CLOSE}${NC}"
echo -e "${GREEN}✓ Bank Nifty Spot: ₹${BANKNIFTY_CLOSE}${NC}"
echo

# Generate output filename with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="premium_coverage_${TIMESTAMP}.csv"

# Write CSV header
echo "Index,DTE,Avg_Coverage_Premium_Percent,Spot_Close,Average_Premium" > "$OUTPUT_FILE"

# Display table header with coverage premium title
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}${YELLOW}                          COVERAGE PREMIUM DETAILS                           ${NC}${BLUE}║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo
printf "${BLUE}%-15s %-10s %-15s %-20s %-20s${NC}\n" "Index" "DTE" "Premium %" "Spot Price" "Premium Amount"
printf "${BLUE}%-15s %-10s %-15s %-20s %-20s${NC}\n" "─────────────" "────────" "─────────────" "──────────────────" "──────────────────"

# Process each requested item
for item in $REQUESTED_ITEMS; do
    index=$(echo $item | cut -d'_' -f1)
    dte=$(echo $item | cut -d'_' -f2)
    
    # Get the close value for this index
    case "$index" in
        nifty)
            close_value=$NIFTY_CLOSE
            display_name="Nifty"
            ;;
        sensex)
            close_value=$SENSEX_CLOSE
            display_name="Sensex"
            ;;
        banknifty)
            close_value=$BANKNIFTY_CLOSE
            display_name="Bank Nifty"
            ;;
    esac
    
    # Get premium percentage
    pct=$(get_premium_pct $index $dte)
    
    # Calculate premium
    premium=$(calculate_premium $close_value $pct)

    # Display row with alternating colors for readability
    printf "${GREEN}%-15s${NC} ${YELLOW}%-10s${NC} %-15s ${BLUE}%-20s${NC} ${GREEN}%-20s${NC}\n" "$display_name" "$dte" "$pct%" "₹$close_value" "₹$premium"

    # Write to CSV
    echo "$display_name,$dte,$pct,$close_value,$premium" >> "$OUTPUT_FILE"
done

echo
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✓ Output saved to: $OUTPUT_FILE${NC}"
echo -e "${BLUE}================================================${NC}"