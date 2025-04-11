from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2')  # Or your chosen model

def get_embedding(text):
    return model.encode(text).tolist()