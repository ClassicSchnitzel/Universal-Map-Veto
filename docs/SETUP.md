# Setup & Installation - Universal MapVeto Tool

Dieses Dokument beschreibt die Installation und Einrichtung für Entwickler.

## 🚀 Schnellstart

### Voraussetzungen
- Windows 10+ oder Linux/macOS
- Python 3.8 oder höher
- Git (optional, aber empfohlen)

### 1. Repository klonen
```bash
git clone https://github.com/ClassicSchnitzel/Universal-MapVeto.git
cd Universal-MapVeto
```

### 2. Virtual Environment erstellen (optional, aber empfohlen)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 4. Anwendung starten
```bash
python app.py
```

Öffnen Sie dann:
- Setup: `http://localhost:5000/`
- Bedienung: `http://localhost:5000/anleitung`

---

## 📁 Ordnerstruktur

```
Universal-MapVeto/
├── app.py                      # Main Flask App
├── requirements.txt            # Dependencies
├── .gitignore                  # Git Config
├── LICENSE                     # MIT Lizenz
├── README.md                   # GitHub Readme
├── templates/                  # HTML Templates
│   ├── game_select.html
│   ├── CS-index.html
│   ├── R6-index.html
│   ├── result.html
│   ├── scores.html
│   └── obs-overlay.html
├── static/                     # Assets
│   ├── css/
│   │   └── shared.css
│   ├── js/
│   │   └── shared.js
│   ├── fonts/
│   └── maps/                   # R6 Map Images
├── docs/                       # Dokumentation
│   ├── SETUP.md               # (Diese Datei)
│   ├── API.md                 # API Referenz
│   ├── BEDIENUNG.md           # User Manual
│   └── PROJEKTSTRUKTUR.md     # Structure Docs
└── build/                      # Build Output (.gitignore)
```

---

## 🔧 Entwicklung

### Abhängigkeiten hinzufügen
Falls Sie neue Packages installieren:
```bash
pip install <package-name>
pip freeze > requirements.txt
```

### Code-Struktur

#### app.py - Flask Backend
```python
@app.route('/cs2')
def cs2():
    return render_template('CS-index.html')

@app.route('/api/state', methods=['GET', 'POST'])
def api_state():
    # State Management
    pass
```

#### templates/ - HTML/Jinja2
- Game Select: Spielauswahl-Interface
- CS-index.html & R6-index.html: Kontrollfenster
- result.html: Ergebnis-Display (OBS)
- scores.html: Score-Tracking (OBS)

#### static/js/shared.js
Zentrale Funktionen:
- `getVetoOrder(format, team1, team2, mapCount)` - Veto-Reihenfolge
- `getRecommendedMapCount(format)` - Empfohlene Map-Anzahl
- `updateMapButtons()` - Map-Buttons aktualisieren
- `handleMapClick(map)` - Map-Auswahl verarbeiten
- `addActionCard(action, team, map)` - Action Cards anzeigen
- `addDeciderCardIfAvailable()` - Decider-Logic

#### static/css/shared.css
- Layout: Flexbox & Grid
- Colors: Dark Mode (#181c1f)
- Cards: .action-card, .map-btn
- Responsive Design

### Modifizieren Sie die App

#### Neue Map hinzufügen (CS2)
In `static/js/shared.js`:
```javascript
const mapImagesByGame = {
    cs2: {
        'NEW_MAP': 'https://example.com/image.jpg',
        // ...
    }
};
```

#### Neue Route hinzufügen (Backend)
In `app.py`:
```python
@app.route('/new-route')
def new_route():
    return render_template('new-template.html')
```

#### Neuen Style hinzufügen
In `static/css/shared.css`:
```css
.new-class {
    display: flex;
    color: #ffffff;
}
```

---

## 🧪 Testen

### Manuelles Testen
1. Starten Sie `python app.py`
2. Öffnen Sie `http://localhost:5000/`
3. Testen Sie verschiedene Formate (BO1, BO3, BO5)
4. Überprüfen Sie OBS-Integration (`/result`, `/scores`)

### Browser-Konsole (F12)
Überprüfen Sie auf JavaScript-Fehler:
- Öffnen Sie die Entwickler-Tools (F12)
- Gehen Sie zum Tab "Console"
- Suchen Sie nach roten Fehlern

---

## 🔌 OBS-Integration

### Browser Source hinzufügen
1. In OBS Studio → Sources → "+"
2. Wählen Sie "Browser"
3. URL: `http://localhost:5000/result`
4. Breite: 1920, Höhe: 1080
5. OK klicken

### Debug-Modus (OBS)
Falls Inhalt nicht lädt:
- Stellen Sie sicher, dass Server läuft (`http://localhost:5000/`)
- Überprüfen Sie die Netzwerkverbindung
- Port 5000 muss frei sein

---

## 🚨 Häufige Probleme

### Problem: Port 5000 bereits in Verwendung
**Lösung:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5000
kill -9 <PID>
```

Oder ändern Sie Port in `app.py`:
```python
app.run(host='127.0.0.1', port=5001, debug=False)
```

### Problem: Module nicht gefunden
**Lösung:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: Virtual Environment aktiviert nicht
**Lösung:**
```bash
# Windows PowerShell (Administrator erforderlich)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Dann neu versuchen
venv\Scripts\activate
```

---

## 📝 Build für Windows EXE

### Requirements
```bash
pip install pyinstaller pillow pystray
```

### Build-Befehl
```bash
pyinstaller MapVeto.spec
```

Das erzeugt ein `dist/` Ordner mit der EXE.

### MapVeto.spec Beispiel
```python
# PyInstaller spec file
a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static')],
    hiddenimports=['pystray', 'PIL'],
    ...
)
```

---

## 🐛 Debugging

### Debug-Modus aktivieren
```python
# In app.py
app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
```

### Logs prüfen
```bash
# Terminal zeigt aktive Requests:
# [2026-02-04 10:00:00] GET / HTTP/1.1 200
# [2026-02-04 10:00:01] POST /api/state HTTP/1.1 200
```

### JavaScript Debugging
```javascript
// In Browser Console (F12)
console.log(state);  // State anzeigen
console.log(veto_order);  // Veto-Reihenfolge
```

---

## 📚 Weiterführende Ressourcen

- [Flask Dokumentation](https://flask.palletsprojects.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [PyInstaller Docs](https://pyinstaller.org/)

---

**Viel Spaß beim Entwickeln! 🎉**
