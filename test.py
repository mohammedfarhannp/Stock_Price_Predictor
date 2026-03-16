# test_nselib.py
from nselib import capital_market
from datetime import datetime, timedelta
import pandas as pd

def fetch_stock_data_nselib(symbol="ROLEXRINGS", from_date="01-01-2025", to_date="16-03-2026"):
    """
    Fetch stock data and map nselib columns to your format
    """
    try:
        print(f"Fetching {symbol} data from {from_date} to {to_date}...")
        
        # Fetch data from nselib
        data = capital_market.price_volume_and_deliverable_position_data(
            symbol=symbol,
            from_date=from_date,
            to_date=to_date
        )
        
        if data is None or data.empty:
            print("❌ No data returned")
            return None
        
        print(f"\n✅ Raw data columns from nselib:")
        for col in data.columns:
            print(f"   - {col}")
        
        # CORRECT MAPPING based on your actual columns
        mapped_data = pd.DataFrame({
            'Date': pd.to_datetime(data['Date']).dt.strftime('%d/%m/%Y'),
            'Open': data['OpenPrice'],        # OpenPrice column
            'High': data['HighPrice'],        # HighPrice column
            'Low': data['LowPrice'],          # LowPrice column
            'Close': data['ClosePrice'],      # ClosePrice column
            'Volume': data['TotalTradedQuantity']  # TotalTradedQuantity column
        })
        
        # Sort by date
        mapped_data = mapped_data.sort_values('Date')
        
        print(f"\n✅ Mapped to your format: Date, Open, High, Low, Close, Volume")
        print(f"   Total records: {len(mapped_data)}")
        print(f"   From: {mapped_data['Date'].iloc[0]}")
        print(f"   To: {mapped_data['Date'].iloc[-1]}")
        
        return mapped_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_specific_dates(symbol="ROLEXRINGS"):
    """Test March 13 and 16 specifically"""
    print("\n" + "="*60)
    print("TESTING SPECIFIC DATES: March 13 & 16, 2026")
    print("="*60)
    
    # Get data for March 2026
    data = fetch_stock_data_nselib(
        symbol=symbol,
        from_date="01-03-2026",
        to_date="17-03-2026"
    )
    
    if data is not None:
        print("\n📊 ALL DATA FOR MARCH 2026:")
        print(data.to_string(index=False))
        
        # Filter for specific dates
        target_dates = ['13/03/2026', '16/03/2026']
        for target in target_dates:
            mask = data['Date'] == target
            if mask.any():
                row = data[mask].iloc[0]
                print(f"\n✅ FOUND DATA FOR {target}:")
                print(f"   Open:  ₹{row['Open']}")
                print(f"   High:  ₹{row['High']}")
                print(f"   Low:   ₹{row['Low']}")
                print(f"   Close: ₹{row['Close']}")
                print(f"   Volume: {row['Volume']}")
            else:
                print(f"\n❌ No data for {target}")
    
    return data

def update_csv_file():
    """Update your existing CSV file with real data"""
    csv_path = "data/raw/ROLEXRINGS_NS_2025-01-01_to_CURRENT.csv"
    
    # Fetch complete data from nselib
    print("\n" + "="*60)
    print("UPDATING CSV WITH REAL DATA")
    print("="*60)
    
    full_data = fetch_stock_data_nselib(
        symbol="ROLEXRINGS",
        from_date="01-01-2025",
        to_date="16-03-2026"
    )
    
    if full_data is not None:
        # Save to your CSV file
        full_data.to_csv(csv_path, index=False)
        print(f"\n✅ CSV updated successfully: {csv_path}")
        print(f"   Records: {len(full_data)}")
        print(f"   Date range: {full_data['Date'].iloc[0]} to {full_data['Date'].iloc[-1]}")
        
        # Show March data specifically
        march_data = full_data[full_data['Date'].str.contains('/03/2026')]
        if not march_data.empty:
            print("\n📊 MARCH 2026 DATA IN YOUR CSV:")
            print(march_data.to_string(index=False))
    
    return full_data

if __name__ == "__main__":
    print("="*60)
    print("NSELIB TO YOUR CSV FORMAT CONVERTER")
    print("="*60)
    
    # Update your CSV file
    update_csv_file()