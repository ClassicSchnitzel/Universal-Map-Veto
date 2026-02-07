# API Dokumentation - Universal MapVeto Tool

## 🔌 Verfügbare Endpoints

### GET Routes (Browser)

#### 1. Spielauswahl
```
GET /
```
**Beschreibung:** Startseitenmenü - Spielauswahl
**Response:** HTML (game_select.html)

#### 2. CS2 Setup
```
GET /cs2
```
**Beschreibung:** Counter-Strike 2 Kontrollfenster
**Response:** HTML (CS-index.html)

#### 3. R6 Setup
```
GET /r6
```
**Beschreibung:** Rainbow Six Siege Kontrollfenster
**Response:** HTML (R6-index.html)

#### 4. Ergebnis-Anzeige
```
GET /result
```
**Beschreibung:** Veto-Ergebnis-Display (für OBS)
**Response:** HTML (result.html)

#### 5. Score-Tracking
```
GET /scores
```
**Beschreibung:** Score-Tracking-Interface
**Response:** HTML (scores.html)

#### 6. Bedienung/Anleitung
```
GET /anleitung
```
**Beschreibung:** Bedienungsanleitung (in HTML)
**Response:** HTML mit Bedienung

#### 7. Programm beenden
```
GET /exit
```
**Beschreibung:** Beendet die Anwendung sauber
**Response:** String "ok" (wenn erfolgreich)

---

### API Routes (JSON)

#### 1. State abrufen
```
GET /api/state
```
**Beschreibung:** Aktuellen Veto-State abrufen
**Response:** JSON

**Beispiel Response:**
```json
{
  "team1Name": "FaZe Clan",
  "team1Short": "FaZe",
  "team1Logo": "/path/to/logo.jpg",
  "team1LogoUrl": "https://example.com/logo.jpg",
  "team2Name": "NAVI",
  "team2Short": "NAVI",
  "team2Logo": "/path/to/logo.jpg",
  "team2LogoUrl": "https://example.com/logo.jpg",
  "format": "bo3",
  "maps": ["Inferno"],
  "selectedMaps": ["Mirage", "Inferno", "Nuke", "Vertigo", "Anubis", "Ancient", "Dust2"],
  "picks": [
    {
      "team": "Team 1",
      "map": "Mirage",
      "type": "ban"
    },
    {
      "team": "Team 2",
      "map": "Vertigo",
      "type": "ban"
    }
  ],
  "textColor": "white",
  "game": "cs2",
  "vetoFinished": false,
  "deciderShown": false
}
```

#### 2. State speichern
```
POST /api/state
Content-Type: application/json

{
  "team1Name": "...",
  "team2Name": "...",
  ...
}
```

**Beschreibung:** Neuen State speichern
**Response:** 
```json
{"status": "ok"}
```

**Error Response:**
```json
{"error": "Error message"}
```

---

## 🔄 State-Struktur

### Kompletter State Object
```javascript
{
  // Teams
  "team1Name": String,           // Vollständiger Teamname
  "team1Short": String,          // Shortcode/Kürzel
  "team1Logo": String,           // Lokale Logo-Datei
  "team1LogoUrl": String,        // Logo als URL
  "team2Name": String,           // Fullständiger Teamname
  "team2Short": String,          // Shortcode/Kürzel
  "team2Logo": String,           // Lokale Logo-Datei
  "team2LogoUrl": String,        // Logo als URL
  
  // Format & Maps
  "format": String,              // "bo1", "bo2", "bo3", "bo5"
  "maps": Array<String>,         // Verfügbare Maps
  "selectedMaps": Array<String>, // Ausgewählte Maps
  
  // Veto-Prozess
  "picks": Array<{               // Alle Veto-Aktionen
    "team": String,              // "Team 1" oder "Team 2"
    "map": String,               // Map-Name
    "type": String               // "ban", "pick", "decider"
  }>,
  
  // UI
  "textColor": String,           // "white" oder "black"
  "game": String,                // "cs2" oder "r6"
  
  // Status
  "vetoFinished": Boolean,       // Veto abgeschlossen?
  "deciderShown": Boolean        // Decider bereits angezeigt?
}
```

---

