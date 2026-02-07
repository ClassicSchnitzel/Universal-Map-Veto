#!/usr/bin/env python3
import subprocess
import webbrowser
import time
import os
import json
import threading
import sys
import atexit
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'universal-mapveto-secret-key-2026'  # Für Sessions

# Globaler State
veto_state = {}
lock = threading.Lock()
tray_icon = None

# Lade Übersetzungen
translations = {}
try:
    translations_path = Path(__file__).resolve().parent / "translations.json"
    with open(translations_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)
except Exception as e:
    print(f"[WARN] Translations konnten nicht geladen werden: {e}")
    translations = {"de": {}, "en": {}}

def get_language():
    """Gibt die aktuelle Sprache aus der Session zurück (Standard: de)"""
    try:
        return session.get('language', 'de')
    except:
        return 'de'

def get_translations():
    """Gibt die Übersetzungen für die aktuelle Sprache zurück"""
    try:
        lang = get_language()
        return translations.get(lang, translations.get('de', {}))
    except:
        return translations.get('de', {})

def _lock_file_path():
    return Path(__file__).resolve().parent / ".mapveto.lock"


def _is_pid_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}"],
            capture_output=True,
            text=True,
            check=False,
        )
        return str(pid) in (result.stdout or "")
    except Exception:
        return False


def _terminate_pid(pid: int) -> bool:
    try:
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/F"],
            capture_output=True,
            text=True,
            check=False,
        )
        return True
    except Exception:
        return False


def ensure_single_instance():
    lock_path = _lock_file_path()
    if lock_path.exists():
        try:
            old_pid = int(lock_path.read_text(encoding="utf-8").strip() or "0")
        except Exception:
            old_pid = 0
        if old_pid and _is_pid_running(old_pid):
            print(f"[OK] Vorherige Instanz gefunden (PID {old_pid}) – wird beendet...")
            _terminate_pid(old_pid)
            time.sleep(1)
    try:
        lock_path.write_text(str(os.getpid()), encoding="utf-8")
    except Exception as e:
        print(f"[WARN] Lock-Datei konnte nicht geschrieben werden: {e}")

    def _cleanup_lock():
        try:
            if lock_path.exists():
                current_pid = os.getpid()
                try:
                    stored_pid = int(lock_path.read_text(encoding="utf-8").strip() or "0")
                except Exception:
                    stored_pid = 0
                if stored_pid == current_pid:
                    lock_path.unlink(missing_ok=True)
        except Exception:
            pass

    atexit.register(_cleanup_lock)


