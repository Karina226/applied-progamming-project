# Work Log

**Student Name: Karina Müller** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?
- **Setup der Entwicklungsumgebung:** Ich habe meine Arbeitsumgebung von Grund auf eingerichtet. Das beinhaltete die Installation von Git zur Versionskontrolle, Visual Studio Code (VS Code) als IDE sowie die Konfiguration der passenden Python-Erweiterungen.
- **Package Management:** Ich habe mich mit dem modernen Package Manager `uv` vertraut gemacht, der deutlich performanter als Standard-pip ist, und mein erstes FastAPI-Projekt initialisiert.
- **Erste Endpunkte:** Ich habe die grundlegende Struktur einer REST-API verstanden und meine ersten drei GET-Endpunkte (`/`, `/status`, `/about`) programmiert.
- **API-Dokumentation:** Ich habe gelernt, wie FastAPI automatisch eine interaktive Swagger UI (unter `/docs`) generiert und wie man diese nutzt, um Endpunkte direkt im Browser zu testen, ohne separate Tools wie Postman zu benötigen.

#### 2. 🚧 What challenges did I face?
- **Konzeptuelle Hürden:** Das Verständnis des lokalen Webservers (localhost bzw. `127.0.0.1:8000`) und wie Uvicorn im Hintergrund als ASGI-Server Anfragen an meine Python-Funktionen weiterleitet, war anfangs abstrakt.
- **Terminal-Nutzung:** Der Umgang mit Kommandozeilenbefehlen und das Einrichten der virtuellen Umgebung (`.venv`) über `uv` erforderte etwas Eingewöhnung.

#### 3. 💡 How did I overcome them?
- **Aktives Mitprogrammieren:** Durch das synchrone Mitprogrammieren während der Vorlesung und das direkte Testen der Ergebnisse im Browser wurde das Konzept von Request und Response schnell greifbar.
- **Dokumentation:** Das Studieren der Fehlermeldungen im Terminal hat geholfen, fehlende Pakete (z.B. wenn Uvicorn nicht installiert war) schnell zu identifizieren.

---

### Day 2

#### 1. ✅ What did I accomplish?
- **Python-Grundlagen gefestigt:** Wiederholung von elementaren Datenstrukturen wie Dictionaries und Listen sowie die Nutzung von f-Strings zur sauberen Textformatierung. Typisierung in Python (`Type Hints`) angewendet.
- **HTTP-Methoden:** Den Unterschied zwischen GET (Daten lesen) und POST (Daten erstellen und Body mitsenden) verinnerlicht.
- **Datenvalidierung:** Erste Berührungspunkte mit Pydantic. Ein `NoteCreate` Model (`BaseModel`) erstellt, um eingehende JSON-Daten automatisch zu typisieren und zu validieren.
- **Datenpersistenz:** Eine einfache Lösung zur Speicherung implementiert. Die Notizen werden nun in einer lokalen `data/notes.json` Datei gesichert, sodass der Zustand (State) der Anwendung auch nach einem Server-Neustart erhalten bleibt (File Persistence).

#### 2. 🚧 What challenges did I face?
- **Dateizugriff:** Beim initialen Startlauf, wenn die `notes.json` Datei noch nicht existierte oder leer war, warf das Programm JSON-Decode-Fehler beim Versuch, Daten zu laden.
- **Status Codes:** Es war anfänglich verwirrend, wann genau welcher HTTP Status Code (z.B. 200 OK, 201 Created oder 422 Unprocessable Entity) vom Server zurückgegeben werden sollte.

#### 3. 💡 How did I overcome them?
- **Robuster Code:** Ich habe das Modul `pathlib` importiert und mit `Path.exists()` eine Vorab-Prüfung eingebaut. So wird die Datei nur ausgelesen, wenn sie auch wirklich vorhanden ist.
- **FastAPI-Features:** Ich habe gelernt, dass FastAPI Status-Codes in den Dekorator-Parametern (z.B. `@app.post(..., status_code=201)`) steuert und Pydantic sich automatisch um den 422-Fehler bei falschen Inputs kümmert.

