from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient
import logging
from config import Config
import flask_monitoringdashboard as dashboard

db = SQLAlchemy()
migrate = Migrate()

# Niestandardowy handler do logowania w MongoDB
class MongoHandler(logging.Handler):
    """Custom logging handler to write logs to MongoDB."""
    def __init__(self, mongo_uri, database, collection):
        super().__init__()
        client = MongoClient(mongo_uri)
        self.collection = client[database][collection]

    def emit(self, record):
        log_entry = self.format(record)
        self.collection.insert_one({
            "log": log_entry,
            "level": record.levelname,
            "message": record.msg,
            "time": record.asctime,
        })

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    dashboard.config.init_from(file='../config.cfg')

    # Inicjalizacja bazy danych
    db.init_app(app)

    # Rejestracja blueprintów
    from app.blueprints.room_blueprint import bp as room_bp
    from app.blueprints.reservation_blueprint import bp as reservation_bp
    from app.blueprints.auth_blueprint import bp as auth_bp
    app.register_blueprint(room_bp, url_prefix='/api')
    app.register_blueprint(reservation_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")

    # Swagger UI
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'  # Ścieżka do pliku JSON z opisem API
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Conference Room Booking API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Komenda CLI do inicjalizacji bazy danych
    @app.cli.command("init-db")
    def init_db():
        """Komenda CLI do inicjalizacji bazy danych."""
        with app.app_context():  # Użyj kontekstu aplikacji
            from app.db import initialize_database
            initialize_database()

    # Konfiguracja logowania do MongoDB
    mongo_uri = app.config.get("MONGO_URI", "mongodb://localhost:27017")
    mongo_handler = MongoHandler(mongo_uri, "logs", "app_logs")
    mongo_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    mongo_handler.setFormatter(formatter)

    # Dodanie MongoHandler do logera aplikacji
    app.logger.addHandler(mongo_handler)

    # Przykładowe logi
    app.logger.info("Aplikacja Flask została uruchomiona.")

    dashboard.bind(app)
    return app
