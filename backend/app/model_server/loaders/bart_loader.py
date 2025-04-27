import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def load_bart_model():
    model_path = os.path.join('app', 'trained-models', 'bart_model')
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    print("[DEBUG] Loading BART model from:", model_path)
    return tokenizer, model

def summarize_text(text, max_length=150):
    tokenizer, model = load_bart_model()
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs['input_ids'], max_length=max_length, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
