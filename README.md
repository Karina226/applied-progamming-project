# 📝 Angewandte Programmierung: Note Taking API & Frontend

Dieses Projekt ist die Abschlussabgabe für das Modul **Angewandte Programmierung (Wirtschaftsinformatik 2.0)**. Es beinhaltet eine professionell strukturierte REST-API mit FastAPI, einer SQLite Datenbank via SQLModel und einem interaktiven Frontend, das mit Streamlit betrieben wird.

## 🚀 Features
- **Komplette CRUD-Funktionalität:** Erstellen, Lesen, Aktualisieren und Löschen von Notizen.
- **Datenbank-Migration:** Alle Daten werden persistent in einer SQLite-Datenbank (`notes.db`) gespeichert.
- **Strikte Validierung:** Gesichert durch komplexe Pydantic-Models (inklusive Regex und Cross-Field Validatoren).
- **Filter & Statistiken:** Suchen via Kategorien, Text, Tags und Zeitstempel.
- **Interaktives Frontend:** Eine intuitive Web-UI zur Visualisierung und Dateneingabe.

## 🛠️ Ausführung

Zuerst alle Abhängigkeiten via `uv` installieren, dann die Terminals starten:

**1. Backend starten (FastAPI):**
```bash
uv run fastapi dev main.py