import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "YHA2RRuKq5Guny1iCXBgwA=="
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://root:passwordjologs19@localhost/thesis_docs"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    """ HUGGINGFACE_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN') or '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' """