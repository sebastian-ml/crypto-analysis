import pandas as pd
from history_fetch import crypto_history
from random_crypto import random_crypto_history, random_coins
from crypto_list import cmc_coins, altcoins as altcoins_bought

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
coins_description = cmc_coins.copy().add_prefix('cds_')
random_coins_description = cmc_coins.copy().add_prefix('rcds_')
altcoins_bought = altcoins_bought.add_prefix('ab_')

crypto_data = altcoins \
    .merge(random_coins,
           left_on='cd_ID',
           right_on='rc_ParentCoin') \
    .merge(random_crypto_history,
           how='left',
           left_on=['rc_ID', 'cd_date'],
           right_on=['rch_ID', 'rch_date']) \
    .merge(coins_description,
           left_on='cd_ID',
           right_on='cds_ID') \
    .merge(random_coins_description,
           left_on='rc_ID',
           right_on='rcds_ID') \
    .merge(altcoins_bought,
           left_on='cd_ID',
           right_on='ab_ID')

crypto_data = crypto_data[
    ['cd_ID', 'cds_Name', 'cd_date', 'cd_price', 'rc_ID', 'rcds_Name',
     'rch_price', 'ab_Buy']
]
crypto_data.rename(
    columns={'cd_ID': 'ID',
             'cds_Name': 'coin_name',
             'cd_date': 'date',
             'cd_price': 'price',
             'ab_Buy': 'buy',
             'rc_ID': 'random_coin_ID',
             'rcds_Name': 'random_coin_name',
             'rch_price': 'random_coin_price'},
    inplace=True)
