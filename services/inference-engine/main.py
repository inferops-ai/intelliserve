# FastAPI app, lifespan, + all routes
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from model_loader import inference_engine
from inference import inference_template

app = FastAPI()

class Parameters(BaseModel):
    max_tokens: int
    temperature: float
    top_p: float

class Request(BaseModel):
    model: str
    prompt: str
    intent_classifier: str
    parameters: Parameters

@app.post("/api/v1/inference")
async def get_responce(body: Request):
    model_engine = body.model
    prompt = body.prompt
    intent_classifier = body.intent_classifier
    parameters = body.parameters
    
    #Need interface to change the prompt based on the classfication 
    classifier_content = inference_template[intent_classifier]
    
    async_call = asyncio.get_running_loop()
    
    response, prompt_tokens, completion_tokens, total_tokens = await async_call.run_in_executor(
        None,
        inference_engine,
        model_engine, 
        prompt,
        classifier_content,
        parameters
    )
    
    return {
        "model": model_engine,
        "response": response,
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        },
        "cached": False
    }

@app.get("/health")
def check_health():
    return {
        "status":"ok",
        "model":"Llama-inference-engine"
    }