from flask import Blueprint, request, jsonify
from app import db
from app.models import Document
from app.services.sbert_service import get_sbert_embedding
import numpy as np
import logging
import json

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
        top_k = data.get('top_k', 10)  # Default to 10 if not provided
        min_similarity = -1.0  # Remove similarity threshold

        if not query:
            logger.warning("Query text is missing in the request.")
            return jsonify({"error": "Query text is required."}), 400

        logger.info(f"Received query: {query}, top_k: {top_k}")

        # Get and normalize query embedding
        query_embedding = np.array(get_sbert_embedding(query))
        query_norm = np.linalg.norm(query_embedding)
        if query_norm == 0:
            logger.warning("Query embedding norm is zero.")
            return jsonify({"documents": []}), 200
        query_embedding = query_embedding / query_norm

        # Stream documents to save memory
        results = []
        for doc in Document.query.yield_per(10):  # Use yield_per for memory efficiency
            embeddings = doc.embeddings
            if isinstance(embeddings, str):
                try:
                    embeddings = json.loads(embeddings)
                except Exception:
                    continue

            if not embeddings or not isinstance(embeddings, list):
                continue

            doc_embedding = np.array(embeddings[0])
            doc_norm = np.linalg.norm(doc_embedding)
            if doc_norm == 0:
                continue
            doc_embedding = doc_embedding / doc_norm

            # Cosine similarity (dot product of normalized vectors)
            boost = 0.1 if any(kw in doc.title.lower() for kw in query.lower().split()) else 0
            similarity = float(np.dot(query_embedding, doc_embedding)) + boost
            # No similarity filter

            results.append({
                "id": doc.id,
                "title": doc.title,
                "abstract": doc.summary,
                "similarity": similarity
            })

        # Sort and limit results to top 10
        results = sorted(results, key=lambda x: x['similarity'], reverse=True)[:10]

        return jsonify({"documents": results}), 200

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
    document = Document.query.get(document_id)
    if not document:
        return jsonify({'error': 'Document not found'}), 404

    # If sections are stored as a JSON string, load them
    try:
        sections = document.sections
        if isinstance(sections, str):
            sections = json.loads(sections)
    except Exception:
        sections = {}

    return jsonify({'sections': sections})

@bp.route('/documents/<int:document_id>/details', methods=['GET'])
def get_document_details(document_id):
    """
    Fetch the title, author, and abstract of a document by its ID.
    """
    try:
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404

        # Defensive: Load author from JSON if stored as string
        author = document.author
        if isinstance(author, str):
            try:
                author = ', '.join(json.loads(author))
            except Exception:
                pass

        return jsonify({
            'title': document.title,
            'author': author,
            'abstract': document.summary
        }), 200
    except Exception as e:
        logger.error(f"Error fetching details for document {document_id}: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500