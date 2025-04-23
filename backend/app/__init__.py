from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import upload_routes, query_routes
    app.register_blueprint(upload_routes.bp, url_prefix="/upload")
    app.register_blueprint(query_routes.bp, url_prefix="/query")

    #added for testing
    @app.route("/", methods=["GET"])
    def index():
        return "Flask backend is running!"

    return app

from . import models  # Import models to register them with SQLAlchemy