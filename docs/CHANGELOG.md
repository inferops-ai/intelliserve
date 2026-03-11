# Changelog 

## 2026-03-06
- Initialied Github repository under inferops-ai/inteeliserve
- Created base folder structure: data/, docs/, helm/, k8s/, monitoring/, notebooks/, scripts/, services/ and tests/
- Added .gitignore, README.md, CHANGELOG.md

intelliserve/
│
├── README.md
├── .gitignore
|
│
├── services/                   # Three microservices
│   ├── api-gateway/                #Handle requests 
│   ├── intent-classifier/          #AI model
│   └── inference-engine/           #Loads and generates the responce
│
├── k8s/                        # Kubernetes manifests
│
├── helm/                       # Helm chart
│
├── monitoring/                 # Prometheus and Grafana
│
├── .github/
│   └── workflows/              # CI/CD pipelines
│
├── notebooks/                  # fine-tuning and experiments
│
├── data/                       # datasets and eval sets
│
├── docs/                       # architecture and decisions
│
├── scripts/                    # cluster and model helpers
│
└── tests/                      # unit, integration, load
- Create a project borad to track works using linear 

## 2026-03-07
- Create a virtual enviroment for the API, and understanding it 
    - Why we need virtual env ? It creates an isolated space for each project, preventing dependency conflict bwteen differernt projects and keeping operating system global python     installation clean. 
    - When used from within a virtual environment, common installation tools such as pip will install Python packages into a virtual environment without needing to be told to do so explicitly.
    Activate command- source .venv/bin/activate
    Deactivate command- deactivate 
    To check which virtual env is activated - echo $VIRTUAL_ENV
    Command to record all requiremnt packages in requiremnts.txt - pip freeze > requirements.txt 

## 2026-03-08
- Understanding FastAPI and why i need to use it 
    - FastAPI is a modern, fast web framework for building APIs with Python based standard python type hints. 
    - I will use FastAPI to handle all incoming requests, checks the redis catch, routes traffic to the classfier and inferenec engine, enforce rate limiting. 
    - Need radis catch to enforce rate limiting. (controlling every request that hits the inference engine)
    - Async await - Program says this operation will take a while fo handle something else while you wait then comeback when the result is ready. 

## 2026-03-11
- Keep reading FastAPI doc
- the request body looks like 
        {
        "model": "llama-3.2-1b", -----> Tells the gateway which inference pod/service to route to 
        "prompt": "Explain Kubernetes in simple terms", --------> User prompt to the model
        "parameters": { ---------->Generation setting passed down to the model 
            "max_tokens": 512,----------->The model will not generate more than 512 tokens in its responce 
            "temperature": 0.7, -------------->Randomness of words, distribution of what word comes next
            "top_p": 0.9   -------------> Instead of considering all possible next words, the model only considers the smallest set of words whose combined probability adds up to 90%. Everything outside that       ---------------------------->Everything outside that "nucleus" is ignored
        },
        "stream": false,    ------------>whether to use streaming (SSE) or wait for full response
        "request_id": "req-abc123" ------------>useful for tracing and logging across services
        }
    - temperature (Low (e.g. 0.1) → the model almost always picks the highest-probability word. Outputs are deterministic and repetitive.
                    High (e.g. 1.5) → the model picks more "surprising" words. Outputs are creative but can go off the rails.
                    0.7 is a middle ground — coherent but not robotic.)
    = top_p (op_p: 1.0 → consider all words (no filtering)
            top_p: 0.9 → only consider the top 90% probability mass
            top_p: 0.5 → very conservative, only the most likely words)
- responce body looks like after get request
        {
            "request_id": "req-abc123",
            "model": "llama-3.2-1b",
            "output": "Kubernetes is a system that automates...",
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 87,
                "total_tokens": 96
            },
            "latency_ms": 340,
            "cached": false
        }
- The flow 
Client          Gateway           Model           Redis
  |                |                |               |
  |--- POST ------>|                |               |
  |                |---- infer ---->|               |
  |                |<--- result ----|               |
  |                |--- SET id:xyz = result ------->|
  |<-- { id: xyz } |                |               |
  |                |                |               |
  |--- GET /xyz -->|                |               |
  |                |--- GET id:xyz --------------->|
  |                |<-- result --------------------|
  |<-- result -----|
- The post need to be checked in Redis catche before it runs in the model if its in redis return the id and do get request using the id to get the responce 
- to run the api getway I used uvicorn 
    command - uvicorn main:app or fastapi dev
- endpoints for POST: /api/v1/infer
- endpoint for GET: /api/v1/infer/request_id