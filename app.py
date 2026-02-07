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
    # Lade Manual-Übersetzungen
    try:
        manual_path = Path(__file__).resolve().parent / "translations_manual.json"
        with open(manual_path, 'r', encoding='utf-8') as f:
            manual_translations = json.load(f)
        
        lang = get_language()
        manual_t = manual_translations.get(lang, manual_translations.get('de', {}))
        
        # Kombiniere mit regulären Übersetzungen für common-Elemente
        t = get_translations()
        t['manual'] = manual_t
        
        return render_template('anleitung.html', t=t, lang=lang)
    except Exception as e:
        print(f"[ERROR] Fehler beim Laden der Bedienung: {e}")
        return f"Fehler beim Laden der Bedienung: {e}", 500

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
