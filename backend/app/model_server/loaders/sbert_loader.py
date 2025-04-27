import os
from sentence_transformers import SentenceTransformer

def load_sbert_model():
    model_path = os.path.join('app', 'trained-models', 'sbert_model')
    model = SentenceTransformer(model_path)
    print("[DEBUG] Loading SBERT model from:", model_path)
    return model

def get_sbert_embedding(text):
    model = load_sbert_model()
    return model.encode(text).tolist()