import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
import numpy as np

df = pd.read_csv("../../experiment/dataset_llm_classified.csv")

def extract_tags(tag_str):
    if pd.isna(tag_str) or tag_str.strip() == "":
        return []
    return [tag.strip() for tag in tag_str.split(",")]

df['tags'] = df['llm_topic'].apply(extract_tags)

df_multilabel = df[df['tags'].apply(len) >= 2].copy()

cooccurrence = {}
for tags in df_multilabel['tags']:
    for tag1, tag2 in combinations(sorted(tags), 2):
        pair = (tag1, tag2)
        cooccurrence[pair] = cooccurrence.get(pair, 0) + 1

tags_list = sorted(set(tag for tags in df['tags'] for tag in tags))
matrix = pd.DataFrame(0, index=tags_list, columns=tags_list)

for (tag1, tag2), count in cooccurrence.items():
    matrix.loc[tag1, tag2] = count
    matrix.loc[tag2, tag1] = count

matrix.to_csv("cooccurrence_matrix.csv")

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9
})

fig, ax = plt.subplots(figsize=(12, 8))

abbreviations = {
    "accessibility": "ACC",
    "api_and_contracts": "API",
    "architecture_patterns": "ARCH",
    "data_persistence": "DATA",
    "governance_and_process": "GOV",
    "infrastructure_and_deployment": "INFRA",
    "microservices_and_modularity": "MICRO",
    "observability": "OBS",
    "others": "OTH",
    "performance_and_scalability": "PERF",
    "security": "SEC",
    "technology_choice": "TECH",
    "testing_strategy": "TEST"
}

matrix = matrix.rename(index=abbreviations, columns=abbreviations)

matrix = matrix.sort_index().sort_index(axis=1)

mask = np.triu(np.ones_like(matrix, dtype=bool))

heatmap = sns.heatmap(
    matrix,
    mask=mask,
    cmap='Greys',
    annot=True,
    fmt='d',
    linewidths=0.1,
    linecolor='grey',
    square=True,
    annot_kws={
        'size': 10,
        'color': 'black'
    },
    cbar_kws={
        'label': 'Número de ADRs',
        'shrink': 1,
        'aspect': 50,
        'pad': 0.02
    },
    vmin=0,
    vmax=matrix.values.max(),
    ax=ax
)

cbar = heatmap.collections[0].colorbar
cbar.set_label("Número de ADRs", labelpad=10)
cbar.outline.set_edgecolor('gray')
cbar.outline.set_linewidth(0.4)

threshold = matrix.values.max() * 0.5

for text in heatmap.texts:
    value = float(text.get_text())
    if value > threshold:
        text.set_color('white')
        text.set_weight('bold')
    else:
        text.set_color('black')

ax.tick_params(axis='both', labelsize=9)
ax.tick_params(axis='x', pad=12)

plt.xticks(rotation=0)
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('figura_rq3_cooccurrence.png', dpi=600, bbox_inches='tight')
plt.close()

# # ==================== TOP 10 PARES ====================
# top_pairs = sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True)[:10]

# print("\n=== TOP 10 PARES DE CO-OCORRÊNCIA ===")
# for (tag1, tag2), count in top_pairs:
#     percentage = count / len(df_multilabel) * 100
#     print(f"{tag1} + {tag2}: {count} ADRs ({percentage:.1f}%)")