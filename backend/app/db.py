from app import db
from app.models import Room  # Importuj modele

def initialize_database():
    """
    Funkcja do inicjalizacji bazy danych.
    Tworzy wszystkie tabele na podstawie modeli.
    """
    db.create_all()
    print("Baza danych została zainicjalizowana!")

    # Dodanie przykładowych danych
    if not Room.query.first():  # Sprawdź, czy tabela jest pusta
        example_room = Room(name="Sala Konferencyjna 1", capacity=10)
        db.session.add(example_room)
        db.session.commit()
        print("Dodano przykładową salę do bazy danych.")
