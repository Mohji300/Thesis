import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForTokenClassification, PretrainedConfig
import torch

# Global variables for the NER model and tokenizer
ner_tokenizer = None
ner_model = None

def load_ner_model():
    """
    Loads the NER model and tokenizer from the specified directory.

    Returns:
        tuple: A tuple containing the tokenizer and model.
    """
    global ner_tokenizer, ner_model

    # Build the path to the model directory
    model_dir = Path('app') / 'trained-models' / '4ner_model'

    # Convert to absolute path and ensure it exists
    model_dir = model_dir.resolve()

    if not model_dir.exists():
        raise FileNotFoundError(f"NER model directory not found at: {model_dir}")

    print(f"[DEBUG] Loading NER model from: {model_dir}")

    try:
        model_path_str = str(model_dir)

        # Load configuration explicitly
        config = PretrainedConfig.from_pretrained(model_path_str, local_files_only=True)

        # Load tokenizer
        ner_tokenizer = AutoTokenizer.from_pretrained(
            model_path_str,
            config=config,
            local_files_only=True
        )

        # Load model
        ner_model = AutoModelForTokenClassification.from_pretrained(
            model_path_str,
            config=config,
            local_files_only=True
        )

        print("[DEBUG] NER model and tokenizer loaded successfully.")

    except Exception as e:
        print(f"[ERROR] Failed to load NER model: {str(e)}")
        raise

def get_entities(text):
    """
    Extracts named entities from the given text using the loaded NER model.

    Args:
        text (str): The input text for named entity recognition.

    Returns:
        list: A list of named entities extracted from the text.
    """
    try:
        if not text or len(text.strip()) == 0:
            print("[WARNING] Empty text provided. Returning an empty list.")
            return []

        # Ensure the model and tokenizer are loaded
        if ner_tokenizer is None or ner_model is None:
            load_ner_model()

        # Tokenize the input text
        inputs = ner_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

        # Perform named entity recognition
        outputs = ner_model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)

        # Decode the entities
        tokens = ner_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        entities = []
        for token, prediction in zip(tokens, predictions[0].tolist()):
            if prediction != 0:  # Assuming 0 is the label for "no entity"
                entity_label = ner_model.config.id2label[prediction]
                entities.append({"entity": entity_label, "token": token})

        return entities

    except Exception as e:
        print(f"[ERROR] Error in get_entities: {e}")
        raise

""" if __name__ == "__main__":
    try:
        # Standalone test for the NER model
        test_text = "Barack Obama was the 44th President of the United States."
        load_ner_model()
        entities = get_entities(test_text)
        print("[DEBUG] Entities extracted successfully.")
        print(entities)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}") """