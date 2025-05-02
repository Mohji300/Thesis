from flask import Blueprint, request, jsonify
from app import bert_model  # Import the globally loaded BERT model
from app.services.bert_service import extract_section  # Import the updated extract_section function

bp = Blueprint('extract', __name__)

@bp.route('/', methods=['GET'])
def extract_index():
    """
    Health check route for the extract service.
    """
    return jsonify({"message": "Extract route is working!"})

@bp.route('/sections', methods=['POST'])
def extract_sections():
    """
    Extracts sections from the given text using the BERT model.

    Expects a JSON payload with the key 'text'.

    Returns:
        JSON response with the predicted sections or an error message.
    """
    try:
        # Parse the request JSON
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']

        # Use the globally loaded BERT model to predict sections
        sections = extract_section(text)

        if sections is None:
            return jsonify({'error': 'Failed to predict sections'}), 500

        return jsonify({'sections': sections})

    except Exception as e:
        # Log and return the error
        return jsonify({'error': str(e)}), 500