from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicjalizacja bazy danych
    db.init_app(app)

    # Rejestracja blueprintów
    from app.routes import bp as room_blueprint
    app.register_blueprint(room_blueprint, url_prefix='/api')

    # Komenda CLI do inicjalizacji bazy danych
    @app.cli.command("init-db")
    def init_db():
        """Komenda CLI do inicjalizacji bazy danych."""
        with app.app_context():  # Użyj kontekstu aplikacji
            from app.db import initialize_database
            initialize_database()

    return app
