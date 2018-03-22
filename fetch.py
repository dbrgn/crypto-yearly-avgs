import json
import os.path
import requests
import statistics

# Config
api_key = ''
api_secret = ''
year = 2017
base_currency = 'CHF'

# Coins
# http GET https://www.cryptocurrencychart.com/api/coin/list Key:$key Secret:$secret > coins.json
coins = [
    ('BTC', 363),
    ('LTC', 366),
    ('XMR', 370),
    ('EOS', 2391),
    ('XTZ', 2797),
]

# Dates
start = '%d-01-01' % year
end = '%d-12-31' % year

# URL
base_url = 'https://www.cryptocurrencychart.com'


def get_filename(coin):
    return 'data/%s-%d.json' % (coin[0].lower(), year)


# Fetch data
print('Fetching data...')
for coin in coins:
    filename = get_filename(coin)

    if os.path.exists(filename):
        print('File %s already exists, skipping' % filename)
        continue

    # Request
    url = '%s/api/coin/history/%s/%s/%s/price/%s' % (base_url, coin[1], start, end, base_currency)
    print('Requesting %s' % url)
    resp = requests.get(url, headers={
        'aKey': api_key,
        'Secret': api_secret,
        'Accept': 'application/json',
    })

    # Error checking
    if resp.status_code != 200:
        print('Could not fetch exchange rate %s-%s: HTTP %s' %
              (coin[0], base_currency, resp.status_code))
        continue

    with open(filename, 'w') as f:
        f.write(resp.text)
    print('Wrote data to %s' % filename)

# Calculate average
print('\nCalculating average price for %d...' % year)
for coin in coins:
    filename = get_filename(coin)

    with open(filename, 'r') as f:
        data_raw = f.read()

    try:
        data = json.loads(data_raw)
    except json.decoder.JSONDecodeError as e:
        print('Could not decode file %s: %s' % (filename, e))
        continue

    daily_prices = [day['price'] for day in data['data']]
    if len(daily_prices) < 30:
        print('Error: Less than 30 days of data for %s!' % coin[0])

    print('Average %s price for %s: %.2f (%d days)' %
         (base_currency, coin[0], statistics.mean(daily_prices), len(daily_prices)))
