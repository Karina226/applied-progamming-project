from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select, or_, col
from pydantic import BaseModel, Field as PydanticField, field_validator, model_validator, ConfigDict
from typing import List, Optional, Annotated
from typing_extensions import Self
from datetime import datetime
import re

# ===============================================
# 1. DATENBANK-KONFIGURATION (SQLModel & SQLite)
# ===============================================
# SQLModel kombiniert SQLAlchemy (Datenbank) mit Pydantic (Validierung).

sqlite_file_name = "notes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
# check_same_thread = False ist für SQLite in Verbindung mit FastAPI notwendig.
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    # Erzeugt die physische Datenbankdatei und alle definierten Tabellen.
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Lifespan-Event: Alles hier drin wird beim Starten der API einmalig ausgeführt.
    #Ideal, um die Datenbankverbindung zu prüfen oder Tabellen zu erstellen.
    create_db_and_tables()
    yield

# Initialisierung der FastAPI-Instanz
app = FastAPI(lifespan=lifespan, title="Notes API", version="2.0.0")

def get_session():
    # Erstellt eine Datenbank-Session für die Dauer eines API-Aufrufs.
    # Wird nach dem Aufruf automatisch geschlossen (Dependency Injection).
    with Session(engine) as session:
        yield session

# SessionDep ist ein Anlass, um den Code in den Endpunkten übersichtlicher zu halten.
SessionDep = Annotated[Session, Depends(get_session)]

# ================================================
# 2. DATENBANK-MODELLE (Relationale Strukur)
# ================================================
# Hier definieren wir in die Tabellen für SQLite.

class NoteTagLink(SQLModel, table=True):
    # Die Verknüpfungstabelle (Link-Table) für eine Many-to-Many Beziehung.
    # Sie verbindet Notizen mit Tags über deren IDs.
    note_id: Optional[int] = Field(default=None, foreign_key="notes.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)

class Tag(SQLModel, table=True):
    # Speichert die Schlagwörter (tags) zentral ab, um Redundanz zu vermeiden.
    __tablename__ = "tags"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    notes: List["Note"] = Relationship(back_populates="tags", link_model=NoteTagLink)

class Note(SQLModel, table=True):
    # Das Haupt-Modell für eine Notiz.
    __tablename__ = "notes"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Relationship verbindet Notizen über die Link-Tabelle mit den Tags.
    tags: List[Tag] = Relationship(back_populates="notes", link_model=NoteTagLink)

# =============================================================
# 3. VALIDIERUNGS-MODELLE (Pydantic V2)
# =============================================================
# Pydantic prüft die Daten, BEVOR sie die Datenbank erreichen.

class NoteCreate(BaseModel):
    #Regeln für die Erstellung einer Notiz über POST.
    # str_strip_whitespace: Entfernt automatisch Leerzeichen am Rand.
    # extra="forbid": Verhindert, dass zusätzliche, unbekannte Felder gesendet werden.
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    title: str = PydanticField(min_length=3, max_length=100)
    content: str = PydanticField(min_length=1, max_length=10000)
    category: str = PydanticField(min_length=2, max_length=30, pattern=r"^[a-z]+$")
    tags: List[str] = PydanticField(default_factory=list, max_length=10)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        # Stellt sicher, dass nur erlaubte Kategorien verwendet werden.
        allowed = {"work", "personal", "school", "ideas", "general"}
        v_lower = v.lower()
        if v_lower not in allowed:
            raise ValueError(f"Category must be one of {allowed}")
        return v_lower

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw: List[str]) -> List[str]:
        cleaned = []
        seen = set()
        for tag in raw:
            t = tag.lower()
            if len(t) < 2:
                raise ValueError("Tags must be at least 2 chars long")
            if not re.match(r"^[a-z0-9-]+$", t):
                raise ValueError("Tags must contain only lowercase letters, numbers, and dashes")
            if t not in seen:
                seen.add(t)
                cleaned.append(t)
        return cleaned

    @model_validator(mode="after")
    def work_notes_need_work_tag(self) -> Self:
        if self.category == "work" and "work" not in self.tags:
            raise ValueError("work notes must include the 'work' tag")
        return self

class NoteUpdate(BaseModel):
    # Definiert, wie die Daten an das Frontend (Streamlit) gesendet werden.
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    title: Optional[str] = PydanticField(default=None, min_length=3, max_length=100)
    content: Optional[str] = PydanticField(default=None, min_length=1, max_length=10000)
    category: Optional[str] = PydanticField(default=None, min_length=2, max_length=30, pattern=r"^[a-z]+$")
    tags: Optional[List[str]] = PydanticField(default=None, max_length=10)

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: List[str]
    created_at: str
    
    class Config:
        from_attributes = True

# ====================================
# 4. API-ENDPUNKTE (Business Logic)
# ====================================

