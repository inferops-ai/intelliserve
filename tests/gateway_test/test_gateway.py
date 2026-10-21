import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ready():
    response = client.get(os.environ["CHECK_READINESS"])
    assert response.status_code == 200
    assert response.json() == { "status":"ok" }
    
def test_live():
    response = client.get(os.environ["CHECK_LIVENESS"])
    assert response.status_code == 200
    assert response.json() == { "status":"ok" }