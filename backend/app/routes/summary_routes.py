from flask import Blueprint, request, jsonify
from app.services.bart_service import summarize_text, summarize_section

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
        
        summary = summarize_text(text)
        logging.info(f"Generated summary: {summary}")

        return jsonify({'summary': summary}), 200

    except Exception as e:
        # Log the error for debugging
        logging.error(f"Error in generate_summary: {e}")
        return jsonify({'error': 'An error occurred while generating the summary'}), 500

@bp.route('/summarize/section', methods=['POST'])
def summarize_section_endpoint():
    """
    Endpoint to summarize a specific section of a file.
    Expects a JSON payload with 'fileContent' and 'sectionName'.
    """
    try:
        # Parse JSON data from the request
        data = request.get_json()
        logging.info(f"Received data for section summarization: {data}")

        if not data or 'fileContent' not in data or 'sectionName' not in data:
            return jsonify({'error': "Missing 'fileContent' or 'sectionName' in the request."}), 400

        # Extract file content and section name
        file_content = data['fileContent']
        section_name = data['sectionName']

        # Summarize the specified section
        summary = summarize_section(file_content, section_name)
        logging.info(f"Generated summary for section '{section_name}': {summary}")

        return jsonify({'summary': summary}), 200

    except Exception as e:
        # Log the error for debugging
        logging.error(f"Error in summarize_section_endpoint: {e}")
        return jsonify({'error': 'An error occurred while summarizing the section.'}), 500