// shared.js - Gemeinsame Funktionen und Daten für alle Overlays

// Map-Bilder (zentral verwaltet)
const mapImagesByGame = {
  cs2: {
    Mirage:    "https://image2url.com/images/1764503489260-9008d34a-94bd-40e2-a4d1-0d34e33ffe87.jpg",
    Inferno:   "https://image2url.com/images/1764503475806-1b72d0b8-7a17-4cd5-aee6-47ae832f0773.jpg",
    Nuke:      "https://image2url.com/images/1764503506529-e9019ef0-06e1-4697-b48b-0e16acbf057e.jpg",
    Ancient:   "https://image2url.com/images/1764503293754-46c5a0e3-9e23-4512-89c7-dcb5772cb885.jpg",
    Anubis:    "https://image2url.com/images/1764503329090-208a8fb9-a2e4-4b16-ac6f-f80edabc3adb.jpg",
    Overpass:  "https://image2url.com/images/1764503517040-cad20bad-3899-40d8-9893-eb20f1319c0d.jpg",
    Vertigo:   "https://image2url.com/images/1764503539387-38efa7a7-efb1-4b46-8707-108bd396b3cc.jpg",
    Train:     "https://image2url.com/images/1764503528661-6cc72d80-8f1e-4396-a0ed-385aa313ae86.jpg",
    Dust2:     "https://image2url.com/images/1764503352970-00c749ac-9e3c-4f02-8d04-a9a3d14c37d0.jpg",
  },
  r6: {
    "Bank": "/static/Maps/Bank.jpg",
    "Border": "/static/Maps/Border.jpg",
    "Chalet": "/static/Maps/Chalet.jpg",
    "Clubhouse": "/static/Maps/Clubhouse.jpg",
    "Consulate": "/static/Maps/Consulate.jpg",
    "Kafe": "/static/Maps/Kafe Dostoyevsky.jpg",
    "Oregon": "/static/Maps/Oregon.jpg",
    "Skyscraper": "/static/Maps/Skyscraper.jpg",
    "Villa": "/static/Maps/Villa.jpg",
  }
};

function getMapImagesForGame(game) {
  if (game && mapImagesByGame[game]) return mapImagesByGame[game];
  return mapImagesByGame.cs2;
}

// Winner-Logik nach Spiel
function winnerOnMap(score1, score2, game = "cs2") {
  if (game === "r6") {
    // R6: Sieg ab 7 Runden mit 2 Runden Vorsprung
    if (score1 >= 7 && score1 - score2 >= 2) return 1;
    if (score2 >= 7 && score2 - score1 >= 2) return 2;
    return 0;
  }
  // CS2/CSGO-Regeln: 13+ gewinnt, bei >13 gewinnt das Team mit mehr Punkten
  if (score1 >= 13 || score2 >= 13) {
    if (score1 > score2) return 1;
    if (score2 > score1) return 2;
  }
  return 0;
}

// Lade Veto-Daten aus der API
async function loadVetoData() {
  try {
    const response = await fetch('/api/state?_=' + Date.now());
    if (response.ok) {
      const data = await response.json();
      if (data && Object.keys(data).length > 0) {
        return data;
      }
    }
  } catch (e) {
    // API nicht verfügbar
  }

  // Fallback: localStorage
  try {
    const stored = localStorage.getItem('vetoResult');
    if (stored) return JSON.parse(stored);
  } catch (e) {
    // Fehler beim localStorage
  }

  return null;
}

// Helper: Ermittle gespielte Maps basierend auf Format
function getPlayedMaps(data) {
  if (!data || !data.team1 || !data.team2) return [];

  if (data.format === "bo1") {
    const bannedMaps = (data.bans || []).map(b => b.map);
    const decider = (data.allMaps || []).find(m => !bannedMaps.includes(m));
    return decider ? [decider] : [];
  }

  if (data.format === "bo2") {
    return (data.picks || []).map(p => p.map);
  }

  const playedMaps = (data.picks || []).map(p => p.map);
  const bans = (data.bans || []).map(b => b.map);
  const decider = (data.allMaps || []).find(m => ![...playedMaps, ...bans].includes(m));
  if (decider) playedMaps.push(decider);
  return playedMaps;
}
