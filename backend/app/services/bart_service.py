import logging
from pathlib import Path
from transformers import BartTokenizer, BartForConditionalGeneration

def load_bart_model():
    """
    Loads the BART model and tokenizer from the specified directory.

    Returns:
        dict: A dictionary containing the BART model and tokenizer.
    """
    # Build the path to the BART model directory
    model_dir = Path('app') / 'trained-models' / 'bart_model'

    # Convert to absolute path and ensure it exists
    model_dir = model_dir.resolve()

    if not model_dir.exists():
        raise FileNotFoundError(f"BART model directory not found at: {model_dir}")

    print(f"[DEBUG] Loading BART model from: {model_dir}")

    try:
        # Load the BART tokenizer and model
        tokenizer = BartTokenizer.from_pretrained(str(model_dir))
        model = BartForConditionalGeneration.from_pretrained(str(model_dir))
        return {"tokenizer": tokenizer, "model": model}

    except Exception as e:
        print(f"[ERROR] Failed to load BART model: {str(e)}")
        raise

def clean_text(text):
    # This removes invalid surrogate pairs and non-UTF-8 encodable characters
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")

def summarize_text(text, max_length=150):
    """
    Summarizes the given text using the locally loaded BART model.

    Args:
        text (str): The input text to summarize.
        max_length (int): The maximum length of the summary.

    Returns:
        str: The summarized text.
    """
    try:
        if not text or len(text.split()) < 20:
            print("[WARNING] Text too short to summarize. Returning original text.")
            return text

        # Clean the text to remove surrogate characters
        text = clean_text(text)

        # Load the BART model and tokenizer
        bart = load_bart_model()
        tokenizer = bart["tokenizer"]
        model = bart["model"]

        # Tokenize the input text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)

        # Generate the summary
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=30,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )

        # Decode the generated summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary

    except Exception as e:
        print(f"[ERROR] Error in summarize_text: {e}")
        raise

""" if __name__ == "__main__":
    try:
        # Standalone test for the BART model
        test_text = "This is a test text for summarization. It contains enough words to generate a meaningful summary."
        summary = summarize_text(test_text)
        print("[DEBUG] Summary generated successfully.")
        print(summary)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}") """