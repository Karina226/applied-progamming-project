import streamlit as st
import requests

# =====================================================================
# 1. KONFIGURATION & MICROSERVICE-ANBINDUNG
# =====================================================================
# Das Frontend läuft unabhängig vom Backend (Microservice-Architektur).
# API_URL ist das "Telefonkabel" zu unserer FastAPI.
API_URL = "http://127.0.0.1:8000"

# st.set_page_config muss immer der allererste Streamlit-Befehl sein.
# 'layout="wide"' nutzt den gesamten Bildschirm, was bei Tabellen/Listen besser aussieht.
st.set_page_config(page_title="Winston Notes Manager", page_icon="📝", layout="wide")
st.title("📝 Wirtschaftsinformatik Notes Manager")

# =====================================================================
# 2. UI-LAYOUT (TABS)
# =====================================================================
# Wir nutzen Tabs statt Buttons, um Formulare ein/auszublenden. 
# Das verhindert, dass die Seite beim Klicken unruhig hin und her springt.
tab_view, tab_create = st.tabs(["📚 Alle Notizen ansehen", "➕ Neue Notiz erstellen"])

# =====================================================================
# 3. REITER 1: NOTIZEN ANZEIGEN (HTTP GET)
# =====================================================================
with tab_view:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.header("Deine Notizen")
    with col2:
        # Ein Button, um die Seite manuell neu zu laden und frische Daten zu holen
        if st.button("Notizen aktualisieren"):
            st.rerun() 

    # Ein try-except-Block schützt die App vor dem Absturz, falls die API offline ist.
    try:
        # Wir senden einen HTTP GET-Request an die REST-API
        response = requests.get(f"{API_URL}/notes")
        
        # Status Code 200 bedeutet "OK" (Daten wurden erfolgreich geliefert)
        if response.status_code == 200:
            notes = response.json() # Konvertiert den JSON-String in ein Python-Dictionary
            
            if not notes:
                st.info("Noch keine Notizen vorhanden. Nutze den zweiten Reiter, um eine anzulegen!")
            
            # Wir iterieren durch alle Notizen und bauen für jede ein Akkordeon (Expander)
            for note in notes:
                with st.expander(f"📌 {note['title']} ({note['category']})"):
                    st.write("**Inhalt:**", note['content'])
                    
                    # Tags sind eine Liste. Mit join() machen wir daraus einen schönen String (wichtig, uni)
                    st.write("**Tags:**", ", ".join(note['tags']) if note['tags'] else "Keine")
                    st.caption(f"ID: {note['id']} | Erstellt am: {note['created_at']}")
                    
                    # =========================================================
                    # LÖSCHEN-FUNKTION (HTTP DELETE)
                    # =========================================================
                    # Jeder Button braucht einen eindeutigen 'key', sonst meckert Streamlit
                    if st.button("🗑️ Diese Notiz löschen", key=f"del_{note['id']}"):
                        # Wir senden einen HTTP DELETE-Request an die spezifische Notiz-URL
                        res = requests.delete(f"{API_URL}/notes/{note['id']}")
                        
                        # Status Code 204 bedeutet "No Content" (Erfolgreich gelöscht)
                        if res.status_code == 204:
                            st.success("Notiz gelöscht!")
                            st.rerun() # Seite sofort neu laden, damit die Notiz im UI verschwindet
        else:
            st.error("Fehler beim Abrufen der Notizen von der API.")
            
    except Exception as e:
        # Dieser Fehler erscheint, wenn man vergisst, Terminal 1 (FastAPI) zu starten
        st.error(f"Verbindung zur API fehlgeschlagen. Läuft das FastAPI Backend auf Port 8000? Fehler: {e}")


# =====================================================================
# 4. REITER 2: NOTIZ ERSTELLEN (HTTP POST)
# =====================================================================
with tab_create:
    st.header("Notiz hinzufügen")
    
    # st.form bündelt alle Eingaben. Sie werden erst gesendet, wenn der Submit-Button geklickt wird.
    # clear_on_submit=True sorgt dafür, dass die Felder danach wieder leer sind.
    with st.form("note_form", clear_on_submit=True):
        new_title = st.text_input("Titel (min. 3 Zeichen)")
        
        # Pydantic-Schutz: Wir nutzen ein Dropdown, damit der Nutzer keinen falschen String tippen kann.
        new_category = st.selectbox("Kategorie", ["work", "personal", "school", "ideas", "general"])
        
        new_tags = st.text_input("Tags (kommagetrennt, z.B. urgent, klausur, winf)")
        new_content = st.text_area("Inhalt")
        
        submitted = st.form_submit_button("Speichern")
        
        # Wenn der User auf "Speichern" klickt:
        if submitted:
            # Daten-Transformation: Wir wandeln den kommagetrennten Text in eine echte Python-Liste um.
            # strip() entfernt dabei versehentliche Leerzeichen (z.B. "uni , wichtig" -> ["uni", "wichtig"])
            tags_list = [t.strip() for t in new_tags.split(",")] if new_tags else []
            
            # Das ist unser JSON-Payload, der exakt zu unserem Pydantic-Modell (NoteCreate) passen muss.
            payload = {
                "title": new_title,
                "content": new_content,
                "category": new_category,
                "tags": tags_list
            }
            
            try:
                # Wir senden einen HTTP POST-Request, um die Daten an die Datenbank zu übergeben
                res = requests.post(f"{API_URL}/notes", json=payload)
                
                # Status Code 201 bedeutet "Created" (Ressource erfolgreich angelegt)
                if res.status_code == 201:
                    st.success("Notiz erfolgreich erstellt! Wechsle zum linken Tab, um sie zu sehen.")
                else:
                    # Falls unsere Pydantic-Validierung im Backend zuschlägt (Status 422),
                    # extrahieren wir die Fehlermeldung aus dem JSON und zeigen sie dem User an.
                    st.error(f"Fehler bei der Eingabe: {res.json().get('detail')}")
                    
            except Exception as e:
                st.error(f"Verbindung zur API fehlgeschlagen: {e}")