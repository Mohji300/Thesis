import os
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

def load_ner_model():
    model_dir = os.path.abspath(os.path.join('app', 'trained-models', '4ner_model'))
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only =True)
    model = AutoModelForTokenClassification.from_pretrained(model_dir, local_files_only =True)
    print("[DEBUG] Loading NER model from:", model_dir)
    return tokenizer, model

def extract_entities(text):
    tokenizer, model = load_ner_model()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs).logits
    predictions = torch.argmax(outputs, dim=2)

    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    labels = predictions[0].tolist()

    entities = []
    for token, label_id in zip(tokens, labels):
        if label_id != 0:  # 0 = 'O' (no entity)
            entities.append((token, label_id))
    return entities
