import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForTokenClassification, BertConfig
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables
bert_tokenizer = None
bert_model = None
label2id = None
id2label = None

def load_bert_model(model_dir):
    """
    Loads a fine-tuned BERT model for token classification from local directory.
    Handles label mappings and avoids classifier shape mismatches.
    """
    global bert_tokenizer, bert_model, label2id, id2label

    logging.debug(f"Loading BERT model from local directory: {model_dir}")

    model_dir_path = Path(model_dir).resolve()
    if not model_dir_path.exists():
        error_message = f"BERT model directory not found at: {model_dir_path}"
        logging.error(error_message)
        raise FileNotFoundError(error_message)

    try:
        # 1. Load tokenizer
        bert_tokenizer = AutoTokenizer.from_pretrained(model_dir_path, local_files_only=True)
        logging.info(f"Loaded Tokenizer from: {model_dir_path}")

        # 2. Load model (let it load its own saved config and classifier)
        bert_model = AutoModelForTokenClassification.from_pretrained(model_dir_path, local_files_only=True)
        logging.info(f"Loaded ModelForTokenClassification from: {model_dir_path}")

        # 3. Extract label mappings from config
        config = bert_model.config
        label2id = config.label2id
        id2label = config.id2label

        # Log label mappings if available
        if label2id and id2label:
            logging.info(f"Label mappings loaded from config: {label2id}")
        else:
            logging.warning("Label mappings not found in config. You may need to define them manually.")

        logging.debug("BERT model and tokenizer loaded successfully.")
        return bert_model, bert_tokenizer

    except Exception as e:
        error_message = f"Failed to load BERT model from local directory: {str(e)}"
        logging.error(error_message)
        raise

def predict_sections(text):
    """
    Predicts the section labels for each token in the given text
    using the loaded BERT model for token classification.

    Args:
        text (str): The input text for section labeling.

    Returns:
        list or None: A list of predicted section labels for each token,
                     or None on error.
    """
    global bert_tokenizer, bert_model, id2label

    try:
        if not text or len(text.strip()) == 0:
            logging.warning("Empty text provided. Returning None.")
            return None

        # Ensure the model and tokenizer are loaded
        if bert_tokenizer is None or bert_model is None:
            load_bert_model()

        # Tokenize the input text, returning word IDs and offsets
        inputs = bert_tokenizer(text, return_offsets_mapping=True, return_tensors="pt", truncation=True, max_length=512)

        # Perform token classification
        with torch.no_grad():
            outputs = bert_model(**inputs)
            logits = outputs.logits

        # Get the predicted class IDs for each token
        predicted_token_class_ids = torch.argmax(logits, dim=2).squeeze().tolist()

        # Map the predicted class IDs to their labels
        predicted_labels = [id2label.get(token_id, str(token_id)) for token_id in predicted_token_class_ids]

        logging.debug(f"Predicted section labels for text: '{text[:50]}...' are '{predicted_labels}'")
        return predicted_labels

    except Exception as e:
        logging.error(f"Error in predict_sections: {e}")
        return None

if __name__ == "__main__":
    try:
        # 1.  Make sure the path is correct
        local_model_dir = "path/to/your/bert_model"  # <--- UPDATE THIS PATH

        # Standalone test for the BERT model loaded from a local directory
        test_text = "This is an abstract.  Here is the introduction.  The literature review follows. We describe the methodology.  The results are presented.  A discussion of the results.  Finally, we conclude."
        model, tokenizer = load_bert_model(local_model_dir)
        predicted_sections = predict_sections(test_text)
        print("[DEBUG] Predicted sections successfully.")
        print(f"Predicted sections: {predicted_sections}")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
