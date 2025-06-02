import requests
import pandas as pd
from io import StringIO

# Test different URL formats
SHEET_ID = "1u2wKp756BwFvE3ZeLgurpRX-yVt1wSrSTbV65b7o-_o"

urls_to_test = [
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/pub?output=csv&gid=0",
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0",
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv",
]

def test_url(url):
    print(f"\nTesting: {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, verify=False, headers=headers, allow_redirects=True)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            # Try to parse as CSV
            df = pd.read_csv(StringIO(response.text))
            print(f"Success! Loaded {len(df)} rows")
            print("Columns:", list(df.columns))
            if len(df) > 0:
                print("First row:", df.iloc[0].to_dict())
            return True
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    print("Testing Google Sheets access...")
    print("Sheet ID:", SHEET_ID)
    
    success = False
    for url in urls_to_test:
        if test_url(url):
            success = True
            break
    
    if not success:
        print("\n❌ All tests failed!")
        print("\nTo fix this:")
        print("1. Open your Google Sheet")
        print("2. File → Share → Publish to web")
        print("3. Choose 'Entire Document' and 'CSV'")
        print("4. Click 'Publish'")
        print("5. Use the published URL")
    else:
        print("\n✅ Connection successful!") 