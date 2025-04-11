from bertopic import BERTopic

bertopic_model = BERTopic.load("my_bertopic_model")  # Replace with your model path

def get_topics(embeddings):
    topics, _ = bertopic_model.transform(embeddings)
    return topics.tolist()