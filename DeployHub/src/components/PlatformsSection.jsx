import { useState } from 'react';
import { PLATFORMS, CATEGORIES } from '../data/platforms';
import PlatformCard from './PlatformCard';

export default function PlatformsSection({ search, activeFilter, setActiveFilter }) {
  const filtered = PLATFORMS.filter(p => {
    const matchCat = activeFilter === 'all' || p.category.includes(activeFilter);
    const q = search.toLowerCase();
    const matchSearch = !q ||
      p.name.toLowerCase().includes(q) ||
      p.tags.some(t => t.toLowerCase().includes(q)) ||
      p.description.toLowerCase().includes(q) ||
      p.category.some(c => c.toLowerCase().includes(q));
    return matchCat && matchSearch;
  });

  return (
    <section className="section" id="platforms">
      <div className="container">
        <h2 className="sec-title">🌐 Explore Platforms</h2>
        <p className="sec-sub">Filter by category to find your perfect hosting match</p>

        <div className="filters">
          {CATEGORIES.map(cat => (
            <button
              key={cat.id}
              className={`filter-btn ${activeFilter === cat.id ? 'active' : ''}`}
              onClick={() => setActiveFilter(cat.id)}
            >
              <span>{cat.icon}</span> {cat.label}
            </button>
          ))}
        </div>

        {filtered.length > 0 ? (
          <div className="grid">
            {filtered.map(p => <PlatformCard key={p.id} platform={p} />)}
          </div>
        ) : (
          <div className="no-results">
            <span>🔎</span>
            <h3>No platforms found</h3>
            <p>Try a different search term or category</p>
          </div>
        )}
      </div>
    </section>
  );
}
