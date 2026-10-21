import os
import sys 
import types

os.environ["CHECK_READINESS"] = "/ready"
os.environ["CHECK_LIVENESS"] = "/live"
os.environ["INFERENCE_PATH"] = "/api/v1/inference"

def inference_func(model_engine,prompt, classifier_content, parameters):
    return "test response", "10", "10", "50"

fake_inference = types.ModuleType("model_loader")
fake_inference.inference_engine = inference_func
fake_inference.model_ready = True
sys.modules["model_loader"] = fake_inference

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "services", "inference-engine")))