import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../../experiment/dataset_llm_classified.csv")
df['wordCount'] = pd.to_numeric(df['wordCount'], errors='coerce')

print("=== ESTATÍSTICAS DE TAMANHO (wordCount) ===")
print(f"Média: {df['wordCount'].mean():.2f} palavras")
print(f"Mediana: {df['wordCount'].median():.2f} palavras")
print(f"Desvio padrão: {df['wordCount'].std():.2f}")
print(f"Mínimo: {df['wordCount'].min()} palavras")
print(f"Máximo: {df['wordCount'].max()} palavras")
print(f"Q1 (25%): {df['wordCount'].quantile(0.25):.2f}")
print(f"Q3 (75%): {df['wordCount'].quantile(0.75):.2f}")

bins = [0, 100, 200, 300, 400, 500, 750, 1000, 1500, float('inf')]
labels = ['0-100', '101-200', '201-300', '301-400', '401-500', 
          '501-750', '751-1000', '1001-1500', '> 1500']
df['size_range'] = pd.cut(df['wordCount'], bins=bins, labels=labels, right=True)

range_counts = df['size_range'].value_counts().sort_index()
range_pct = (range_counts / len(df) * 100).round(2)

print("\n=== DISTRIBUIÇÃO POR FAIXAS ===")
for size_range, count, pct in zip(range_counts.index, range_counts.values, range_pct.values):
    print(f"{size_range:12s}: {count:4d} ADRs ({pct:5.2f}%)")

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9
})

fig, ax = plt.subplots(figsize=(6.5, 4.5))

bars = ax.bar(
    range_counts.index.astype(str),
    range_pct.values,
    color="0.6"
)

ax.set_xlabel('Intervalo de contagem de palavras')
ax.set_ylabel('Frequência (%)')

for bar, percentage, count in zip(
    bars,
    range_pct.values,
    range_counts.values
):
    height = bar.get_height()
    ax.annotate(
        f'{percentage:.2f}%\n({count})',
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

plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig('figura_rq4_tamanho.png', dpi=600, bbox_inches='tight')
plt.close()
