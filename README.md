# Intelliserve
IntelliServe is a self-hosted AI inference platform built on Kubernetes, designed to serve quantized LLMs (LLaMA 3.2 / Mistral 7B) with production-grade reliability. Built from scratch to explore the full stack of modern AI infrastructure — from model serving and LoRA fine-tuning to autoscaling, observability, and cloud deployment.
User request
    → API Gateway
        → Intent Classifier (DistilBERT) → "this is a summarize request"
            → Inference Engine (LLaMA/Mistral) → actual generated response
                → back to user
