
#Tag 1
# --- IMPORT ---
# Wir importieren FastAPI, das ist unser "Baukasten", um die API zu erstellen.
from fastapi import FastAPI


#--- APP SETUP ---
# Hier initialsieren wir unsere API-Anwendung. 'app' ist das Hauptobjekt, über das alles gesteuert wird.
app = FastAPI ()


#===========================================
# --- UNTERRICHT: Die ersten 3 Endpunkte ---
#===========================================

# 1. Der Root-Endpunkt (Startseite)
@app.get("/")
def root():
    """Gibt die einfache Begrüßung zurück, wenn man http://127.0.0.1:8000/ aufruft."""
    return {"message": "Hello, World!"}

# 2. Der Status-Endpunkt
@app.get("/about")
def get_about():
    """Gibt Infos über das Projekt zurück. Hier kannst du deinen echten Namen eintragen!"""
    return{
        "project":"My First API",
        "author":"Karina",
        "course": "Applied Programming"
    }
#Bsp:
#@app.get("/name/{name}")
#def greet_name(name: str):
#    return {"message": f"Hello, {name}!"}


#=======================================
# --- HAUSAUFGABEN (Task 1, 2 und 3) ---
#=======================================

# --- TASK 1: Square Calculator (Quadratzahl berechnen) ---
# {number} in der URL bedeutet, dass der Nutzer hier eine beliebige Zahl eingeben kann (z.B. /square/5)
@app.get ("/square/{number}")
def calculate_square(number: int):
    """Nimmt eine Zahl aus der URL, berechnet das Quadrat und gibt das Ergebnis zurück."""
    #Berechnung: Zahl mal Zahl
    result = number * number

    #Rückgabe als Dictionary (wird automatisch in JSON umgewandelt)
    #Mit f"..." (f-strings) können wir Variablen direkt in den Text einbauen
    return{
        "number": number,
        "square": result,
        "calculation": f"{number} * {number} = {result}"
    }


# --- TASK 2: Student Info (Deine Studenten-Infos) ---
@app.get("/student")
def get_student():
    """Gibt deine persönlichen Studenten-Informationen zurück."""
    # Passe diese Werte einfach an deine echten Daten an!
    return {
        "name": "Kari",             # <-- Hier deinen Namen eintragen
        "semester": 2,                   # <-- Hier dein Semester eintragen
        "course": "Wirtschaftsinformatik 2.0",
        "university": "Hochschule C" # <-- Hier deine Uni eintragen
    }


# --- TASK 3: Double Calculator (Zahl verdoppeln) ---
# Genau wie beim Square Calculator nehmen wir hier wieder eine {number} aus der URL
@app.get("/double/{number}")
def calculate_double(number: int):
    """Nimmt eine Zahl aus der URL, verdoppelt sie und gibt das Ergebnis zurück."""
    # Berechnung: Zahl mal 2
    result = number * 2
    
    return {
        "number": number,
        "double": result,
        "calculation": f"{number} × 2 = {result}"
    }

#@app.get("/calculate/{number}")
#def calculate(number: float):
#    result = number * 7 + 5
#    return {"message":f"Der verrechnete Wert von {number} ist {result}"}