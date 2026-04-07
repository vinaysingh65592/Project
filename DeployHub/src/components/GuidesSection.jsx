import { useState } from 'react';
import { GUIDES } from '../data/platforms';

const GUIDE_CATS = [
  { id: 'all', label: '🌐 All' },
  { id: 'static', label: '📄 Static/HTML' },
  { id: 'frontend', label: '⚛️ Frontend' },
  { id: 'python', label: '🐍 Python' },
  { id: 'docker', label: '🐳 Docker/Any' },
  { id: 'php', label: '🐘 PHP' },
];

export default function GuidesSection() {
  const [activeCat, setActiveCat] = useState('all');
  const [openGuide, setOpenGuide] = useState(null);

  const filtered = GUIDES.filter(g => activeCat === 'all' || g.category === activeCat);

  return (
    <section className="section" id="guides">
      <div className="container">
        <h2 className="sec-title">📖 Step-by-Step Deployment Guides</h2>
        <p className="sec-sub">Complete instructions for deploying on every major platform</p>

        <div className="filters guide-filters">
          {GUIDE_CATS.map(c => (
            <button
              key={c.id}
              className={`filter-btn ${activeCat === c.id ? 'active' : ''}`}
              onClick={() => setActiveCat(c.id)}
            >
              {c.label}
            </button>
          ))}
        </div>

        <div className="guides-list">
          {filtered.map(guide => (
            <div key={guide.id} className="guide-card">
              <button
                className="guide-header"
                onClick={() => setOpenGuide(openGuide === guide.id ? null : guide.id)}
              >
                <div className="guide-header-left">
                  <span className="guide-icon">{guide.icon}</span>
                  <div>
                    <h3>{guide.platform}</h3>
                    <span className="guide-lang">{guide.lang}</span>
                  </div>
                </div>
                <div className="guide-header-right">
                  <span className="guide-steps-count">{guide.steps.length} steps</span>
                  <span className="guide-chevron">{openGuide === guide.id ? '▲' : '▼'}</span>
                </div>
              </button>

              {openGuide === guide.id && (
                <div className="guide-body">
                  {/* Requirements */}
                  <div className="guide-requirements">
                    <h4>📋 Requirements</h4>
                    <div className="req-tags">
                      {guide.requirements.map((r, i) => (
                        <span key={i} className="req-tag">{r}</span>
                      ))}
                    </div>
                  </div>

                  {/* Steps */}
                  <div className="guide-steps">
                    {guide.steps.map((step, i) => (
                      <div key={i} className="step">
                        <div className="step-num">{i + 1}</div>
                        <div className="step-content">
                          <h4>{step.title}</h4>
                          <pre className="step-desc">{step.desc}</pre>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="guide-footer">
                    <span>🎉 You're live! Good luck with your deployment.</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
