import os
import json
import re
from time import sleep
import pandas as pd
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TEST_MODE = False
N_TEST = 5
MAX_RETRIES = 3
OUTPUT_FILE = "dataset_llm_classified_test.csv" if TEST_MODE else "dataset_llm_classified.csv"

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "ADR Topic Classification TCC"
    }
)

adrs = []
with open("dataset.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        adrs.append(json.loads(line))

if TEST_MODE:
    adrs = adrs[:N_TEST]
    print(f"[MODO TESTE] Executando apenas nas primeiras {N_TEST} ADRs.")

BASE_PROMPT = """You are an experienced software architect analyzing Architecture Decision Records (ADRs).

An ADR documents one or more architectural decisions that have significant impact on a software project.
Your task is to classify the ADR based on its **central architectural decision**, not merely on technologies or terms mentioned.

Important guidelines:
- Focus on the **main decision being made**, the problem it addresses, and its consequences.
- Technologies mentioned only as means or supporting elements should NOT determine the classification.
- Do NOT rely on keyword matching; interpret the meaning of the text.
- An ADR may belong to more than one topic if multiple architectural decisions are central.
- If none of the predefined topics apply, propose ONE new topic in snake_case.

Predefined architectural topics:
1. data_persistence
2. technology_choice
3. microservices_and_modularity
4. api_and_contracts
5. infrastructure_and_deployment
6. observability
7. security
8. testing_strategy
9. architecture_patterns
10. performance_and_scalability
11. governance_and_process
12. others

Few-shot examples:

Example 1:
ADR summary:
The project needs to expose services to external partners. Several authentication mechanisms are discussed (API Keys, OAuth2, mTLS).
OAuth2 is selected to standardize access and ease third-party integration.
Consequences include changes to API contracts and onboarding processes.

Correct classification:
api_and_contracts, security

Example 2:
ADR summary:
The system faces scalability issues due to tight coupling between components.
The architecture is restructured into independently deployable services.
Technologies such as Docker and Kubernetes are mentioned as enablers.

Correct classification:
microservices_and_modularity

Now analyze the following ADR:

---
{content}
---

Your task:
- Assign ALL applicable topics from the predefined list.
- You may select ONE or MORE topics.
- If none apply, propose ONE new topic in snake_case.
- Do NOT include explanations, numbering, or extra text.

Respond ONLY with a comma-separated list of topic names in snake_case.

Example response:
data_persistence, performance_and_scalability
"""

processed_ids = set()
results = []

if os.path.exists(OUTPUT_FILE):
    df_existing = pd.read_csv(OUTPUT_FILE)
    results = df_existing.to_dict("records")
    processed_ids = set(df_existing["adr_id"].astype(str))
    print(f"[CHECKPOINT] {len(processed_ids)} ADRs ja processada. Continuando...")
else:
    print("[CHECKPOINT] Nenhum resultado anterior encontrado. Iniciando do zero.")

for i, adr in enumerate(adrs):
    adr_id = adr.get("id", f"ADR_{i+1:05d}")

    if adr_id in processed_ids:
        continue

    prompt = BASE_PROMPT.replace("{content}", adr["content"])

    response = "ERROR"

    for attempt in range(MAX_RETRIES):
        try:
            completion = client.chat.completions.create(
                model="anthropic/claude-opus-4.5",
                messages=[
                    {"role": "system", "content": "You are a precise text classification system."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=50
            )

            raw_resp = completion.choices[0].message.content.strip()

            response = raw_resp.split("\n")[0].strip()
            response = response.lstrip(", \t").rstrip(", \t")
            response = response.lower()

            if not response:
                response = "others"

            break

        except Exception as e:
            msg = str(e).lower()

            print(f"[{adr_id}] Tentativa {attempt+1} falhou: {str(e)[:80]}")

            if "limit exceeded" in msg or "quota" in msg:
                print("Quota excedida. Salvando progresso e encerrando.")
                raise SystemExit
            
            if attempt == MAX_RETRIES - 1:
                response = "ERROR"
            else:
                sleep(3 ** attempt)

    results.append({
        "adr_id": adr_id,
        "repositoryUrl": adr["repositoryUrl"],
        "path": adr["path"],
        "title": adr.get("title"),
        "wordCount": adr.get("wordCount"),
        "status": adr.get("status"),
        "llm_topic": response,
        "content_preview": re.sub(r"\s+", " ", adr["content"][:80])
    })

    df_partial = pd.DataFrame(results)
    df_partial.to_csv(OUTPUT_FILE, index=False)

    print(f"{adr_id} → GPT: {response}")

print(f"\nResultados salvos em: {OUTPUT_FILE}")
