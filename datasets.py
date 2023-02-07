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
btc_data['date'] = btc_data['date'].astype('datetime64[ns]')

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
           how='left',
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
    inplace=True
)

btc_data = btc_data \
    .merge(coins_description,
           left_on='ID',
           right_on='cds_ID')
btc_data = btc_data[['ID', 'cds_Name', 'date', 'price']]
btc_data.rename(
    columns={'cds_Name': 'coin_name'},
    inplace=True
)

# Get prices for all coins when buying and when selling
prices_on_buy = crypto_data[
    crypto_data.groupby('ID')['date'].transform('min') == crypto_data['date']]
prices_on_sell = crypto_data[
    crypto_data.groupby('ID')['date'].transform('max') == crypto_data['date']]

# Set price 0 if coin is not available on certain date
prices_on_sell['random_coin_price'] = prices_on_sell[
    'random_coin_price'].fillna(0)
prices_on_sell['price'] = prices_on_sell['price'].fillna(0)

prices_on_buy = prices_on_buy.add_prefix('pob_')
prices_on_sell = prices_on_sell.add_prefix('pos_')

btc_price = btc_data[['date', 'price']].add_prefix('bd_')

altcoins_bought = altcoins_bought \
    .merge(coins_description,
           left_on='ab_ID',
           right_on='cds_ID') \
    .merge(random_coins,
           left_on='ab_ID',
           right_on='rc_ParentCoin') \
    .merge(random_coins_description,
           left_on='rc_ID',
           right_on='rcds_ID') \
    .merge(prices_on_sell,
           left_on='ab_ID',
           right_on='pos_ID') \
    .merge(prices_on_buy,
           left_on='ab_ID',
           right_on='pob_ID') \
    .merge(btc_price,
           left_on='ab_Date',
           right_on='bd_date')

altcoins_bought = altcoins_bought[['ab_ID', 'cds_Name', 'ab_Buy', 'ab_Date',
                                   'rc_ID', 'rcds_Name', 'pob_price',
                                   'pob_random_coin_price',
                                   'pos_price', 'pos_random_coin_price',
                                   'bd_price']]
altcoins_bought.rename(
    columns={'ab_ID': 'ID',
             'cds_Name': 'coin_name',
             'ab_Buy': 'buy',
             'ab_Date': 'date',
             'rc_ID': 'random_coin_ID',
             'rcds_Name': 'random_coin_name',
             'pob_price': 'price_buy',
             'pob_random_coin_price': 'random_coin_price_buy',
             'pos_price': 'price_sell',
             'pos_random_coin_price': 'random_coin_price_sell',
             'bd_price': 'bitcoin_price_buy'},
    inplace=True
)
