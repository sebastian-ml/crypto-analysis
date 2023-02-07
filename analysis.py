import matplotlib.pyplot as plt
import numpy as np
from datasets import altcoins_bought, btc_data

plt.style.use('seaborn')

# Coins included in analysis
altcoins_table = altcoins_bought[['coin_name', 'buy', 'date']]

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

# Calculate profit for altcoins and bitcoin
invested_amount = 100
btc_price_sell = btc_data.query('date == date.max()')['price']
btc_price_sell = btc_price_sell.iloc[0]

altcoins_bought['%_profit'] = altcoins_bought[
                                  'price_sell'] \
                              / altcoins_bought[
                                  'price_buy'] - 1
altcoins_bought['profit'] = invested_amount * altcoins_bought['%_profit']

altcoins_bought['%_random_coin_profit'] = altcoins_bought[
                                              'random_coin_price_sell'] \
                                          / altcoins_bought[
                                              'random_coin_price_buy'] - 1
altcoins_bought['random_coin_profit'] = invested_amount \
                                        * altcoins_bought[
                                            '%_random_coin_profit']

altcoins_bought['%_bitcoin_profit'] = btc_price_sell \
                                      / altcoins_bought['bitcoin_price_buy'] - 1
altcoins_bought['bitcoin_profit'] = invested_amount * \
                                    altcoins_bought['%_bitcoin_profit']

# For further analysis we get only coins from group 1 (unknown) and 2 (buy)
altcoins_1_2 = altcoins_bought[altcoins_bought['buy'] >= 1]

# Coins
fig_3, ax_3 = plt.subplots()

altcoins_1_2 = altcoins_1_2.sort_values('profit')
ax_3.barh(altcoins_1_2['coin_name'],
          altcoins_1_2['profit'])

ax_3.set_title('Profit generated by altcoins')

# Random coins
fig_4, ax_4 = plt.subplots()

altcoins_1_2 = altcoins_1_2.sort_values('random_coin_profit')
ax_4.barh(altcoins_1_2['random_coin_name'],
          altcoins_1_2['random_coin_profit'])

ax_4.set_title('Profit generated by random altcoins')

# Compare average profit
avg_profit_1_2 = altcoins_1_2['%_profit'].mean()
avg_profit_2 = altcoins_1_2[altcoins_1_2['buy'] == 2]['%_profit'].mean()

random_coin_avg_profit_1_2 = altcoins_1_2['%_random_coin_profit'].mean()
random_coin_avg_profit_2 = altcoins_1_2[altcoins_1_2['buy'] == 2][
    '%_random_coin_profit'].mean()

bitcoin_avg_profit_1_2 = altcoins_1_2['%_bitcoin_profit'].mean()
bitcoin_avg_profit_2 = altcoins_1_2[altcoins_1_2['buy'] == 2][
    '%_bitcoin_profit'].mean()

# Format values as percent
avg_profit_1_2 = round(avg_profit_1_2 * 100, 2)
avg_profit_2 = round(avg_profit_2 * 100, 2)
random_coin_avg_profit_1_2 = round(random_coin_avg_profit_1_2 * 100, 2)
random_coin_avg_profit_2 = round(random_coin_avg_profit_2 * 100, 2)
bitcoin_avg_profit_1_2 = round(bitcoin_avg_profit_1_2 * 100, 2)
bitcoin_avg_profit_2 = round(bitcoin_avg_profit_2 * 100, 2)

labels = ['unknown (1) & invest (2)', 'invest (2)']
coin_profit = [avg_profit_1_2, avg_profit_2]
random_coin_profit = [random_coin_avg_profit_1_2, random_coin_avg_profit_2]
bitcoin_profit = [bitcoin_avg_profit_1_2, bitcoin_avg_profit_2]

# Altcoins and random altcoins
x = np.arange(len(labels))
width = 0.35

fig_5, ax_5 = plt.subplots()

rects1 = ax_5.bar(x - width / 2, coin_profit, width, label='Altcoins')
rects2 = ax_5.bar(x + width / 2, random_coin_profit, width,
                  label='Random altcoins')
ax_5.set_ylabel('Profit (%)')
ax_5.set_xticks(x, labels)
ax_5.set_title('Average percentage profit generated by one altcoin')
ax_5.legend()

ax_5.bar_label(rects1, padding=3)
ax_5.bar_label(rects2, padding=3)

# Altcoins, random altcoins and bitcoin
width = 0.25

fig_6, ax_6 = plt.subplots()

rects3 = ax_6.bar(x, coin_profit, width, label='Altcoins')
rects4 = ax_6.bar(x + width, random_coin_profit, width, label='Random altcoins')
rects5 = ax_6.bar(x + width * 2, bitcoin_profit, width, label='Bitcoin')

ax_6.set_ylabel('Profit (%)')
ax_6.set_xticks(x + width, labels)
ax_6.set_title('Average percentage profit generated by altcoins and Bitcoin')
ax_6.legend()

ax_6.bar_label(rects3, padding=3)
ax_6.bar_label(rects4, padding=3)
ax_6.bar_label(rects5, padding=3)

plt.show()
