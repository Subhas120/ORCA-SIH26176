import React from 'react';

export default function RiskCard() {
  const riskData = {
    level: 'MODERATE',
    score: 34,
    maxScore: 100,
    statusClass: 'moderate',
    decisionSource: 'Deterministic Safety Engine (Rule V2.4)',
    reasons: [
      { text: 'Wind speed elevated (22 km/h, gusting to 27 km/h)', severity: 'warning' },
      { text: 'Wave height moderate (1.2 m significant wave height)', severity: 'warning' },
      { text: 'No severe official warning active (Coast Guard & IMD clear)', severity: 'safe' }
    ]
  };

  return (
    <div className="panel-card risk-panel-container">
      <div className="panel-header">
        <div className="panel-title-group">
          <div className="panel-title-with-icon">
            <span className="icon-badge warning">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
            </span>
            <h3>SAFETY RISK</h3>
          </div>
          <p className="panel-subtitle">Deterministic evaluation & operational threshold</p>
        </div>
        <div className="panel-tag risk-engine-tag">DETERMINISTIC RULE</div>
      </div>

      <div className="risk-display-hero">
        <div className="risk-score-box">
          <div className="score-number-group">
            <span className="score-val">{riskData.score}</span>
            <span className="score-denom">/{riskData.maxScore}</span>
          </div>
          <span className="score-subtext">AGGREGATE INDEX</span>
        </div>

        <div className="risk-status-badge-box">
          <div className={`risk-banner-pill ${riskData.statusClass}`}>
            <span className="status-ping"></span>
            <span className="risk-banner-text">{riskData.level}</span>
          </div>
          <span className="risk-action-hint">Exercise caution in coastal transit</span>
        </div>
      </div>

      {/* Horizontal Meter / Gauge */}
      <div className="risk-meter-wrapper">
        <div className="meter-scale-labels">
          <span className="scale-lbl low">LOW (0-25)</span>
          <span className="scale-lbl moderate active">MODERATE (26-50)</span>
          <span className="scale-lbl high">HIGH (51-75)</span>
          <span className="scale-lbl extreme">EXTREME (76-100)</span>
        </div>
        <div className="risk-meter-track">
          <div className="meter-zone zone-low" title="Low: 0-25"></div>
          <div className="meter-zone zone-moderate" title="Moderate: 26-50"></div>
          <div className="meter-zone zone-high" title="High: 51-75"></div>
          <div className="meter-zone zone-extreme" title="Extreme: 76-100"></div>
          <div
            className="meter-needle-pointer"
            style={{ left: `${riskData.score}%` }}
          >
            <div className="needle-head"></div>
            <div className="needle-line"></div>
          </div>
        </div>
      </div>

      {/* Why this risk */}
      <div className="risk-reasons-container">
        <div className="reasons-heading">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="9 11 12 14 22 4"></polyline>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
          </svg>
          <span>WHY THIS RISK?</span>
        </div>
        <ul className="reasons-list">
          {riskData.reasons.map((item, idx) => (
            <li key={idx} className={`reason-item ${item.severity}`}>
              <span className="bullet-dot"></span>
              <span className="reason-text">{item.text}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Decision source badge */}
      <div className="risk-footer-meta">
        <div className="decision-source-box">
          <span className="source-label">Decision source:</span>
          <span className="source-badge">Safety Engine</span>
        </div>
        <span className="rule-spec">Failsafe: Rule-based priority over AI text</span>
      </div>
    </div>
  );
}
