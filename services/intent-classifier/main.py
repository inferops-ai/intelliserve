import asyncio
import os 
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from classifier import classify_text, model_ready

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
app = FastAPI()

class Request(BaseModel):
    prompt: str

@app.post(os.getenv("INTENT_PATH"))
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

@app.get(os.getenv("CHECK_READINESS"))
def check_ready():
    if model_ready:
        return {
            "status":"ok",
            "model":"distilbert-intent-classifier" 
        }
    else:
        raise HTTPException(status_code=503, detail="Model is not loaded yet")

@app.get(os.getenv("CHECK_LIVENESS"))
def check_health():
    return {
        "status":"ok",
        "model":"distilbert-intent-classifier"
    }