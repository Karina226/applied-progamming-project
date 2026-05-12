import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool  # WICHTIG für In-Memory-Tests!
from main import app, get_session

# --- TEST DATENBANK SETUP ---
# Wir nutzen eine RAM-Datenbank. Der StaticPool sorgt dafür, dass die 
# Tabellen während des gesamten Tests im Arbeitsspeicher festgehalten werden!
sqlite_url = "sqlite://" 
engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Hier ist der Magic-Fix!
)

# Diese Funktion überschreibt die normale get_session() aus unserer main.py
def override_get_session():
    with Session(engine) as session:
        yield session

# Wir teilen FastAPI mit, dass es für die Datenbankverbindung unsere Test-Funktion nutzen soll
app.dependency_overrides[get_session] = override_get_session

# Unser Client für die virtuellen HTTP-Requests
client = TestClient(app)

# Fixture: Wird vor JEDEM Test automatisch ausgeführt
@pytest.fixture(autouse=True)
def setup_and_teardown():
    # 1. Erstelle alle Tabellen frisch
    SQLModel.metadata.create_all(engine)
    yield
    # 2. Lösche alle Tabellen nach dem Test wieder
    SQLModel.metadata.drop_all(engine)


# --- DIE TESTS ---

def test_read_empty_notes():
    """Testet, ob die Liste am Anfang bei einer leeren Datenbank wirklich leer ist."""
    response = client.get("/notes")
    assert response.status_code == 200
    assert response.json() == []

def test_create_note():
    """Testet die erfolgreiche Erstellung einer Notiz mit allen geforderten Feldern."""
    valid_data = {
        "title": "Prüfungsvorbereitung",
        "content": "Alles lernen für WINF 2.0",
        "category": "school",
        "tags": ["wichtig", "klausur"]
    }
    
    response = client.post("/notes", json=valid_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Prüfungsvorbereitung"
    assert data["category"] == "school"
    assert "wichtig" in data["tags"]
    assert "id" in data

def test_create_note_validation_error():
    """Testet, ob unsere strikte Pydantic-Validierung funktioniert."""
    invalid_data = {
        "title": "Test Notiz",
        "content": "Ein bisschen Text",
        "category": "falsche_kategorie_gibt_es_nicht",
        "subject": "Das sollte einen Fehler werfen",
        "tags": []
    }
    
    response = client.post("/notes", json=invalid_data)
    
    # Da die Validierung fehlschlägt, erwarten wir einen 422 Fehler
    assert response.status_code == 422