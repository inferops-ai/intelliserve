import os
import sys 
import types

os.environ["CHECK_READINESS"] = "/ready"
os.environ["CHECK_LIVENESS"] = "/live"


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "services", "api-gateway")))