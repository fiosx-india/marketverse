from services.nse_service import nse

print("Connected:", nse.is_connected())

symbols = nse.get_fno_symbols()

print(f"Total F&O Stocks: {len(symbols)}")
print(symbols[:10])
