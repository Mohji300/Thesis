import requests
from app.config import Config

API_URL = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"}

def get_entities(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()