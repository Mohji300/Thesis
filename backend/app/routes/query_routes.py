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
            return jsonify({"error": "Query text is required."}), 400

        query_embedding = np.array(get_sbert_embedding(query))
        documents = Document.query.all()
        if not documents:
            return jsonify({"error": "No documents found in database."}), 404

        results = []
        for doc in documents:
            # Skip if embeddings are missing or invalid

            if not doc.embeddings or not isinstance(doc.embeddings, list):
                logger.warning(f"Document {doc.id} has invalid embeddings.")
                continue
            doc_embedding = doc.embeddings[0]  # Get the first embedding
            if doc_embedding is None or not isinstance(doc_embedding, (list, np.ndarray)):
                logger.warning(f"Document {doc.id} embedding is None or invalid.")
                continue

            # Convert to NumPy array if it's a list
            doc_embedding = np.array(doc_embedding)

            # Calculate the distance between query embedding and document embedding
            try:
                distance = np.linalg.norm(query_embedding - doc_embedding)
                results.append({'document': doc, 'distance': distance})
            except Exception as e:
                logger.error(f"Error calculating distance for document {doc.id}: {e}")
                continue

        # Sort by similarity (distance)
        results = sorted(results, key=lambda x: x['distance'])
        top_results = results[:top_k]

        response = [{
            "id": doc['document'].id,
            "title": doc['document'].title,
            "abstract": getattr(doc['document'], 'abstract', '')  # Use .abstract, fallback to '' if missing
        } for doc in top_results]

        return jsonify({"documents": response}), 200

    except Exception as e:
        logger.error(f"An error occurred during document search: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
    

# Endpoint to fetch the summary of a document by its ID
@bp.route('/documents/<int:document_id>/summary', methods=['GET'])
def get_document_summary(document_id):
    """
    Fetch the summary of a document by its ID.
    """
    try:
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404

        return jsonify({'summary': document.summary}), 200
    except Exception as e:
        logger.error(f"Error fetching summary for document {document_id}: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500


# Endpoint to fetch the sections of a document by its ID
@bp.route('/documents/<int:document_id>/sections', methods=['GET'])
def get_document_sections(document_id):
    try:
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404

        # Defensive: Try to load JSON if it's a string
        sections = getattr(document, 'sections', None)
        if isinstance(sections, str):
            import json
            try:
                sections = json.loads(sections)
            except Exception:
                sections = None

        if not isinstance(sections, dict):
            logger.error(f"Document {document_id} sections attribute is not a dictionary or is missing.")
            return jsonify({'error': 'Document sections not available'}), 500

        predefined_sections = ['Abstract', 'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5']
        filtered_sections = {key: value for key, value in sections.items() if key in predefined_sections}

        return jsonify({'sections': filtered_sections}), 200
    except Exception as e:
        logger.error(f"Error fetching sections for document {document_id}: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500