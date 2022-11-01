import pandas as pd
from history_fetch import crypto_history
from random_crypto import random_crypto_history, random_coins

# Display settings
pd.set_option('display.max_columns', 20)

"""
Prepare datasets for analysis. 
Perform joins, delete unnecessary columns, rename columns.
"""

btc_data = crypto_history.loc[crypto_history['ID'] == 1]
btc_data = btc_data[['ID', 'date', 'price']]

altcoins = crypto_history.loc[crypto_history['ID'] != 1]
altcoins = altcoins[['ID', 'date', 'price']]

altcoins = altcoins.add_prefix('cd_')
random_coins = random_coins.add_prefix('rc_')
random_crypto_history = random_crypto_history.add_prefix('rch_')

crypto_data = altcoins.merge(random_coins,
                             left_on='cd_ID',
                             right_on='rc_ParentCoin')
crypto_data = pd.merge(crypto_data,
                       random_crypto_history,
                       how='left',
                       left_on=['rc_ID', 'cd_date'],
                       right_on=['rch_ID', 'rch_date'])

crypto_data = crypto_data[
    ['cd_ID', 'cd_date', 'cd_price', 'rc_ID', 'rch_price']
]
crypto_data.rename(
    columns={'cd_ID': 'ID', 'cd_date': 'date', 'cd_price': 'price',
             'rc_ID': 'random_coin_ID', 'rch_price': 'random_coin_price'},
    inplace=True)

print(crypto_data.head())
