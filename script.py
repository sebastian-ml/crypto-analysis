from crypto_list import altcoins_to_analyze
import pandas as pd
import requests
import json
import math

seconds_in_day = 86400
max_days_per_fetch = 100  # Coinmarketcap day limit per request


def get_days_between_dates(start_date, end_date):
    return (end_date - start_date) / seconds_in_day


def get_num_of_fetches(days_needed, max_days_per_fetch):
    return math.ceil(days_needed / (max_days_per_fetch - 1))


def get_date_ranges(ranges, start_date, end_date):
    if ranges == 1:
        return [{'start_date': start_date, 'end_date': end_date}]

    days_to_add = max_days_per_fetch - 1
    date_ranges = []

    for i in range(ranges):
        current_start = start_date + (i * days_to_add * seconds_in_day) + \
                        (0 if i == 0 else seconds_in_day)
        current_end = start_date + ((i + 1) * days_to_add * seconds_in_day)

        if i == ranges - 1:
            current_end = end_date

        date_ranges.append(
            {'start_date': current_start, 'end_date': current_end}
        )

    return date_ranges


def parse_historical_data(coin_id, start_date, end_date):
    url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=' + \
          str(coin_id) + '&convertId=2781' + '&timeStart=' + \
          str(start_date) + '&timeEnd=' + \
          str(end_date)

    cmc_api = requests.get(url)
    parse_json = json.loads(cmc_api.text)

    return parse_json['data']['quotes']


def parse_day_stats(coin_data):
    return {
        'time': coin_data['timeClose'],
        'price': round(coin_data['quote']['close'], 2)
    }


def get_historical_data(coin_id, date_ranges):
    coin_stats = []

    for i in date_ranges:
        historical_data = parse_historical_data(coin_id,
                                                i['start_date'],
                                                i['end_date'])
        date_and_price = list(map(parse_day_stats, historical_data))

        coin_stats.extend(date_and_price)

    return coin_stats


def get_coin_data(start_date, end_date, coin_id):
    days_needed = get_days_between_dates(start_date, end_date)
    fetches_needed = get_num_of_fetches(days_needed, max_days_per_fetch)
    date_ranges = get_date_ranges(fetches_needed, start_date, end_date)

    return get_historical_data(coin_id, date_ranges)


def pd_to_unix(date):
    return int(pd.Timestamp(date).timestamp())


def get_crypto_history(coins_df, last_date):
    df = pd.DataFrame(columns=['time', 'price', 'ID'])

    for index, row in coins_df.iterrows():
        coin_id = row['ID']
        start_date = pd_to_unix(row['Date'])
        coin_data = get_coin_data(start_date, last_date, coin_id)
        coin_data_df = pd.DataFrame(coin_data)
        coin_data_df['ID'] = coin_id

        df = pd.concat([df, coin_data_df])

    return df


# The oldest date is the first day of analysis
first_buy_unix = pd_to_unix(altcoins_to_analyze['Date'].min())
last_buy_unix = pd_to_unix('2021-12-31')

# Get Bitcoin historical data.
btc_id = 1
btc_data = get_coin_data(first_buy_unix, last_buy_unix, btc_id)
df = pd.DataFrame(btc_data)
df['ID'] = btc_id

# Get altcoins historical data
altcoins_data = get_crypto_history(altcoins_to_analyze, last_buy_unix)
df = pd.concat([df, altcoins_data])
df.reset_index(drop=True, inplace=True)

df.to_excel('crypto_historical_data.xlsx')
