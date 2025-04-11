from bertopic import BERTopic

bertopic_model = BERTopic.load("../trained-models/bertopic-model/bertopic_model") 

def get_topics(embeddings):
    topics, _ = bertopic_model.transform(embeddings)
    return topics.tolist()