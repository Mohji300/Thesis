from flask import Blueprint, request, jsonify
from app import db
from app.models import Document
from app.services.sbert_service import get_sbert_embedding
import numpy as np

bp = Blueprint('query', __name__, url_prefix='/query')

@bp.route('/search', methods=['POST'])
def search_documents():
    query = request.json['query']
    query_embedding = np.array(get_sbert_embedding(query))
    top_k = request.json.get('top_k', 10)

    documents = Document.query.all()
    results = []
    for doc in documents:
        doc_embedding = np.array(doc.embeddings[0])
        distance = np.linalg.norm(query_embedding - doc_embedding)
        results.append({'document': doc, 'distance': distance})

    results.sort(key=lambda x: x['distance'])
    top_results = [result['document'] for result in results[:top_k]]

    return jsonify([{
        'id': doc.id,
        'title': doc.title,
        'summary': doc.summary,
        'topics': doc.topics
    } for doc in top_results])