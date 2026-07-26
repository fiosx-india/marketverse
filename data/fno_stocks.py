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






import os
import pandas as pd

def send_to_main():
    # தற்போதைய சப்-ஃபைலின் பெயர் (உங்கள் ஃபைல் பெயருக்கு ஏற்ப மாற்றிக் கொள்ளவும்)
    current_file_name = "file1.xlsx" 
    
    # மெயின் ஃபைல் சேமிக்கப்பட்டுள்ள முழுமையான மற்றும் சரியான பாத் (Path)
    main_file_path = r"C:\MyFiles\MainFile.xlsx"
    
    # சப்-ஃபைல் இருக்கும் ஃபோல்டர் பாத் (நடப்பு ஃபோல்டர்)
    current_file_path = os.path.join(os.getcwd(), current_file_name)
    
    # சப்-ஃபைல் உள்ளதா என சோதித்தல்
    if os.path.exists(current_file_path):
        try:
            # சப்-ஃபைலைப் படித்தல்
            df = pd.read_excel(current_file_path)
            df['Source_File'] = current_file_name
            
            # மெயின் ஃபைல் ஏற்கனவே இருக்கிறதா என சோதித்து இணைத்தல்
            if os.path.exists(main_file_path):
                main_df = pd.read_excel(main_file_path)
                # பழைய டேட்டாவுடன் புதிய டேட்டாவைச் சேர்த்தல்
                combined_df = pd.concat([main_df, df], ignore_index=True)
            else:
                combined_df = df
                
            # மெயின் ஃபைலில் சேமித்தல் (இதுவே நேரடி இணைப்பு)
            combined_df.to_excel(main_file_path, index=False)
            print(f"Success: Data from '{current_file_name}' successfully sent and updated in Main File!")
            
        except Exception as e:
            print(f"Error while processing the file: {e}")
    else:
        print(f"Error: '{current_file_name}' was not found in the current folder. Please check the file name.")

if __name__ == "__main__":
    send_to_main()
