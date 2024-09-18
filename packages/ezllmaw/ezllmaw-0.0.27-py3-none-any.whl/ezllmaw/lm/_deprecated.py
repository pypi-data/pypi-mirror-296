from pydantic import Field, BaseModel
import requests

headers={
    "Content-Type": "application/json",
    }

def pack_gen(url, payload, request, endpoint="ollama"):
    payload.update({"prompt": request})
    if endpoint=="ollama":
        url = f"{url}/api/generate"
    if endpoint=="groq":
        ...
    return url, payload

def pack_em(url, payload, request):
    payload.update({"input": request})
    url = f"{url}/api/embed"
    return url, payload

def pack_chat(url, payload, request, endpoint="ollama"):
    """\
    "messages": [
        {
            "role": "user",
            "content": "why is the sky blue?"
        },
        {
            "role": "assistant",
            "content": "due to rayleigh scattering."
        },
        {
            "role": "user",
            "content": "how is that different than mie scattering?"
        }
    ]
    """
    payload.update({"messages": request})
    if endpoint=="ollama":
        url = f"{url}/api/chat"
    if endpoint=="groq":
        url = f"{url}/chat/completions"
    return url, payload



class OllamaLLM(BaseModel):
    """
    Ref1: https://dev.to/jayantaadhikary/using-the-ollama-api-to-run-llms-and-generate-responses-locally-18b7
    
    Ref2: https://medium.com/@shmilysyg/setup-rest-api-service-of-ai-by-using-local-llms-with-ollama-eb4b62c13b71

    Ref3: https://github.com/ollama/ollama/blob/main/docs/api.md
    """
    base_url:str = Field(default="http://localhost:11434", description="api url")
    model:str = Field(default="llama3.1", description="model name")
    stream:bool = Field(default=False)
    temperature:float = Field(default=0)
    type:str = Field(default="gen", description="gen, chat, embeddings")
    end_point:str = Field(default="ollama", description="api endpoint")

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
        if self.type=="gen":
            url, payload= pack_gen(url=url, payload=payload, request=request)
        elif self.type=="embeddings":
            url, payload= pack_em(url=url, payload=payload, request=request)
        elif self.type=="chat":
            url, payload= pack_chat(url=url, payload=payload, request=request)
        else:
            raise ValueError("Other type of models are not implmented yet.")
        
        response = requests.post(url=url, headers=headers, json=payload)
        response = response.json()
        
        if self.type=="gen":
            return response["response"] 
        elif self.type=="embeddings":
            return response["embeddings"]
        elif self.type=="chat":
            return response["message"]
        else:
            raise ValueError("Other type of models are not implmented yet.")
        
class GroqLLM(BaseModel):
    base_url:str = Field(default="https://api.groq.com/openai/v1", description="api url")
    model:str = Field(default="llama-3.1-8b-instant", description="model name")
    stream:bool = Field(default=False)
    temperature:float = Field(default=0)
    type:str = Field(default="chat", description="chat")
    end_point:str = Field(default="groq", description="API endpoint")
    api_key:str = Field(..., description="api key")

    def __call__(self, request):
        return self.forward(request)
    
    def forward(self, request):
        headers.update({"Authorization": f"Bearer {self.api_key}"})
        payload = {
            "model": self.model,
            "stream": self.stream,
            "temperature": self.temperature,
        }
        url = self.base_url
        if self.type=="chat":
            url, payload= pack_chat(url=url, payload=payload, request=request, endpoint=self.end_point)
        else:
            raise ValueError("Other type of models are not implmented yet.")
        
        response = requests.post(url=url, headers=headers, json=payload)
        response = response.json()
        # print(response)
        

        if self.type=="chat":
            try:
                message =  response["choices"][0]["message"]
                return message
            except:
                raise ValueError(response)
        else:
            raise ValueError("Other type of models are not implmented yet.")