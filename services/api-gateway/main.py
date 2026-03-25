import uuid
import hashlib
import os
from dotenv import load_dotenv
import redis.asyncio as redis
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

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

app = FastAPI()

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
        await client_redis.hset(f'infer:{str(uuid_id)}',mapping={
            'status': 'completed',
            'responce': 'Kubernetes is a system that automates...',
            'model': body.model,
            'created_at': 'When the request created',
            'completed_at': 'When the request is completed',
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
        "output": client_responce['responce'],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 87,
            "total_tokens": 96
        },
        "latency_ms": 340,
        "cached": True
    }
    


