# 📖 Work Log: Applied Programming (WINF 2.0)

**Student Name:** Karina Müller

---

## Week 1

### Day 1: Die Architektur von Web-Services

#### 1. ✅ What did I accomplish?
Der erste Tag diente der Grundsteinlegung. Ich habe mich mit dem **Client-Server-Prinzip** vertraut gemacht und gelernt, wie Anfragen über das HTTP-Protokoll verarbeitet werden. Nach der Installation von Python und dem Paketmanager `uv` habe ich meine erste **FastAPI-Instanz** erzeugt. Ich habe verstanden, dass FastAPI auf **Asynchronous Server Gateway Interface (ASGI)** basiert, was es extrem schnell macht. Konkret habe ich erste Endpunkte implementiert und dabei gelernt, wie man **Path-Parameter** (z. B. in `/square/{number}`) nutzt, um Variablen direkt aus der URL zu extrahieren. Ein Highlight war die Nutzung der interaktiven Swagger-Dokumentation unter `/docs`, die es ermöglicht, API-Spezifikationen ohne externe Tools wie Postman zu testen.

#### 2. 🚧 What challenges did I face?
Die größte Hürde war zu Beginn die **Decorator-Syntax** (`@app.get`). Ich hatte Schwierigkeiten zu verstehen, wie eine Funktion "weiß", dass sie auf einen URL-Pfad reagieren soll, ohne dass ich sie explizit im Code aufrufe. Zudem war die automatische Typkonvertierung (Data Coercion) von String-URLs in Python-Integer gewöhnungsbedürftig.

#### 3. 💡 How did I overcome them?
Ich habe recherchiert, wie Decorators in Python als "Wrapper" fungieren, die Funktionen bei der FastAPI-Instanz registrieren. Durch das bewusste Provozieren von Fehlern (z. B. Senden eines Buchstabens an einen Integer-Pfad) habe ich gelernt, wie FastAPI automatisch Validierungsfehler generiert.

---

### Day 2: Datenschemata und Persistenz

#### 1. ✅ What did I accomplish?
Heute stand die Modellierung von Datenobjekten im Fokus. Ich habe **Pydantic-Modelle** (`BaseModel`) eingeführt, um die Struktur meiner Notizen (Titel, Inhalt, Kategorie) zu definieren. Ein zentraler Punkt war der Unterschied zwischen **Eingabe-Modellen** (`NoteCreate`) und **Antwort-Modellen** (`Note`), da Felder wie die `id` oder der Zeitstempel niemals vom Client gesendet, sondern immer vom Server generiert werden sollten. Um Daten über einen Server-Neustart hinaus zu erhalten, habe ich eine dateibasierte Speicherung in einer `notes.json` implementiert und dabei den Umgang mit dem `JSON`-Modul und `Pathlib` in Python vertieft.

#### 2. 🚧 What challenges did I face?
Die Synchronisation zwischen dem Python-Arbeitsspeicher (`notes_db` Liste) und der physischen Datei war fehleranfällig. Besonders das Management der eindeutigen IDs (Primary Keys) stellte ein Problem dar, wenn die Datei manuell verändert wurde oder mehrere Notizen schnell hintereinander erstellt wurden.

#### 3. 💡 How did I overcome them?
Ich habe eine robuste Logik für den `note_id_counter` entwickelt, die beim Start der App den höchsten existierenden Wert aus der JSON-Datei ausliest (`max(ids) + 1`). So wurde sichergestellt, dass IDs niemals doppelt vergeben werden, selbst wenn der Server abstürzt.

---

### Day 3: Relationale Datenbanken & REST-Prinzipien

#### 1. ✅ What did I accomplish?
An Tag 3 habe ich den größten architektonischen Schritt gemacht: Die Migration von einer flachen JSON-Datei zu einer **relationalen SQLite-Datenbank** mittels **SQLModel**. Ich habe gelernt, wie man **Many-to-Many-Beziehungen** sauber abbildet. Da eine Notiz mehrere Tags haben kann, habe ich eine **Link-Tabelle** (`NoteTagLink`) erstellt. Außerdem habe ich die REST-Prinzipien vertieft und Endpunkte für das vollständige **CRUD-Spektrum** (Create, Read, Update, Delete) gebaut, inklusive `PUT` (vollständiges Ersetzen) und `PATCH` (teilweises Aktualisieren unter Nutzung von `exclude_unset=True`).

#### 2. 🚧 What challenges did I face?
Das größte Problem war die **Normalisierung**. Da SQLite keine Listen (`List[str]`) speichern kann, war ich versucht, Tags einfach als langen Text-String zu speichern. Mir wurde jedoch klar, dass dies die Suche nach einzelnen Tags unmöglich oder extrem langsam machen würde.

#### 3. 💡 How did I overcome them?
Ich habe mich für die saubere relationale Lösung mit einer Verknüpfungstabelle entschieden. Dabei habe ich gelernt, wie man `Relationship`-Objekte in SQLModel nutzt, um über **Foreign Keys** hinweg Daten abzufragen. Das war zwar komplexer in der Ersteinrichtung, bietet aber eine professionelle Datenintegrität.

---

## Week 2

### Day 4: Qualitätssicherung durch Testing

#### 1. ✅ What did I accomplish?
Heute habe ich gelernt, wie man professionelle **Unit- und Integrationstests** mit `pytest` schreibt. Ich habe den **FastAPI TestClient** genutzt, um automatisierte Anfragen an meine API zu senden. Dabei habe ich das **Arrange-Act-Assert-Pattern** angewendet: Testdaten vorbereiten, den Endpunkt aufrufen und das Ergebnis (Statuscode und JSON-Body) prüfen. Ich habe gezielt Tests für Erfolgsfälle (200 OK, 201 Created) und Fehlerfälle (404 Not Found, 422 Validation Error) geschrieben.

