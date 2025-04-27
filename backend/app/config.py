import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "11c0632d-42dd-42da-9947-7e2904e474ecLD5GwZ6tPeeUEPUrWr/z6A=="
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://root:DevPass09078010@localhost/Thesis_Docs"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    """ HUGGINGFACE_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN') or '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' """