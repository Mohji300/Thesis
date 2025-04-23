import requests
from app.config import Config

# Hugging Face API URL for your SBERT model
API_URL = "https://api-inference.huggingface.co/models/JunLomerio/Thesis/trained-models/sbert_model"

# Authorization headers with Hugging Face API token
headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"}

def get_embedding(text):
    # Payload containing the input text
    payload = {"inputs": text}
    
    # Sending a POST request to the Hugging Face API
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Returning the embedding from the JSON response
    return response.json()