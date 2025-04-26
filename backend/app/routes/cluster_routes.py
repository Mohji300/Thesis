from flask import Blueprint, request, jsonify
from app.services.bertopic_service import get_topics
from app.services.sbert_service import get_sbert_embedding

bp = Blueprint('cluster', __name__)

@bp.route('/', methods=['GET'])
def cluster_index():
    return jsonify({"message": "Cluster route is working!"})

@bp.route('/assign', methods=['POST'])
def assign_cluster():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        embedding = get_sbert_embedding(text)
        topics = get_topics([embedding])

        return jsonify({'topics': topics})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
