# 🎓 Applied Programming (WINF 2.0) - Note Taking API & Dashboard

Dieses Repository enthält das finale Lernprojekt für den Kurs **Applied Programming (Wirtschaftsinformatik)** an der **Hochschule Coburg**. 

Es handelt sich um ein vollständiges Note-Management-System, das eine RESTful API (Backend) mit einer relationalen Datenbank und einem interaktiven Web-Dashboard (Frontend) vereint. Sämtliche API-Endpunkte aus den Kurstagen wurden in einer einzigen FastAPI-App (`main.py`) gebündelt, um maximale Übersichtlichkeit zu gewährleisten.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-blue.svg)](https://www.sqlite.org/)

---

## 🚀 Features & Lernfortschritt

Im Laufe des Kurses wurde die Architektur von einer einfachen JSON-Dateispeicherung (Day 2) auf eine **professionelle relationale SQLite-Datenbank** (Day 3 / Task 6) migriert.

* **Complete CRUD:** Erstellen, Lesen, Aktualisieren und Löschen von Notizen.
* **Tag-System (N:M):** Zuweisung mehrerer Tags pro Notiz über eine relationale Link-Tabelle.
* **Komplexe Filter:** Notizen durchsuchen via Text (`search`), Kategorien (`category`) oder Zeitstempel (`created_after`).
* **Strikte Validierung:** Pydantic-Modelle weisen fehlerhafte Daten sofort ab, bevor sie die Datenbank erreichen.
* **Interaktives UI:** Ein modernes Streamlit-Frontend zur einfachen Visualisierung und Datenpflege.
* **Test-Driven:** Eine integrierte `pytest`-Suite testet alle Haupt-Endpunkte isoliert mit einer In-Memory-Datenbank.

---

## 🗂️ Projektstruktur

WINF-Project/
├── main.py              # Komplette FastAPI-App (Routen, Pydantic- & Datenbank-Modelle)
├── frontend.py          # Streamlit Frontend (Web-Interface)
├── test_main.py         # Pytest-Suite (isoliertes Testen der Endpunkte)
├── notes.db             # Relationale SQLite-Datenbank (wird beim Start automatisch erstellt)
└── README.md            # Diese Dokumentation

---

## 🛠️ Setup & Installation

Das Projekt nutzt den modernen Package-Manager `uv`.

**1. Repository klonen & ins Verzeichnis wechseln**
git clone <dein-repo-url>
cd <dein-ordner>

**2. Alle Abhängigkeiten installieren**
uv add fastapi sqlmodel pydantic streamlit requests pytest

---

## ▶️ Lokale Ausführung

Um die komplette Microservice-Architektur zu starten, öffne **zwei separate Terminals**:

**Terminal 1: FastAPI Backend starten**
uv run fastapi dev main.py
*Die interaktive Swagger-Dokumentation (API-Docs) ist nun unter `http://127.0.0.1:8000/docs` erreichbar.*

**Terminal 2: Streamlit Frontend starten**
uv run streamlit run frontend.py
*Das Dashboard öffnet sich automatisch im Browser unter `http://localhost:8501`.*

---

## 🧪 Automatisierte Tests ausführen

Die API wird durch umfangreiche Tests abgesichert. Die Tests nutzen den internen `TestClient` und eine flüchtige In-Memory-Datenbank (`StaticPool`), sodass die echte `notes.db` beim Testen nicht überschrieben wird.

# Gesamte Test-Suite ausführen
uv run pytest test_main.py -v

---

## 📡 API Endpunkte (Übersicht)

Die vollständige und interaktive Dokumentation generiert FastAPI automatisch unter `/docs`. Hier ist ein grober Überblick der implementierten Ressourcen:

### 📝 Notes & Filter
| Method | Endpoint | Beschreibung |
|--------|----------|-------------|
| `POST` | `/notes` | Erstellt eine neue Notiz |
| `GET`  | `/notes` | Listet Notizen (unterstützt Query-Filter wie `?category=work&search=klausur`) |
| `GET`  | `/notes/{id}` | Gibt eine spezifische Notiz zurück |
| `DELETE`| `/notes/{id}` | Löscht eine Notiz |

### 🏷️ Kategorien & Tags
| Method | Endpoint | Beschreibung |
|--------|----------|-------------|
| `GET`  | `/tags` | Listet alle einzigartigen Tags auf |
| `GET`  | `/tags/{tag}/notes` | Gibt alle Notizen mit einem bestimmten Tag zurück |
| `GET`  | `/categories` | Listet alle einzigartigen Kategorien auf |

---

## 🛡️ Strikte Input-Validierung (Pydantic)

Die API nutzt **Pydantic V2**, um das Prinzip *"Stop trusting your inputs"* umzusetzen. Ungültige Anfragen werden mit einem `HTTP 422 Unprocessable Entity` abgelehnt.

**Beispiele für automatisches Blockieren:**
* `{"title": ""}` → **422 Error:** Titel ist zu kurz (min. 3 Zeichen).
* `{"category": "banane"}` → **422 Error:** Kategorie ist nicht in der Whitelist enthalten.
* `{"unbekanntes_feld": "xyz"}` → **422 Error:** Extra-Felder sind verboten (`extra="forbid"`).

**Daten-Normalisierung:**
Tags werden vor dem Speichern automatisch in der API bereinigt.  
Aus Eingaben wie `["URGENT", "  klausur  "]` wird in der Datenbank automatisch und sauber formatiert gespeichert: `["urgent", "klausur"]`.

---

## 🏛️ Key Code Concepts (Architektur-Entscheidungen)

* **Dependency Injection (`SessionDep`):** Jeder Endpunkt erhält automatisch eine frische Datenbank-Verbindung, die nach der Antwort sofort sicher wieder geschlossen wird.
* **Many-to-Many Relationship:** Die Verknüpfungstabelle `NoteTagLink` ermöglicht es, dass ein Tag (z. B. "wichtig") nur einmal in der Datenbank existiert, aber beliebig vielen Notizen zugeordnet werden kann.
* **Session.refresh():** Wird genutzt, um nach einem `commit()` die von SQLite generierte ID in das Python-Objekt zurückzuladen.