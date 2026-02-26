import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv("../../experiment/topic_frequency.csv")

df = df.sort_values("Percentage", ascending=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9
})

sns.set_palette("Blues")

fig, ax = plt.subplots(figsize=(6.5, 4.5))

bars = ax.barh(
    df["Topic"],
    df["Percentage"],
    color="0.6"
)

ax.set_xlabel('Frequência (%)')

for bar, percentage in zip(bars, df['Percentage']):
    width = bar.get_width()
    ax.annotate(f'{percentage:.2f}%',
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0),
                textcoords="offset points",
                ha='left', va='center', fontsize=9)

ax.xaxis.grid(True, linestyle='--', alpha=0.2)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.savefig('figura_rq1_frequencia_topicos.png', dpi=600, bbox_inches='tight')
