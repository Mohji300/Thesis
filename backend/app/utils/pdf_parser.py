import io
import pdfminer.high_level

def parse_pdf(file_stream):
    try:
        text = pdfminer.high_level.extract_text(io.BytesIO(file_stream))
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None