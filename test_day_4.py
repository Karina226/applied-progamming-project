import pytest
import requests
from faker import Faker


name_faker = Faker()

BASE_URL = "http://localhost:8000"

def test_read_root():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World!"

def test_check_404_error():
    response = requests.get(f"{BASE_URL}/nonexistent")
    assert response.status_code == 404

def test_greetings():
    name = name_faker.first_name()
    response = requests.get (f"{BASE_URL}/greetings/{name}")

    assert response.status_code == 200
    data = response.json()
    assert data ["message"] == f"Hello {name}!"

    #uv add Faker bei terminal


#Hausaufgabe

import requests

BASE_URL = "http://127.0.0.1:8000"

# ==========================================
# --- 1. CRUD TESTS ---
# ==========================================

def test_create_note():
    note_data = {
        "title": "Test Note",
        "content": "Test content",
        "category": "Testing",
        "tags": ["test"]
    }
    response = requests.post(f"{BASE_URL}/notes", json=note_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Note"

def test_list_notes():
    response = requests.get(f"{BASE_URL}/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_note_by_id():
    create_resp = requests.post(f"{BASE_URL}/notes", json={"title": "Get Me", "content": "C", "category": "Test"})
    note_id = create_resp.json()["id"]
    
    response = requests.get(f"{BASE_URL}/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"

def test_update_note():
    create_resp = requests.post(f"{BASE_URL}/notes", json={"title": "Old", "content": "C", "category": "Test"})
    note_id = create_resp.json()["id"]
    
    update_data = {"title": "New Title", "content": "New C", "category": "New Cat", "tags": []}
    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_note():
    create_resp = requests.post(f"{BASE_URL}/notes", json={"title": "Delete Me", "content": "C", "category": "Test"})
    note_id = create_resp.json()["id"]
    
    response = requests.delete(f"{BASE_URL}/notes/{note_id}")
    assert response.status_code in [200, 204]
    assert requests.get(f"{BASE_URL}/notes/{note_id}").status_code == 404

# ==========================================
# --- 2. FILTER TESTS ---
# ==========================================

def test_filter_by_category():
    requests.post(f"{BASE_URL}/notes", json={"title": "Cat Test", "content": "C", "category": "SpecialCat"})
    response = requests.get(f"{BASE_URL}/notes?category=SpecialCat")
    assert response.status_code == 200
    for note in response.json():
        assert note["category"] == "SpecialCat"

def test_filter_by_search():
    requests.post(f"{BASE_URL}/notes", json={"title": "UniqueSearchTerm", "content": "C", "category": "Test"})
    response = requests.get(f"{BASE_URL}/notes?search=UniqueSearchTerm")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_filter_by_tag():
    requests.post(f"{BASE_URL}/notes", json={"title": "Tag Test", "content": "C", "category": "Test", "tags": ["UniqueTag"]})
    response = requests.get(f"{BASE_URL}/notes?tag=uniquetag")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_combined_filters():
    requests.post(f"{BASE_URL}/notes", json={"title": "Combo", "content": "C", "category": "ComboCat", "tags": ["combotag"]})
    response = requests.get(f"{BASE_URL}/notes?category=ComboCat&search=Combo&tag=combotag")
    assert response.status_code == 200

# ==========================================
# --- 3. ERROR CASES ---
# ==========================================

def test_create_note_missing_field():
    response = requests.post(f"{BASE_URL}/notes", json={"title": "Test"}) # Fehlt alles andere
    assert response.status_code == 422

def test_get_nonexistent_note():
    assert requests.get(f"{BASE_URL}/notes/999999").status_code == 404

def test_update_nonexistent_note():
    assert requests.put(f"{BASE_URL}/notes/999999", json={"title": "New", "content": "C", "category": "Cat"}).status_code == 404

def test_delete_nonexistent_note():
    assert requests.delete(f"{BASE_URL}/notes/999999").status_code == 404

# ==========================================
# --- 4. DAY 3 FEATURES ---
# ==========================================

def test_notes_statistics():
    response = requests.get(f"{BASE_URL}/notes/stats")
    assert response.status_code == 200
    assert "total_notes" in response.json()

def test_patch_note():
    resp = requests.post(f"{BASE_URL}/notes", json={"title": "Old", "content": "Old Content", "category": "Test"})
    note_id = resp.json()["id"]
    
    response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"title": "Patched Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Patched Title"
    assert response.json()["content"] == "Old Content"