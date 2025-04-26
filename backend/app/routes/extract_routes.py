from flask import Blueprint, request, jsonify
from app.services.ner_service import get_entities

bp = Blueprint('extract', __name__)

@bp.route('/', methods=['GET'])
def extract_index():
    return jsonify({"message": "Extract route is working!"})

@bp.route('/entities', methods=['POST'])
def extract_entities():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        entities = get_entities(text)

        return jsonify({'entities': entities})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
