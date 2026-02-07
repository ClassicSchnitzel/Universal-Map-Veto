# Universal MapVeto Tool

> Professionelle Map-Veto-Verwaltung für Esports-Turniere und Live-Streams

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.0-green.svg)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)

---

## 📋 Überblick

Das **Universal MapVeto Tool** ist eine benutzerfreundliche Anwendung zur automatisierten Verwaltung von Map-Veto-Prozessen in professionellen Esports-Serien. Mit Live-Ergebnissen, Score-Tracking und OBS-Integration ist es ideal für Streamer, Turniere und Teams.

**Unterstützte Spiele:**
- 🎮 **Counter-Strike 2 (CS2)** - BO1, BO3, BO5
- 🎮 **Rainbow Six Siege (R6)** - BO1, BO2, BO3, BO5

---

## ✨ Features

### 🎯 Kern-Features
- ✅ **Automatisierte Veto-Reihenfolgen** für alle Formate (BO1/BO2/BO3/BO5)
- ✅ **Visuelle Map-Auswahl** mit Bildern und klarer Anzeige
- ✅ **Team-Verwaltung** mit Logos (Datei/URL), Namen und Kurznamen
- ✅ **Live-Ergebnis-Anzeige** mit Action Cards (Ban/Pick/Decider)
- ✅ **Score-Tracking** mit automatischer Berechnung
- ✅ **Anpassbare Textfarben** (Weiß/Schwarz) für alle Ausgaben

### 🔗 Integration & Streaming
- ✅ **OBS-Integration** mit Browser-Quellen
- ✅ **Mehrere Fenster-Layout** - Kontrollfenster, Ergebnis, Scores
- ✅ **Automatische Datenpeicherung** in JSON-Format
- ✅ **Responsive Design** für verschiedene Bildschirmauflösungen

### 🎨 Benutzerfreundlichkeit
- ✅ **Intuitive Oberfläche** mit visuellen Elementen
- ✅ **Sicherheits-Warnungen** bei zu wenigen Maps
- ✅ **Einzelinstanz-Management** - nur eine Instanz läuft
- ✅ **Dark Mode** für lange Streaming-Sessions

---

## 🚀 Installation

### Systemanforderungen
- **OS:** Windows 10 oder höher
- **Python:** 3.8+ (falls aus Quelle installiert)
- **RAM:** 512 MB minimum
- **Bildschirm:** Dual-Monitor empfohlen

### Schnellstart

#### Option 1: Executable (Einfach)
```bash
1. Laden Sie "Universal MapVeto.exe" herunter
2. Doppelklick zum Starten
3. Fenster öffnen sich automatisch auf http://localhost:5000
```

#### Option 2: Aus Quelle (Entwicklung)
```bash
# Repository klonen
git clone https://github.com/ClassicSchnitzel/Universal-MapVeto.git
cd Universal-MapVeto

# Abhängigkeiten installieren
pip install -r requirements.txt

# Anwendung starten
python app.py
```

---

## 📖 Bedienung

### Schritt 1: Spielauswahl
Starten Sie das Tool und wählen Sie zwischen:
- **CS2** - Counter-Strike 2
- **Rainbow Six Siege** - Rainbow Six

### Schritt 2: Setup-Fenster
Konfigurieren Sie:
1. **Veto-Format** (BO1/BO3/BO5 oder R6: BO1/BO2/BO3/BO5)
2. **Textfarbe** (Weiß/Schwarz)
3. **Team 1 & 2** - Namen, Kurznamen, Logos
4. **Map-Pool** - Wählen Sie 7-8 Maps aus
5. **Starting Team** - Welches Team beginnt

### Schritt 3: Veto-Prozess
- Klicken Sie auf Maps um diese zu bannen/picken
- Das System zeigt automatisch die Aktion an
- Action Cards dokumentieren alle Vetos
- Letzte verbleibende Map wird als **Decider** markiert

### Schritt 4: OBS-Integration
Verwenden Sie diese URLs in OBS:
- **Ergebnis:** `http://localhost:5000/result`
- **Scores:** `http://localhost:5000/scores`

---

## 🎮 Veto-Reihenfolgen

### CS2 BO3 (Standard)
```
1. Team A bannt Map 1
2. Team B bannt Map 2
3. Team A bannt Map 3
4. Team B bannt Map 4
5. Team A bannt Map 5
6. Team B bannt Map 6
7. Team A pickt Map A
8. Team B pickt Map B
→ 1 Map übrig = DECIDER
```

### R6 BO2 (Einzigartig - KEINE Decider)
```
1-6. Beide Teams bannen (3 Bans pro Team)
7.   Team A pickt Map 1
8.   Team B pickt Map 2
→ Garantiert 2 Maps für beide Teams
```

*Detaillierte Reihenfolgen siehe Bedienung (/anleitung)*

---

## 📊 Datenformat

Veto-Ergebnisse werden automatisch in `vetoresult.json` gespeichert:

