import { useState } from 'react';

export default function PlatformCard({ platform: p }) {
  const [flipped, setFlipped] = useState(false);

  return (
    <div className={`card ${flipped ? 'flipped' : ''}`} style={{ '--accent': p.color }}>
      <div className="card-front">
        <div className="card-header">
          <span className="card-icon">{p.icon}</span>
          <div>
            <h3 className="card-name">{p.name}</h3>
            <div className="card-cats">
              {p.category.map(c => (
                <span key={c} className="tag">{c}</span>
              ))}
            </div>
          </div>
          {p.badge && <span className="badge">{p.badge}</span>}
        </div>
        <p className="card-desc">{p.description}</p>
        <div className="card-free">
          <span className="free-label">🆓 Free:</span> {p.free}
        </div>
        <div className="card-tags">
          {p.tags.slice(0, 5).map(t => (
            <span key={t} className="tag tag-sm">{t}</span>
          ))}
          {p.tags.length > 5 && <span className="tag tag-sm">+{p.tags.length - 5}</span>}
        </div>
        <div className="card-actions">
          <a href={p.url} target="_blank" rel="noreferrer" className="btn-visit">
            Visit Site ↗
          </a>
          <button className="btn-details" onClick={() => setFlipped(true)}>
            Pros & Cons →
          </button>
        </div>
      </div>
      <div className="card-back">
        <button className="btn-back" onClick={() => setFlipped(false)}>← Back</button>
        <h3>{p.name} — Details</h3>
        <div className="pros-cons">
          <div className="pros">
            <h4>✅ Pros</h4>
            <ul>{p.pros.map((pro, i) => <li key={i}>{pro}</li>)}</ul>
          </div>
          <div className="cons">
            <h4>❌ Cons</h4>
            <ul>{p.cons.map((con, i) => <li key={i}>{con}</li>)}</ul>
          </div>
        </div>
        <a href={p.url} target="_blank" rel="noreferrer" className="btn-visit">
          Visit {p.name} ↗
        </a>
      </div>
    </div>
  );
}
