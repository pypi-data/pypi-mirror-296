from ezllmaw.lm.base_lm import BaseLM
from pydantic import Field
import requests
from typing import List

def pack_request(url, payload, request, headers, endpoint="ollama"):
    payload.update({"input": request})
    if endpoint=="ollama":
        url = f"{url}/api/embed"
    else:
        raise ValueError(f"endpoint {endpoint} is not implemented yet.")
    return {
        "url": url,
        "headers": headers,
        "json": payload
    }
    
class OllamaEmbeddings(BaseLM):
    base_url:str = Field(default="http://localhost:11434", description="api url")
    model:str = Field(default="mxbai-embed-large:latest", description="model name")
    
    def __call__(self, request):
        return self.forward(request)
    
    def forward(self, request):
        payload = {
            "model": self.model,
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
            return response["embeddings"]
        except:
            raise ValueError(response)
