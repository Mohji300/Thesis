from sentence_transformers import SentenceTransformer

model = SentenceTransformer('../trained-models/sbert')

def get_embedding(text):
    return model.encode(text).tolist()