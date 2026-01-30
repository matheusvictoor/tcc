import os
import json
from time import sleep
import pandas as pd
from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextGenParameters

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL_WATSONX = os.getenv("URL_WATSONX")
PROJECT_ID  = os.getenv("PROJECT_ID")

TEST_MODE = False # alterar para False para rodar nas 300
N_TEST = 5 # numero de adrs no modo de teste
MAX_RETRIES = 3 # tentativas em caso de falha

adrs = []
with open("sample_300.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        adrs.append(json.loads(line))

manual = pd.read_csv("manual_annotation_300.csv")

if TEST_MODE:
    adrs = adrs[:N_TEST]
    manual = manual.iloc[:N_TEST].reset_index(drop=True)
    print(f"[MODO TESTE] Executando apenas nas primeiras {N_TEST} ADRs.")

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=Credentials(
        api_key=API_KEY,
        url=URL_WATSONX,
        version="5.3"
    ),
    project_id=PROJECT_ID,
    params=TextGenParameters(
        temperature=0.0,
        max_new_tokens=100,
        stop_sequences=["\n"]
    )
)

BASE_PROMPT = """You are an experienced software architect analyzing Architecture Decision Records (ADRs). Each ADR documents one or more architectural decisions.

Below is the content of an ADR:

---
{content}
---

I have defined the following architectural topics:

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

Your task:
- Assign **all topics** from the list above that apply to this ADR.
- You may select **one or more** topics.
- If the ADR clearly fits none of these, propose **one new topic** in snake_case (short and architectural).
- Do **not** include explanations, numbers, or extra text.

Respond **only** with a comma-separated list of topic names in snake_case.

Example response:  
data_persistence, performance_and_scalability"""

results = []
for i, adr in enumerate(adrs):
    adr_id = f"ADR_{i+1:03d}"
    prompt = BASE_PROMPT.replace("{content}", adr["content"])

    response = "ERROR"
    for attempt in range(MAX_RETRIES):
        try:
            raw_resp = model.generate_text(prompt=prompt).strip()
            response = raw_resp.split("\n")[0].strip()
            response = response.lstrip(", \t").rstrip(", \t")
            # if not response:
            #     response = "others"
            break
        except Exception as e:
            print(f"[{adr_id}] Tentativa {attempt+1} falhou: {str(e)[:80]}")
            if attempt == MAX_RETRIES - 1:
                response = "ERROR"
            else:
                sleep(2 ** attempt)
        
    results.append({
        "id": adr_id,
        "content": adr["content"][:100].replace("\n", " "),
        "my_topic": manual.loc[i, "my_topic"],
        "llm_topic": response
    })
    print(f"ADR_{i+1:03d} → LLM: {response}")

output_file = "llm_classification_test.csv" if TEST_MODE else "llm_classification_300.csv"
df = pd.DataFrame(results)
df.to_csv(output_file, index=False)
print(f"\nResultados salvos em: {output_file}")