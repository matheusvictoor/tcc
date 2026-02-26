import pandas as pd
import matplotlib.pyplot as plt

# Carregar dataset (use o normalizado se já tiver rodado o script de padronização)
df = pd.read_csv("../../experiment/dataset_llm_classified_normalized.csv")
status_col = "status_normalized"

# Tratar valores vazios como 'unknown'
df["status_normalized"] = df["status_normalized"].fillna("unknown")

# Contar frequências
status_counts = df["status_normalized"].value_counts()
status_pct = (status_counts / len(df) * 100).round(2)

print("=== DISTRIBUIÇÃO DE STATUS ===")
for status, count, pct in zip(status_counts.index, status_counts.values, status_pct.values):
    print(f"{status:15s}: {count:4d} ADRs ({pct:5.2f}%)")

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9
})

fig, ax = plt.subplots(figsize=(6.5, 4.5))

x_positions = range(len(status_counts))

bars = ax.bar(
    x_positions,
    status_pct.values,
    color="0.6"
)

ax.set_xticks(x_positions)
ax.set_xticklabels(
    [s.capitalize() if s != 'unknown' else 'Unknown'
     for s in status_counts.index],
    rotation=45,
    ha='right'
)

ax.set_xlabel('Status da ADR')
ax.set_ylabel('Frequencia (%)')

ax.set_xticklabels(
    [s.capitalize() if s != 'unknown' else 'Unknown'
     for s in status_counts.index],
    rotation=45,
    ha='right'
)

for bar, pct, count in zip(
    bars,
    status_pct.values,
    status_counts.values
):
    height = bar.get_height()
    ax.annotate(
        f'{pct:.2f}%\n({count})',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha='center',
        va='bottom',
        fontsize=9
    )

ax.yaxis.grid(True, linestyle='--', alpha=0.2)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig('figura_rq5_status.png', dpi=600, bbox_inches='tight')