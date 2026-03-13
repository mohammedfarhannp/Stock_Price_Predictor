# main.py
import sys
import os

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import STOCK_SYMBOL
from fetch_data import fetch_stock_data

def main():
    print("=" * 50)
    print("STOCK PREDICTOR - Testing Phase")
    print("=" * 50)
    
    # Step 1: Fetch data
    print("\n[1] Testing data fetch...")
    data_path = fetch_stock_data()
    
    if data_path:
        print(f"\n[+] Data fetch successful! File saved at:\n   {data_path}")
    else:
        print("\n[-] Data fetch failed. Check your internet connection or stock symbol.")
        return
    
    print("\n" + "=" * 50)
    print("✓ Setup complete! Ready for next steps.")
    print("=" * 50)

if __name__ == "__main__":
    main()