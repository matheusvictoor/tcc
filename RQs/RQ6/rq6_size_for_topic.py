import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dataset
df = pd.read_csv("../../experiment/dataset_llm_classified.csv")

# Extrair tags (multilabel)
def extract_tags(tag_str):
    if pd.isna(tag_str) or tag_str.strip() == "":
        return []
    return [tag.strip() for tag in tag_str.split(",")]

df['tags'] = df['llm_topic'].apply(extract_tags)

# Explodir para análise por tag (cada ADR pode aparecer múltiplas vezes)
df_exploded = df.explode('tags')
df_exploded = df_exploded[df_exploded['tags'].notna() & (df_exploded['tags'] != '')]

# Estatísticas por tópico
stats_by_topic = df_exploded.groupby('tags')['wordCount'].agg([
    ('count', 'count'),
    ('mean', 'mean'),
    ('median', 'median'),
    ('std', 'std'),
    ('min', 'min'),
    ('max', 'max')
]).sort_values('median', ascending=False)

print("=== TAMANHO MÉDIO POR TÓPICO (ordenado por mediana) ===")
print(stats_by_topic.to_string())

# Filtrar tópicos com pelo menos 50 ocorrências para o gráfico
min_count = 50
topics_to_plot = stats_by_topic[stats_by_topic['count'] >= min_count].index.tolist()
df_plot = df_exploded[df_exploded['tags'].isin(topics_to_plot)].copy()

# ==================== GRÁFICO (PADRÃO RQ2–RQ5) ====================

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9
})

fig, ax = plt.subplots(figsize=(6.5, 4.5))

# Ordenar por mediana (decrescente)
ordered_topics = sorted(
    topics_to_plot,
    key=lambda t: df_exploded[df_exploded['tags'] == t]['wordCount'].median(),
    reverse=True
)

sns.boxplot(
    y='tags',
    x='wordCount',
    data=df_plot,
    order=ordered_topics,
    color="0.6",
    fliersize=2,
    linewidth=0.8,
    ax=ax
)

ax.set_xlabel('Número de palavras')
ax.set_ylabel('')

ax.tick_params(axis='both', labelsize=8)

ax.grid(axis='x', linestyle='--', alpha=0.2)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig('figura_rq6_size_for_topic.png', dpi=600, bbox_inches='tight')
plt.close()

# Teste simples: diferença entre maior e menor mediana
if len(stats_by_topic) >= 2:
    max_median = stats_by_topic['median'].max()
    min_median = stats_by_topic['median'].min()
    print(f"\n=== DIFERENÇA ENTRE MAIOR E MENOR MEDIANA ===")
    print(f"Maior mediana: {max_median:.0f} palavras")
    print(f"Menor mediana: {min_median:.0f} palavras")
    print(f"Diferença: {max_median - min_median:.0f} palavras")