# Zadanie rekrutacyjne: System zarządzania rezerwacjami sal konferencyjnych

### Opis projektu
Twoim zadaniem jest stworzenie systemu do zarządzania rezerwacjami sal konferencyjnych w biurowcu. System powinien umożliwiać pracownikom przeglądanie dostępności sal, dokonywanie rezerwacji oraz zarządzanie już istniejącymi rezerwacjami.

### Wymagania techniczne
- Frontend: Next.js 14 (App Router)
- Backend: Python (Flask)
- Baza danych: PostgreSQL
- API: REST
- Autoryzacja: JWT
- Testy: Jest (frontend) i pytest (backend)

### Funkcjonalności do zaimplementowania

#### Backend (Python/Flask)
1. API do zarządzania salami konferencyjnymi:
   - CRUD dla sal konferencyjnych
   - Endpoint zwracający dostępność sal w zadanym przedziale czasowym
   - System rezerwacji z obsługą konfliktów czasowych
   - Walidacja dat i godzin rezerwacji
   
2. System autoryzacji:
   - Rejestracja i logowanie użytkowników
   - Generowanie i walidacja JWT
   - Role użytkowników (admin, user)

3. Baza danych:
   - Modelowanie relacji między salami, rezerwacjami i użytkownikami
   - Implementacja soft delete
   - Indeksy dla optymalizacji zapytań

#### Frontend (Next.js)
1. Interfejs użytkownika:
   - Responsywny kalendarz z widokiem tygodniowym/miesięcznym
   - Drag & drop dla tworzenia/modyfikacji rezerwacji
   - Filtrowanie sal po parametrach (pojemność, wyposażenie)
   
2. Zarządzanie stanem:
   - Implementacja cache'owania z wykorzystaniem React Query
   - Obsługa formularzy z React Hook Form
   - Stan globalny (można użyć Zustand lub Redux)

3. Funkcje administracyjne:
   - Panel admina do zarządzania salami
   - Raporty wykorzystania sal
   - Eksport danych do xlsx

### Wymagania dodatkowe
1. **Optymalizacja wydajności:**
   - Implementacja paginacji i infinite scroll
   - Lazy loading komponentów
   - Optymalizacja zapytań do bazy danych

2. **Testy:**
   - Min. 80% pokrycia testami jednostkowymi
   - Testy integracyjne dla kluczowych funkcjonalności
   - Testy E2E dla głównych ścieżek użytkownika

3. **Dokumentacja:**
   - API documentation (Swagger/OpenAPI)
   - README z instrukcją instalacji i uruchomienia
   - Dokumentacja techniczna głównych komponentów

### Punkty dodatkowe
- Implementacja powiadomień real-time (WebSocket)
- CI/CD pipeline
- Konteneryzacja (Docker)
- Monitoring i logowanie (np. Sentry)
- Obsługa wielu języków (i18n)

### Kryteria oceny
1. **Architektura i wzorce projektowe (30%)**
   - Czysty kod i przestrzeganie zasad SOLID
   - Odpowiednia separacja warstw
   - Przemyślana struktura projektu

2. **Jakość kodu (25%)**
   - Czytelność i maintainability
   - Obsługa błędów
   - Nazewnictwo zmiennych i funkcji

3. **Wydajność i skalowalność (20%)**
   - Optymalizacja zapytań
   - Cachowanie
   - Indeksowanie bazy danych

4. **Testy (15%)**
   - Pokrycie testami
   - Jakość testów
   - Scenariusze testowe

5. **Dokumentacja i inne aspekty (10%)**
   - Kompletność dokumentacji
   - Historia commitów
   - Dodatkowe funkcjonalności

### Sposób dostarczenia
1. Kod źródłowy w repozytorium Git (GitHub/GitLab)
2. Dokumentacja w README.md
3. Instrukcja instalacji i uruchomienia
4. Opcjonalnie: działające demo

### Uwagi końcowe
- Zwróć szczególną uwagę na bezpieczeństwo aplikacji
- Zadbaj o obsługę edge cases
- Pamiętaj o walidacji danych wejściowych
- Zastosuj dobre praktyki Git (conventional commits)