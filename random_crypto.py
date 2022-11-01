import pandas as pd
import requests
import json
import os
from random import randint
from crypto_list import altcoins_to_analyze
from history_fetch import get_crypto_history, last_buy_unix

# List of coins which mimic USD - will be excluded from analysis
stablecoins = [
    {'name': 'tether', 'id': 825},
    {'name': 'binance_usd', 'id': 4687},
    {'name': 'dai', 'id': 4943},
    {'name': 'usd_coin', 'id': 3408},
    {'name': 'true_usd', 'id': 2563},
    {'name': 'usdd', 'id': 19891},
    {'name': 'pax_dollar', 'id': 3330},
    {'name': 'neutrino_usd', 'id': 5068},
    {'name': 'fei_usd', 'id': 8642},
    {'name': 'gemini_dollar', 'id': 3306},
]


def parse_top_100(date):
    url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/historical?convert=USD&date=' \
          + str(date) + '&limit=100&start=1'
    response_api = requests.get(url)
    data = response_api.text
    parse_json = json.loads(data)
    top_100 = pd.DataFrame(parse_json['data'])
    top_100 = top_100[['id', 'cmc_rank']]

    return top_100


def get_random_coin_id(top_100, coin_exceptions_ids):
    """Get random coin from top 100.
    Choose again if coin should not be picked. e.g. stablecoin."""
    random_coin_id = top_100.at[randint(0, 99), 'id']

    if random_coin_id not in coin_exceptions_ids:
        return random_coin_id

    return get_random_coin_id(top_100, coin_exceptions_ids)


def assign_random_coins(coins_df):
    """Get random coin from top100 for each analyzed coin.
    Ensure there are no duplicates and there are no stablecoins."""
    random_coins = pd.DataFrame(columns=['ID', 'Date', 'ParentCoin'])
    exceptions = list(map(lambda x: x['id'], stablecoins))

    for index, row in coins_df.iterrows():
        date = row['Date']
        id = row['ID']
        top_100 = parse_top_100(date)
        random_coin_id = get_random_coin_id(top_100, exceptions)
        exceptions.append(random_coin_id)
        random_coins = random_coins.append({'ID': random_coin_id,
                                            'Date': date,
                                            'ParentCoin': id},
                                           ignore_index=True)

    return random_coins


random_coins = assign_random_coins(altcoins_to_analyze)
historical_data_path = os.path.isfile('./random_crypto_historical_data.xlsx')

if not historical_data_path:
    random_coins_historical = get_crypto_history(random_coins,
                                                 last_buy_unix)
    random_coins_historical['date'] = random_coins_historical['date'].apply(
        lambda x: x[:10])
    random_coins_historical.reset_index(drop=True, inplace=True)
    random_coins_historical.to_excel('random_crypto_historical_data.xlsx')

random_crypto_history = pd.read_excel('random_crypto_historical_data.xlsx')
