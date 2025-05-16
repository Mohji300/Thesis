import pdfplumber
import re
import os
import io
import json
import unicodedata

# --- CONFIGURATION ---
SECTION_ALIASES = {
    "ABSTRACT": ["ABSTRACT"],
    "INTRODUCTION": ["INTRODUCTION", "CHAPTER I", "CHAPTER 1", "1 INTRODUCTION, 1.1. Background of the study"],
    "REVIEW OF RELATED LITERATURE": [
        "REVIEW OF RELATED LITERATURE",
        "RELATED LITERATURE AND STUDIES",
        "CHAPTER II",
        "CHAPTER 2",
        "THEORETICAL FRAMEWORK",
        "REVIEW OF RELATED LITERATURE AND STUDIES",
        "2 THEORETICAL FRAMEWORK",
        "RELATED LITERATURE"
    ],
    "METHODOLOGY": ["METHODOLOGY", "CHAPTER III", "3 METHODOLOGY, 3 MATERIALS AND METHODS, CHAPTER 3, RESEARCH DESIGN AND METHODOLOGY", "CHAPTER III METHODOLOGY"],
    "RESULTS AND DISCUSSION": ["RESULTS AND DISCUSSION", "CHAPTER IV", "4 RESULTS AND DISCUSSION"],
    "CONCLUSION": [
        "CONCLUSION",
        "SUMMARY, CONCLUSIONS, AND RECOMMENDATIONS",
        "SUMMARY, CONCLUSIONS AND RECOMMENDATIONS",
        "SUMMARY CONCLUSIONS AND RECOMMENDATIONS",
        "5 SUMMARY, CONCLUSIONS, AND RECOMMENDATIONS",
        "5 SUMMARY, CONCLUSIONS AND RECOMMENDATIONS",
        "5 SUMMARY CONCLUSIONS AND RECOMMENDATIONS",
        "SUMMARY OF FINDINGS, CONCLUSIONS AND RECOMMENDATIONS",
        "CHAPTER V",
        "CHAPTER 5",
        "CHAPTER 5 SUMMARY OF FINDINGS, CONCLUSIONS, AND RECOMMENDATIONS",
        "CHAPTER V SUMMARY OF FINDINGS, CONCLUSIONS, AND RECOMMENDATIONS",
        "CHAPTER V SUMMARY, CONCLUSIONS AND RECOMMENDATIONS"
    ]
}

STOP_WORDS = [
    "TABLE OF CONTENTS", "LIST OF", "ACKNOWLEDGEMENT", "APPENDICES", "BIONOTE",
    "REFERENCES", "BIBLIOGRAPHY", "GLOSSARY", "INDEX", "CURRICULUM VITAE"
]

def clean_text(text):
    text = re.sub(r'(?<=\w)-\n(?=\w)', '', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[^\S\r\n]+', ' ', text)
    return text.strip()

def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    return clean_text(full_text)

def remove_toc(text):
    toc_keywords = ["TABLE OF CONTENTS", "Page", "CHAPTER"]
    if any(keyword in text for keyword in toc_keywords):
        toc_end = re.search(r'(?i)CHAPTER\s+1', text)
        if toc_end:
            return text[toc_end.start():]
    return text

def normalize_section_headers(text):
    text = re.sub(
        r"(CHAPTER\s+[VXILC\d]+)\s*\n([^\n]{0,100})?\n([^\n]{0,100})",
        lambda m: f"{m.group(1)} {m.group(2)} {m.group(3)}".strip(),
        text,
        flags=re.IGNORECASE
    )
    return text

def extract_section(text, aliases, next_aliases, stop_words):
    all_stops = [alias for sublist in next_aliases for alias in sublist] + stop_words
    for title in aliases:
        pattern = rf"(?<=\n){re.escape(title)}\s*\n+(.*?)(?=\n(?:{'|'.join(map(re.escape, all_stops))})\s*\n|\Z)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            print(to_ascii(f"[MATCHED HEADER] → {title}"))
            section_text = match.group(1).strip()
            lines = section_text.splitlines()
            content_lines = [line for line in lines if not re.match(r'.*\b\d{1,3}\b$', line.strip())]
            return "\n".join(content_lines).strip()
    return ""

def extract_all_sections(text):
    results = []

    # First extract abstract before TOC is removed
    abstract_body = extract_section(text, SECTION_ALIASES["ABSTRACT"], list(SECTION_ALIASES.values())[1:], STOP_WORDS)
    if abstract_body:
        results.append({"section": "ABSTRACT", "content": f"ABSTRACT\n{clean_text(abstract_body)}"})

    # Then remove TOC
    text = remove_toc(text)

    section_keys = list(SECTION_ALIASES.keys())[1:]  # Skip ABSTRACT
    for i, section in enumerate(section_keys):
        aliases = SECTION_ALIASES[section]
        next_aliases = [SECTION_ALIASES[k] for k in section_keys[i+1:]]

        section_body = extract_section(text, aliases, next_aliases, STOP_WORDS)

        if section.upper() == "CONCLUSION" and section_body:
            stop_idx = re.search(r'\b(REFERENCES|BIBLIOGRAPHY|APPENDICES)\b', section_body, re.IGNORECASE)
            if stop_idx:
                section_body = section_body[:stop_idx.start()]

        if section_body:
            results.append({"section": section, "content": f"{section}\n{clean_text(section_body)}"})

    return results

def write_output(sections, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for sec in sections:
            f.write(f"\n--- {sec['section']} ---\n")
            f.write(f"{sec['content']}\n")

def extract_text_from_pdf_bytes(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    return clean_text(full_text)

def safe_parse_json(json_str):
    try:
        return json.loads(json_str)
    except Exception:
        return {}
    
def to_ascii(text):
    if isinstance(text, str):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

# --- MAIN EXECUTION ---
# if __name__ == "__main__":
#    input_pdf_path = r"C:\Users\DANIEL\Documents\thesis_project\thesis_papers\BUbot An Ai-Powered Student Assistive Chatbot For General Queries And Information In Bicol University.pdf"
#    output_txt_path = r"C:\Users\DANIEL\Downloads\Extracted-BUbot An Ai-Powered Student Assistive Chatbot For General Queries And Information In Bicol University.txt"

#    print("🔍 Extracting sections from PDF...")
#    full_text = extract_text_from_pdf(input_pdf_path)
#    extracted_sections = extract_all_sections(full_text)
#    write_output(extracted_sections, output_txt_path)

#    print(f"✅ Finished. Output written to:\n{output_txt_path}")
#    for sec in extracted_sections:
#        print(f"\n--- {sec['section']} ---\n{sec['content'][:500]}...\n")
