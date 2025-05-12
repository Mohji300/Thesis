from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import Document
from app.utils.pdf_parser import extract_text_from_pdf_bytes, safe_parse_json, extract_all_sections
from app.services.bart_service import summarize_text
from app.services.sbert_service import get_sbert_embedding
from app.services.bertopic_service import get_topics
import numpy as np
import json
import unicodedata

bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_error(message, status_code=400):
    return jsonify({'error': message}), status_code

def safe_unicode(text):
    if isinstance(text, str):
        return text.encode('utf-8', 'ignore').decode('utf-8')
    return text

def to_ascii(text):
    if isinstance(text, str):
        # Normalize and encode to ASCII, ignoring non-ASCII characters
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

@bp.route('/', methods=['GET'])
def upload_index():
    return jsonify({"message": "Upload route is working!"})

@bp.route('/document', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            print("[ERROR] No file part in the request")
            return handle_error('No file part')

        file = request.files['file']
        if file.filename == '':
            print("[ERROR] No selected file")
            return handle_error('No selected file')

        if not allowed_file(file.filename):
            print("[ERROR] Unsupported file type")
            return handle_error('Unsupported file type')

        print("[DEBUG] File received successfully")

        pdf_content = extract_text_from_pdf_bytes(file.read())
        if not pdf_content or len(pdf_content.strip()) < 10:
            print("[ERROR] Failed to extract meaningful text from PDF")
            return handle_error('Failed to extract meaningful text from PDF')

        print(f"[DEBUG] PDF content extracted successfully, length: {len(pdf_content)}")

        title = request.form.get('title', 'Untitled')
        metadata_raw = request.form.get('metadata', '{}')
        metadata = safe_parse_json(metadata_raw)

        print(f"[DEBUG] Title: {title}, Metadata: {metadata}")

        if len(pdf_content) < 100:
            print("[WARNING] PDF content too short for models. Using dummy summary/entities/topics.")
            summary = "Summary unavailable due to short content."
            sections = {}
            embedding = get_sbert_embedding(pdf_content)
            topics = ["General"]
        else:
            print("[DEBUG] Starting custom section extraction...")
            extracted_sections = extract_all_sections(pdf_content)
            print("[DEBUG] Section extraction complete.")

            # Convert list of dicts to a dict: {section: content}
            sections = {sec['section']: sec['content'] for sec in extracted_sections}

            print("[DEBUG] Extracted sections:")
            for sec, content in sections.items():
                print(f"  - {sec} (length: {len(content)})")

            # Use Abstract as summary if present, else summarize all sections
            if "ABSTRACT" in sections:
                summary = sections["ABSTRACT"]
            else:
                labeled_summaries = []
                for sec, content in sections.items():
                    print(f"[DEBUG] Summarizing section: {sec}")
                    section_summary = summarize_text(content)
                    labeled_summaries.append(f"[{sec}] {section_summary}")
                summary = "\n\n".join(labeled_summaries)
            print("[DEBUG] Summarization complete.")

            print("[DEBUG] Starting SBERT embedding generation...")
            embedding = get_sbert_embedding(pdf_content)
            if hasattr(embedding, "tolist"):
                embedding_list = embedding.tolist()
            else:
                embedding_list = embedding
            print("[DEBUG] SBERT embedding complete.")

            print("[DEBUG] Starting BERTopic clustering...")
            embedding_for_topic = np.array(embedding_list)
            topics = get_topics([embedding_for_topic])
            print("[DEBUG] BERTopic clustering complete.")

        # Parse authors as a list (split by comma)
        author_raw = metadata.get('author', 'Unknown')
        if isinstance(author_raw, str):
            author = [a.strip() for a in author_raw.split(',')]
        else:
            author = [str(author_raw)]

        document = Document(
            title=to_ascii(title),
            author=json.dumps([to_ascii(a) for a in author], ensure_ascii=False),
            year=metadata.get('year', 0),
            metadata=json.dumps({to_ascii(str(k)): to_ascii(str(v)) for k, v in metadata.items()}, ensure_ascii=False),
            summary=to_ascii(summary),
            sections={to_ascii(str(k)): to_ascii(str(v)) for k, v in sections.items()},
            embeddings=json.dumps([embedding_list], ensure_ascii=False),
            topics=json.dumps([to_ascii(str(t)) for t in topics], ensure_ascii=False)
        )
        db.session.add(document)
        db.session.commit()

        print("[DEBUG] Document saved to database successfully")

        return jsonify({'message': 'Document uploaded successfully', 'document_id': document.id}), 201

    except Exception as e:
        print(f"[ERROR] during document upload: {e}")
        return handle_error(f"An error occurred during upload or processing: {str(e)}", 500)