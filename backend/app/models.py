from app import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    document_metadata = db.Column(db.JSON)  # Metadata about the document
    summary = db.Column(db.Text)
    sections = db.Column(db.JSON)  # Stores sections predicted by BERT
    embeddings = db.Column(db.JSON)  # Stores embeddings for the document
    topics = db.Column(db.JSON)  # Stores topics for the document
    author = db.Column(db.String(255))  # Author of the document
    year = db.Column(db.String(10))  # Year of publication

    def __repr__(self):
        return f'<Document {self.title}>'