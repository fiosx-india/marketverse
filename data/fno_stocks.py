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







Sub SendToMainFile()
    Dim wsSub As Worksheet
    Dim wbMain As Workbook
    Dim MainFilePath As String
    
    ' தற்போதைய சப்-ஃபைல் ஷீட்
    Set wsSub = ActiveSheet
    
    ' உங்கள் மெயின் ஃபைல் இருக்கும் சரியான பாத் (Path) மற்றும் பெயரை இங்கு கொடுக்கவும்
    MainFilePath = "C:\MyFiles\MainFile.xlsx"
    
    On Error Resume Next
    ' மெயின் ஃபைலை பின்னணியில் திறத்தல்
    Set wbMain = Workbooks.Open(MainFilePath)
    On Error GoTo 0
    
    If wbMain Is Nothing Then
        MsgBox "மெயின் ஃபைலைக் கண்டுபிடிக்க முடியவில்லை! பாத்தை சரிபார்க்கவும்.", vbCritical
        Exit Sub
    End If
    
    ' சப்-ஃபைலில் உள்ள டேட்டாவை மெயின் ஃபைலுக்கு மாற்றுவதற்கான கோடு இங்கு செயல்படும்
    
    ' மெயின் ஃபைலை சேமித்து மூடுதல்
    wbMain.Save
    wbMain.Close False
    
    MsgBox "தகவல் வெற்றிகரமாக மெயின் ஃபைலுக்கு அனுப்பப்பட்டுவிட்டது!", vbInformation, "Sent Successfully"
    
    ' இன்டர்நெட் அல்லது மெமரி குப்பைகள் சேராதவாறு கிளியர் செய்தல்
    Application.CutCopyMode = False
End Sub
