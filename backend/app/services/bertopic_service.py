import requests
from app.config import Config

# Hugging Face API URL for your BERTopic model
API_URL = "https://api-inference.huggingface.co/models/JunLomerio/Thesis/trained-models/bertopic_model"

# Authorization headers with Hugging Face API token
headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_API_TOKEN}"}

def get_topics(embeddings):
    # Payload containing the input embeddings
    payload = {"inputs": embeddings}
    
    # Sending a POST request to the Hugging Face API
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Returning the topics from the JSON response
    return response.json()