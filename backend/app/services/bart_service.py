import requests
from app.config import Config

API_URL = "https://api-inference.huggingface.co/models/JunLomerio/Thesis/trained-models/bart_model"
""" headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"} """

def summarize_text(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, """ headers=headers """, json=payload)
    return response.json()[0]['summary_text']