from flask import Blueprint, request, jsonify
from app import db
from app.models import Document
from app.services.sbert_service import get_sbert_embedding
import numpy as np
import logging
import json
from app.models import Document

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
        top_k = data.get('top_k', 1)

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
            embeddings = doc.embeddings
            # Convert JSON string to Python list
            if isinstance(embeddings, str):
                try:
                    embeddings = json.loads(embeddings)
                except Exception:
                    logger.warning(f"Document {doc.id} embeddings could not be parsed from JSON.")
                    continue

            if not embeddings or not isinstance(embeddings, list):
                logger.warning(f"Document {doc.id} has invalid embeddings.")
                continue

            doc_embedding = embeddings[0]
            if doc_embedding is None or not isinstance(doc_embedding, (list, np.ndarray)):
                logger.warning(f"Document {doc.id} embedding is None or invalid.")
                continue

            doc_embedding = np.array(doc_embedding)

            # Calculate the distance between query embedding and document embedding
            try:
                distance = np.linalg.norm(query_embedding - doc_embedding)
                results.append({'document': doc, 'distance': distance})
            except Exception as e:
                logger.error(f"Error calculating distance for document {doc.id}: {e}")
                continue

        # Sort results based on distance (lower = more similar)
        results = sorted(results, key=lambda x: x['distance'])
        top_results = results[:top_k]

        response = [{
            "id": result['document'].id,
            "title": result['document'].title,
            "abstract": result['document'].summary,
            "distance": result['distance']
        } for result in top_results]

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
    document = Document.query.get(document_id)
    if not document:
        return jsonify({'error': 'Document not found'}), 404

    # If sections are stored as a JSON string, load them
    import json
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