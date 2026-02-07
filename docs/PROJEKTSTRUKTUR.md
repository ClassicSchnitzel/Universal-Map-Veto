# Projektstruktur - Universal MapVeto Tool

Diese Struktur ist optimiert für GitHub und lokale Entwicklung.

```
Universal-MapVeto/
│
├── 📄 app.py                          # Flask Backend (Hauptdatei)
├── 📄 requirements.txt                # Python Dependencies
├── 📄 .gitignore                      # Git Ignore Rules
├── 📄 LICENSE                         # MIT Lizenz
├── 📄 README.md                       # GitHub Readme
│
├── 📁 templates/                      # HTML Templates (Jinja2)
│   ├── game_select.html               # Spielauswahl (Startseite)
│   ├── CS-index.html                  # CS2 Kontrollfenster
│   ├── R6-index.html                  # R6 Kontrollfenster
│   ├── result.html                    # Ergebnis-Anzeige
│   ├── scores.html                    # Score-Tracking
│   └── obs-overlay.html               # OBS Overlay (optional)
│
├── 📁 static/                         # Statische Assets
│   ├── 📁 css/
│   │   └── shared.css                 # Gemeinsames Styling
│   ├── 📁 js/
│   │   └── shared.js                  # Gemeinsame Funktionen
│   ├── 📁 fonts/
│   │   └── (Schriftdateien)
│   └── 📁 maps/
│       └── (R6 Map-Bilder in JPG/PNG)
│
├── 📁 docs/                           # Dokumentation
│   ├── SETUP.md                       # Entwickler Setup Guide
│   ├── API.md                         # API Dokumentation
│   └── BEDIENUNG.md                   # Benutzer-Handbuch (Alt)
│
├── 📁 config/                         # Konfiguration (optional)
│   └── config.example.py              # Beispiel-Konfiguration
│
└── 📁 build/                          # Build Ordner (in .gitignore)
    └── MapVeto/ (wird ignoriert)
```

## 📋 Datei-Beschreibungen

### Hauptdateien
- **app.py** - Alle Flask-Routen und Server-Logik
- **requirements.txt** - Alle Python-Abhängigkeiten (pip install)
- **.gitignore** - Dateien die Git ignorieren soll (build/, __pycache__, etc.)
- **LICENSE** - MIT Lizenz für das Projekt
- **README.md** - Hauptdokumentation (wird auf GitHub angezeigt)

### Templates/ Ordner
Jinja2 HTML-Templates für die Weboberfläche:
- **game_select.html** - Startseitenmenü (CS2 oder R6 wählen)
- **CS-index.html** - Counter-Strike 2 Kontrollfenster
- **R6-index.html** - Rainbow Six Siege Kontrollfenster
- **result.html** - Veto-Ergebnis-Anzeige (für OBS)
- **scores.html** - Score-Tracking (für OBS)
- **obs-overlay.html** - Optionales OBS-Overlay

### Static/ Ordner
Alle statischen Ressourcen (JavaScript, CSS, Bilder):

#### static/css/
- **shared.css** - Alle Styles (Flexbox, Farben, Responsive Design)

#### static/js/
- **shared.js** - Map-Definitionen und Hilfsfunktionen

#### static/fonts/
- Schriftdateien (falls custom fonts verwendet)

#### static/maps/
- **R6 Map-Bilder** (JPG/PNG)
- CS2 Maps sind externe URLs

### Docs/ Ordner
Zusätzliche Dokumentation:
- **SETUP.md** - Installation und Entwickler-Setup
- **API.md** - API Endpoints Referenz
- **BEDIENUNG.md** - Ausführliches Benutzer-Handbuch

## 🚀 Für GitHub High laden

### Schritt 1: Repository initialisieren
```bash
git init
git add .
git commit -m "Initial commit: Universal MapVeto Tool v3.0"
```

### Schritt 2: Mit GitHub verbinden
```bash
git remote add origin https://github.com/ClassicSchnitzel/Universal-MapVeto.git
git branch -M main
git push -u origin main
```

### Schritt 3: .gitignore Prüfen
Diese Ordner/Dateien werden NICHT hochgeladen:
- ❌ build/ (PyInstaller output)
- ❌ __pycache__/ (Python Cache)
- ❌ venv/ (Virtual Environment)
- ❌ *.exe (Executables)
- ❌ .env (Umgebungsvariablen)
- ❌ vetoresult.json (Generated file)

## 📦 Installation nach GitHub

Benutzer können dann einfach:
```bash
git clone https://github.com/ClassicSchnitzel/Universal-MapVeto.git
cd Universal-MapVeto
pip install -r requirements.txt
python app.py
```

## 🔧 Entwickler-Setup

Siehe [docs/SETUP.md](../docs/SETUP.md) für detaillierte Anweisungen.

---

**Diese Struktur ist GitHub-ready und sauber! ✨**
