from flask import Blueprint, request, jsonify
from app.services.bart_service import summarize_text

bp = Blueprint('summary', __name__)

@bp.route('/', methods=['GET'])
def summary_index():
    return jsonify({"message": "Summary route is working!"})

@bp.route('/generate', methods=['POST'])
def generate_summary():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        summary = summarize_text(text)

        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
