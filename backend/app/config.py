import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://user:password@host/database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HUGGINGFACE_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN') or 'your_huggingface_token'