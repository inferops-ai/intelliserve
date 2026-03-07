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