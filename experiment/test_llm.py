import os
from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextGenParameters

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL_WATSONX = os.getenv("URL_WATSONX")
PROJECT_ID  = os.getenv("PROJECT_ID")

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

BASE_PROMPT = """Escreva uma musica de quatro estrofes"""

try:
    response = model.generate_text(prompt=BASE_PROMPT).strip()
    response = response.split("\n")[0].strip()
    print(f"Resposta -> {response}")


except Exception as e:
    print(f"Falhou: {str(e)}")
