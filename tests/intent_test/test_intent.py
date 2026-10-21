import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ready():
    response = client.get(os.environ["CHECK_READINESS"])
    assert response.status_code == 200
    assert response.json() == { "status":"ok", "model":"distilbert-intent-classifier" }
    
def test_live():
    response = client.get(os.environ["CHECK_LIVENESS"])
    assert response.status_code == 200
    assert response.json() == { "status":"ok", "model":"distilbert-intent-classifier" }
    
def test_classify_model():
    response = client.post(os.environ["INTENT_PATH"], json={"prompt": "test classifier"})
    assert response.status_code == 200
    assert response.json() == { "intent": "greeting", "confidence": 0.9 }

def test_classify_missing():
    response = client.post(os.environ["INTENT_PATH"], json={})
    assert response.status_code == 422