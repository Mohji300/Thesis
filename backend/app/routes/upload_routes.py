from flask import Blueprint, request, jsonify
from app import db
from app.models import Document
from app.utils.pdf_parser import parse_pdf
from app.services.bart_service import summarize_text
from app.services.ner_service import get_entities
from app.services.sbert_service import get_sbert_embedding
from app.services.bertopic_service import get_topics

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        pdf_text = parse_pdf(file.read())
        title = request.form.get('title', 'Untitled')
        metadata = request.form.get('metadata', '{}')

        summary = summarize_text(pdf_text)
        entities = get_entities(pdf_text)
        embedding = get_sbert_embedding(pdf_text)
        topics = get_topics([embedding])

        document = Document(title=title, text=pdf_text, metadata=metadata, summary=summary, entities=entities, embeddings=[embedding], topics=topics)
        db.session.add(document)
        db.session.commit()

        return jsonify({'message': 'Document uploaded successfully', 'document_id': document.id}), 201
    return jsonify({'error': 'Failed to upload document'}), 500