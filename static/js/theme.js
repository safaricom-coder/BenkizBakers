(function() {
  const THEME_KEY = 'flexr_theme';

  function applyTheme(theme) {
    if (theme === 'auto') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    } else {
      document.documentElement.setAttribute('data-theme', theme || 'light');
    }
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  }

  // expose globally
  window.BenkizTheme = { applyTheme, toggleTheme, THEME_KEY };

  // init asap
  const saved = localStorage.getItem(THEME_KEY) || 'light';
  applyTheme(saved);
})();