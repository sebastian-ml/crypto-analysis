import pandas as pd
import requests
import json

"""
"Buy" column legend:
0 - no invest
1 - unknown
2 - invest
"""
altcoins = pd.read_excel('cryptocurrencies.xlsx')

response_api = requests.get(
    'https://web-api.coinmarketcap.com/v1/cryptocurrency/map')
data = response_api.text
parse_json = json.loads(data)

# Simple data cleaning
cmc_coins = pd.DataFrame(parse_json['data'])
cmc_coins = cmc_coins[['id', 'name', 'symbol']]
cmc_coins.rename(columns=str.capitalize, inplace=True)
cmc_coins.rename(columns={'Id': 'ID'}, inplace=True)

altcoins_to_analyze = pd.merge(altcoins, cmc_coins, on='ID')


print(altcoins_to_analyze)