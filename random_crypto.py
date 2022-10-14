import pandas as pd
import requests
import json
from random import randint
from crypto_list import altcoins_to_analyze

random_coins_data = pd.DataFrame(
    columns=['date', 'price', 'random_coin_id', 'coin_id']
)

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


def get_random_coin(top_100, stablecoins_ids):
    """Get random coin from top 100.
    If it's a stablecoin then get another coin."""
    random_coin_id = top_100.at[randint(0, 99), 'id']

    if random_coin_id in stablecoins_ids:
        get_random_coin(top_100, stablecoins_ids)

    return random_coin_id


top_100 = parse_top_100('2022-10-12')
stablecoins_ids = list(map(lambda x: x['id'], stablecoins))
random_coin = get_random_coin(top_100, stablecoins_ids)
