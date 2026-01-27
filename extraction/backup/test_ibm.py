from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextGenParameters

class IBMCloudLLM:
    def __init__(self, model_id: str, api_key: str, service_url: str, project_id: str, max_new_tokens: int = 512):
        self.model_name = model_id.split('/')[1] if '/' in model_id else model_id
        self.model = ModelInference(
            model_id=model_id,
            credentials=Credentials(
            api_key=api_key,
            url=service_url
        ),
            project_id=project_id,
            params=TextGenParameters(max_new_tokens=max_new_tokens)
        )

    def generate(self, prompt: str) -> str:
        response = self.model.generate_text(prompt=prompt)
        return response