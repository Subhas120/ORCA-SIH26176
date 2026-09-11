import React from 'react';

export default function EvidencePanel() {
  const evidenceSources = [
    {
      name: 'Weather Observation',
      badge: 'METEOROLOGY',
      badgeClass: 'badge-blue',
      updated: '10 min ago',
      confidence: 92,
      details: 'Wind, pressure, & precipitation radar from regional marine meteorological feed.',
      status: 'verified'
    },
    {
      name: 'Ocean Observation',
      badge: 'HYDROLOGY',
      badgeClass: 'badge-cyan',
      updated: '15 min ago',
      confidence: 87,
      details: 'Wave height, tidal cycle & current drift sensors anchored off Kochi channel.',
      status: 'verified'
    },
    {
      name: 'Official Warning',
      badge: 'ADVISORY',
      badgeClass: 'badge-amber',
      updated: '5 min ago',
      confidence: 98,
      details: 'Indian Coast Guard & Disaster Authority bulletins. No active cyclone alert.',
      status: 'active-clear'
    }
  ];

  return (
    <div className="panel-card evidence-panel-container">
      <div className="panel-header">
        <div className="panel-title-group">
          <div className="panel-title-with-icon">
            <span className="icon-badge blue">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
              </svg>
            </span>
            <h3>EVIDENCE & SOURCES</h3>
          </div>
          <p className="panel-subtitle">Multi-agent inputs grounding risk decisions</p>
        </div>
        <div className="panel-tag demo-tag">DEMO SOURCES</div>
      </div>

      <div className="evidence-cards-list">
        {evidenceSources.map((item, idx) => (
          <div key={idx} className="evidence-source-card">
            <div className="evidence-card-top">
              <div className="source-identification">
                <span className={`source-type-pill ${item.badgeClass}`}>{item.badge}</span>
                <h4 className="source-title">{item.name}</h4>
              </div>
              <div className="source-confidence-meter">
                <div className="confidence-label-row">
                  <span className="conf-text">Confidence</span>
                  <strong className="conf-value">{item.confidence}%</strong>
                </div>
                <div className="confidence-track">
                  <div
                    className="confidence-fill"
                    style={{ width: `${item.confidence}%` }}
                  ></div>
                </div>
              </div>
            </div>

            <p className="source-description">{item.details}</p>

            <div className="evidence-card-bottom">
              <div className="update-timestamp">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <span>Updated: {item.updated}</span>
              </div>
              <span className="demo-source-tag">[Demo Data]</span>
            </div>
          </div>
        ))}
      </div>

      <div className="evidence-footer-summary">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
        </svg>
        <span>Deterministic Rule Engine ingests and cross-validates all 3 feeds before computing safety scores.</span>
      </div>
    </div>
  );
}
