# Loads model + tokenizer at startup
import os
from dotenv import load_dotenv
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

def inference_engine(model_engine, prompt, classifier_content, parameters):
    tokenzier = AutoTokenizer.from_pretrained(
        model_engine,
        token=os.getenv("HF_TOKEN")
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_engine,
        quantization_config=BitsAndBytesConfig(load_in_8bit=True),
        token=os.getenv("HF_TOKEN")
    )
    
    message = [
        {"role": "system", "content": classifier_content},
        {"role": "user", "content": prompt}
    ]

    inputs = tokenzier.apply_chat_template(
        message,
        add_generation_prompt=True,
        tokenzie=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    outputs = model.generate(
        **inputs, 
        max_new_tokens=parameters.max_tokens,
        temperature=parameters.temperature,
        top_p=parameters.top_p,
        do_sample=True  
    )
    response = tokenzier.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
    
    #Count prompt tokens
    prompt_tokens = inputs["input_ids"].shape[1]
    #Count completion tokens
    completion_tokens = outputs.shape[1] - prompt_tokens
    #Total
    total_tokens = outputs.shape[1]

    return response, prompt_tokens, completion_tokens, total_tokens

