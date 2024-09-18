from pydantic import Field, BaseModel

class BaseLM(BaseModel):
    """
    Ref1: https://dev.to/jayantaadhikary/using-the-ollama-api-to-run-llms-and-generate-responses-locally-18b7
    
    Ref2: https://medium.com/@shmilysyg/setup-rest-api-service-of-ai-by-using-local-llms-with-ollama-eb4b62c13b71

    Ref3: https://github.com/ollama/ollama/blob/main/docs/api.md
    """
    base_url:str = Field(default="http://localhost:11434", description="api url")
    model:str = Field(default="llama3.1:latest", description="model name")
    stream:bool = Field(default=False)
    temperature:float = Field(default=0)
    headers:dict = Field(default={"Content-Type": "application/json"})
    end_point:str = Field(default="ollama", description="api endpoint")

    def __call__(self, request):
        return self.forward(request)
    
    def forward(self, request):
        pass