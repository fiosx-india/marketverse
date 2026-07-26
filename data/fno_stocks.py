# ==========================================
# MarketVerse F&O Stock Universe
# ==========================================

FNO_STOCKS = [
    {"name": "Reliance Industries Ltd", "symbol": "RELIANCE.NS", "sector": "Energy"},
    {"name": "HDFC Bank Ltd", "symbol": "HDFCBANK.NS", "sector": "Banking"},
    {"name": "ICICI Bank Ltd", "symbol": "ICICIBANK.NS", "sector": "Banking"},
    {"name": "State Bank of India", "symbol": "SBIN.NS", "sector": "Banking"},
    {"name": "Axis Bank Ltd", "symbol": "AXISBANK.NS", "sector": "Banking"},
    {"name": "Kotak Mahindra Bank Ltd", "symbol": "KOTAKBANK.NS", "sector": "Banking"},
    {"name": "IndusInd Bank Ltd", "symbol": "INDUSINDBK.NS", "sector": "Banking"},
    {"name": "Punjab National Bank", "symbol": "PNB.NS", "sector": "Banking"},

    {"name": "Infosys Ltd", "symbol": "INFY.NS", "sector": "IT"},
    {"name": "Tata Consultancy Services", "symbol": "TCS.NS", "sector": "IT"},
    {"name": "HCL Technologies", "symbol": "HCLTECH.NS", "sector": "IT"},
    {"name": "Wipro Ltd", "symbol": "WIPRO.NS", "sector": "IT"},
    {"name": "Tech Mahindra", "symbol": "TECHM.NS", "sector": "IT"},

    {"name": "Larsen & Toubro", "symbol": "LT.NS", "sector": "Infrastructure"},
    {"name": "Bharti Airtel", "symbol": "BHARTIARTL.NS", "sector": "Telecom"},
    {"name": "Tata Motors", "symbol": "Automobile", "sector": "Automobile"},
    {"name": "Maruti Suzuki", "symbol": "MARUTI.NS", "sector": "Automobile"},
    {"name": "Mahindra & Mahindra", "symbol": "M&M.NS", "sector": "Automobile"},
    {"name": "Bajaj Auto", "symbol": "BAJAJ-AUTO.NS", "sector": "Automobile"},
    {"name": "Eicher Motors", "symbol": "EICHERMOT.NS", "sector": "Automobile"},

    {"name": "Sun Pharmaceutical", "symbol": "SUNPHARMA.NS", "sector": "Pharma"},
    {"name": "Dr. Reddy's Laboratories", "symbol": "DRREDDY.NS", "sector": "Pharma"},
    {"name": "Cipla Ltd", "symbol": "CIPLA.NS", "sector": "Pharma"},
    {"name": "Divi's Laboratories", "symbol": "DIVISLAB.NS", "sector": "Pharma"},

    {"name": "NTPC Ltd", "symbol": "NTPC.NS", "sector": "Power"},
    {"name": "Power Grid Corporation", "symbol": "POWERGRID.NS", "sector": "Power"},
    {"name": "ONGC Ltd", "symbol": "ONGC.NS", "sector": "Oil & Gas"},
    {"name": "BPCL Ltd", "symbol": "BPCL.NS", "sector": "Oil & Gas"},
    {"name": "Coal India Ltd", "symbol": "COALINDIA.NS", "sector": "Mining"},

    {"name": "Tata Steel", "symbol": "TATASTEEL.NS", "sector": "Metals"},
    {"name": "JSW Steel", "symbol": "JSWSTEEL.NS", "sector": "Metals"},
    {"name": "Hindalco Industries", "symbol": "HINDALCO.NS", "sector": "Metals"},

    {"name": "Adani Enterprises", "symbol": "ADANIENT.NS", "sector": "Diversified"},
    {"name": "Adani Ports", "symbol": "ADANIPORTS.NS", "sector": "Ports"},
]

# ==========================================
# Helper Functions
# ==========================================

def get_symbols():
    return [stock["symbol"] for stock in FNO_STOCKS]


def get_names():
    return [stock["name"] for stock in FNO_STOCKS]


def get_stock(symbol):
    for stock in FNO_STOCKS:
        if stock["symbol"] == symbol:
            return stock
    return None


def search_stock(keyword):
    keyword = keyword.lower()

    return [
        stock
        for stock in FNO_STOCKS
        if keyword in stock["name"].lower()
        or keyword in stock["symbol"].lower()
    ]


def get_sector_stocks(sector):
    return [
        stock
        for stock in FNO_STOCKS
        if stock["sector"].lower() == sector.lower()
    ]


def get_index_stocks(index_name):
    return [
        stock
        for stock in FNO_STOCKS
        if index_name in stock.get("index", [])
    ]


def get_all_sectors():
    return sorted(
        list(
            {
                stock["sector"]
                for stock in FNO_STOCKS
            }
        )
    )










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
