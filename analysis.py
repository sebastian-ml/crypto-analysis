import matplotlib.pyplot as plt
import numpy as np
from datasets import altcoins_bought, btc_data

plt.style.use('seaborn')


# Coins included in analysis
altcoins_table = altcoins_bought[['coin_name', 'buy', 'date']]
print(altcoins_table)

coins_by_buy_group = altcoins_table['buy'].value_counts()
largest_group_count = max(coins_by_buy_group)

coins_by_buy_group.plot(kind='bar',
                        title='Number of coins in each group')

plt.xticks(rotation='horizontal')
plt.yticks(np.arange(0, largest_group_count + 1, 1))

# Bitcoin
buy_dates = altcoins_table[altcoins_table['buy'] > 0]
buy_dates = buy_dates[['date']]
btc_data['date'] = btc_data['date'].astype('datetime64[ns]')

btc_prices_on_buy = buy_dates.merge(
    btc_data,
    left_on='date',
    right_on='date'
)

fig, ax = plt.subplots()

ax.plot(btc_data['date'],
        btc_data['price'],
        zorder=1)

ax.scatter(btc_prices_on_buy['date'],
           btc_prices_on_buy['price'],
           s=30,
           c='r',
           zorder=2)

ax.xaxis.set_major_locator(plt.MaxNLocator(7))
ax.tick_params(axis='x', labelrotation=45)
ax.set_title("Bitcoin's price history")

plt.show()
