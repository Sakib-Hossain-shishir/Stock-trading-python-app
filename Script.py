import os
import time
import requests
import csv
from dotenv import load_dotenv

load_dotenv()

POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')
LIMIT = 1000
SLEEP_TIME = 12  # seconds between requests to respect 5 calls/minute

URL = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
response = requests.get(URL)
tickers = []

data = response.json()
if 'results' in data:
    tickers.extend(data['results'])
else:
    print("Error fetching first page:", data)
    exit()

while 'next_url' in data and data['next_url']:
    print('Requesting next page:', data['next_url'])
    time.sleep(SLEEP_TIME)  # respect rate limit
    next_url = data['next_url']
    if "apiKey=" not in next_url:
        next_url += f"&apiKey={POLYGON_API_KEY}"
    response = requests.get(next_url)
    data = response.json()
    if 'results' in data:
        tickers.extend(data['results'])
    else:
        print("Error fetching page:", data)
        break

print("Total tickers fetched:", len(tickers))


# ---------------- Example tickers ----------------
Example_tickers = {'ticker': 'HSPTU',
                   'name': 'Horizon Space Acquisition II Corp. Units',
                   'market': 'stocks',
                   'locale': 'us',
                   'primary_exchange': 'XNAS',
                   'type': 'et',
                   'active': True,
                   'currency_name': 'usd',
                   'cik': '0002032950',
                   'composite_figi': 'BBG00KX4T8H6'
                   }
# ---------------- CSV export ----------------
fieldnames = list(Example_tickers.keys())
output_csv = 'tickers.csv'
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for t in tickers:
        row = {key: t.get(key, '') for key in fieldnames}
        writer.writerow(row)
print(f'wrote {len(tickers)} rows to {output_csv}')