from flask import Blueprint, request, jsonify
import logging
import numpy as np
from app.services.bertopic_service import get_topics  # Import your service functions
from app.services.sbert_service import get_sbert_embedding

bp = Blueprint('cluster', __name__)

# Configure logging (if not already configured elsewhere)
logging.basicConfig(level=logging.INFO,  # Set the desired logging level
                    format='%(asctime)s - %(levelname)s - %(message)s')

@bp.route('/', methods=['GET'])
def cluster_index():
    """
    Endpoint for testing the cluster route.
    """
    return jsonify({"message": "Cluster route is working!"})

@bp.route('/assign', methods=['POST'])
def assign_cluster():
    """
    Assigns a cluster (topic) to the input text using BERTopic.
    Handles errors robustly and logs extensively.
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            logging.error("Request missing 'text' field.")
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']

        # 1. Get the embedding
        try:
            embedding = get_sbert_embedding(text)
            if not isinstance(embedding, np.ndarray):
                raise ValueError("get_sbert_embedding did not return a NumPy array.")
            if np.ndim(embedding) != 1:  # Check for correct dimensionality
                raise ValueError(f"Expected 1D embedding, got {np.ndim(embedding)}D.")
            logging.debug(f"Successfully obtained embedding with shape: {embedding.shape}")
        except Exception as e:
            logging.error(f"Error getting embedding: {e}")
            return jsonify({'error': f'Error processing text: {e}'}), 500

        # 2. Assign cluster (topic)
        try:
            topics = get_topics([embedding])  # Pass as a list of embeddings
            if not isinstance(topics, list):
                raise ValueError("get_topics did not return a list.")
            if len(topics) != 1:
                raise ValueError(f"Expected 1 topic, but got {len(topics)}: {topics}")

            logging.debug(f"Successfully obtained topics: {topics}")
            return jsonify({'topics': topics})  # Return the result

        except Exception as e:
            logging.error(f"Error assigning cluster: {e}")
            return jsonify({'error': f'Error assigning cluster: {e}'}), 500

    except Exception as e:
        # Catch any unexpected errors during the entire process
        logging.critical(f"Unexpected error in assign_cluster: {e}")
        return jsonify({'error': 'Internal server error'}), 500
