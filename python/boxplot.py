import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys

data = pd.read_csv(sys.argv[1])
sns.set_theme(style="whitegrid")
ax = sns.boxplot(data=data)
ax.set(ylabel='Runtime ( min )')

plt.show()