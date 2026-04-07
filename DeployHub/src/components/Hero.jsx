import { useEffect, useRef } from 'react';
import { PLATFORMS } from '../data/platforms';

export default function Hero({ search, setSearch }) {
  const inputRef = useRef();

  useEffect(() => {
    const handler = (e) => {
      if (e.key === '/' && document.activeElement !== inputRef.current) {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  return (
    <header className="hero">
      <div className="bg-effects">
        <div className="bg-glow g1" />
        <div className="bg-glow g2" />
        <div className="bg-glow g3" />
      </div>
      <div className="container hero-content">
        <div className="hero-badge">✨ {PLATFORMS.length}+ Free Platforms • All Languages • Step-by-Step Guides</div>
        <h1>
          Deploy <span className="grad-1">Anything</span>,<br />
          <span className="grad-2">Anywhere</span>, Free.
        </h1>
        <p className="hero-sub">
          The ultimate directory of free hosting platforms with complete deployment guides for every language and framework.
        </p>
        <div className="search-box">
          <span className="si">🔍</span>
          <input
            ref={inputRef}
            id="searchInput"
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search platforms, languages, frameworks..."
            autoComplete="off"
          />
          {search && (
            <button className="search-clear" onClick={() => setSearch('')}>✕</button>
          )}
          <kbd>/</kbd>
        </div>
        <div className="hero-stats">
          <div className="stat"><strong>{PLATFORMS.length}+</strong><span>Platforms</span></div>
          <div className="stat-sep" />
          <div className="stat"><strong>10+</strong><span>Languages</span></div>
          <div className="stat-sep" />
          <div className="stat"><strong>100%</strong><span>Free Tiers</span></div>
          <div className="stat-sep" />
          <div className="stat"><strong>Step-by-Step</strong><span>Guides</span></div>
        </div>
        <a href="#platforms" className="hero-cta">
          Explore Platforms <span>↓</span>
        </a>
      </div>
    </header>
  );
}
