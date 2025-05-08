from app.utils.embedder import SBERTEmbedder
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get the SBERTEmbedder instance (Singleton)
embedder = SBERTEmbedder()


def get_sbert_embedding(text):
    """
    Generates an SBERT embedding for the given text.

    Args:
        text (str): The text to embed.

    Returns:
        np.ndarray: The embedding as a NumPy array, or None on error.
    """
    try:
        embedding = embedder.get_embedding(text)
        if embedding is None:
            logging.warning(f"Failed to get embedding for text: '{text}'")
            return None
        return np.array(embedding)  # Convert to NumPy array
    except Exception as e:
        logging.error(f"Error in get_sbert_embedding: {e}")
        return None  # Or consider raising the exception again