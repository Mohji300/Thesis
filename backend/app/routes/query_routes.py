from flask import Blueprint, request, jsonify
from app import db
from app.models import Document
from app.services.sbert_service import get_sbert_embedding
import numpy as np
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('query', __name__)

# Optional: Health check route
@bp.route('/', methods=['GET'])
def query_index():
    logger.info("Health check route accessed.")
    return jsonify({"message": "Query route is working!"})

# Actual Search Route
@bp.route('/search', methods=['POST'])
def search_documents():
    try:
        data = request.get_json()
        query = data.get('query', '')
        top_k = data.get('top_k', 10)

        if not query:
            logger.warning("Query text is missing in the request.")
            return jsonify({"error": "Query text is required."}), 400

        logger.info(f"Received query: {query}, top_k: {top_k}")

        # Get query embedding
        query_embedding = np.array(get_sbert_embedding(query))
        logger.info("Query embedding generated successfully.")

        # Retrieve all documents
        documents = Document.query.all()

        if not documents:
            logger.warning("No documents found in the database.")
            return jsonify({"error": "No documents found in database."}), 404

        results = []
        for doc in documents:

            print(f"Type of doc.embeddings[0]: {type(doc.embeddings[0])}")
            print(f"Value of doc.embeddings[0]: {doc.embeddings[0]}")
            doc_embedding = np.array(doc.embeddings[0])
            if isinstance(doc.embeddings[0], dict):
                continue
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

        logger.info(f"Returning top {len(top_results)} results.")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"An error occurred during document search: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500