```json
{
  "team1Name": "FaZe Clan",
  "team1Short": "FaZe",
  "team2Name": "NAVI",
  "team2Short": "NAVI",
  "format": "bo3",
  "maps": ["Inferno"],
  "picks": [
    {
      "team": "Team 1",
      "map": "Mirage",
      "type": "ban"
    }
  ],
  "textColor": "white",
  "game": "cs2"
}
```

---

## 🔧 Entwicklung

### Projektstruktur
```
Universal-MapVeto/
├── app.py                 # Flask Backend
├── templates/
│   ├── game_select.html   # Spielauswahl
│   ├── CS-index.html      # CS2 Kontrollfenster
│   ├── R6-index.html      # R6 Kontrollfenster
│   ├── result.html        # Ergebnis-Anzeige
│   ├── scores.html        # Score-Tracking
│   └── obs-overlay.html   # OBS Overlay (optional)
├── static/
│   ├── shared.js          # Gemeinsame Funktionen
│   ├── shared.css         # Gemeinsames Styling
│   └── Maps/              # Map-Bilder (R6)
├── vetoresult.json        # Veto-Ergebnisse (Auto-generiert)
└── README.md              # Diese Datei
```

### Abhängigkeiten
```
Flask==2.3.0
Pillow==9.5.0
pystray==0.19.4
```

### Erweiterungen hinzufügen
1. Neue Map-Definitionen in `shared.js` hinzufügen
2. Veto-Logik in Template-Dateien anpassen
3. CSS in `shared.css` ergänzen

---

## 🎯 Tipps für Streamer

### Optimal Setup für Mehrmonitor
```
Monitor 1: Kontrollfenster (Setup & Veto)
Monitor 2: Ergebnis-Fenster (OBS Browser Source)
Monitor 3: Score-Fenster (OBS Browser Source)
```

### Logo-Empfehlungen
- **Größe:** 256x256 oder 512x512 Pixel
- **Format:** PNG (mit Transparenz) oder JPG
- **Verhältnis:** Quadratisch (1:1)

### OBS Browser Source
```
URL: http://localhost:5000/result
Breite: 1920
Höhe: 1080
Aktualisierungsrate: 30 FPS
```

---

## 🐛 Fehlersuche

### Problem: Port 5000 bereits in Verwendung
**Lösung:** Ändern Sie den Port in `app.py`:
```python
app.run(host='127.0.0.1', port=5001, debug=False)
```

### Problem: Logos laden nicht
**Lösung:**
- Überprüfen Sie Dateigröße (unter 5MB)
- Format muss JPG oder PNG sein
- Falls URL: Testen Sie diese im Browser

### Problem: Fenster öffnet sich nicht
**Lösung:**
- Stellen Sie sicher, dass Port 5000 frei ist
- Antivirus kann den Zugriff blockieren
- Probieren Sie einen anderen Browser (Edge, Chrome)

---

## 📝 Lizenz

Dieses Projekt ist unter der **MIT License** lizenziert - siehe [LICENSE](LICENSE) für Details.

---

## 👨‍💻 Autor

**ClassicSchnitzel**
- GitHub: [@ClassicSchnitzel](https://github.com/ClassicSchnitzel)
- Kontakt: Discord oder GitHub Issues

---

## 🙏 Credits

- **Frameworks:** Flask, Jinja2
- **Libraries:** Pillow, pystray
- **Icons & Assets:** Community contributions

---

## 📊 Statistiken

- **Unterstützte Formate:** 7 (BO1, BO2, BO3, BO5 für CS2 & R6)
- **Maps:** 7 (CS2) + 9 (R6)
- **Veto-Sequenzen:** 8+ automatisierte Reihenfolgen
- **Benutzer pro Instanz:** Unbegrenzt (Multi-Client)

---

## 🤝 Beitragen

Interessiert an Verbesserungen? Hier ist wie:

1. Fork dieses Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit deine Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Öffne einen Pull Request

---

## 📮 Support

Haben Sie Fragen oder Probleme?
- 📧 **GitHub Issues:** Erstellen Sie ein Ticket
- 💬 **Discord:** Community-Support
- 📖 **In-App Guide:** `/anleitung` Seite aufrufen

---

## 🎉 Changelog

### v3.0 (Aktuell)
- ✨ Team-Kurznamen System
- ✨ Visuelle Action Cards (Ban/Pick/Decider)
- ✨ Erweiterte Veto-Reihenfolgen
- 🐛 Decider-Logik für BO5 korrigiert
- 📈 Performance-Optimierungen

### v2.5
- ✨ BO2 Support für R6
- 🐛 UI Verbesserungen

### v2.0
- ✨ Redesign mit visuellen Karten
- ✨ OBS-Integration

### v1.0
- 🎉 Initial Release

---

## 📄 Zusätzliche Ressourcen

- [Bedienung (In-App)](/anleitung)
- [API-Dokumentation](#) (Coming Soon)
- [Entwickler-Leitfaden](#) (Coming Soon)

---

<div align="center">

**⭐ Wenn dir dieses Projekt gefällt, gib uns einen Star! ⭐**

Made with ❤️ by ClassicSchnitzel

</div>
