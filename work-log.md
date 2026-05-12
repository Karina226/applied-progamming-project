# Work Log

**Student Name:** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## 1. ✅ What did I accomplish?

_Reflect on the activities, exercises, and work you completed today._

**Guiding questions:**
- What topics or concepts did you work with?
- What exercises or projects did you complete?
- What tools or technologies did you use?
- What did you learn or practice?


---

## 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

**Guiding questions:**
- What was difficult to understand?
- Where did you get stuck?
- What errors or problems did you face?
- What felt frustrating or confusing?


---

## 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

**Guiding questions:**
- What strategies did you try?
- Who or what helped you (instructor, classmates, documentation)?
- What did you learn from solving the problem?
- What questions do you still have?


---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?

Heute habe ich meine komplette Entwicklungsumgebung aufgesetzt. Ich habe Git, VS Code (inklusive Python-Erweiterung) und den Package-Manager uv installiert.
Danach habe ich gelernt, was eine API überhaupt ist (das Restaurant-Kellner-Prinzip) und meine allererste eigene API mit FastAPI geschrieben. Ich habe gelernt, wie man einfache GET-Routen erstellt und wie automatisch JSON-Daten zurückgegeben werden.
In der Hausaufgabe habe ich das Wissen direkt angewendet und drei weitere Endpunkte (/square/{number}, /student und /double/{number}) programmiert. Besonders cool war es, die Endpunkte direkt über die automatisch generierte Dokumentation unter /docs zu testen.

---

#### 2. 🚧 What challenges did I face?

Am Anfang waren die vielen neuen Tools (Terminal, VS Code, uv) ein bisschen überwältigend. Außerdem war es anfangs ungewohnt zu verstehen, wie Variablen aus der URL (sogenannte Path Parameters wie {number}) direkt an die Python-Funktion übergeben werden und wie man diese dann in der Funktion verarbeitet.

---

#### 3. 💡 How did I overcome them?

Ich habe mich strikt an die Schritt-für-Schritt-Anleitung aus der Präsentation gehalten. Bei den Hausaufgaben hat es extrem geholfen, nach jeder kleinen Code-Änderung direkt in den Browser zu gehen und den Endpunkt über /docs ("Try it out") zu testen. So habe ich sofort gesehen, ob meine Berechnungen und f-Strings richtig funktionieren, und konnte Fehler schnell korrigieren.

---

### Day 2

#### 1. ✅ What did I accomplish?

Der Fokus lag heute auf Python-Grundlagen (Variablen, Datentypen, Listen, Dictionaries, f-Strings und Funktionen mit Type Hints). Danach haben wir uns HTTP-Methoden (GET vs. POST) und JSON genauer angesehen.
Das große Projekt war eine "Note Taking API". Ich habe gelernt, wie man Datenmodelle mit Pydantic (BaseModel) erstellt und Daten nicht nur abruft, sondern über POST auch anlegt. Das Highlight war die Datenspeicherung: Die Notizen werden jetzt dauerhaft in einer notes.json Datei auf der Festplatte gespeichert. Für die Hausaufgabe habe ich das Modell um eine "Kategorie" erweitert, Endpunkte zum Filtern und für Statistiken geschrieben und sogar einen Bonus-Endpunkt zum Löschen (DELETE) hinzugefügt.

---

#### 2. 🚧 What challenges did I face?

Ich hatte einen Server-Absturz mit einem fiesen Fehler: pydantic_core._pydantic_core.ValidationError: 1 validation error for Note category Field required.
Das passierte, als ich für die Hausaufgabe das Feld category als Pflichtfeld in meinen Python-Code eingebaut habe. Als ich den Server neu startete, stürzte er sofort ab, weil in meiner alten notes.json Datei noch Test-Notizen vom Anfang lagen, die dieses neue Feld logischerweise noch nicht hatten.

---

#### 3. 💡 How did I overcome them?

Ich habe gelernt, dass mein Python-Code und die gespeicherte Datenbank (notes.json) zwei getrennte Dinge sind. Wenn ich im Code neue Pflichtfelder definiere, sind die alten Daten plötzlich "ungültig" für den strengen Pydantic-Check. Ich habe das Problem gelöst, indem ich die notes.json manuell im Editor geöffnet und bei den alten Notizen händisch das Feld "category": "..." ergänzt habe. Das war quasi meine erste manuelle "Datenbank-Migration"! Danach lief der Server wieder perfekt.

---

### Day 3

#### 1. ✅ What did I accomplish?

Heute haben wir unsere Notiz-App auf ein echtes "Produktions-Level" gehoben. Wir haben gelernt, wie man REST APIs richtig designt (Ressourcen als Nomen, HTTP Methoden korrekt nutzen) und den Unterschied zwischen Path- und Query-Parametern verstanden. Ich habe die App um vollständige CRUD-Funktionen (POST, GET, PUT, DELETE) erweitert.
Das absolute Highlight war aber die Hausaufgabe (Task 6): Ich habe die komplette Datenspeicherung von einer fehleranfälligen JSON-Datei in eine echte SQLite-Datenbank mithilfe von SQLModel umgebaut! Zudem habe ich diverse Filter eingebaut (nach Datum, Kategorien, Volltextsuche), einen PATCH-Endpunkt für Teil-Updates geschrieben und "Many-to-Many" Datenbank-Beziehungen für die Tags implementiert.

---

#### 2. 🚧 What challenges did I face?

Die Datenbank-Migration war anfangs eine große Herausforderung. Es war nicht sofort intuitiv, warum wir nun zwei verschiedene Arten von Modellen brauchen(Pydantic-Modelle für die API Ein- und Ausgaben wie NoteCreate oder NoteResponse, und SQLModel-Modelle für die eigentlichen Datenbank-Tabellen).
Besonders knifflig war die Logik beim Speichern von neuen Notizen mit Tags: Man muss zuerst in der Datenbank prüfen, ob der Tag schon existiert, und ihn entweder abrufen oder neu anlegen, bevor man ihn an die Notiz anhängt. Auch der neue PATCH-Endpunkt war ungewohnt, da ich genau prüfen musste, welche Felder der User überhaupt mitgeschickt hat.

---

#### 3. 💡 How did I overcome them?

Ich habe die Folien sehr genau studiert und die bereitgestellten Code-Snippets Schritt für Schritt in meine App integriert. Der Einsatz einer SQLite-Viewer Extension in VS Code war ein echter Gamechanger: So konnte ich mir live die generierte notes.db Datei ansehen und visuell prüfen, ob die "Link-Tabelle" zwischen Notizen und Tags von SQLModel korrekt befüllt wurde. Bei den Endpunkten (wie PATCH oder den kombinierten Filtern) hat mir intensives Testen über die FastAPI-Docs (/docs) geholfen, um sofort zu sehen, ob meine Logik funktioniert oder ob Fehler geworfen werden.

---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 5

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 6

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 8

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 9

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---


# 🎉 Congratulations! You did it! 🎓✨












