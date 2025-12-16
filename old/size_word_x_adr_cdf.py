import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

INPUT_FILE = Path("data.jsonl")
df = pd.read_json(INPUT_FILE, lines=True)

# Garantir que as colunas necessárias existem
if 'wordCount' not in df.columns:
    raise ValueError("O dataset precisa conter a coluna 'wordCount'.")

# ---- 1. Estratificação pelo tamanho das ADRs ----
quartis = df['wordCount'].quantile([0.25, 0.5, 0.75, 1]).to_dict()

def classify_size(wc):
    if wc <= quartis[0.25]:
        return 'pequena'
    elif wc <= quartis[0.75]:
        return 'média'
    else:
        return 'grande'

df['tamanhoCategoria'] = df['wordCount'].apply(classify_size)

sorted_wc = np.sort(df['wordCount'])
cdf_wc = np.arange(1, len(sorted_wc) + 1) / len(sorted_wc)
plt.figure(figsize=(8, 5))
plt.plot(sorted_wc, cdf_wc, marker='.', linestyle='none')
plt.xlabel("Número de Tokens")
plt.ylabel("Proporção acumulada de ADRs")
plt.title("CDF - Distribuição do Tamanho das ADRs (em tokens)")
plt.grid(True)

for i, (q_label, q_val) in enumerate(quartis.items(), start=1):

    cdf_val = (sorted_wc <= q_val).mean()
    
    plt.scatter(q_val, cdf_val, color="red", zorder=5)
    plt.annotate(
        f"Q{i} ({q_label*100:.0f}%)\n{int(q_val)} tokens",
        xy=(q_val, cdf_val), 
        xytext=(q_val+500, cdf_val-0.1),
        arrowprops=dict(facecolor="black", arrowstyle="->"),
        bbox=dict(boxstyle="round,pad=0.3", fc="lightblue", alpha=0.5)
    )
    
plt.savefig("size_word_x_adr_cdf.png", dpi=300, bbox_inches="tight")