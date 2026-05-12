# ============================================================================
# DAY 4: Advanced API Features
# ============================================================================
# Goal: Write and run tests for our APIs
#       - Use pytest to write unit tests for our API endpoints
#       - Use FastAPI's TestClient to simulate API requests
#       - Use Requests library to test API endpoints from outside the app
# Topics: Testing FastAPI applications, pytest, TestClient, Requests library
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
from pathlib import Path

# Create FastAPI application
app = FastAPI(
    title="Applied Programming Course API",
    description="Reference implementation for Day 4",
    version="1.0.0"
)

# ----------------------------------------------------------------------------
# PYDANTIC MODELS
# ----------------------------------------------------------------------------

class GreetingResponse(BaseModel):
    """Response model for greeting endpoints

    Attributes:
        message (str): The greeting message to be returned to the client
    """
    message: str

# ----------------------------------------------------------------------------
# DAY 4: API ENDPOINTS FOR TESTING
# ----------------------------------------------------------------------------

@app.get("/", response_model=GreetingResponse)
def read_root():
    """Welcome endpoint - returns greeting message"""
    return {"message": "Hello World!"}




@app.get("/greetings/{name}", response_model=GreetingResponse)
def read_greeting(name: str):
    """Personalized greeting endpoint - returns greeting message with name"""
    return {"message": f"Hello {name}!"}


# ----------------------------------------------------------------------------
# BUGGY ENDPOINT - For Teaching Purposes
# ----------------------------------------------------------------------------

@app.get("/is-adult/{age}")
def check_adult(age: int):
    """
    Check if person is an adult (18 or older)
    Example: /is-adult/17
    """
    is_adult = age > 18

    return {
        "age": age,
        "is_adult": is_adult,
        "can_vote": is_adult,
        "can_drive": is_adult
    }

# ----------------------------------------------------------------------------
# DAY 4: COURSE API (POST Endpoints & File Persistence)
# ----------------------------------------------------------------------------

class CourseCreate(BaseModel):
    """Modell für das Erstellen eines Kurses (Input vom Nutzer, noch ohne ID)"""
    code: str
    name: str
    semester: int
    ects: int
    lecturer: str

class Course(BaseModel):
    """Modell für den fertigen Kurs (Output, inklusive ID)"""
    id: int
    code: str
    name: str
    semester: int
    ects: int
    lecturer: str

# Dateipfad für die Datenspeicherung
COURSES_FILE = Path("courses.json")

def load_courses():
    """Lädt die Kurse aus der JSON-Datei und berechnet die nächste freie ID."""
    courses_db = []
    course_id_counter = 1
    
    if COURSES_FILE.exists():
        with open(COURSES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            courses_db = [Course(**course) for course in data]
            
            if courses_db:
                course_id_counter = max(c.id for c in courses_db) + 1
                
    return courses_db, course_id_counter

def save_courses(courses_db):
    """Speichert die Kurse als JSON ab."""
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        courses_data = [course.dict() for course in courses_db]
        json.dump(courses_data, f, indent=2, ensure_ascii=False)


@app.post("/courses", status_code=201)
def create_course(course: CourseCreate) -> Course:
    """Erstellt einen neuen Kurs und speichert ihn in der Datei."""
    courses_db, course_id_counter = load_courses()
    
    # Check auf Duplikate: Gibt es den Kurs-Code schon?
    for existing in courses_db:
        if existing.code.upper() == course.code.upper():
            raise HTTPException(
                status_code=409,
                detail=f"Course with code '{course.code}' already exists"
            )
            
    # Neuen Kurs anlegen (**course.dict() entpackt alle Felder automatisch)
    new_course = Course(
        id=course_id_counter,
        **course.dict()
    )
    
    courses_db.append(new_course)
    save_courses(courses_db)
    
    return new_course


@app.get("/courses")
def list_courses(semester: int = None, min_ects: int = 0) -> list[Course]:
    """Gibt alle Kurse zurück, optional gefiltert nach Semester und ECTS."""
    courses_db, _ = load_courses()
    
    filtered = courses_db
    
    # Filter anwenden
    if semester is not None:
        filtered = [c for c in filtered if c.semester == semester]
        
    if min_ects > 0:
        filtered = [c for c in filtered if c.ects >= min_ects]
        
    return filtered
 