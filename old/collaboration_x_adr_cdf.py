import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

INPUT_FILE = Path("data.jsonl")
df = pd.read_json(INPUT_FILE, lines=True)

if "authors" in df.columns:
    df["num_authors"] = df["authors"].apply(lambda x: len(x) if isinstance(x, dict) else 0)
else:
    raise ValueError("O dataset precisa conter a coluna 'authors'.")

# ---- 1. Estratificação pelo tamanho das ADRs ----
quartis = df['num_authors'].quantile([0.25, 0.5, 0.75, 1]).to_dict()
def classify_collaboration(n):
    if n <= quartis[0.25]:
        return 'Baixa'
    elif n <= quartis[0.75]:
        return 'Média'
    else:
        return 'Alta'

df["level_collaboration"] = df["num_authors"].apply(classify_collaboration)
sorted_wc = np.sort(df['num_authors'])
cdf_wc = np.arange(1, len(sorted_wc) + 1) / len(sorted_wc)

plt.figure(figsize=(8, 5))
plt.plot(sorted_wc, cdf_wc, marker='.', linestyle='none')
plt.xlabel("Número de colaboradores por ADR")
plt.ylabel("Proporção acumulada de ADRs")
plt.title("CDF - Distribuição de Colaboradores em ADRs")
plt.grid(True, linestyle="--", alpha=0.6)

for i, (label, value) in enumerate(quartis.items(), start=1):
    cdf_value = df["num_authors"].le(value).mean()
    if i == 1:
        xytext = (value + 1, cdf_value - 0.3)
    elif i == 4:
        xytext = (value, cdf_value + 0.1)
    else:
        xytext = (value + 2, cdf_value - 0.1)

    if i < 2 or ( i == 2 and value < 2):
        textbox = 'colaborador'
    else:
        textbox = 'colaboradores'


    plt.scatter(value, cdf_value, color="red")
    plt.annotate(
        f"Q{i} ({label*100:.0f}%)\n{int(value)} {textbox}",
        xy=(value, cdf_value),
        xytext=xytext,
        arrowprops=dict(facecolor="black", arrowstyle="->"),
        bbox=dict(facecolor="lightblue", alpha=0.7, boxstyle="round,pad=0.3")
    )
    
plt.savefig("collaboration_adr_cdf.png", dpi=300, bbox_inches="tight")