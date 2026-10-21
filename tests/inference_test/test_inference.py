import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ready():
    response = client.get(os.environ["CHECK_READINESS"])
    assert response.status_code == 200
    assert response.json() == { "status":"ok", "model":"Llama-inference-engine" }
    
def test_live():
    response = client.get(os.environ["CHECK_LIVENESS"])
    assert response.status_code == 200
    assert response.json() == { "status":"ok", "model":"Llama-inference-engine" }
    
def test_inference_model():
    response = client.post(os.environ["INFERENCE_PATH"], json={
        "model": "meta-llama/Llama-3.2-1B-Instruct",
        "prompt": "Write if/else statement in function using java ?",
        "intent_classifier": "code_generation",
        "parameters": {
            "max_tokens": 50,
            "temperature": 0.7,
            "top_p": 0.9
        }
    })
    assert response.status_code == 200
    assert response.json() == {
        "model": "meta-llama/Llama-3.2-1B-Instruct",
        "response": "test response",
        "usage": {
            "prompt_tokens": "10",
            "completion_tokens": "10",
            "total_tokens": "50"
        },
        "cached": False
    }
    
def test_inference_missing():
    response = client.post(os.environ["INFERENCE_PATH"], json={})
    assert response.status_code == 422
    