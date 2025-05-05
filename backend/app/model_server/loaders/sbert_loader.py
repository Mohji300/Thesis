import os
import logging
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the SBERT model once when the module is loaded
_sbert_model = None

def load_sbert_model():
    global _sbert_model
    if _sbert_model is None:
        model_path = os.path.join('app', 'trained-models', 'sbert_model')
        print("[DEBUG] Loading SBERT model from:", model_path)
        try:
            _sbert_model = SentenceTransformer(model_path)
            logging.debug("[DEBUG] SBERT model loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading SBERT model: {e}")
            raise
    return _sbert_model

def get_sbert_embedding(text):
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")

        sbert_model = load_sbert_model()

        # Encode to NumPy array
        embedding = sbert_model.encode(text, convert_to_numpy=True)
        embedding = np.array(embedding)

        # Ensure 2D shape: (1, embedding_dim)
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        if not isinstance(embedding, np.ndarray):
            raise TypeError("get_sbert_embedding did not return a NumPy array.")

        logging.debug(f"[DEBUG] Embedding shape: {embedding.shape}, dtype: {embedding.dtype}")
        return embedding

    except Exception as e:
        logging.error(f"Error getting embedding: {e}")
        raise