@app.post("/notes", status_code=201, response_model=NoteResponse)
def create_note(note: NoteCreate, session: SessionDep):
    # Erstellt eine neue Notiz. Tags werden gesucht und verknüpft oder neu angelegt.
    db_note = Note(title=note.title, content=note.content, category=note.category)
    
    tag_objects = []
    for tag_name in note.tags:
        statement = select(Tag).where(Tag.name == tag_name)
        existing_tag = session.exec(statement).first()
        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            # Falls nicht vorhanden: Neuen Tag erstellen.
            new_tag = Tag(name=tag_name)
            session.add(new_tag)
            tag_objects.append(new_tag)
            
    db_note.tags = tag_objects
    session.add(db_note)
    session.commit() # Speichert die Änderungen dauerhaft in der notes.db.
    session.refresh(db_note) # Lädt die generierte ID zurück in das Objekt.
    
    return format_note_response(db_note)

@app.get("/notes", response_model=List[NoteResponse])
def list_notes(
    # Listet Notizen auf. Unterstützt Filterung nach Kategorie und Volltextsuche.
    session: SessionDep,
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None
):
    statement = select(Note)
    
    # Filterung direkt auf SQL-Ebene (Performant).
    if category:
        statement = statement.where(Note.category == category)
    if search:
        search_lower = search.lower()
        statement = statement.where(
            or_(
                col(Note.title).ilike(f"%{search_lower}%"),
                col(Note.content).ilike(f"%{search_lower}%")
            )
        )
    if tag:
        tag_lower = tag.lower()
        statement = statement.join(Note.tags).where(Tag.name == tag_lower)
    if created_after:
        statement = statement.where(Note.created_at >= datetime.fromisoformat(created_after))
    if created_before:
        statement = statement.where(Note.created_at <= datetime.fromisoformat(created_before))
        
    notes = session.exec(statement).all()
    return [format_note_response(n) for n in notes]

@app.get("/notes/stats")
def get_note_stats(session: SessionDep):
    notes = session.exec(select(Note)).all()
    
    categories = {}
    tag_counts = {}
    
    for note in notes:
        categories[note.category] = categories.get(note.category, 0) + 1
        for tag in note.tags:
            tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1
            
    top_tags = [{"tag": k, "count": v} for k, v in sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)[:5]]
    
    return {
        "total_notes": len(notes),
        "by_category": categories,
        "top_tags": top_tags,
        "unique_tags_count": len(tag_counts)
    }

@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, session: SessionDep):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return format_note_response(note)

@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_update: NoteCreate, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    db_note.title = note_update.title
    db_note.content = note_update.content
    db_note.category = note_update.category
    
    tag_objects = []
    for tag_name in note_update.tags:
        existing_tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            new_tag = Tag(name=tag_name)
            session.add(new_tag)
            tag_objects.append(new_tag)
            
    db_note.tags = tag_objects
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return format_note_response(db_note)

@app.patch("/notes/{note_id}", response_model=NoteResponse)
def partial_update_note(note_id: int, note_update: NoteUpdate, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    update_data = note_update.model_dump(exclude_unset=True)
    
    if "title" in update_data:
        db_note.title = update_data["title"]
    if "content" in update_data:
        db_note.content = update_data["content"]
    if "category" in update_data:
        db_note.category = update_data["category"]
        
    if "tags" in update_data:
        tag_objects = []
        for tag_name in update_data["tags"]:
            existing_tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
            if existing_tag:
                tag_objects.append(existing_tag)
            else:
                new_tag = Tag(name=tag_name)
                session.add(new_tag)
                tag_objects.append(new_tag)
        db_note.tags = tag_objects

    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return format_note_response(db_note)

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    # Löscht eine Notiz dauerhaft aus der Datenbank.
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return # Bei 204 wird kein Content zurückgegeben.

@app.get("/tags", response_model=List[str])
def list_tags(session: SessionDep):
    tags = session.exec(select(Tag)).all()
    return sorted([tag.name for tag in tags])

@app.get("/tags/{tag_name}/notes", response_model=List[NoteResponse])
def get_notes_by_tag(tag_name: str, session: SessionDep):
    tag = session.exec(select(Tag).where(Tag.name == tag_name.lower())).first()
    if not tag:
        return []
    return [format_note_response(note) for note in tag.notes]

@app.get("/categories", response_model=List[str])
def list_categories(session: SessionDep):
    notes = session.exec(select(Note)).all()
    categories = set(note.category for note in notes)
    return sorted(list(categories))

@app.get("/categories/{category_name}/notes", response_model=List[NoteResponse])
def get_notes_by_category(category_name: str, session: SessionDep):
    notes = session.exec(select(Note).where(Note.category == category_name.lower())).all()
    return [format_note_response(note) for note in notes]

def format_note_response(db_note: Note) -> NoteResponse:
    return NoteResponse(
        id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        category=db_note.category,
        tags=[tag.name for tag in db_note.tags],
        created_at=db_note.created_at.isoformat()
    )