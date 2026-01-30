import pandas as pd

# Carregar o arquivo com as classificações
df = pd.read_csv("gpt-4.1-mini_classification_300_with_metrics.csv")

# Função para converter string "a, b" em conjunto
def parse_tags(tag_str):
    if pd.isna(tag_str) or not str(tag_str).strip():
        return set()
    return set(tag.strip() for tag in str(tag_str).split(","))

# Aplicar parsing
df["human_set"] = df["my_topic"].apply(parse_tags)
df["llm_set"] = df["llm_topic"].apply(parse_tags)


# Calcular cobertura das tags humanas pela LLM
def human_tag_coverage(human_set, llm_set):
    if len(human_set) == 0:
        # Se humano não atribuiu nenhuma tag, consideramos cobertura total (ou pode ignorar)
        return 1.0
    intersection = len(human_set & llm_set)
    return intersection / len(human_set)

df["human_tag_coverage"] = df.apply(
    lambda row: human_tag_coverage(row["human_set"], row["llm_set"]), axis=1
)

# Média geral
mean_coverage = df["human_tag_coverage"].mean()

print("\n📌 Modelo: gpt-4.1-mini\n")
print(f"📊 Cobertura das minha tags")
print(f"----------------------------------")
print(f"% médio das minhas tags cobertas pela LLM: {mean_coverage:.4f} ({mean_coverage*100:.2f}%)")

# Opcional: salvar com a nova métrica
df.to_csv("gpt-4.1-mini_classification_300_with_coverage.csv", index=False)

# Exemplo de análise adicional (opcional)
print(f"\n🔍 Distribuição:")
print(f"- Cobertura = 100% (todas as tags humanas foram acertadas): {(df['human_tag_coverage'] == 1.0).sum()} / {len(df)}")
print(f"- Cobertura = 0% (nenhuma tag humana foi acertada): {(df['human_tag_coverage'] == 0.0).sum()} / {len(df)}")