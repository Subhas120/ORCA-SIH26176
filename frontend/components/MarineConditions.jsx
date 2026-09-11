import React from 'react';

export default function MarineConditions() {
  const conditions = [
    {
      label: 'WIND VELOCITY',
      value: '22',
      unit: 'km/h',
      detail: 'SSW (210°) • Gusts 27 km/h',
      status: 'warning',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"></path>
        </svg>
      )
    },
    {
      label: 'WAVE & SWELL',
      value: '1.2',
      unit: 'm',
      detail: 'Significant height • Period 6.4s',
      status: 'warning',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M2 12c.6.5 1.2.5 2.5 0s2.5-.5 3.8 0 2.5.5 3.8 0 2.5-.5 3.8 0 2.5.5 3.8 0 2.5-.5 3.8 0M2 17c.6.5 1.2.5 2.5 0s2.5-.5 3.8 0 2.5.5 3.8 0 2.5-.5 3.8 0 2.5.5 3.8 0 2.5-.5 3.8 0M2 7c.6.5 1.2.5 2.5 0s2.5-.5 3.8 0 2.5.5 3.8 0 2.5-.5 3.8 0 2.5.5 3.8 0 2.5-.5 3.8 0"></path>
        </svg>
      )
    },
    {
      label: 'SURFACE VISIBILITY',
      value: '8.5',
      unit: 'km',
      detail: 'Clear horizon • Minimal haze',
      status: 'safe',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        </svg>
      )
    },
    {
      label: 'SEA STATE',
      value: 'MODERATE',
      unit: '',
      detail: 'Beaufort Scale 4 • Small whitecaps',
      status: 'warning',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 6v6l4 2"></path>
        </svg>
      )
    }
  ];

  return (
    <div className="panel-card conditions-card-container">
      <div className="panel-header">
        <div className="panel-title-group">
          <div className="panel-title-with-icon">
            <span className="icon-badge cyan">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
            </span>
            <h3>MARINE CONDITIONS</h3>
          </div>
          <p className="panel-subtitle">Current oceanographic & meteorological observations</p>
        </div>
        <div className="panel-tag demo-tag">DEMO TELEMETRY</div>
      </div>

      <div className="conditions-grid">
        {conditions.map((item, idx) => (
          <div key={idx} className={`condition-item-box ${item.status}`}>
            <div className="condition-top">
              <div className="condition-icon-badge">{item.icon}</div>
              <span className="condition-metric-label">{item.label}</span>
            </div>
            <div className="condition-val-row">
              <span className="condition-val">{item.value}</span>
              {item.unit && <span className="condition-unit">{item.unit}</span>}
            </div>
            <div className="condition-detail">{item.detail}</div>
          </div>
        ))}
      </div>

      <div className="conditions-footer-note">
        <span className="dot-radar"></span>
        <span>Sensor Buoy INCOIS-04 & Coastal Radar Station (Simulated Stream)</span>
      </div>
    </div>
  );
}
