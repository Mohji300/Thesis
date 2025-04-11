from app import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    document_metadata = db.Column(db.JSON)  # Renamed attribute
    summary = db.Column(db.Text)
    entities = db.Column(db.JSON)
    embeddings = db.Column(db.JSON)
    topics = db.Column(db.JSON)

    def __repr__(self):
        return f'<Document {self.title}>'