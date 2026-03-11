from fastapi import FastAPI
from pydantic import BaseModel

class Parameters(BaseModel):
    max_tokens: int
    temperature: float
    top_p: float
    
class Request(BaseModel):
    model: str
    prompt: str
    parameters: Parameters
    stream: bool
    request_id: str

app = FastAPI()

@app.post("/api/v1/infer/")
async def create_body(body: Request):
    return { "request_id": body.request_id, "status": "done" }

@app.get("/api/v1/infer/")
async def get_responce(id):
    return {
        "request_id": id,
        "model": "llama-3.2-1b",
        "output": "Kubernetes is a system that automates...",
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 87,
            "total_tokens": 96
        },
        "latency_ms": 340,
        "cached": False
    }
    
#Integrate with redis

