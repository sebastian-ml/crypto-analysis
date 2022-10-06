from crypto_list import altcoins_to_analyze
import pandas as pd
import requests
import json
import math

# The oldest date is the first day of analysis
first_buy = altcoins_to_analyze['Date'].min()
first_buy_unix = int(pd.Timestamp(first_buy).timestamp())

end_date = '2021-12-31'
end_buy_unix = int(pd.Timestamp(end_date).timestamp())

# Get Bitcoin historical data.
# Coinmarketcap allows to fetch max 100 days per request.
btc_id = 1

convert_id = 2781
max_days_per_fetch = 100
seconds_in_day = 86400

days_needed = (end_buy_unix - first_buy_unix) / seconds_in_day
fetches_needed = math.ceil(days_needed / (max_days_per_fetch - 1))

date_ranges = []

start_date = first_buy_unix
end_date = end_buy_unix

if days_needed < max_days_per_fetch:
    date_ranges.append({'start_date': start_date, 'end_date': end_date})
else:
    for i in range(fetches_needed):
        if i > 0:
            start_date = end_date + seconds_in_day
        if i < fetches_needed - 2:
            end_date = start_date + (max_days_per_fetch - 1) * seconds_in_day
        if i == fetches_needed - 1:
            end_date = end_buy_unix

        date_ranges.append(
            {'start_date': start_date, 'end_date': end_date})

btc_data = []

for i in date_ranges:
    history_url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=' + str(
        btc_id) + '&convertId=' + str(
        convert_id) + '&timeStart=' + str(
        i['start_date']) + '&timeEnd=' + str(
        i['end_date'])

    btc_api = requests.get(history_url)
    parse_btc_api = json.loads(btc_api.text)
    btc_raw = parse_btc_api['data']['quotes']

    for j in btc_raw:
        time = j['timeClose']
        price = round(j['quote']['close'], 2)
        data = {'coin_id': btc_id, 'time': time, 'price': price}

        btc_data.append(data)

df = pd.DataFrame(btc_data)