## 🔗 JavaScript Functions (Frontend)

Diese Funktionen sind in `static/js/shared.js` definiert:

### 1. Veto-Reihenfolge abrufen
```javascript
getVetoOrder(format, team1, team2, mapCount, startTeam)
```
**Rückgabe:** Array von Veto-Objekten
```javascript
[
  { team: "Team 1", action: "ban", mapCount: 7 },
  { team: "Team 2", action: "ban", mapCount: 6 },
  ...
]
```

### 2. Empfohlene Map-Anzahl
```javascript
getRecommendedMapCount(format)
```
**Rückgabe:** Integer (7 oder 8)

### 3. Map-Buttons aktualisieren
```javascript
updateMapButtons()
```
**Effekt:** Rendert alle verfügbaren Maps als klickbare Buttons

### 4. Map-Auswahl verarbeiten
```javascript
handleMapClick(map)
```
**Parameter:** map (String - Map-Name)
**Effekt:** Führt Ban/Pick aus, aktualisiert UI

### 5. Action Card hinzufügen
```javascript
addActionCard(action, team, map)
```
**Parameter:**
- action: "ban" | "pick" | "decider"
- team: "Team 1" | "Team 2"
- map: String (Map-Name)

### 6. Decider-Card anzeigen
```javascript
addDeciderCardIfAvailable()
```
**Effekt:** Zeigt Decider-Card wenn nur 1 Map übrig

### 7. State laden/speichern
```javascript
async function loadState()
async function saveState()
```

---

## 📡 Kommunikation (Frontend ↔ Backend)

### State synchronisieren
```javascript
// Frontend speichert State
fetch('/api/state', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(state)
})
.then(r => r.json())
.then(data => console.log(data))

// Frontend lädt State
fetch('/api/state')
.then(r => r.json())
.then(data => state = data)
```

---

## 🎯 Beispiel: Kompletter Veto-Prozess

### 1. State initialisieren
```javascript
state = {
  team1Name: "FaZe Clan",
  team2Name: "NAVI",
  format: "bo3",
  selectedMaps: ["Mirage", "Inferno", "Nuke", "Vertigo", "Anubis", "Ancient", "Dust2"],
  picks: [],
  game: "cs2",
  textColor: "white"
}
```

### 2. Veto-Reihenfolge abrufen
```javascript
veto_order = getVetoOrder("bo3", "Team 1", "Team 2", 7, "Team 1")
// Returns array with 8 steps: ban, ban, ban, ban, ban, ban, pick, pick
```

### 3. Maps anzeigen
```javascript
updateMapButtons()  // Zeigt 7 clicable Map-Buttons
```

### 4. Team bannt/pickt
```javascript
handleMapClick("Mirage")
// → Team 1 bannt Mirage
// → AddActionCard wird aufgerufen
// → State wird updated
// → UI wird aktualisiert
```

### 5. State speichern
```javascript
saveState()  // Speichert state in /api/state
// → Speichert auch in vetoresult.json
```

---

## 🔐 CORS & Sicherheit

Die App hat CORS aktiviert:
```python
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
```

**Hinweis:** Für Produktionseinsatz sollte CORS eingeschränkt werden.

---

## 📊 Datenfluss-Diagramm

```
Frontend (Browser)
    ↓
game_select.html
    ↓
CS-index.html / R6-index.html (Setup)
    ↓
User klickt Map → handleMapClick()
    ↓
addActionCard() + updateUI()
    ↓
saveState() → POST /api/state
    ↓
Backend (app.py)
    ↓
save vetoresult.json
    ↓
result.html / scores.html laden State
    ↓
OBS Browser Source zeigt Ergebnis
```

---

## 🧪 Test-URLs

```
http://localhost:5000/               # Spielauswahl
http://localhost:5000/cs2            # CS2 Setup
http://localhost:5000/r6             # R6 Setup
http://localhost:5000/result         # Ergebnis (OBS)
http://localhost:5000/scores         # Scores (OBS)
http://localhost:5000/anleitung      # Bedienung
http://localhost:5000/api/state      # JSON State
http://localhost:5000/exit           # Exit App
```

---

**Version:** 3.0
**Letzte Aktualisierung:** 2026-02-04
