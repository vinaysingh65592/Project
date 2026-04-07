import { useState, useEffect } from 'react';

export default function Navbar({ theme, setTheme }) {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const links = [
    { label: 'Platforms', href: '#platforms' },
    { label: 'Compare', href: '#compare' },
    { label: 'Guides', href: '#guides' },
    { label: 'Databases', href: '#databases' },
  ];

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="nav-inner">
        <a href="#" className="logo">
          <span className="logo-emoji">🚀</span>
          Deploy<span className="accent">Hub</span>
        </a>
        <div className={`nav-links ${mobileOpen ? 'open' : ''}`}>
          {links.map(l => (
            <a key={l.label} href={l.href} onClick={() => setMobileOpen(false)}>{l.label}</a>
          ))}
        </div>
        <div className="nav-actions">
          <button
            className="theme-toggle"
            onClick={() => setTheme(t => t === 'dark' ? 'light' : 'dark')}
            title="Toggle theme"
          >
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
          <button
            className={`mobile-menu ${mobileOpen ? 'active' : ''}`}
            onClick={() => setMobileOpen(o => !o)}
            aria-label="Toggle menu"
          >
            <span /><span /><span />
          </button>
        </div>
      </div>
    </nav>
  );
}
