import matplotlib.pyplot as plt
import pandas as pd

# Carregar dados
df = pd.read_csv("topic_frequency.csv")
df = df.sort_values("Percentage", ascending=True)

# Configuração estilo científico
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9
})

fig, ax = plt.subplots(figsize=(6.5, 4.5))  # tamanho compatível com coluna dupla

# Barras em escala de cinza
bars = ax.barh(
    df["Topic"],
    df["Percentage"],
    color="0.5",          # cinza médio
    edgecolor="black",
    linewidth=0.6
)

# Eixos
ax.set_xlabel("Frequência (%)")
ax.set_ylabel("")
ax.set_title("Distribuição de tópicos arquiteturais em ADRs (N = 5,471)")

# Remover grid excessivo
ax.grid(False)

# Adicionar valores nas barras
for bar in bars:
    width = bar.get_width()
    if width < 0.1:
        label = f"{width:.2f}%"
    else:
        label = f"{width:.1f}%"

    ax.text(
        width - 1 if width > 3 else width + 0.3,
        bar.get_y() + bar.get_height()/2,
        label,
        va='center',
        ha='right' if width > 3 else 'left',
        fontsize=7
    )

# Ajustar layout
plt.tight_layout()

# Salvar em alta qualidade
plt.savefig("figura_rq1_frequencia_topicos_ieee.png", dpi=600, bbox_inches="tight")

plt.close()