import os
from bertopic import BERTopic
from app.model_server.loaders.sbert_loader import load_sbert_model

# Load the BERTopic model and SBERT model once when this module is loaded
_bertopic_model = None

def load_bertopic_model():
    global _bertopic_model
    if _bertopic_model is None:
        bertopic_model_path = os.path.join("app", "trained-models", "bertopic_model")
        print("[DEBUG] Loading SBERT model for BERTopic...")
        embedding_model = load_sbert_model()
        print("[DEBUG] Loading BERTopic model from:", bertopic_model_path, "with loaded SBERT model.")
        try:
            _bertopic_model = BERTopic.load(bertopic_model_path, embedding_model=embedding_model)
            print("[DEBUG] BERTopic model loaded successfully with custom SBERT.")
        except Exception as e:
            print(f"[ERROR] Error loading BERTopic model: {e}")
            raise
    return _bertopic_model

def get_bertopic_topics(texts):
    """
    Generates topics for the given texts using the *already loaded* BERTopic model.

    Args:
        texts (list of str): A list of documents to generate topics for.

    Returns:
        list: A list of topics for the input texts.
    """
    model = load_bertopic_model()
    try:
        topics, _ = model.transform(texts)
        return topics
    except Exception as e:
        print(f"[ERROR] Error transforming texts with BERTopic: {e}")
        raise
