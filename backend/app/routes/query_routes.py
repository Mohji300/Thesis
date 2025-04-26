from flask import Blueprint, request, jsonify
from app import db
from app.models import Document
from app.services.sbert_service import get_sbert_embedding
import numpy as np

bp = Blueprint('query', __name__)

# Optional: Health check route (you can remove later if you want)
@bp.route('/', methods=['GET'])
def query_index():
    return jsonify({"message": "Query route is working!"})

# Actual Search Route
@bp.route('/search', methods=['POST'])
def search_documents():
    try:
        data = request.get_json()
        query = data.get('query', '')
        top_k = data.get('top_k', 10)

        if not query:
            return jsonify({"error": "Query text is required."}), 400

        # Get query embedding
        query_embedding = np.array(get_sbert_embedding(query))

        # Retrieve all documents
        documents = Document.query.all()

        if not documents:
            return jsonify({"error": "No documents found in database."}), 404

        results = []
        for doc in documents:
            # Assume each doc has a single embedding stored
            doc_embedding = np.array(doc.embeddings[0])
            distance = np.linalg.norm(query_embedding - doc_embedding)
            results.append({'document': doc, 'distance': distance})

        # Sort results based on distance (lower = more similar)
        results.sort(key=lambda x: x['distance'])
        top_results = [result['document'] for result in results[:top_k]]

        # Format results for JSON
        response = [{
            "id": doc.id,
            "title": doc.title,
            "summary": doc.summary,
            "topics": doc.topics
        } for doc in top_results]

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
