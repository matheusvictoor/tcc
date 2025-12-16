import json
import random
import csv
from pathlib import Path

# Configurações
INPUT_FILE = "../extraction/dataset.jsonl"
OUTPUT_SAMPLE = "sample_300.jsonl"
OUTPUT_CSV = "manual_annotation_300.csv"
SAMPLE_SIZE = 300

def main():
    # Ler todas as ADRs
    adrs = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    adrs.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar linha: {e}")
    
    print(f"Total de ADRs carregadas: {len(adrs)}")
    
    if len(adrs) < SAMPLE_SIZE:
        raise ValueError(f"Dataset tem apenas {len(adrs)} ADRs, mas você pediu {SAMPLE_SIZE}.")
    
    # seleciona amostra aleatória
    random.seed(42)
    sample = random.sample(adrs, SAMPLE_SIZE)
    
    # salva amostra em JSONL
    with open(OUTPUT_SAMPLE, "w", encoding="utf-8") as f:
        for adr in sample:
            f.write(json.dumps(adr, ensure_ascii=False) + "\n")
    
    print(f"Amostra de {SAMPLE_SIZE} ADRs salva em: {OUTPUT_SAMPLE}")
    
    # cria CSV para anotação manual
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "repositoryUrl", "path", "title", "content_snippet", "topic_human", "notes"])
        for i, adr in enumerate(sample):
            # gera ID único (índice ou hash)
            adr_id = f"ADR_{i+1:03d}"

            repo = adr.get("repositoryUrl", "").rstrip("/")
            path = adr.get("path", "").lstrip("/")
            title = adr.get("title", "")
            content = adr.get("content", "")
            snippet = content[:500].replace("\n", " ").replace("\r", " ")
            writer.writerow([adr_id, repo, path, title, snippet, "", ""])
    
    print(f"Planilha para anotação manual criada: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()