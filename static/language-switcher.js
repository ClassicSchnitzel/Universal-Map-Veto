/**
 * Language Switcher Utility for Universal MapVeto
 * Adds language switching functionality to all pages
 */

function initLanguageSwitcher() {
  // Get current language from HTML lang attribute
  const currentLang = document.documentElement.lang || 'de';
  
  // Check if switcher already exists
  if (document.querySelector('.lang-switcher-fixed')) {
    return;
  }
  
  // Create language switcher HTML
  const switcherHTML = `
    <div class="lang-switcher-fixed">
      <button class="lang-btn ${currentLang === 'de' ? 'active' : ''}" onclick="setLanguage('de')" title="Deutsch">DE</button>
      <button class="lang-btn ${currentLang === 'en' ? 'active' : ''}" onclick="setLanguage('en')" title="English">EN</button>
    </div>
  `;
  
  // Inject switcher into body
  if (document.body) {
    document.body.insertAdjacentHTML('beforeend', switcherHTML);
  }
  
  // Add styles dynamically
  if (!document.getElementById('lang-switcher-styles')) {
    const style = document.createElement('style');
    style.id = 'lang-switcher-styles';
    style.innerHTML = `
      .lang-switcher-fixed {
        position: fixed !important;
        top: 16px !important;
        right: 16px !important;
        z-index: 999999 !important;
        display: flex !important;
        gap: 8px;
        background: rgba(34, 34, 34, 0.98) !important;
        padding: 8px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.8);
      }
      .lang-btn {
        padding: 8px 16px;
        background: #333;
        color: #fff;
        border: 2px solid #444;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.95em;
        font-weight: bold;
        transition: all 0.2s;
        font-family: 'BebasNeue', Arial, sans-serif;
        letter-spacing: 0.5px;
      }
      .lang-btn:hover {
        background: #444;
        border-color: #00be29;
        transform: translateY(-2px);
      }
      .lang-btn.active {
        background: #00be29 !important;
        color: #000 !important;
        border-color: #00be29 !important;
      }
    `;
    document.head.appendChild(style);
  }
}

function setLanguage(lang) {
  if (lang !== 'de' && lang !== 'en') {
    console.error('Invalid language:', lang);
    return;
  }
  
  fetch(`/set_language/${lang}`)
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        window.location.reload();
      } else {
        console.error('Error setting language:', data.message);
      }
    })
    .catch(err => {
      console.error('Error setting language:', err);
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(initLanguageSwitcher, 100);
  });
} else {
  setTimeout(initLanguageSwitcher, 100);
}
