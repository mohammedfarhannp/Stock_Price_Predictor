# test_march16.py
from nselib import capital_market
from datetime import datetime
import pandas as pd
import os

# Hardcoded test date
TEST_DATE = "16-03-2026"
STOCK_SYMBOL = "ROLEXRINGS"

def fetch_single_day_data(date_str, symbol=STOCK_SYMBOL):
    """
    Fetch data for a single date and extract 6 components:
    DATE, OPEN, HIGH, LOW, CLOSE, VOLUME
    """
    print("=" * 60)
    print(f"TESTING: Fetch data for {date_str}")
    print("=" * 60)
    
    try:
        # Parse the date
        test_date = datetime.strptime(date_str, '%d-%m-%Y')
        
        # For single day, fetch a small range (day before to day after)
        from_date = (test_date - timedelta(days=1)).strftime('%d-%m-%Y')
        to_date = (test_date + timedelta(days=1)).strftime('%d-%m-%Y')
        
        print(f"\n[1] Fetching range: {from_date} to {to_date}")
        
        # Fetch data from nselib
        data = capital_market.price_volume_and_deliverable_position_data(
            symbol=symbol,
            from_date=from_date,
            to_date=to_date
        )
        
        if data is None or data.empty:
            print("❌ No data returned from nselib")
            return None
        
        print(f"\n[2] Raw data columns from nselib:")
        for col in data.columns:
            print(f"    - {col}")
        
        print(f"\n[3] Raw data shape: {data.shape}")
        print("\n[4] Raw data preview:")
        print(data.head())
        
        # Filter for our specific date
        target_date_obj = test_date.date()
        data['Date_obj'] = pd.to_datetime(data['Date']).dt.date
        day_data = data[data['Date_obj'] == target_date_obj]
        
        if day_data.empty:
            print(f"\n❌ No data found specifically for {date_str}")
            return None
        
        print(f"\n[5] Found data for {date_str}:")
        
        # Extract the 6 required components
        extracted = {
            'DATE': date_str,
            'OPEN': float(day_data['OpenPrice'].iloc[0]),
            'HIGH': float(day_data['HighPrice'].iloc[0]),
            'LOW': float(day_data['LowPrice'].iloc[0]),
            'CLOSE': float(day_data['ClosePrice'].iloc[0]),
            'VOLUME': int(day_data['TotalTradedQuantity'].iloc[0])
        }
        
        # Display extracted data
        print(f"\n[6] EXTRACTED 6 COMPONENTS:")
        print(f"    DATE:   {extracted['DATE']}")
        print(f"    OPEN:   ₹{extracted['OPEN']:.2f}")
        print(f"    HIGH:   ₹{extracted['HIGH']:.2f}")
        print(f"    LOW:    ₹{extracted['LOW']:.2f}")
        print(f"    CLOSE:  ₹{extracted['CLOSE']:.2f}")
        print(f"    VOLUME: {extracted['VOLUME']:,}")
        
        return extracted
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        return None

def save_to_temp_csv(data, filename="temp_march16.csv"):
    """Save extracted data to temp CSV file"""
    if data is None:
        print("\n❌ No data to save")
        return False
    
    # Create DataFrame with exact columns needed
    df = pd.DataFrame([data])
    
    # Save to temp CSV
    df.to_csv(filename, index=False)
    print(f"\n[7] Data saved to: {filename}")
    
    # Verify the save
    if os.path.exists(filename):
        print(f"    File size: {os.path.getsize(filename)} bytes")
        
        # Read back to verify
        verify_df = pd.read_csv(filename)
        print(f"\n[8] Verification - CSV contents:")
        print(verify_df.to_string(index=False))
        
        return True
    else:
        print("❌ Failed to save file")
        return False

if __name__ == "__main__":
    # Create temp directory if it doesn't exist
    os.makedirs("temp", exist_ok=True)
    
    # Test with March 16, 2026
    extracted_data = fetch_single_day_data(TEST_DATE)
    
    if extracted_data:
        # Save to temp CSV
        save_to_temp_csv(extracted_data, "temp/march16_data.csv")
        
        print("\n" + "=" * 60)
        print("✅ TEST PASSED: Successfully extracted 6 components")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED: Could not extract data for March 16, 2026")
        print("=" * 60)
        
        # Try alternative: fetch a wider range
        print("\nTrying alternative: Fetching full March data...")
        try:
            alt_data = capital_market.price_volume_and_deliverable_position_data(
                symbol=STOCK_SYMBOL,
                from_date="01-03-2026",
                to_date="31-03-2026"
            )
            if alt_data is not None and not alt_data.empty:
                print("\nFull March data columns:")
                for col in alt_data.columns:
                    print(f"    - {col}")
                print("\nMarch data preview:")
                print(alt_data.head())
                
                # Save full March data for inspection
                alt_data.to_csv("temp/march_full_data.csv", index=False)
                print("\nFull March data saved to: temp/march_full_data.csv")
        except Exception as e:
            print(f"Alternative also failed: {e}")