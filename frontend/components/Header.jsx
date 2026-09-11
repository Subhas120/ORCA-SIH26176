import React from 'react';

export default function Header({ location = 'Kochi, Kerala' }) {
  return (
    <header className="orca-header">
      <div className="header-left">
        <div className="brand-badge">
          <div className="brand-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
          </div>
          <div className="brand-text">
            <div className="brand-title">
              <span className="orca-name">ORCA</span>
              <span className="tech-badge">CORE v1.0</span>
            </div>
            <p className="brand-subtitle">Marine Ecosystem Intelligence & Decision Support</p>
          </div>
        </div>
      </div>

      <div className="header-center">
        <div className="situation-pill">
          <span className="radar-dot"></span>
          <span className="situation-title">LIVE MARINE SITUATION</span>
          <span className="situation-zone">{location.toUpperCase()}</span>
        </div>
      </div>

      <div className="header-right">
        <div className="telemetry-item">
          <span className="telemetry-label">LOCATION</span>
          <span className="telemetry-value">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
            {location}
          </span>
        </div>
        <div className="telemetry-divider"></div>
        <div className="telemetry-item">
          <span className="telemetry-label">SYSTEM STATUS</span>
          <span className="telemetry-value status-online">
            <span className="pulse-indicator"></span>
            CONNECTED
          </span>
        </div>
        <div className="telemetry-divider"></div>
        <div className="telemetry-item">
          <span className="telemetry-label">TELEMETRY SYNC</span>
          <span className="telemetry-value muted">Live [Demo Mode]</span>
        </div>
      </div>
    </header>
  );
}
