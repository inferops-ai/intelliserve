import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from classifier import classify_text

app = FastAPI()

class Request(BaseModel):
    prompt: str

@app.post("/api/v1/intent")
async def get_classify(body: Request):
    prompt = body.prompt
    
    async_call = asyncio.get_running_loop()
    
    predict_output, confidence = await async_call.run_in_executor(
        None,
        classify_text,
        prompt
    )
    
    return {
        "intent": predict_output,
        "confidence": confidence
    }

@app.get("/health")
def check_health():
    return {
        "status":"ok",
        "model":"distilbert-intent-classifier"
    }