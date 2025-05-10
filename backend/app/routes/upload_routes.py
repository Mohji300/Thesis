from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import Document
from app.utils.pdf_parser import parse_pdf
from app.services.bart_service import summarize_text
from app.services.bert_service import extract_section
from app.services.sbert_service import get_sbert_embedding
from app.services.bertopic_service import get_topics
import json
import numpy as np

bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_error(message, status_code=400):
    return jsonify({'error': message}), status_code

@bp.route('/', methods=['GET'])
def upload_index():
    return jsonify({"message": "Upload route is working!"})

@bp.route('/document', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            return handle_error('No file part')

        file = request.files['file']
        if file.filename == '':
            return handle_error('No selected file')

        if not allowed_file(file.filename):
            return handle_error('Unsupported file type')

        pdf_content = parse_pdf(file.read())
        if not pdf_content or len(pdf_content.strip()) < 10:
            return handle_error('Failed to extract meaningful text from PDF')

        print(f"[DEBUG] PDF content extracted successfully, length: {len(pdf_content)}")

        title = request.form.get('title', 'Untitled')

        # Parse metadata safely
        metadata = request.form.get('metadata')
        if metadata:
            try:
                metadata = json.loads(metadata)
            except Exception as e:
                print(f"[ERROR] Failed to parse metadata: {e}")
                metadata = {}
        else:
            metadata = {}

        # Fallback: if text too short, use dummy values
        if len(pdf_content) < 100:
            print("[WARNING] PDF content too short for models. Using dummy summary/entities/topics.")
            summary = "Summary unavailable due to short content."
            sections = []
            embedding = get_sbert_embedding(pdf_content)
            topics = ["General"]
        else:
            print("[DEBUG] Starting summarization...")
            summary = summarize_text(pdf_content)
            print("[DEBUG] Summarization complete.")

            print("[DEBUG] Starting Section extraction...")
            sections = extract_section(pdf_content)
            print("[DEBUG] Section extraction complete.")

            print("[DEBUG] Starting SBERT embedding generation...")
            embedding = get_sbert_embedding(pdf_content)
            print("[DEBUG] SBERT embedding complete.")

            print("[DEBUG] Starting BERTopic clustering...")
            topics = get_topics([embedding])
            print("[DEBUG] BERTopic clustering complete.")

        # Convert embedding to list for JSON serialization
        if isinstance(embedding, np.ndarray):
            embedding_serializable = embedding.tolist()
        elif isinstance(embedding, list):
            embedding_serializable = [e.tolist() if hasattr(e, 'tolist') else e for e in embedding]
        else:
            embedding_serializable = embedding

        # Extract authors as a comma-separated string
        authors = ', '.join(metadata.get('authors', []))
        year = metadata.get('year', '')

        document = Document(
            title=title,
            # text=pdf_content,
            document_metadata=metadata,
            summary=summary,
            sections=sections,
            embeddings=embedding_serializable,
            topics=topics,
            author=authors,
            year=year
        )
        db.session.add(document)
        db.session.commit()

        return jsonify({'message': 'Document uploaded successfully', 'document_id': document.id}), 201

    except Exception as e:
        print(f"[ERROR] during document upload: {e}")
        return handle_error(f"An error occurred during upload or processing: {str(e)}", 500)