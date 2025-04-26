import io
import json
import PyPDF2

def parse_pdf(file_stream):
    """Parses PDF bytes and returns extracted text."""
    try:
        pdf_text = ""
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_stream))
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                pdf_text += page_text
        print(f"Successfully extracted text from PDF. Total length: {len(pdf_text)} characters.")
        return pdf_text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None

def safe_parse_json(json_string):
    """Safely parses a JSON string to a Python dictionary."""
    try:
        if json_string:
            return json.loads(json_string)
        else:
            return {}
    except Exception as e:
        print(f"Error parsing metadata JSON: {e}")
        return {}
