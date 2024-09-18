from ezllmaw.lm.base_lm import BaseLM
from pydantic import Field
import requests

def pack_request(url, payload, request, headers, endpoint="ollama"):
    payload.update({"prompt": request})
    if endpoint=="ollama":
        url = f"{url}/api/generate"
    else:
        raise ValueError(f"endpoint {endpoint} is not implemented yet.")
    return {
        "url": url,
        "headers": headers,
        "json": payload
    }


class OllamaGenLM(BaseLM):
    """
    Ref1: https://dev.to/jayantaadhikary/using-the-ollama-api-to-run-llms-and-generate-responses-locally-18b7
    
    Ref2: https://medium.com/@shmilysyg/setup-rest-api-service-of-ai-by-using-local-llms-with-ollama-eb4b62c13b71

    Ref3: https://github.com/ollama/ollama/blob/main/docs/api.md
    """
    base_url:str = Field(default="http://localhost:11434", description="api url")
    model:str = Field(default="llama3.1:latest", description="model name")

    def __call__(self, request):
        return self.forward(request)
    
    def forward(self, request):
        payload = {
            "model": self.model,
            "stream": self.stream,
            "options": {
                "temperature": self.temperature
            },
        }
        url = self.base_url
        request = pack_request(url=url, payload=payload, request=request, headers=self.headers)
        
        response = requests.post(**request)
        # response = requests.post(url=url, headers=self.headers, json=payload)
        response = response.json()
        try:
            return response["response"]
        except:
            raise ValueError(response)