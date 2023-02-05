import matplotlib.pyplot as plt
import numpy as np
from datasets import altcoins_bought, btc_data

plt.style.use('seaborn')

# Coins included in analysis
altcoins_table = altcoins_bought[['coin_name', 'buy', 'date']]
print(altcoins_table)

coins_by_buy_group = altcoins_table['buy'].value_counts()

fig_1, ax_1 = plt.subplots()

ax_1.bar(coins_by_buy_group.index,
         coins_by_buy_group.values)

ax_1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax_1.set_title('Number of coins in each group')

# Random coins
altcoins_table_with_random = altcoins_bought[['coin_name', 'buy',
                                              'date', 'random_coin_name']]
print(altcoins_table_with_random)

# Bitcoin
buy_dates = altcoins_table[altcoins_table['buy'] > 0]
buy_dates = buy_dates[['date']]
btc_data['date'] = btc_data['date'].astype('datetime64[ns]')

btc_prices_on_buy = buy_dates.merge(
    btc_data,
    left_on='date',
    right_on='date'
)

fig_2, ax_2 = plt.subplots()

ax_2.plot(btc_data['date'],
          btc_data['price'],
          zorder=1)

ax_2.scatter(btc_prices_on_buy['date'],
             btc_prices_on_buy['price'],
             s=30,
             c='r',
             zorder=2)

ax_2.xaxis.set_major_locator(plt.MaxNLocator(7))
ax_2.tick_params(axis='x', labelrotation=45)
ax_2.set_title("Bitcoin's price history")

plt.show()
