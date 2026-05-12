#tag 2
#Wir importieren alle nötigen Werkzeuge für unsere API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path


###############################
### Note API Endpoints (Tag 2)
###############################


#---DATENMODELLE(Pydantic)---
# Hier definieren wir, wie unsere Daten aussehen sollen.
# FastAPI und Pydantic prüfen automatisch, ob die Eingaben der Nutzer dazu passen.
class NoteCreate(BaseModel):
    """das Modell für eine NEUE Notiz(Eingabe des Nutzers, noch ohne ID)"""
    title: str
    content: str
    # --- HAUSAUFGABE TASK 1: Kategorie-Feld hinzufügen ---
    category: str

class Note(BaseModel):
    """das Modell für eine GESPEICHERTE Notiz (Ausgabe der API, mit ID und Zeitstempel)"""
    id: int
    title: str
    content: str
    # --- HAUSAUFGABE TASK 1: Kategorie-Feld hinzufügen ---
    category: str
    created_at: str


# --- SPEICHER & DATENBANK-SETUP ---
# Da wir noch keine "echte" Datenbank wie SQL haben, speichern wir die Notizen
# in einer Liste im Arbeitsspeicher und parallel in einer JSON-Datei auf einer der Festplatte.

notes_db = []       #Unsere "In-Memory" Datenbank (Liste mit Notizen)
note_id_counter = 1        #Zähler, der jedem neuen Eintrag eine automatische ID gibt
NOTES_FILE = Path("data/notes.json")


# --- DATEI-FUNKTIONEN (Persistenz) ---

def load_notes():
    """Lädt die Notizen aus der JSON-Datei, wenn der Server startet."""
    global notes_db, note_id_counter    # Wir greifen auf die globalen Variablen zu

# Prüfen, ob die Datei überhaupt schon existiert
    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:  # WARUM 'R' UND F????
            data = json.load(f) #JSON-Text in Python-Daten(Dictionaries) umwandeln
            #Jedes Dictionary aus der Datei wieder in ein Note-Objekt umwandeln
            notes_db = [Note(**note) for note in data]

            # Den Zähler für die nächste ID aktualisieren (höchste ID + 1)
            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

    #return notes_db, note_id_counter


def save_notes():
    """Speichert die aktuellen Notizen aus dem Arbeitsspeicher in die JSON-Datei."""
    #NOTES_FILE.parent.mkdir(parents=True, exist_ok=True) #WAS BIST DU ????

    with open(NOTES_FILE, 'w') as f:
        # Alle Note-Objekte in Dictionaries umwandeln (für JSON nötig)
        notes_data = [note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)

# --- FASTAPI APP SETUP ---
# Hier erstellen wir die eigentliche API-Anwendung
app = FastAPI(
    title= "Applied Programming Course HS-Coburg",
    description="Simple note management API",
    version="1.0.0"
)      

#Wir rufen direkt beim Start die Lade-Funktion auf, damit alte Notizen nicht weg sind
load_notes()

# --- ENDPUNKTE (Routen) ---

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate) -> Note:
    """Erstellt eine neue Notiz und speichert sie.""" #doc-string
    global note_id_counter
# Wir erstellen ein neues Note-Objekt aus den Eingaben (inkl. Task 1: Kategorie)
    #notes_db, note_id_counter = load_notes() #WAS IST DAS??
    new_note = Note(
        id=note_id_counter,
        title=note.title,
        content=note.content,
        category = note.category, #--- HAUSAUFGABE TASK 1: Kategorie beim Erstellen übernehmen ---
        created_at=datetime.now(timezone.utc).isoformat()  #utc = universal time code 
    )

    notes_db.append(new_note) #zur internen Liste hinzufügen
    note_id_counter += 1     #Zähler für die nächste Notiz hochsetzen

    save_notes()    #in die notes.json Datei speichern, damit sie nicht verloren geht
    return new_note     #Die erstellte Notiz als Bestätigung zurückgeben

# im Terminal "uv run fastapi dev" und dann return drücken
# nicht zwei mal Execute auf website drücken

@app.get("/notes")
def list_notes() -> list[Note]:
    """Gibt eine Liste ALLER gespeicherten Notizen zurück"""
    #notes_db, counter = load_notes()
    return notes_db


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    """Sucht und gibt eine ganz bestimmte Notiz anhand ihrer ID zurück."""
    for note in notes_db:
        if note.id == note_id:
            return note # Notiz gefunden -> zurückgeben
    
    # Wenn die Schleife durchläuft ohne etwas zu finden, geben wir einen 404 Fehler aus
    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )
#ich führe eine Daten-Migration durch in notes.json durch und füge meine Kategorie ein!!! sonst ERROR sonst kann ich kein 'category' einfügen ODER Datei löschen

# ==========================================
# --- HAUSAUFGABE TASK 2: Filter by Category ---
# ==========================================
@app.get("/notes/category/{category}")
def get_notes_by_category(category: str):
    """Gibt alle Notizen zurück, die zu einer bestimmten Kategorie gehören."""
    filtered_notes = [] # Eine leere Liste für die Ergebnisse
    
    for note in notes_db:
        # Wenn die Kategorie der Notiz mit der gesuchten übereinstimmt...
        if note.category == category:
            filtered_notes.append(note) # ...fügen wir sie zur Ergebnis-Liste hinzu
            
    return filtered_notes

# ==========================================
# --- HAUSAUFGABE TASK 3: Add Statistics Endpoint ---
# ==========================================
@app.get("/notes/stats")
def get_notes_stats():
    """Gibt Statistiken über die gespeicherten Notizen zurück."""
    categories = {} # Ein leeres Dictionary zum Zählen
    
    # Wir gehen jede Notiz durch
    for note in notes_db:
        # Wenn wir die Kategorie schon kennen, zählen wir +1
        if note.category in categories:
            categories[note.category] += 1
        # Wenn die Kategorie neu ist, setzen wir den Zähler auf 1
        else:
            categories[note.category] = 1
            
    # Wir geben ein Dictionary zurück, das FastAPI in JSON umwandelt
    return {
        "total_notes": len(notes_db), # Anzahl ALLER Notizen
        "by_category": categories     # Die gezählten Kategorien
    }

# ==========================================
# --- HAUSAUFGABE BONUS: Delete Endpoint ---
# ==========================================
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    """Löscht eine bestimmte Notiz anhand ihrer ID."""
    # enumerate() gibt uns gleichzeitig den Index (i) und die Notiz in der Liste
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i) # Entfernt das Element an der Stelle 'i' aus der Liste
            save_notes()    # Datei aktualisieren, damit es auch auf der Festplatte weg ist
            return {"message": "Note deleted"}
            
    # Wenn wir die ID nicht finden, Fehler 404 werfen
    raise HTTPException(status_code=404, detail="Note not found")



