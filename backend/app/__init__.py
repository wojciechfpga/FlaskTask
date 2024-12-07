from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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

    return app
