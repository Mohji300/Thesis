import logging
from pathlib import Path
from bertopic import BERTopic
import torch  # Import torch for tensor handling

# Configure logging (if not already configured elsewhere)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable for the BERTopic model
bertopic_model = None

def load_bertopic_model():
    """
    Loads the BERTopic model from the specified directory.

    Returns:
        BERTopic: The loaded BERTopic model.
    """
    global bertopic_model

    # Build the path to the BERTopic model directory
    model_dir = Path('app') / 'trained-models' / 'bertopic_model'

    # Convert to absolute path and ensure it exists
    model_dir = model_dir.resolve()

    if not model_dir.exists():
        error_message = f"BERTopic model directory not found at: {model_dir}"
        logging.error(error_message)
        raise FileNotFoundError(error_message)

    logging.debug(f"Loading BERTopic model from: {model_dir}")

    try:
        # Load the BERTopic model
        bertopic_model = BERTopic.load(str(model_dir))
        logging.debug("BERTopic model loaded successfully.")
    except Exception as e:
        error_message = f"Failed to load BERTopic model: {e}"
        logging.error(error_message)
        raise RuntimeError(error_message)  # Use RuntimeError for loading errors

def get_topics(embeddings):
    """
    Generates topics using the locally loaded BERTopic model, handling potential issues
    with the input embeddings, aligning with the get_embedding logic.

    Args:
        embeddings: A list of embeddings (torch.Tensor) or None.

    Returns:
        list: A list of topic IDs (integers). Returns a list of -1s if there are issues.
    """
    global bertopic_model

    try:
        if not embeddings:  # Check for None or empty list
            logging.warning("No embeddings provided. Returning an empty list.")
            return []

        # Ensure the BERTopic model is loaded
        if bertopic_model is None:
            load_bertopic_model()

        # 1. Validate input type
        if not isinstance(embeddings, list):
            error_message = f"Expected a list of torch.Tensor, got {type(embeddings)}"
            logging.error(error_message)
            raise ValueError(error_message)

        # 2. Validate embeddings within the list and convert to tensor
        processed_embeddings = []
        for i, embedding in enumerate(embeddings):
            if not isinstance(embedding, torch.Tensor):
                error_message = f"Expected torch.Tensor at index {i}, got {type(embedding)}"
                logging.error(error_message)
                return [-1] * len(embeddings)  # Return -1 for all, consistent error handling

            if embedding.ndim != 1:
                error_message = f"Expected 1D tensor at index {i}, got {embedding.ndim}D"
                logging.error(error_message)
                return [-1] * len(embeddings)

            if torch.any(torch.isnan(embedding)) or torch.any(torch.isinf(embedding)):
                logging.warning(f"Embedding at index {i} contains NaN or Inf. Returning -1 for all.")
                return [-1] * len(embeddings)

            processed_embeddings.append(embedding)

        # Stack the tensors for BERTopic
        embeddings_tensor = torch.stack(processed_embeddings)

        # 3. Call BERTopic's transform
        topics, _ = bertopic_model.transform(embeddings_tensor)

        logging.debug(f"BERTopic transform returned topics: {topics}")
        return topics.tolist()  # Ensure JSON serializable

    except Exception as e:
        error_message = f"Error in get_topics: {e}"
        logging.error(error_message)
        raise  # Re-raise to be handled by the caller (Flask route)
