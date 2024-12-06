from app import create_app, db
from flask_migrate import Migrate

# Inicjalizacja aplikacji i migracji
app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
