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
|       ├── data/                       # datasets and eval sets
│
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
|
├── docs/                       # architecture and decisions
│
├── scripts/                    # cluster and model helpers
│
└── tests/                      # unit, integration, load
- Create a project borad to track works using linear 

## 2026-03-07
- Create a virtual enviroment for the API, and understanding it 
    - Why we need virtual env ? It creates an isolated space for each project, preventing dependency conflict bewteen differernt projects and keeping operating system global python     installation clean. 
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

## 2026-03-12
Redis catche 

Cache 1 — Async Result Store
Keyed by request_id. Created when a job is dispatched, read during polling.
Fields:
status — pending, processing, completed, or failed
response — the inference output
model — which model handled it
created_at — when the request arrived
completed_at — when inference finished
error — populated only on failure

Cache 2 — Prompt Deduplication Store
Keyed by a SHA-256 hash of the prompt. Checked before dispatching any job.
Fields:
request_id — pointer to the full result in Cache 1
model — which model produced it

If there's a hit, the gateway returns the cached response immediately and never touches the inference engine.

The combined flow:

The corrected flow on a cache hit:

Request arrives with a prompt
Gateway hashes the prompt → checks Cache 2
Hit → retrieve request_id from Cache 2 → use it to fetch the full result from Cache 1 → return response to client
Miss → generate new request_id, dispatch to inference engine, write result to Cache 1, write prompt_hash → request_id to Cache 2

Both caches live in the same Redis instance, just under different key patterns — something like infer:{request_id} for Cache 1 and prompt:{sha256hash} for Cache 2. And both should have a TTL set via expire after writing.

## 2026-03-17 
Containerize the the api-gateway using DOCKER
To create a dockerfile, needed to create a Dockerfile inside the app directory
FROM - Defines the base image to start the build process from
WORKDIR - Create a working directory inside the docker image file system
COPY - Copy files or directories from the host machine in to image file system
RUN - Run command, typically for creating a package or updating a script
CMD - Default command to run when the container starts 

Docker Cli -    docker build -t app-gateway . (To build the container)
           -    docker run --env-file .env -p 8000:80 app-gateway (Run the container and map the localhost 8000 port with 80 conatiner port and use .env file from local and inject the values at runtime)

---> When you run a Docker container, it's like a mini isolated computer inside your real computer. It has its own network, its own filesystem, its own localhost.
So when your gateway code says "connect to localhost:6379", it means "connect to port 6379 on this container's localhost" — not your actual machine's localhost where Redis is running.
It's like two separate houses. Shouting "come to my living room" from house A doesn't bring someone from house B — they're in different buildings.
The three scenarios:

Before Docker — everything ran on your actual machine, so localhost meant the same thing to everyone. Gateway and Redis were in the same "house."
Gateway in Docker, Redis on host — they're in different "houses." host.docker.internal is essentially a bridge between them, a special address that means "go back to the real machine."
Both in Docker Compose — they're in the same "neighbourhood" with a shared internal network. Each service gets a name, and they find each other by that name instead of localhost. This is the cleanest setup.

That's fundamentally the networking problem Docker Compose solves — it puts all your services on the same internal network so they can talk to each other naturally.

To solve this problem we need dockercompose 
Docker Compose - Used to make a communication between two containers 
               - It protect us writing repetative docker-cli command multiple times
               - Easly startup multiple container at the same time and connect them together 
               - docker-compose.yaml to create docker compose file 
    docker-compose.yaml --> services - are the containers we need to create and run
        compose command - docker-compose up --build -> to build an image and run it 
                        - docker-compose up -> to run the container

## 2026-03-19
Research: Transformers, Fine-tuning, and DistilBERT for Intent Classifier
Transformers - Attention, instade of reading the text sequentially, it looks all the words at once and asks: "For each word in this sentence, which other words should I pay attention to in order to understand it?"
Multi-head attention runs this process in parallel several times. 
BERT - Bidirectional Encoder Representations from Transformers - Reads in both directions simultaneously.
BERT Learned from massive text using two self-supervised tasks
    - Masked language modeling 
    - Next sentence prediction
After pre-training, BERT has rich, general-purpose language representations baked into its weights. You then fine-tune it on your specific task by adding a small task-specific head on top and training on your labeled data.

## 2026-03-24
How DistlBERT works 
Your text:   "Book me a flight"
     ↓
Tokenizer:   [CLS] book me a flight [SEP]  →  [101, 2338, 2033, 1037, 3462, 102]
     ↓
DistilBERT:  Every token talks to every other token
     ↓
[CLS] output: A summary of the whole sentence (768 numbers)
     ↓
Classifier:  "This is a book_flight intent" ✅

Tokenization - Coverts texts into numerical format so the model can process
[CLS] - The model learns to use as a summary token 

Created a file in intent-classfier microservice 
1. config.py — Start here, no dependencies
Define your label mappings, model checkpoint, num_labels, max_length, and output path. Everything else imports from this file so it needs to exist first.
2. dataset.py — Maps to INT-28
Write your tokenization logic and data loading here. It imports the tokenizer config from config.py. Use a small toy dataset at this stage — real intent data comes later.
3. train.py — Maps to INT-27, INT-29, INT-30
This is the bulk of your current tickets. It imports from both config.py and dataset.py. By the end of INT-30 you'll have a fine-tuned model saved to disk.
4. classifier.py — After training is done
Loads the saved fine-tuned model and exposes a classify(text) function. You can't write this meaningfully until train.py has produced a model checkpoint.
5. app.py — Last
The FastAPI layer that wraps classifier.py and exposes the /classify endpoint. This is the final step before wiring the microservice into IntelliServe.

Created a dataset
240 examples — 40 per class: 6 labels 
-------------------------------------------------------------------------------------------------
text_generation     |  Wide variety — stories, poems, emails, speeches, slogans, reviews
summarization       |  Covers papers, meetings, transcripts, books, legal docs, reports
question_answering  |  Mix of factual, conceptual, and technical questions
code_generation     |  Multiple languages — Python, SQL, JS, Bash, YAML, Terraform, Rust
translation         |  15+ language pairs, different document types and formality levels
chitchat            |  Natural conversational tone — emotional, curious, playful, philosophical
--------------------------------------------------------------------------------------------------

## 2026-03-26