---

### Day 3

#### 1. ✅ What did I accomplish?
- **Complete CRUD:** Die REST-Architektur durch Hinzufügen der fehlenden PUT- (Update) und DELETE-Operationen vervollständigt.
- **Query Parameter:** Komplexe Filterlogiken eingebaut, um Notizen über die URL nach Suchbegriffen, Kategorien und Tags filtern zu können.
- **Datenbank-Migration (Meilenstein):** Den größten Architekturwechsel durchgeführt! Die alte JSON-File-Lösung wurde durch eine echte, relationale SQLite-Datenbank ersetzt, die über SQLModel (ORM) angebunden wurde.
- **Resource Relationships:** Das Konzept von Viele-zu-Viele-Beziehungen (Many-to-Many) kennengelernt, um Notizen mehrere Tags zuzuordnen und umgekehrt.

#### 2. 🚧 What challenges did I face?
- **ORM Komplexität:** Die Übersetzung der Many-to-Many Beziehung in die Datenbankstruktur von SQLModel war die bislang größte konzeptuelle Hürde.
- **Logik-Fehler:** Das saubere Anlegen von Tags – sodass keine Duplikate in der Datenbank entstehen, sondern bestehende Tags wiederverwendet werden – erforderte komplexere Query-Logiken.

#### 3. 💡 How did I overcome them?
- **Link-Tabelle:** Durch das Definieren einer expliziten Verknüpfungstabelle (`NoteTagLink`) mit Foreign Keys (`note_id` und `tag_id`) ließ sich die Relation sauber abbilden.
- **Datenbank-Abfragen:** Vor dem Speichern eines Tags in der POST-Methode frage ich nun explizit ab, ob der Tag (`where(Tag.name == ...)`) bereits existiert, und verknüpfe andernfalls das existierende Objekt.

---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?
- **Test-Driven Development (TDD) Basics:** Die Notwendigkeit von automatisierten Tests verstanden, um Regressionen (das Brechen von bestehendem Code bei neuen Features) zu vermeiden.
- **Pytest Integration:** Eine Test-Suite mit `pytest` aufgesetzt.
- **Testing-Muster:** Das Arrange-Act-Assert (Vorbereiten - Handeln - Überprüfen) Pattern angewandt, um meine bestehenden CRUD-Endpunkte systematisch abzusichern.
- **TestClient:** Den internen FastAPI `TestClient` genutzt, um API-Aufrufe simulieren zu können, ohne den Uvicorn-Server in einem separaten Terminal laufen lassen zu müssen.

#### 2. 🚧 What challenges did I face?
- **Error-Case Testing:** Das Testen von Erfolgsfällen (200, 201) war recht logisch, aber das gezielte Provozieren und Abfangen von Fehlern (z.B. das Löschen einer nicht existierenden Notiz für einen 404-Fehler) erforderte ein Umdenken.

#### 3. 💡 How did I overcome them?
- **Systematischer Ansatz:** Ich habe dedizierte Testfunktionen geschrieben, die ganz bewusst fehlerhafte Payloads senden (z.B. fehlende Pflichtfelder), um sicherzustellen, dass die API korrekterweise mit einem 422 Unprocessable Entity antwortet.

---

### Day 5

#### 1. ✅ What did I accomplish?
- **Deep Dive Pydantic Validation:** Das Prinzip "Stop trusting your inputs" verinnerlicht und die Validierung der API massiv gehärtet.
- **Field Constraints:** Strikte Regeln (wie `min_length`, `max_length` und Regex-Pattern) über `Field()` auf die BaseModel-Attribute angewendet.
- **Custom Validators:** Eigene `@field_validator` Methoden geschrieben, um Strings automatisch zu normalisieren (z.B. `.strip().lower()`), bevor sie in der Datenbank landen.
- **Model Configuration:** Über `ConfigDict` globale Verhaltensregeln für die Pydantic-Klassen definiert.

