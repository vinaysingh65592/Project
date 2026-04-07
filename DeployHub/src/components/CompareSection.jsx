import { TOP_PICKS } from '../data/platforms';

export default function CompareSection() {
  return (
    <section className="section section-alt" id="compare">
      <div className="container">
        <h2 className="sec-title">🏆 Top Picks by Use Case</h2>
        <p className="sec-sub">Curated recommendations for the most common scenarios</p>
        <div className="compare-grid">
          {TOP_PICKS.map((pick, i) => (
            <div key={i} className="compare-card" style={{ '--accent': pick.color }}>
              <div className="compare-rank">{pick.rank}</div>
              <h3>{pick.title}</h3>
              <div className="compare-platform">{pick.platform}</div>
              <p>{pick.desc}</p>
              <a href={pick.url} target="_blank" rel="noreferrer" className="compare-link">
                Visit {pick.platform} →
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
