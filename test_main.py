from fastapi.testclient import TestClient
from main import app

# Wir nutzen den TestClient von FastAPI für unsere automatisierten Tests
client = TestClient(app)

def test_read_empty_notes():
    # Testet, ob die Liste am Anfang leer ist
    response = client.get("/notes")
    assert response.status_code == 200
    assert response.json() == []

def test_create_note():
    # Testet das Anlegen einer Notiz
    response = client.post(
        "/notes",
        json={"subject": "WINF", "content": "Prüfungsvorbereitung"}
    )
    assert response.status_code == 200
    assert response.json()["subject"] == "WINF"
    assert response.json()["id"] == 1