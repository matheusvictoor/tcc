import pandas as pd
import re

INPUT_FILE = "dataset_llm_classified.csv"
OUTPUT_FILE = "dataset_llm_classified_normalized.csv"

df = pd.read_csv(INPUT_FILE)

if "status" not in df.columns:
    raise ValueError("Coluna 'status' não encontrada no dataset.")

# pega valores unicos (incluindo vazios)
unique_status = df["status"].fillna("(EMPTY)").unique()

# limpa espaços extras
unique_status = [str(status).strip() for status in unique_status]

# remove duplicatas apos strip
unique_status = sorted(set(unique_status))

print("Status únicos encontrados:\n")
for status in unique_status:
    print(f"- {status}")

print(f"\nTotal de status distintos: {len(unique_status)}")

STATUS_KEYWORDS = [
    "accepted",
    "adopted",
    "approved",
    "decided",
    "proposed",
    "proposal",
    "pending",
    "discussing",
    "rejected",
    "deprecated",
    "superseded",
    "draft",
    "done"
]

def extract_status(text):
    if pd.isna(text):
        return None
    
    text = str(text).lower()
    
    # remove markdown links e imagens
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    
    # remove HTML
    text = re.sub(r'<!--.*?-->', '', text)
    
    # remove datas
    text = re.sub(r'\d{4}-\d{2}-\d{2}', '', text)
    text = re.sub(r'\d{2}/\d{2}/\d{4}', '', text)
    
    # procura palavra-chave
    for keyword in STATUS_KEYWORDS:
        if keyword in text:
            return keyword
    
    return None

df["status_extracted"] = df["status"].apply(extract_status)

NORMALIZATION_MAP = {
    "accepted": "accepted",
    "adopted": "accepted",
    "approved": "accepted",
    "decided": "accepted",
    "done": "accepted",
    "proposed": "proposed",
    "proposal": "proposed",
    "pending": "proposed",
    "discussing": "proposed",
    "rejected": "rejected",
    "deprecated": "deprecated",
    "superseded": "superseded",
    "draft": "draft"
}

df["status_normalized"] = df["status_extracted"].map(NORMALIZATION_MAP)

print("\n=== STATUS NORMALIZADOS ===\n")

final_status = df["status_normalized"].dropna().unique()

for s in sorted(final_status):
    print("-", s)

print(f"\nTotal de status finais: {len(final_status)}")

df.to_csv(OUTPUT_FILE, index=False)

print(f"\nArquivo normalizado salvo como: {OUTPUT_FILE}")