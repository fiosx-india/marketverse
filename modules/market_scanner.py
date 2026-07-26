"""
=========================================================
MarketVerse AI - Market Scanner
=========================================================
Scans market data and identifies trading opportunities.
=========================================================
"""

from modules.intelligence_engine import IntelligenceEngine
from data.mcx_commodities import MCX_COMMODITIES
import streamlit as st


@st.cache_data(ttl=60)
def scan_market(stocks):

    if not stocks:
        return []

    engine = IntelligenceEngine()
    results = []

    for stock in stocks:

        symbol = stock.get("symbol")
        if not symbol:
            continue

        try:
            result = engine.run(symbol)

            market = result.get("market", {})
            news = result.get("news", {})

            price = market.get("price", 0)
            volume = market.get("volume", 0)
            confidence = news.get("confidence", 50)
            volatility = result.get("volatility", 0)

            if price <= 0:
                continue

            signal = "HOLD"

            rsi = market.get("rsi", 50)

            if rsi < 30:
                signal = "BUY"

            elif rsi > 70:
                signal = "SELL"

            elif confidence >= 70 and volatility >= 1.5:
                signal = "BUY"

            elif confidence >= 70 and volatility <= 0.7:
                signal = "SELL"

            results.append({
                "symbol": symbol,
                "price": round(price, 2),
                "change_percent": round(volatility, 2),
                "volume": volume,
                "confidence": confidence,
                "signal": signal
            })

        except Exception as e:
            print(f"Scanner Error - {symbol}: {e}")
            import traceback
            traceback.print_exc()
            continue

    results.sort(
        key=lambda x: (x["confidence"], x["volume"]),
        reverse=True
    )

    return results


def top_buy(results, limit=5):
    return [x for x in results if x["signal"] == "BUY"][:limit]


def top_sell(results, limit=5):
    return [x for x in results if x["signal"] == "SELL"][:limit]


def top_volume(results, limit=5):
    return sorted(
        results,
        key=lambda x: x["volume"],
        reverse=True
    )[:limit]
    
def scan_mcx():
    """
    Scan all MCX commodities.
    Reuses the existing market scanner.
    """
    return scan_market(MCX_COMMODITIES)

if __name__ == "__main__":

    demo = [
        {"symbol": "RELIANCE.NS"},
        {"symbol": "TCS.NS"},
        {"symbol": "INFY.NS"},
        {"symbol": "HDFCBANK.NS"},
        {"symbol": "ICICIBANK.NS"},
    ]

    scanned = scan_market(demo)

    print("\nTop Buy")
    print(top_buy(scanned))

    print("\nTop Sell")
    print(top_sell(scanned))

    print("\nTop Volume")
    print(top_volume(scanned))

    print("\nMCX Scan")
    mcx_results = scan_mcx()
    print(mcx_results)







# --- SUB-FILE DEEP LINE INSPECTOR (இதனை 50/60 சப்-பைல்களின் இறுதியில் வைக்கவும்) ---
import os
import ast

def inspect_subfile_lines():
    """Scans lines of this specific file to find errors, syntax issues, or incorrect lines."""
    current_file = __file__ if '__file__' in locals() or '__file__' in globals() else "sub_module.py"
    analysis_result = {
        "filename": os.path.basename(current_file),
        "total_lines": 0,
        "error_detected": False,
        "error_details": "No errors found. All lines clean ✅"
    }
    
    try:
        if os.path.exists(current_file):
            with open(current_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            analysis_result["total_lines"] = len(lines)
            code_content = "".join(lines)
            
            # AST parsing to catch syntax/line errors precisely
            ast.parse(code_content)
            
    .except SyntaxError as se:
        analysis_result["error_detected"] = True
        analysis_result["error_details"] = f"Syntax Error at Line {se.lineno}: {se.text.strip() if se.text else str(se)}"
    except Exception as e:
        analysis_result["error_detected"] = True
        analysis_result["error_details"] = f"Error in file: {str(e)}"
        
    return analysis_result
