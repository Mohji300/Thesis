import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForTokenClassification, PretrainedConfig, BertConfig  # Import BertConfig
import torch
import logging

# Configure logging (if not already configured elsewhere)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables for the BERT model and tokenizer
bert_tokenizer = None
bert_model = None
label2id = None
id2label = None

def load_bert_model(model_dir=None):
    """
    Loads the BERT model and tokenizer for TOKEN classification
    from the specified directory.

    Args:
        model_dir (str or Path, optional): The directory containing the BERT model. Defaults to None.

    Returns:
        tuple: A tuple containing the tokenizer and model.
    """
    global bert_tokenizer, bert_model, label2id, id2label

    # Use the provided model_dir or default to the internal path
    if model_dir is None:
        model_dir = Path('app') / 'trained-models' / 'bert_model'

    # Convert to absolute path and ensure it exists
    model_dir = Path(model_dir).resolve()

    if not model_dir.exists():
        error_message = f"BERT section extraction model directory not found at: {model_dir}"
        logging.error(error_message)
        raise FileNotFoundError(error_message)

    logging.debug(f"Loading BERT section extraction model from: {model_dir}")

    try:
        model_path_str = str(model_dir)

        # Load configuration explicitly
        config = BertConfig.from_pretrained(model_path_str, local_files_only=True)

        # Load tokenizer
        bert_tokenizer = AutoTokenizer.from_pretrained(
            model_path_str,
            config=config,
            local_files_only=True
        )

        # Load model for TOKEN classification
        bert_model = AutoModelForTokenClassification.from_pretrained(
            model_path_str,
            config=config,
            local_files_only=True
        )

        # Load label mappings from config if available
        if hasattr(bert_model.config, "label2id") and hasattr(bert_model.config, "id2label"):
            label2id = bert_model.config.label2id
            id2label = bert_model.config.id2label
            logging.debug(f"Loaded label mappings: label2id={label2id}, id2label={id2label}")
        else:
            logging.warning("Label mappings (label2id, id2label) not found in model config.")
            # Define label mappings if they are not in the config
            unique_labels = ['Abstract', 'Introduction', 'Literature Review', 'Methodology', 'Results', 'Discussion', 'Conclusion']  # Example labels, change as needed
            label2id = {label: i for i, label in enumerate(unique_labels)}
            id2label = {i: label for label, i in label2id.items()}
            bert_model.config.label2id = label2id
            bert_model.config.id2label = id2label
            config.num_labels = len(unique_labels)
            logging.info(f"Inferred label mappings: label2id={label2id}, id2label={id2label}")

        logging.debug("BERT section extraction model and tokenizer loaded successfully.")

    except Exception as e:
        error_message = f"Failed to load BERT section extraction model: {str(e)}"
        logging.error(error_message)
        raise

def predict_section(text):
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
            raise RuntimeError("BERT model or tokenizer not loaded.")

        # Tokenize input text and separate model inputs from offset_mapping
        encoding = bert_tokenizer(
            text,
            return_offsets_mapping=True,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        inputs = {
            "input_ids": encoding["input_ids"],
            "attention_mask": encoding["attention_mask"],
        }

        # Forward pass without offset_mapping
        with torch.no_grad():
            outputs = bert_model(**inputs)
            logits = outputs.logits

        # Get predictions
        predicted_token_class_ids = torch.argmax(logits, dim=2).squeeze().tolist()

        # Convert predictions to labels
        predicted_labels = [id2label.get(token_id, str(token_id)) for token_id in predicted_token_class_ids]

        logging.debug(f"Predicted section labels for text: '{text[:50]}...' are '{predicted_labels}'")
        return predicted_labels

    except Exception as e:
        logging.error(f"Error in predict_sections: {e}")
        return None

