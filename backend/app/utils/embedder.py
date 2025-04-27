import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import logging

# Configure logging (you might want to adjust this to your app's logging setup)
logging.basicConfig(level=logging.INFO)


class SBERTEmbedder:
    """
    A class to manage loading and using the SBERT model for embeddings.
    This ensures the model is loaded only once, improving efficiency.
    """

    _instance = None  # Singleton pattern

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_model()  # Load model only once
        return cls._instance

    def __init__(self):
        # This init will run only once due to the singleton pattern
        pass

    def _load_model(self):
        """Loads the SBERT model."""

        self.model_dir = Path('app') / 'trained-models' / 'sbert_model'
        self.model_dir = self.model_dir.resolve()

        if not self.model_dir.exists():
            raise FileNotFoundError(f"SBERT model directory not found at: {self.model_dir}")

        logging.info(f"Loading SBERT model from: {self.model_dir}")

        try:
            self.model = SentenceTransformer(str(self.model_dir))
            logging.info("SBERT model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load SBERT model: {e}")
            raise

    def get_embedding(self, text):
        """
        Generates embeddings for the given text.

        Args:
            text (str): The input text.

        Returns:
            list: A list of embeddings or None on error.
        """
        try:
            if not text or not text.strip():
                logging.warning("Empty text provided. Returning None.")
                return None  # Or [] if you prefer an empty list

            embedding = self.model.encode(text, convert_to_tensor=True)
            return embedding.tolist()

        except Exception as e:
            logging.error(f"Error generating embedding for text: {e}")
            return None  # Or raise, depending on your error handling policy


"""
if __name__ == "__main__":
    try:
        embedder = SBERTEmbedder()  # Get the instance
        test_text = "This is a test sentence."
        embedding = embedder.get_embedding(test_text)
        if embedding:
            logging.info("Embedding generated successfully.")
            print(embedding)
        else:
            logging.error("Failed to generate embedding.")
    except FileNotFoundError as e:
        logging.error(str(e))
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}") """