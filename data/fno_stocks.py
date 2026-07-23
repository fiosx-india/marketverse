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
    {"name": "Tata Motors", "symbol": "TATAMOTORS.NS", "sector": "Automobile"},
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
    