def save_state():
    """Speichere State in JSON für OBS"""
    try:
        with lock:
            with open("vetoresult.json", "w", encoding='utf-8') as f:
                json.dump(veto_state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Fehler: {e}")

def start_tray_icon():
    """Startet ein Tray-Icon zum Beenden der App (Windows)."""
    try:
        import pystray
        from PIL import Image
    except Exception as e:
        print(f"[WARN] Tray-Icon nicht verfügbar: {e}")
        return

    icon_path = Path(__file__).resolve().parent / "icon.ico"
    if not icon_path.exists():
        print("[WARN] icon.ico nicht gefunden – Tray-Icon wird ohne Bild gestartet.")
        tray_image = None
    else:
        try:
            tray_image = Image.open(str(icon_path))
        except Exception:
            tray_image = None

    def _exit_action(icon, item):
        try:
            save_state()
        finally:
            os._exit(0)

    menu = pystray.Menu(pystray.MenuItem("Programm beenden", _exit_action))
    global tray_icon
    tray_icon = pystray.Icon("Universal MapVeto", tray_image, "Universal MapVeto", menu)
    try:
        tray_icon.run_detached()
    except Exception:
        thread = threading.Thread(target=tray_icon.run, daemon=True)
        thread.start()

@app.route('/')
def index():
    return render_template('game_select.html', t=get_translations(), lang=get_language())

@app.route('/cs2')
def cs2():
    return render_template('CS-index.html', t=get_translations(), lang=get_language())

@app.route('/r6')
def r6():
    return render_template('R6-index.html', t=get_translations(), lang=get_language())

@app.route('/result')
def result():
    return render_template('result.html', t=get_translations(), lang=get_language())

@app.route('/scores')
def scores():
    return render_template('scores.html', t=get_translations(), lang=get_language())

@app.route('/set_language/<lang>')
def set_language(lang):
    """Setzt die Sprache in der Session"""
    if lang in ['de', 'en']:
        session['language'] = lang
        return jsonify({'status': 'success', 'language': lang})
    return jsonify({'status': 'error', 'message': 'Invalid language'}), 400

@app.route('/obs')
def obs():
    return render_template('obs-overlay.html', t=get_translations(), lang=get_language())

@app.route('/anleitung')
def anleitung():
    """Zeige die Bedienung als HTML-Seite an"""
    bedienung_content = """╔═══════════════════════════════════════════════════════════════════════════╗
║         UNIVERSAL MAPVETO TOOL - VOLLSTÄNDIGE BEDIENUNGSANLEITUNG        ║
║                      Created by ClassicSchnitzel                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

INHALTSVERZEICHNIS
══════════════════
1. Überblick
2. Installation und erste Schritte
3. Hauptmenü und Spielauswahl
4. Setup-Fenster (Kontrollfenster)
5. Veto-Prozess
6. Ergebnis-Fenster
7. Score-Tracking
8. OBS-Integration
9. Besonderheiten pro Spiel
10. Tipps & Tricks
11. Fehlersuche


1. ÜBERBLICK
════════════
Das Universal MapVeto Tool verwaltet Map-Vetos für mehrere Spiele professionell.
Es bietet eine benutzerfreundliche Oberfläche zur Verwaltung von Team-Vetoprozessen
mit Live-Ergebnis-Anzeige und Score-Tracking.

Unterstützte Spiele:
    • CS2 (Counter-Strike 2)        - BO1, BO3, BO5
    • Rainbow Six Siege (R6)         - BO1, BO2, BO3, BO5

Features:
    ✓ Team-Logos (Datei-Upload oder URL)
    ✓ Team-Kurznamen/Shortcodes
    ✓ Anpassbare Textfarbe (Weiß/Schwarz)
    ✓ Visuelle Map-Auswahl mit Bildern
    ✓ Live-Ergebnis-Anzeige
    ✓ Score-Tracking
    ✓ OBS-Integration (Browsersource)
    ✓ Automatische Datenpeicherung


2. INSTALLATION & ERSTE SCHRITTE
═════════════════════════════════

a) Starten Sie "Universal MapVeto.exe"
     → Automatisch werden 3 Fenster geöffnet:
        1. Kontrollfenster (Setup & Veto-Management)
        2. Ergebnis-Fenster (für OBS/Stream)
        3. Score-Fenster (für Punktestand)

b) Falls Fenster nicht öffnen, manuell aufrufen:
     • Setup:     http://localhost:5000/
     • Ergebnis:  http://localhost:5000/result
     • Scores:    http://localhost:5000/scores
     • Anleitung: http://localhost:5000/anleitung

c) Fenster-Layout für Streamer:
     Monitor 1: Kontrollfenster (Setup, Veto-Management)
     Monitor 2: Ergebnis-Fenster (OBS Browser Source)
     Monitor 3: Score-Fenster (OBS Browser Source)


3. HAUPTMENÜ - SPIELAUSWAHL
════════════════════════════

Das erste Fenster zeigt 3 Optionen:

     [CS2]               → Startet CS2 Veto-Tool
     [Rainbow Six]       → Startet R6 Veto-Tool
     [Bedienung]         → Zeigt diese Anleitung

     Button "Programm beenden" → Beendet das gesamte Tool


4. SETUP-FENSTER (KONTROLLFENSTER)
════════════════════════════════════

Das Kontrollfenster ist die zentrale Verwaltungsstelle für den gesamten
Veto-Prozess. Hier konfigurieren Sie Teams, Maps, Logos und starten den Veto.


SCHRITT A: VETO-FORMAT WÄHLEN
────────────────────────────
Wählen Sie das beste-of Format für die Serie:

    CS2:  [BO1]  [BO3]  [BO5]
    R6:   [BO1]  [BO2]  [BO3]  [BO5]

Das Format bestimmt:
    • Empfohlene Map-Anzahl (BO1/BO3=7, BO2=8, BO5=7)
    • Veto-Reihenfolge (Bans und Picks)
    • Ob es einen "Decider" gibt (letzte verbleibende Map)


SCHRITT B: TEXTFARBE WÄHLEN
──────────────────────────
Wählen Sie die Textfarbe für die Ergebnis- und Score-Fenster:

    [●] Weiß    [●] Schwarz

Diese Farbe wird auf allen Anzeigeseiten (result.html, scores.html) verwendet.


SCHRITT C: TEAM 1 KONFIGURIEREN
───────────────────────────────
    Team-Name:     Geben Sie den vollständigen Teamnamen ein (z.B. "FaZe Clan")
    Team-Kürzel:   Optionales Shortcode (z.B. "FaZe") - wird bevorzugt angezeigt

    Team-Logo:
        • DATEI: Klick "Datei auswählen" → JPG oder PNG hochladen
                 Beste Größe: Quadratische Bilder
        • ODER URL: Link zu Logo einfügen (z.B. Team-Website)
        • Hinweis: Datei-Upload hat Priorität vor URL!


SCHRITT D: TEAM 2 KONFIGURIEREN
───────────────────────────────
Wie Team 1 - wiederholen Sie den Prozess für Team 2.


SCHRITT E: MAP-POOL AUSWÄHLEN
─────────────────────────────
Maps werden als visuelle Karten angezeigt:

    CS2 verfügbare Maps:
        • Mirage, Inferno, Nuke, Vertigo, Anubis, Ancient, Dust2

    R6 verfügbare Maps:
        • Bank, Border, Chalet, Clubhouse, Consulate, Kafe, Oregon, Skyscraper, Villa

Auswahl:
    • Klicken Sie auf Map-Karten um sie auszuwählen/abzuwählen
    • Zähler oben links zeigt aktuelle Anzahl: "X/Y Maps"
    • Empfohlene Anzahl wird automatisch bei Format-Änderung gesetzt

    Format-Empfehlungen:
        CS2:
            • BO1: 7 Maps
            • BO3: 7 Maps
            • BO5: 7 Maps
        R6:
            • BO1: 7 Maps
            • BO2: 8 Maps
            • BO3: 7 Maps
            • BO5: 7 Maps

    Sicherheitswarnung:
        • Weniger als 3 Maps → Warnung vor Veto-Start
        • Sie müssen dennoch bestätigen, wenn gewünscht


SCHRITT F: STARTING TEAM WÄHLEN
──────────────────────────────
Wählen Sie, welches Team den Veto-Prozess beginnt:

    [Team 1]  [Team 2]

Das Starting Team wird das erste Ban oder Pick machen.


SCHRITT G: NEUES VETO STARTEN
──────────────────────────────
Klick auf:
    [Veto starten]

Das System startet den automatisierten Veto-Prozess und zeigt live:
    • Aktuelles Team (wer ist dran)
    • Verfügbare Maps (klickbar)
    • Veto-Reihenfolge


5. VETO-PROZESS
════════════════

Während des Vetos:

    AKTUELLE AKTION:
    ────────────────
    Wird oben angezeigt:
        "Team 1 bannt..." oder "Team 2 pickt..."

    MAP AUSWAHL:
    ───────────
    • Klicken Sie auf die gewünschte Map
    • Maps verschwinden sofort nach Auswahl
    • Das System speichert automatisch die Aktion

    ACTION CARDS (Veto-Verlauf):
    ──────────────────────────
    Jede Aktion wird als Karte angezeigt:
        ┌─────────────────────┐
        │  [Map-Bild]         │
        │  Team: Kürzel/Name  │
        │  Map: Name          │
        │  BAN / PICK / DECIDER
        └─────────────────────┘

    Farben:
        • BAN:     Rote Karte
        • PICK:    Grüne Karte
        • DECIDER: Gold/Gelb Karte (letzte verbleibende Map in BO1/BO3/BO5)


VETO-REIHENFOLGEN
─────────────────

CS2 BO1 (3 Bans pro Team):
    1. Team A bannt
    2. Team B bannt
    3. Team A bannt
    4. Team B bannt
    5. Team A bannt
    6. Team B bannt
    → 1 Map übrig = DECIDER (letzte Map)

CS2 BO3 (3 Bans pro Team + Picks):
    1. Team A bannt
    2. Team B bannt
    3. Team A bannt
    4. Team B bannt
    5. Team A bannt
    6. Team B bannt
    7. Team A pickt
    8. Team B pickt
    → 1 Map übrig = DECIDER

CS2 BO5 (3 Bans pro Team + 2 Picks):
    1. Team A bannt
    2. Team B bannt
    3. Team A bannt
    4. Team B bannt
    5. Team A bannt
    6. Team B bannt
    7. Team A pickt
    8. Team B pickt
    9. Team A pickt
    10. Team B pickt
    → 1 Map übrig = DECIDER

R6 BO1 (wie CS2 BO1):
    → 3 Bans pro Team, 1 DECIDER

R6 BO2 (6 Bans, 2 Picks):
    1. Team A bannt
    2. Team B bannt
    3. Team A bannt
    4. Team B bannt
    5. Team A bannt
    6. Team B bannt
    7. Team A pickt Map 1
    8. Team B pickt Map 2
    → KEINE DECIDER! (2 Maps für beide Teams garantiert)

R6 BO3 (wie CS2 BO3):
    → 3 Bans pro Team, 2 Picks pro Team, 1 DECIDER

R6 BO5 (wie CS2 BO5):
    → 3 Bans pro Team, 2 Picks pro Team, 1 DECIDER


6. ERGEBNIS-FENSTER
═══════════════════

Das Ergebnis-Fenster zeigt:
    • Team 1 vs Team 2 (mit Logos und Kurznamen)
    • Alle drei Maps der Serie in visuellen Karten
    • Veto-Verlauf mit Action Cards (Ban/Pick/Decider)

    Für OBS:
    ────────
    Nutzen Sie diese URL als Browser Source:
        http://localhost:5000/result

    Empfohlene Größe: 1920x1080 (Vollscreen ist möglich)

    Copy-Button:
    ────────────
    Am oberen Rand gibt es einen [Kopieren]-Button zum Kopieren der OBS-URL
    in die Zwischenablage.


7. SCORE-TRACKING
══════════════════

Das Score-Fenster zeigt die aktuellen Ergebnisse:

    CS2 Scoring:
    ────────────
    • Jede Map = max. 16 Punkte
    • Sieg: 13 Punkte zuerst oder 16 Punkte absolut
    • Team-Namen in gewählter Farbe (Weiß/Schwarz)

    R6 Scoring:
    ───────────
    • Jede Map = 7 Punkte zum Gewinnen
    • Serie-Sieg: 7 Punkte mit 2 Punkten Vorsprung
    • Team-Namen in gewählter Farbe (Weiß/Schwarz)

    Eingaben:
    ────────
    Sie können direkt in die Score-Felder klicken und Punkte eingeben:
        • Team 1 Score für Map 1: [   ]
        • Team 2 Score für Map 1: [   ]
        • (für jede gespielte Map)

    Für OBS:
    ────────
    Browser Source URL:
        http://localhost:5000/scores

    Empfohlene Größe: 1920x1080 oder angepasst an Überlage


8. OBS-INTEGRATION
═══════════════════

Browsersources in OBS hinzufügen:

    1. Öffnen Sie OBS Studio
    2. Klick: "+ Quelle" → Browser
    3. URL eingeben: http://localhost:5000/result  (oder /scores)
    4. Breite: 1920, Höhe: 1080
    5. Klick OK

    Mehrere Quellen möglich:
    ────────────────────
    • Quelle 1: http://localhost:5000/result (Veto-Ergebnis)
    • Quelle 2: http://localhost:5000/scores (Score-Tracking)

    Sie können Größe und Position individuell in OBS anpassen.


9. BESONDERHEITEN PRO SPIEL
═════════════════════════════

CS2:
────
• Formate: BO1, BO3, BO5
• Available Maps: 7
• Starting Team: Wechselt automatisch zwischen Serien
• Decider: Zeigt letzte Map klar an
• Score: 0-16 Punkte pro Map

Rainbow Six Siege:
──────────────────
• Formate: BO1, BO2, BO3, BO5
• Available Maps: 9
• BO2 Besonderheit: KEINE DECIDER (immer 2 Maps picked)
• Starting Team: Kann gewählt werden
• Score: 0-7 Punkte pro Map


10. TIPPS & TRICKS
═════════════════

Monitor-Setup für Streamer:
──────────────────────────
    Monitor 1: Kontrollfenster (1280x800)
              → Nur Sie sehen das Setup
    Monitor 2: Ergebnis-Fenster (1920x1080)
              → OBS Browser Source
    Monitor 3: Score-Fenster (1920x1080)
              → OBS Browser Source
              
Alternative: Fenster arrangieren und Teile screenshauren

Team-Logos:
───────────
    • Beste Größe: 512x512 oder 256x256 Pixel
    • Formate: JPG, PNG (transparent möglich)
    • URL-Beispiel: https://example.com/logo.png
    • Datei-Upload: Lokale Datei hat Vorrang

Team-Namen & Kurznamen:
───────────────────────
    • Vollname: "Team Name" (wird in Setup angezeigt)
    • Kürzel: "TN" (wird bevorzugt in result.html und scores.html angezeigt)
    • Beispiel: Vollname="FaZe Clan", Kürzel="FaZe"

Neues Veto schnell starten:
──────────────────────────
    • Button "Neues Veto starten" → Setzt alles zurück
    • Maps-Auswahl bleibt erhalten
    • Team-Infos bleiben erhalten

Fehlerhafte Auswahl korrigieren:
─────────────────────────────
    • Während Veto läuft → Neue Serie starten
    • "Neues Veto starten" Button
    • Alle bisherigen Actionen werden gelöscht

Datenpeicherung:
────────────────
    • Alle Ergebnisse speichern automatisch in "vetoresult.json"
    • Datei wird nach jedem Veto-Schritt aktualisiert
    • Für Rekordierungen oder Archivierung nutzbar


11. FEHLERSUCHE
════════════════

Problem: Fenster öffnet sich nicht / Port 5000 in Verwendung
─────────────────────────────────────────────────────────────
Lösung:
    • Ändern Sie Port in app.py: app.run(..., port=5001, ...)
    • Oder stoppen Sie andere Programme, die Port 5000 verwenden
    • netstat -ano | findstr :5000  (in PowerShell zum Prüfen)

Problem: Logos laden nicht
──────────────────────────
Lösung:
    • Überprüfen Sie die Dateigröße (unter 5MB)
    • Format muss JPG oder PNG sein
    • Falls URL: Testen Sie die URL im Browser direkt
    • Versuchen Sie eine neue Datei hochzuladen

Problem: Maps werden nicht angezeigt
─────────────────────────────────────
Lösung:
    • Aktualisieren Sie den Browser (F5)
    • Browser-Cache leeren (Ctrl+Shift+Delete)
    • Konsole öffnen (F12) und auf Fehler prüfen

Problem: Scores synchronisieren nicht
──────────────────────────────────────
Lösung:
    • Aktualisieren Sie das Score-Fenster (F5)
    • Prüfen Sie die Netzwerkverbindung (localhost sollte erreichbar sein)
    • Starten Sie das Tool neu

Problem: Score wird auf falsch berechnet
─────────────────────────────────────────
Lösung:
    • Geben Sie manuelle Scores ein
    • Oder starten Sie neues Veto mit korrekter Map-Auswahl

Problem: Decider wird nicht angezeigt (BO5)
────────────────────────────────────────────
Lösung:
    • Decider zeigt sich erst, wenn genau 1 Map übrig ist
    • In BO5 sollte dies nach 4 Maps der Fall sein
    • Überprüfen Sie, dass BO5 Format korrekt gesetzt ist

Problem: Programm stürzt ab
────────────────────────────
Lösung:
    • Fenster neu starten
    • Falls persistent: Aktualisieren Sie die Software


DATENFORMAT
════════════
Die Veto-Ergebnisse werden in vetoresult.json gespeichert:

    {
      "team1Name": "FaZe Clan",
      "team1Short": "FaZe",
      "team2Name": "NAVI",
      "team2Short": "NAVI",
      "format": "bo3",
      "maps": ["Inferno"],
      "selectedMaps": ["Inferno", "Mirage", "..."],
      "picks": [
        {"team": "Team 1", "map": "Mirage", "type": "ban"},
        ...
      ],
      "textColor": "white",
      "game": "cs2"
    }


TASTENKÜRZEL (Browser)
══════════════════════
    F5              Seite aktualisieren
    F12             Entwickler-Konsole (für Debugging)
    Ctrl+Shift+Del  Cache leeren
    Ctrl+P          Drucken


SUPPORT & UPDATES
═════════════════
Dieses Tool wurde von ClassicSchnitzel erstellt.


Datum: 2026
═════════════════════════════════════════════════════════════════════════════"""
    
    html = f"""<!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <title>CS2 Map Veto Tool - Bedienung</title>
        <style>
            body {{
                background: #181c1f;
                color: #ffffff;
                font-family: 'Courier New', monospace;
                padding: 40px;
                max-width: 1000px;
                margin: 0 auto;
                line-height: 1.6;
            }}
            pre {{
                background: #222;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #00be29;
                overflow-x: auto;
            }}
            a {{
                color: #00be29;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <pre>{bedienung_content}</pre>
        <p style="text-align: center; margin-top: 40px;">
            <a href="/" style="background: #00be29; color: #000; padding: 10px 20px; border-radius: 4px; text-decoration: none;">← Zurück</a>
        </p>
    </body>
    </html>"""
    return html

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(veto_state)

@app.route('/api/state', methods=['POST'])
def set_state():
    global veto_state
    try:
        veto_state = request.get_json()
        save_state()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/exit')
def exit_app():
    """Beende die Anwendung sauber"""
    try:
        save_state()
        print("[OK] Programm wird beendet...")
        os._exit(0)
    except:
        return "Fehler beim Beenden", 500

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

def find_browser():
    """Suche nach Edge oder Chrome an verschiedenen Orten"""
    # Mögliche Pfade für Edge
    edge_paths = [
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    
    # Mögliche Pfade für Chrome
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    
    # Suche Edge
    for path in edge_paths:
        if os.path.exists(path):
            return "edge", path
    
    # Suche Chrome
    for path in chrome_paths:
        if os.path.exists(path):
            return "chrome", path
    
    # Kein Browser gefunden
    return None, None

if __name__ == '__main__':
    ensure_single_instance()
    # Initialisiere JSON-Datei
    save_state()
    print("[OK] MapVeto Server startet...")
    start_tray_icon()
    
    # Warte kurz, bis Server lädt
    time.sleep(1)
    
    # Öffne Browser
    browser_type, browser_path = find_browser()
    
    if browser_type == "edge":
        print(f"[OK] Öffne mit Microsoft Edge ({browser_path})...")
        subprocess.Popen([browser_path, "http://localhost:5000/"])
    elif browser_type == "chrome":
        print(f"[OK] Öffne mit Google Chrome ({browser_path})...")
        subprocess.Popen([browser_path, "http://localhost:5000/"])
    else:
        print("[OK] Öffne mit Standard-Browser...")
        webbrowser.open("http://localhost:5000/")
    
    print("[OK] Server läuft auf http://localhost:5000")
    print("[OK] OBS-Overlay: http://localhost:5000/obs")
    print("[OK] JSON-Datei: vetoresult.json")
    
    # Starte Server
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
