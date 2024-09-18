from ezllmaw.lm.base_lm import BaseLM
from pydantic import Field
from typing import List
import requests
import numpy as np

def pack_request(url, payload, request, headers):
    payload.update(request)
    url = f"{url}/api/reranks"
    return {
        "url": url,
        "headers": headers,
        "json": payload
    }
    
class ReRanker(BaseLM):
    top_n:int = 3
    def __call__(self, query:str, docs:List[str]):
        return self.forward(query, docs)
    
    def forward(self, query:str, docs:List[str]):
        request = {"query": query, "docs": docs}
        payload = {}
        url = self.base_url
        request = pack_request(url=url, payload=payload, request=request, headers=self.headers)
        
        response = requests.post(**request)
        # response = requests.post(url=url, headers=self.headers, json=payload)
        response = response.json()
        try:
            return response["score"]
        except:
            raise ValueError(response)
    
    def sigmoid(self, z):
        if isinstance(z, list):
            z = np.array(z)
        return 1/(1 + np.exp(-z))
    
    def cutoff(self, docs:List[str], score:List[float]):
        docs_score = list(zip(docs, score))
        docs_score.sort(key=lambda x: x[1], reverse=True)
        return docs_score[:self.top_n]