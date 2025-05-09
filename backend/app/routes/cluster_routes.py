from flask import Blueprint, request, jsonify
import logging
import numpy as np
import torch

from app.services.bertopic_service import get_topics
from app.services.sbert_service import get_sbert_embedding

bp = Blueprint('cluster', __name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def to_json_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, list):
        return [to_json_serializable(i) for i in obj]
    return obj

@bp.route('/', methods=['GET'])
def cluster_index():
    return jsonify({"message": "Cluster route is working!"})

@bp.route('/assign', methods=['POST'])
def assign_cluster():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            logging.error("Request missing 'text' field.")
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']

        embedding = get_sbert_embedding(text)
        if not isinstance(embedding, np.ndarray):
            raise ValueError("get_sbert_embedding did not return a NumPy array.")

        embedding_tensor = torch.tensor(embedding)
        topics = get_topics([embedding_tensor])
        topics = to_json_serializable(topics)

        return jsonify({'topics': topics})

    except Exception as e:
        logging.error(f"Error in assign_cluster: {e}")
        return jsonify({'error': 'Internal server error'}), 500
