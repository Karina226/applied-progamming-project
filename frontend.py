import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="My Notes App", layout="wide")
st.title("📝 Wirtschaftsinformatik Notes Manager")

# Tab-Layout
tab1, tab2 = st.tabs(["📚 Alle Notizen ansehen", "➕ Neue Notiz erstellen"])

with tab1:
    st.header("Deine Notizen")
    if st.button("Notizen aktualisieren"):
        pass # Streamlit lädt die Seite neu

    try:
        response = requests.get(f"{API_URL}/notes")
        if response.status_code == 200:
            notes = response.json()
            if not notes:
                st.info("Noch keine Notizen vorhanden.")
            else:
                for note in notes:
                    with st.expander(f"📌 {note['title']} ({note['category']})"):
                        st.write("**Inhalt:**", note['content'])
                        st.write("**Tags:**", ", ".join(note['tags']) if note['tags'] else "Keine")
                        st.caption(f"Erstellt am: {note['created_at']}")
        else:
            st.error("Fehler beim Abrufen der Notizen.")
    except Exception as e:
        st.error(f"Verbindung zur API fehlgeschlagen: {e}")

with tab2:
    st.header("Notiz hinzufügen")
    with st.form("note_form", clear_on_submit=True):
        new_title = st.text_input("Titel (min. 3 Zeichen)")
        new_category = st.selectbox("Kategorie", ["work", "personal", "school", "ideas", "general"])
        new_tags = st.text_input("Tags (kommagetrennt, z.B. urgent, projekt)")
        new_content = st.text_area("Inhalt")
        
        submitted = st.form_submit_button("Speichern")
        
        if submitted:
            tags_list = [t.strip() for t in new_tags.split(",")] if new_tags else []
            payload = {
                "title": new_title,
                "content": new_content,
                "category": new_category,
                "tags": tags_list
            }
            try:
                res = requests.post(f"{API_URL}/notes", json=payload)
                if res.status_code == 201:
                    st.success("Notiz erfolgreich erstellt! Wechsle zum anderen Tab, um sie zu sehen.")
                else:
                    st.error(f"Fehler: {res.json().get('detail')}")
            except Exception as e:
                st.error(f"Verbindung zur API fehlgeschlagen: {e}")