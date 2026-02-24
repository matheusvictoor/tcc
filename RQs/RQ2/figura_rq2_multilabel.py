import matplotlib.pyplot as plt
import seaborn as sns
from multilabel_distribution import generate_multilabel_distribution

df, distribution_df = generate_multilabel_distribution()

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9
})

fig, ax = plt.subplots(figsize=(6.5, 4.5))

bars = ax.bar(
    distribution_df["Number_of_Tags"].astype(str),
    distribution_df["Percentage"],
    color="0.6"
)

ax.set_xlabel('Número de Tópicos por ADR')
ax.set_ylabel('Frequência (%)')

for bar, percentage, count in zip(
    bars,
    distribution_df['Percentage'],
    distribution_df['Count']
):
    height = bar.get_height()
    ax.annotate(f'{percentage:.2f}%\n({count})',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=9)

ax.yaxis.grid(True, linestyle='--', alpha=0.2)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.savefig('figura_rq2_multilabel.png', dpi=600, bbox_inches='tight')

print("\n=== ESTATÍSTICAS ===")
print(f"Média de tags por ADR: {df['num_tags'].mean():.2f}")
print(f"Mediana de tags por ADR: {df['num_tags'].median():.2f}")
print(f"ADR com mais tags: {df['num_tags'].max()}")
print(f"Porcentagem de ADRs com 1 tag: {(df['num_tags'] == 1).sum() / len(df) * 100:.2f}%")
print(f"Porcentagem de ADRs com 2+ tags: {(df['num_tags'] >= 2).sum() / len(df) * 100:.2f}%")
print(f"Porcentagem de ADRs com 3+ tags: {(df['num_tags'] >= 3).sum() / len(df) * 100:.2f}%")