import pandas as pd
from sklearn.metrics import f1_score

# Carregar dados
df = pd.read_csv(
    "gpt-4.1-mini_classification_300.csv",
    quotechar='"',
    escapechar='\\',
    on_bad_lines='warn'  # mostra aviso, mas continua
)

# Lista fixa de todas as categorias possíveis
ALL_CATEGORIES = [
    "data_persistence",
    "technology_choice",
    "microservices_and_modularity",
    "api_and_contracts",
    "infrastructure_and_deployment",
    "observability",
    "security",
    "testing_strategy",
    "architecture_patterns",
    "performance_and_scalability",
    "governance_and_process",
    "others"
]

# Função para converter string "a, b" em conjunto
def parse_tags(tag_str):
    if pd.isna(tag_str) or tag_str.strip() == "":
        return set()
    return set(tag.strip() for tag in tag_str.split(","))

# Aplicar parsing
df["human_set"] = df["my_topic"].apply(parse_tags)
df["llm_set"] = df["llm_topic"].apply(parse_tags)

# === 1. Jaccard Similarity média ===
def jaccard(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)

df["jaccard"] = df.apply(lambda row: jaccard(row["human_set"], row["llm_set"]), axis=1)
mean_jaccard = df["jaccard"].mean()

# === 2. F1-score macro (multilabel binário) ===
# Criar matriz binária: 1 se categoria está presente, 0 caso contrário
y_true = []
y_pred = []

for _, row in df.iterrows():
    true_vec = [1 if cat in row["human_set"] else 0 for cat in ALL_CATEGORIES]
    pred_vec = [1 if cat in row["llm_set"] else 0 for cat in ALL_CATEGORIES]
    y_true.append(true_vec)
    y_pred.append(pred_vec)

f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)
f1_micro = f1_score(y_true, y_pred, average="micro", zero_division=0)

# === Resultados ===
print("\n📌 Modelo: gpt-4.1-mini\n")
print(f"📊 Métricas de Concordância (300 ADRs)")
print(f"----------------------------------")
print(f"Jaccard Similarity média: {mean_jaccard:.4f}")
print(f"F1-score macro:           {f1_macro:.4f}")
print(f"F1-score micro:           {f1_micro:.4f}")

# Opcional: salvar resultados detalhados
df.to_csv("gpt-4.1-mini_classification_300_with_metrics.csv", index=False)