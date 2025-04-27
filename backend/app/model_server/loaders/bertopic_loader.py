import os
from bertopic import BERTopic

def load_bertopic_model():
    model_path = os.path.join('app', 'trained-models', 'bertopic_model')
    model = BERTopic.load(model_path)
    print("[DEBUG] Loading SBERT model from:", model_path)
    return model

def get_bertopic_topics(texts):
    model = load_bertopic_model()
    topics, _ = model.fit_transform(texts)
    return topics
