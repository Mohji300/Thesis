from flask import Blueprint, request, jsonify
from app.services.bart_service import summarize_long_text
import logging

bp = Blueprint('summary', __name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)

@bp.route('/', methods=['GET'])
def summary_index():
    return jsonify({"message": "Summary route is working!"})

@bp.route('/generate', methods=['POST'])
def generate_summary():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        logging.info(f"Received data: {data}")
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        # Extract text and generate summary
        text = data['text']
        logging.info(f"Text to summarize: {text}")
        
        # Use summarize_long_text for better contextual summaries
        summary = summarize_long_text(text)
        logging.info(f"Generated summary: {summary}")

        return jsonify({'summary': summary}), 200

    except Exception as e:
        # Log the error for debugging
        logging.error(f"Error in generate_summary: {e}")
        return jsonify({'error': 'An error occurred while generating the summary'}), 500