#### 2. 🚧 What challenges did I face?
Ein schwieriges Thema war die **Test-Isolation**. Da die Tests in die Datenbank schreiben, haben sich die Ergebnisse gegenseitig beeinflusst. Ein Test, der die Anzahl der Notizen prüft, schlug fehl, wenn ein vorheriger Test bereits eine Notiz angelegt hatte.

#### 3. 💡 How did I overcome them?
Ich habe eine **Test-Fixture** erstellt, die für jeden Testlauf eine neue, flüchtige **In-Memory-Datenbank** im RAM erzeugt. Durch das Überschreiben der Datenbank-Engine während der Testphase blieben meine produktiven Daten in der `notes.db` geschützt und jeder Test startete in einer definierten, sauberen Umgebung.

---

### Day 5: Advanced Validation & Security

#### 1. ✅ What did I accomplish?
Tag 5 widmete sich der Absicherung der API. Ich habe **Pydantic-Validatoren** genutzt, um komplexe Regeln durchzusetzen (z. B. Regex-Pattern für Tag-Namen). Ich habe gelernt, wie man mit `ConfigDict(extra="forbid")` verhindert, dass Angreifer oder fehlerhafte Clients zusätzliche, nicht definierte Felder an die API schicken. Außerdem habe ich **Model-Validatoren** implementiert, die Abhängigkeiten zwischen mehreren Feldern prüfen (Cross-Field Validation).

#### 2. 🚧 What challenges did I face?
Die Validierung von Tags war tückisch: Ich wollte sicherstellen, dass Tags wie " WInF " und "winf" als derselbe Tag behandelt werden, um Redundanz in der Datenbank zu vermeiden. Die Herausforderung lag darin, diese Bereinigung (Sanitization) performant in den Validierungsprozess zu integrieren.

#### 3. 💡 How did I overcome them?
Ich habe eine zentrale **Normalisierungs-Funktion** geschrieben, die innerhalb des `@field_validator` aufgerufen wird. Diese nutzt `strip()`, `lower()` und ein Python-`set`, um Duplikate bereits vor dem Datenbank-Eintrag zu eliminieren. Das garantiert eine "Single Source of Truth" für meine Schlagwörter.

---

### Day 6: Refactoring & Reference-Testing

#### 1. ✅ What did I accomplish?
Heute stand ein umfassendes Code-Refactoring an. Ich habe die gesamten alten "Spielzeug-Endpunkte" (wie Begrüßungen oder einfache Rechenaufgaben aus Woche 1) entfernt, um eine reine, fokussierte REST-API für Notizen abzugeben. Ein weiterer Fokus lag darauf, die offizielle Referenz-Test-Suite gegen meine App laufen zu lassen. Dabei habe ich gelernt, wie man detaillierte Fehlermeldungen analysiert, um die Kompatibilität meiner Endpoints (Statuscodes, JSON-Strukturen) zu optimieren.

#### 2. 🚧 What challenges did I face?
Ein technisches Detail war das Verhalten bei der Lösch-Funktion. Während ich anfangs einen Statuscode 200 zurückgab, forderte die offizielle Suite einen 204 (No Content). Auch die alphabetische Sortierung von Tags in der Antwort war eine Anforderung, die ich erst durch das Scheitern der Tests bemerkt habe.

#### 3. 💡 How did I overcome them?
Ich habe die Endpunkte systematisch angepasst: Die Rückgabewerte wurden auf `Response(status_code=204)` umgestellt und die Listen-Rückgaben im Backend mit `sorted()` versehen. Das Bestehen der Referenz-Tests gab mir die Sicherheit, dass meine API stabil und standardkonform arbeitet.

---

## Week 3

### Day 7: Full-Stack Integration mit Streamlit

#### 1. ✅ What did I accomplish?
Zum Abschluss habe ich ein grafisches Benutzerinterface mit **Streamlit** entwickelt. Ich habe gelernt, wie man eine **Microservice-Architektur** bedient, indem das Frontend über die `requests`-Library mit der REST-API kommuniziert. Ich habe ein Dashboard mit **Tabs** erstellt, das die Trennung zwischen Datenanzeige und Dateneingabe optisch sauber löst. Besonders wichtig war hierbei das **State-Management** (`st.session_state`), um Daten über mehrere Interaktionen hinweg flüssig darzustellen.

#### 2. 🚧 What challenges did I face?
Ein technisches Problem war das Feedback der API im Frontend. Wenn eine Validierung im Backend fehlschlug (z. B. Titel zu kurz), hat die API einen 422-Fehler gesendet, den das Frontend zunächst nicht aussagekräftig für den Nutzer dargestellt hat.

#### 3. 💡 How did I overcome them?
Ich habe das Error-Handling im Frontend verbessert. Durch das Auslesen des `detail`-Feldes aus der JSON-Antwort der API konnte ich die exakten Validierungsfehler von Pydantic (z. B. "Mindestens 3 Zeichen erforderlich") direkt als Warnung in der Streamlit-UI anzeigen. Zudem habe ich Dropdown-Menüs für Kategorien eingebaut, um Eingabefehler von vornherein technisch auszuschließen.

---

# 🎉 Fazit
Dieses Projekt hat mir den gesamten Lebenszyklus einer modernen Web-Anwendung aufgezeigt: Von der ersten Route über die persistente Datenbankstruktur und automatisierte Tests bis hin zum fertigen User Interface. Die Kombination aus FastAPI und Streamlit hat mir verdeutlicht, wie effizient man heute robuste und skalierbare Softwarelösungen in Python entwickeln kann.