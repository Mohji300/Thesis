from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config  # Use your original config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

# Model Imports (Load local models once at startup)
from app.model_server.loaders.sbert_loader import load_sbert_model
from app.model_server.loaders.bart_loader import load_bart_model
from app.model_server.loaders.ner_loader import load_ner_model
from app.model_server.loaders.bertopic_loader import load_bertopic_model

# Global model variables
sbert_model = None
bart_model = None
ner_model = None
bertopic_model = None

def create_app(config_class=Config):
    global sbert_model, bart_model, ner_model, bertopic_model

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for frontend
    CORS(app)

    # Initialize database
    db.init_app(app)
    migrate.init_app(app)

    # ==== Load Models at Startup ====
    sbert_model = load_sbert_model()
    bart_model = load_bart_model()
    ner_model = load_ner_model()
    bertopic_model = load_bertopic_model()

    print("Models loaded successfully!")

    # ==== Register Blueprints ====
    from .routes import upload_routes, query_routes, summary_routes, extract_routes, cluster_routes

    app.register_blueprint(upload_routes.bp, url_prefix="/upload")
    app.register_blueprint(query_routes.bp, url_prefix="/query")
    app.register_blueprint(summary_routes.bp, url_prefix="/summary")
    app.register_blueprint(extract_routes.bp, url_prefix="/extract")
    app.register_blueprint(cluster_routes.bp, url_prefix="/cluster")

    # Health check
    @app.route("/", methods=["GET"])
    def index():
        return "Flask backend (with local models) is running!"

    # Import models AFTER db is initialized
    from . import models

    return app
