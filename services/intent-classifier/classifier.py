import config
import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(config.MODEL_CHECKPOINT)
model = AutoModelForSequenceClassification.from_pretrained(config.MODEL_OUTPUT_DIR)
model.eval()

def classify_text(text):
    tokenize_text = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=config.MAX_LENGTH
    )
    
    #don't track the weight, not training the model
    with torch.no_grad():
        logits = model(**tokenize_text).logits
    
    predict_classify = np.argmax(logits, axis=1)
    
    return config.ID_TO_LABEL[predict_classify.item()]

example_text = ["Can you turn this paragraph into a shorter version?",
                "Build me a function that reverses a string in Java",
                "Convert this to Spanish please",
                "What does gradient descent mean?",
                "What's up man?"]

for i in example_text:
    print(classify_text(i))
    

