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

def load_bert_model(model_dir=None):
    global bert_tokenizer, bert_model, label2id, id2label

    if model_dir is None:
        model_dir = Path("app/trained-models/bert_model")

    model_dir = Path(model_dir).resolve()

    if not model_dir.exists():
        raise FileNotFoundError(f"BERT model directory not found at: {model_dir}")
    
    logging.info(f"Loading BERT model from: {model_dir}")

    try:
        config = BertConfig.from_pretrained(model_dir, local_files_only=True)

        # Load tokenizer
        bert_tokenizer = AutoTokenizer.from_pretrained(model_dir, config=config, local_files_only=True)

        # Load model
        bert_model = AutoModelForTokenClassification.from_pretrained(model_dir, config=config, local_files_only=True)

        # Load label mappings or define fallback
        if hasattr(bert_model.config, "label2id") and bert_model.config.label2id:
            label2id = bert_model.config.label2id
            id2label = bert_model.config.id2label
        else:
            logging.warning("label2id/id2label not found in config. Defining manually.")
            unique_labels = ['Abstract', 'Introduction', 'Literature Review', 'Methodology', 'Results', 'Discussion', 'Conclusion']
            label2id = {label: i for i, label in enumerate(unique_labels)}
            id2label = {i: label for label, i in label2id.items()}
            bert_model.config.label2id = label2id
            bert_model.config.id2label = id2label
            bert_model.config.num_labels = len(unique_labels)

        logging.info("BERT model and tokenizer loaded successfully.")
        return bert_model, bert_tokenizer

    except Exception as e:
        logging.error(f"Failed to load BERT model: {e}")
        raise

def extract_section(text, model_dir="app/trained-models/bert_model"):
    global bert_tokenizer, bert_model, id2label

    try:
        if not text.strip():
            logging.warning("Empty text received. Skipping prediction.")
            return None

        # Lazy-load the model if not already loaded
        if bert_model is None or bert_tokenizer is None:
            logging.warning("Model or tokenizer not initialized. Loading now...")
            load_bert_model(model_dir)

        encoding = bert_tokenizer(
            text,
            return_offsets_mapping=True,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        # Don't pass offset_mapping to the model
        inputs = {
            "input_ids": encoding["input_ids"],
            "attention_mask": encoding["attention_mask"],
        }

        with torch.no_grad():
            outputs = bert_model(**inputs)
            logits = outputs.logits

        predicted_token_class_ids = torch.argmax(logits, dim=2).squeeze().tolist()
        predicted_labels = [id2label.get(idx, str(idx)) for idx in predicted_token_class_ids]

        logging.debug(f"Predicted section labels: {predicted_labels}")
        return predicted_labels

    except Exception as e:
        logging.error(f"Error in extract_sections: {e}")
        return None
