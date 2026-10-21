import os
import sys 
import types

os.environ["CHECK_READINESS"] = "/ready"
os.environ["CHECK_LIVENESS"] = "/live"
os.environ["REDIS_HOST"] = "127.0.0.1"
os.environ["REDIS_PORT"] = "6379"
os.environ["GATEWAY_PATH"] = "/api/v1/infer/"
os.environ["INTENT_ENDPOINT"] = "http://127.0.0.1:8001/api/v1/intent"
os.environ["INFERENCE_ENDPOINT"] = "http://127.0.0.1:8002/api/v1/inference"


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "services", "api-gateway")))