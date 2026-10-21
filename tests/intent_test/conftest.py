import os
import sys 
import types

os.environ["INTENT_PATH"] = "/api/v1/intent"
os.environ["CHECK_READINESS"] = "/ready"
os.environ["CHECK_LIVENESS"] = "/live"

def classifier_func(prompt):
    return "greeting", 0.9

fake_classifier = types.ModuleType("classifier")
fake_classifier.classify_text = classifier_func
fake_classifier.model_ready = True
sys.modules["classifier"] = fake_classifier

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "services", "intent-classifier")))
