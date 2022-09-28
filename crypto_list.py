import pandas as pd
import requests
import json

"""
0 - no invest
1 - unknown
2 - invest
"""

crypto_ids = [[1697, 0], [328, 2], [2010, 2], [1758, 2], [873, 1], [131, 2],
              [2336, 0], [1808, 2], [1720, 2], [1376, 2], [1214, 2], [789, 0],
              [512, 2], [1528, 1], [372, 0], [3155, 0], [2469, 1], [1896, 2],
              [2566, 1], [1839, 2], [2307, 0], [1274, 1], [2758, 2], [2827, 1],
              [1958, 1], [3957, 1], [1975, 2], [2603, 1], [4066, 2], [2267, 2],
              [3218, 1], [1660, 1], [6636, 2], [3794, 1], [1955, 1], [1027, 2]]

altcoins = pd.DataFrame(crypto_ids, columns=['ID', 'Buy'])

response_api = requests.get(
    'https://web-api.coinmarketcap.com/v1/cryptocurrency/map')
data = response_api.text
parse_json = json.loads(data)

# Simple data cleaning
cmc_coins = pd.DataFrame(parse_json['data'])
cmc_coins = cmc_coins[['id', 'name', 'symbol']]
cmc_coins.rename(columns=str.capitalize, inplace=True)
cmc_coins.rename(columns={'Id': 'ID'}, inplace=True)
