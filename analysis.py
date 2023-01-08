import matplotlib.pyplot as plt
import numpy as np
from datasets import altcoins_bought

# Coins included in analysis
altcoins_table = altcoins_bought[['coin_name', 'buy', 'date']]
print(altcoins_table)

coins_by_buy_group = altcoins_table['buy'].value_counts()
largest_group_count = max(coins_by_buy_group)

coins_by_buy_group.plot(kind='bar',
                        title='Number of coins in each group')
plt.xticks(rotation='horizontal')
plt.yticks(np.arange(0, largest_group_count + 1, 1))

plt.show()
