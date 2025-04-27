from app.utils.embedder import SBERTEmbedder
import logging

# Configure logging (if not already done elsewhere)
logging.basicConfig(level=logging.INFO)

# Get the SBERTEmbedder instance (Singleton)
embedder = SBERTEmbedder()


def get_sbert_embedding(text):
    """
    Generates an SBERT embedding for the given text.

    Args:
        text (str): The text to embed.

    Returns:
        list: The embedding as a list, or None on error.
    """
    try:
        embedding = embedder.get_embedding(text)
        if embedding is None:
            logging.warning(f"Failed to get embedding for text: '{text}'")
        return embedding
    except Exception as e:
        logging.error(f"Error in get_sbert_embedding: {e}")
        return None  # Or consider raising the exception again