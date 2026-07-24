# ==========================================
# MarketVerse MCX Commodity Universe
# ==========================================

MCX_COMMODITIES = [
    {"name": "Gold", "symbol": "GOLD", "sector": "Precious Metals", "exchange": "MCX"},
    {"name": "Silver", "symbol": "SILVER", "sector": "Precious Metals", "exchange": "MCX"},
    {"name": "Crude Oil", "symbol": "CRUDEOIL", "sector": "Energy", "exchange": "MCX"},
    {"name": "Natural Gas", "symbol": "NATURALGAS", "sector": "Energy", "exchange": "MCX"},
    {"name": "Copper", "symbol": "COPPER", "sector": "Base Metals", "exchange": "MCX"},
    {"name": "Zinc", "symbol": "ZINC", "sector": "Base Metals", "exchange": "MCX"},
    {"name": "Aluminium", "symbol": "ALUMINIUM", "sector": "Base Metals", "exchange": "MCX"},
    {"name": "Lead", "symbol": "LEAD", "sector": "Base Metals", "exchange": "MCX"},
    {"name": "Nickel", "symbol": "NICKEL", "sector": "Base Metals", "exchange": "MCX"},
]

def get_symbols():
    return [item["symbol"] for item in MCX_COMMODITIES]

def get_names():
    return [item["name"] for item in MCX_COMMODITIES]

def get_commodity(symbol):
    for item in MCX_COMMODITIES:
        if item["symbol"] == symbol:
            return item
    return None

def search_commodity(keyword):
    keyword = keyword.lower()
    return [
        item for item in MCX_COMMODITIES
        if keyword in item["name"].lower()
        or keyword in item["symbol"].lower()
    ]

def get_sector_commodities(sector):
    return [
        item for item in MCX_COMMODITIES
        if item["sector"].lower() == sector.lower()
    ]

def get_all_sectors():
    return sorted({item["sector"] for item in MCX_COMMODITIES})
