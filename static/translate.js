/**
 * Automatic Translation Helper für Universal MapVeto
 * Übersetzt häufig verwendete Begriffe automatisch basierend auf der Sprache
 */

// Einfache Mapping von deutschen zu englischen Begriffen
const translationMap = {
  'de': {
    'Team 1': 'Team 1',
    'Team 2': 'Team 2',
    'Team 1 Name:': 'Team 1 Name:',
    'Team 2 Name:': 'Team 2 Name:',
    'Team 1 Logo:': 'Team 1 Logo:',
    'Team 2 Logo:': 'Team 2 Logo:',
    'Team-Kurzname:': 'Team-Kurzname:',
    'Team 1 Kurzname:': 'Team 1 Kurzname:',
    'Team 2 Kurzname:': 'Team 2 Kurzname:',
    'Map-Pool': 'Map-Pool',
    'Vorhandene Maps': 'Vorhandene Maps',
    'Verfügbare Maps': 'Verfügbare Maps',
    'Gewählte Maps': 'Gewählte Maps',
    'Ausgewählte Maps': 'Ausgewählte Maps',
    'Veto-Format': 'Veto-Format',
    'Best of 1': 'Best of 1',
    'Best of 2': 'Best of 2',
    'Best of 3': 'Best of 3',
    'Best of 5': 'Best of 5',
    'BO1': 'BO1',
    'BO2': 'BO2',
    'BO3': 'BO3',
    'BO5': 'BO5',
    'Startendes Team': 'Startendes Team',
    'Textfarbe': 'Textfarbe',
    'Weiß': 'White',
    'Schwarz': 'Black',
    'veto starten': 'Veto starten',
    'Veto starten': 'Start Veto',
    'Zurücksetzen': 'Reset',
    'Maps gewonnen': 'Maps gewonnen',
    'Serienstand': 'Serienstand',
    'Runde': 'Runde',
    'Score': 'Score',
    'Scores': 'Scores',
    'Pick': 'Pick',
    'Ban': 'Ban',
    'Strip': 'Strip',
    'Decider': 'Decider'
  },
  'en': {
    'Team 1': 'Team 1',
    'Team 2': 'Team 2',
    'Team 1 Name:': 'Team 1 Name:',
    'Team 2 Name:': 'Team 2 Name:',
    'Team 1 Logo:': 'Team 1 Logo:',
    'Team 2 Logo:': 'Team 2 Logo:',
    'Team-Kurzname:': 'Team Shortname:',
    'Team 1 Kurzname:': 'Team 1 Shortname:',
    'Team 2 Kurzname:': 'Team 2 Shortname:',
    'Map-Pool': 'Map Pool',
    'Vorhandene Maps': 'Available Maps',
    'Verfügbare Maps': 'Available Maps',
    'Gewählte Maps': 'Selected Maps',
    'Ausgewählte Maps': 'Selected Maps',
    'Veto-Format': 'Veto Format',
    'Best of 1': 'Best of 1',
    'Best of 2': 'Best of 2',
    'Best of 3': 'Best of 3',
    'Best of 5': 'Best of 5',
    'BO1': 'BO1',
    'BO2': 'BO2',
    'BO3': 'BO3',
    'BO5': 'BO5',
    'Startendes Team': 'Starting Team',
    'Textfarbe': 'Text Color',
    'Weiß': 'White',
    'Schwarz': 'Black',
    'veto starten': 'Start Veto',
    'Veto starten': 'Start Veto',
    'Zurücksetzen': 'Reset',
    'Maps gewonnen': 'Maps Won',
    'Serienstand': 'Series Score',
    'Runde': 'Round',
    'Score': 'Score',
    'Scores': 'Scores',
    'Pick': 'Pick',
    'Ban': 'Ban',
    'Strip': 'Strip',
    'Decider': 'Decider'
  }
};

function applyTranslations(language) {
  if (!translationMap[language] || language === 'de') {
    return; // Keine Übersetzung nötig wenn Deutsch
  }

  const translations = translationMap[language];

  // Übersetze alle Text-Nodes im DOM
  function translateNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent.trim();
      if (text && translations[text]) {
        node.textContent = translations[text];
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      // Überspringe Script und Style Tags
      if (node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
        for (let child of node.childNodes) {
          translateNode(child);
        }
      }

      // Übersetze Placeholders und Title-Attribute
      if (node.placeholder && translations[node.placeholder]) {
        node.placeholder = translations[node.placeholder];
      }
      if (node.title && translations[node.title]) {
        node.title = translations[node.title];
      }
    }
  }

  translateNode(document.body);
}

// Initialisiere Übersetzungen
document.addEventListener('DOMContentLoaded', () => {
  const currentLang = document.documentElement.lang || 'de';
  applyTranslations(currentLang);
});
