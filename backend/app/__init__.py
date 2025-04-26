from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  # Allow Angular frontend access
from .config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS (important for frontend connection)
    CORS(app)

    # Initialize database
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register Blueprints (routes)
    from .routes import upload_routes, query_routes, summary_routes, extract_routes, cluster_routes

    app.register_blueprint(upload_routes.bp, url_prefix="/upload")
    app.register_blueprint(query_routes.bp, url_prefix="/query")
    app.register_blueprint(summary_routes.bp, url_prefix="/summary")
    app.register_blueprint(extract_routes.bp, url_prefix="/extract")
    app.register_blueprint(cluster_routes.bp, url_prefix="/cluster")

    # Health check (optional: test if Flask is running)
    @app.route("/", methods=["GET"])
    def index():
        return "Flask backend is running!"

    # Important: Import models last (after db init)
    from . import models

    return app
