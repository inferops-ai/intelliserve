import uuid
import hashlib
import os
import httpx
import time
from dotenv import load_dotenv
import redis.asyncio as redis
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
app = FastAPI()
#Connect with redis
client_redis = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), decode_responses=True)

#Remove spaces and lowercase the string 
def normaliz_str(str_val):
    lower_str = str_val.lower().strip()
    arr, val = [], ''
    for i in lower_str:
        if i == ' ' and val != '':
            arr.append(val)
            val = ''
        else:
            if i != ' ':
                val += i
    if val != '':
        arr.append(val)
    return ' '.join(arr)

class Parameters(BaseModel):
    max_tokens: int
    temperature: float
    top_p: float
    
class Request(BaseModel):
    model: str
    prompt: str
    parameters: Parameters
    stream: bool

@app.post("/api/v1/infer/")
async def create_body(body: Request):
    #Create a unique id for the request id 
    uuid_id = uuid.uuid4()
    #hashing the prompt
    prompt = body.prompt
    hashed_prompt = hashlib.sha256(normaliz_str(prompt).encode()).hexdigest()
    
    # check the prompt hash exist in the redis in catche 2 
    check_cache = await client_redis.hgetall(f'prompt:{hashed_prompt}')
    
    #if exist return the request id,else if not add new cache 1 and cache 2 with responce and return the request id 
    if len(check_cache):
        return { "request_id":check_cache['request_id'], "status":"done"}
    else:
        start_time = time.time()
        #Call the intent classifier endpoint to get the intent 
        async with httpx.AsyncClient() as client:
            intent_responce = await client.post(os.getenv("INTENT_ENDPOINT"), json={"prompt":prompt})
        intent_responce = intent_responce.json()
    
        async with httpx.AsyncClient(timeout=300.0) as client:
            inference_responce = await client.post(os.getenv("INFERENCE_ENDPOINT"), json={
                "model": body.model,
                "prompt": body.prompt,
                "intent_classifier": intent_responce['intent'],
                "parameters":{
                    "max_tokens": body.parameters.max_tokens,
                    "temperature": body.parameters.temperature,
                    "top_p": body.parameters.top_p
                }
            })
        inference_responce = inference_responce.json()
        end_time = time.time()
            
        await client_redis.hset(f'infer:{str(uuid_id)}',mapping={
            'status': 'completed',
            'prompt': prompt,
            'response': inference_responce['response'],
            'intent': intent_responce['intent'],
            'confidence': intent_responce['confidence'],
            'model': body.model,
            "prompt_tokens": inference_responce['usage']['prompt_tokens'],
            "completion_tokens": inference_responce['usage']['completion_tokens'],
            "total_tokens": inference_responce['usage']['total_tokens'],
            'created_at': start_time,
            'completed_at': end_time,
            'error': 'error'
        })
        await client_redis.expire(f'infer:{str(uuid_id)}', 1200)
        await client_redis.hset(f'prompt:{hashed_prompt}', mapping={
            'request_id': str(uuid_id)
        })
        await client_redis.expire(f'prompt:{hashed_prompt}', 900)
    return {"request_id": str(uuid_id), "status":"done"}

@app.get("/api/v1/infer/")
async def get_responce(id):
    client_responce = await client_redis.hgetall(f'infer:{id}')
    return {
        "request_id": id,
        "model": client_responce['model'],
        "output": client_responce['response'],
        "usage": {
            "prompt_tokens": client_responce['prompt_tokens'],
            "completion_tokens": client_responce['completion_tokens'],
            "total_tokens": client_responce['total_tokens']
        },
        "latency_ms": round((float(client_responce['completed_at'])-float(client_responce['created_at'])) * 1000, 2),
        "cached": True,
    }
    
#for kuberentes to check the app is running 
@app.get("/health")
def check_health():
    return {
        "status": "ok"
    }
    