#### 2. 🚧 What challenges did I face?
- **Unerwünschte Inputs:** Standardmäßig ignoriert Pydantic zusätzliche JSON-Felder im Body, die nicht im Modell definiert sind. Das kann zu schwer findbaren Bugs führen (z.B. wenn der User `tagz` statt `tags` schreibt).
- **Cross-Field Validierung:** Ein Validator sollte prüfen, ob Notizen der Kategorie 'work' zwingend den Tag 'work' enthalten. Dies brach jedoch später die bereitgestellte Test-Suite des Dozenten.

#### 3. 💡 How did I overcome them?
- **Extra Forbid:** Ich habe `extra="forbid"` im `ConfigDict` gesetzt. Dadurch werden Payloads mit fehlerhaften Zusatzfeldern sofort abgelehnt.
- **Architekturentscheidung:** Den Cross-Field `@model_validator` habe ich aus didaktischen Gründen implementiert, ihn aber auskommentiert, um die Testabdeckung und Kompatibilität mit den Anforderungen des Professors nicht zu gefährden.

---

### Day 6

#### 1. ✅ What did I accomplish?
- **Python Decorators:** Die Magie hinter Konstrukten wie `@app.get` oder `@field_validator` entschlüsselt. Ich verstehe nun, dass Decorators Funktionen sind, die das Verhalten anderer Funktionen erweitern ("wrappen"), ohne deren Kerncode zu verändern.
- **Test-Suite Ausführung:** Die offizielle `test_main.py` Test-Suite des Dozenten heruntergeladen, ausgeführt und analysiert.
- **Refactoring:** Meinen Backend-Code auf Basis der Testergebnisse der Dozenten-Suite angepasst und optimiert.

#### 2. 🚧 What challenges did I face?
- **Test Failures:** Beim ersten Durchlauf der offiziellen Test-Suite schlugen einige Tests fehl. Meine API war an manchen Stellen entweder zu strikt (durch meine eigenen Regex-Pattern) oder zu tolerant.

#### 3. 💡 How did I overcome them?
- **Debugging:** Systematisch die `assert`-Fehlermeldungen von Pytest analysiert und meine Pydantic-Validierungslogik in `main.py` schrittweise angepasst, bis alle Balken im Terminal grün waren.

---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?
- **Frontend Development:** Den Wechsel vom Backend- zum Full-Stack-Entwickler gemacht! Mein erstes interaktives Web-Dashboard mit dem Framework `Streamlit` gebaut.
- **API-Integration:** Das Streamlit-Frontend so programmiert, dass es über die `requests`-Bibliothek als Client fungiert und GET/POST-Calls an meine laufende lokale FastAPI sendet.
- **UI-Design:** Ein sauberes Benutzerinterface entworfen, das mit Tabs (`st.tabs`), interaktiven Formularen (`st.form`) und Expandern zur übersichtlichen Darstellung der Notizen arbeitet.

#### 2. 🚧 What challenges did I face?
- **State Management:** Nach dem Absenden des Formulars zur Erstellung einer neuen Notiz, aktualisierte sich die Liste der angezeigten Notizen im Streamlit-Frontend nicht automatisch. Die neue Notiz war erst nach einem manuellen Page-Reload sichtbar.

#### 3. 💡 How did I overcome them?
- **Streamlit Execution Flow:** Ich habe mich in den Execution-Flow von Streamlit eingearbeitet. Durch das Verwenden des Parameters `clear_on_submit=True` im Formular und das anschließende Auslösen von `st.rerun()` nach einem erfolgreichen API-Call (`status_code == 201`), konnte ich einen sofortigen automatischen Reload der Oberfläche erzwingen.

---

# 🎉 Congratulations! You did it! 🎓✨