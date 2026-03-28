import config
import torch
import numpy as np
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(config.MODEL_CHECKPOINT)
model = AutoModelForSequenceClassification.from_pretrained(config.MODEL_OUTPUT_DIR)

#switches model to inference mode, disable dropout
model.eval()

def classify_text(text):
    tokenize_text = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=config.MAX_LENGTH
    )
    
    #disables gradient computation during inference
    with torch.no_grad():
        logits = model(**tokenize_text).logits
    
    probs = F.softmax(logits, dim=-1)
    confidence = probs.max().item()
   
    #pick the highest scoring
    predict_classify = np.argmax(logits, axis=1)
    
    #the predict integer back to a readable intent string
    predict_output = config.ID_TO_LABEL[predict_classify.item()]
    
    return predict_output, confidence


    

