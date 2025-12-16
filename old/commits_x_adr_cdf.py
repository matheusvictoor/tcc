import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

INPUT_FILE = Path("data.jsonl")
df = pd.read_json(INPUT_FILE, lines=True)

# Garantir que as colunas necessárias existem
if 'numberOfCommits' not in df.columns:
    raise ValueError("O dataset precisa conter a coluna 'numberOfCommits'.")

# ---- 2. Estratificação pelo nível de colaboração ----
# Quartis da colaboração
quartis = df['numberOfCommits'].quantile([0.25, 0.5, 0.75, 1]).to_dict()

def classify_collaboration(commits):
    if commits <= quartis[0.25]:
        return 'pouca'
    elif commits <= quartis[0.75]:
        return 'média'
    else:
        return 'muita'

df['colaboracaoCategoria'] = df['numberOfCommits'].apply(classify_collaboration)

# CDF para colaboração
sorted_commits = np.sort(df['numberOfCommits'])
cdf_commits = np.arange(1, len(sorted_commits) + 1) / len(sorted_commits)
plt.figure(figsize=(8, 5))
plt.plot(sorted_commits, cdf_commits, marker='.', linestyle='none')
plt.xlabel("Número de Commits")
plt.ylabel("Proporção acumulada de ADRs")
plt.title("CDF - Como os commits se distribuem entre as ADRs")
plt.grid(True)

for i, (q_label, q_val) in enumerate(quartis.items(), start=1):
    cdf_val = (sorted_commits <= q_val).mean()

    if i == 1:
        xytext = (q_val + 5, cdf_val - 0.3)
    elif i == 4:
        xytext = (q_val - 1, cdf_val + 0.1)
    else:
        xytext = (q_val + 5, cdf_val - 0.1)

    plt.scatter(q_val, cdf_val, color="red", zorder=5)
    plt.annotate(
        f"Q{i} ({q_label*100:.0f}%)\n{int(q_val)} commits",
        xy=(q_val, cdf_val), 
        xytext=xytext,
        arrowprops=dict(facecolor="black", arrowstyle="->"),
        bbox=dict(boxstyle="round,pad=0.3", fc="lightblue", alpha=0.5)
    )

plt.savefig("commits_x_adr_cdf.png", dpi=300, bbox_inches="tight")