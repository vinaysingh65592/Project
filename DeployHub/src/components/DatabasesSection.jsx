import { DATABASES } from '../data/platforms';

export default function DatabasesSection() {
  return (
    <section className="section section-alt" id="databases">
      <div className="container">
        <h2 className="sec-title">🗄️ Free Databases</h2>
        <p className="sec-sub">Every project needs a database — here are the best free options</p>
        <div className="db-grid">
          {DATABASES.map(db => (
            <a
              key={db.id}
              href={db.url}
              target="_blank"
              rel="noreferrer"
              className="db-card"
              style={{ '--accent': db.color }}
            >
              <div className="db-top">
                <span className="db-icon">{db.icon}</span>
                <span className="db-badge">{db.badge}</span>
              </div>
              <h3 className="db-name">{db.name}</h3>
              <span className="db-type">{db.type}</span>
              <p className="db-desc">{db.description}</p>
              <div className="db-free">
                <span>🆓</span> {db.free}
              </div>
              <div className="db-link">Visit {db.name} ↗</div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
