import React, { useState } from 'react';

export const SUPPORTED_LOCATIONS = [
  {
    name: 'Kochi, Kerala',
    center: [9.95, 76.21],
    userPosition: [9.9312, 76.2673],
    coordsText: "09°55'N | 76°12'E"
  },
  {
    name: 'Mumbai, Maharashtra',
    center: [18.94, 72.80],
    userPosition: [18.9220, 72.8347],
    coordsText: "18°55'N | 72°50'E"
  },
  {
    name: 'Chennai, Tamil Nadu',
    center: [13.08, 80.29],
    userPosition: [13.0827, 80.2707],
    coordsText: "13°05'N | 80°17'E"
  },
  {
    name: 'Visakhapatnam, Andhra Pradesh',
    center: [17.70, 83.25],
    userPosition: [17.6868, 83.2185],
    coordsText: "17°41'N | 83°17'E"
  },
  {
    name: 'Goa (Mormugao)',
    center: [15.42, 73.78],
    userPosition: [15.4120, 73.8010],
    coordsText: "15°24'N | 73°48'E"
  }
];

export const getTomorrowDate = () => {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  return d.toISOString().split('T')[0];
};

export default function TripSituation({ currentSituation, onApplySituation }) {
  const [formData, setFormData] = useState({
    location: currentSituation.location,
    date: currentSituation.date || getTomorrowDate(),
    time: currentSituation.time || '06:00',
    activity: currentSituation.activity || 'Fishing',
    vesselType: currentSituation.vesselType || 'Small Fishing Boat',
    duration: currentSituation.duration || '4 hours',
    crewSize: currentSituation.crewSize || 4,
    preferredZone: currentSituation.preferredZone || 'Suitable Zone'
  });

  const [notification, setNotification] = useState('');

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const locObj = SUPPORTED_LOCATIONS.find(l => l.name === formData.location) || SUPPORTED_LOCATIONS[0];
    
    const updatedSituation = {
      ...formData,
      center: locObj.center,
      userPosition: locObj.userPosition,
      coordsText: locObj.coordsText
    };

    onApplySituation(updatedSituation);
    setNotification('Scenario updated • Evaluation context dispatched');

    setTimeout(() => {
      setNotification('');
    }, 4000);
  };

  return (
    <div className="panel-card trip-situation-panel">
      <div className="panel-header">
        <div className="panel-title-group">
          <div className="panel-title-with-icon">
            <span className="icon-badge cyan">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                <circle cx="12" cy="12" r="10"></circle>
              </svg>
            </span>
            <h3>TRIP & SITUATION</h3>
          </div>
          <p className="panel-subtitle">Configure the scenario ORCA should evaluate</p>
        </div>
        <div className="panel-tag demo-tag">DEMO INPUTS</div>
      </div>

      <form onSubmit={handleSubmit} className="situation-form-grid">
        {/* Row 1: Location, Date, Departure Time */}
        <div className="form-group">
          <label htmlFor="situation-location">Location</label>
          <select
            id="situation-location"
            className="marine-select"
            value={formData.location}
            onChange={e => handleChange('location', e.target.value)}
          >
            {SUPPORTED_LOCATIONS.map(loc => (
              <option key={loc.name} value={loc.name}>
                {loc.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="situation-date">Date</label>
          <input
            type="date"
            id="situation-date"
            className="marine-form-input"
            value={formData.date}
            onChange={e => handleChange('date', e.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="situation-time">Departure Time</label>
          <input
            type="time"
            id="situation-time"
            className="marine-form-input"
            value={formData.time}
            onChange={e => handleChange('time', e.target.value)}
          />
        </div>

        {/* Row 2: Activity, Vessel Type, Duration */}
        <div className="form-group">
          <label htmlFor="situation-activity">Activity</label>
          <select
            id="situation-activity"
            className="marine-select"
            value={formData.activity}
            onChange={e => handleChange('activity', e.target.value)}
          >
            <option value="Fishing">Fishing</option>
            <option value="Passenger Transit">Passenger Transit</option>
            <option value="Research">Research</option>
            <option value="Diving">Diving</option>
            <option value="Recreation">Recreation</option>
            <option value="Cargo / Transport">Cargo / Transport</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="situation-vessel">Vessel Type</label>
          <select
            id="situation-vessel"
            className="marine-select"
            value={formData.vesselType}
            onChange={e => handleChange('vesselType', e.target.value)}
          >
            <option value="Small Fishing Boat">Small Fishing Boat</option>
            <option value="Fishing Trawler">Fishing Trawler</option>
            <option value="Passenger Boat">Passenger Boat</option>
            <option value="Research Vessel">Research Vessel</option>
            <option value="Cargo Vessel">Cargo Vessel</option>
            <option value="Recreational Boat">Recreational Boat</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="situation-duration">Trip Duration</label>
          <select
            id="situation-duration"
            className="marine-select"
            value={formData.duration}
            onChange={e => handleChange('duration', e.target.value)}
          >
            <option value="1 hour">1 hour</option>
            <option value="2 hours">2 hours</option>
            <option value="4 hours">4 hours</option>
            <option value="8 hours">8 hours</option>
            <option value="12 hours">12 hours</option>
          </select>
        </div>

        {/* Row 3: Crew Size, Preferred Zone, Action Button */}
        <div className="form-group">
          <label htmlFor="situation-crew">Crew Size</label>
          <input
            type="number"
            id="situation-crew"
            className="marine-form-input"
            min="1"
            max="100"
            value={formData.crewSize}
            onChange={e => handleChange('crewSize', parseInt(e.target.value, 10) || 1)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="situation-zone">Preferred Zone</label>
          <select
            id="situation-zone"
            className="marine-select"
            value={formData.preferredZone}
            onChange={e => handleChange('preferredZone', e.target.value)}
          >
            <option value="Suitable Zone">Suitable Zone</option>
            <option value="Moderate Risk Zone">Moderate Risk Zone</option>
            <option value="Any Available Zone">Any Available Zone</option>
          </select>
        </div>

        <div className="form-group form-action-group">
          <label className="action-label-placeholder">&nbsp;</label>
          <button type="submit" className="apply-scenario-btn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <span>APPLY SCENARIO</span>
          </button>
        </div>
      </form>

      {/* Scenario Summary Banner */}
      <div className="scenario-summary-bar">
        <div className="summary-details">
          <span className="summary-badge">ACTIVE SCENARIO</span>
          <span className="summary-item">
            <strong>{currentSituation.activity}</strong> • {currentSituation.vesselType}
          </span>
          <span className="summary-divider">|</span>
          <span className="summary-item location-name">{currentSituation.location}</span>
          <span className="summary-divider">|</span>
          <span className="summary-item">{currentSituation.time} ({currentSituation.date}) • {currentSituation.duration}</span>
          <span className="summary-divider">|</span>
          <span className="summary-item">Crew: {currentSituation.crewSize}</span>
          <span className="summary-divider">|</span>
          <span className="summary-item zone-target">{currentSituation.preferredZone}</span>
        </div>
        <div className="summary-mode-tag">DEMO MODE</div>
      </div>

      {notification && (
        <div className="scenario-notification">
          <span className="check-icon">✓</span>
          <span>{notification}</span>
        </div>
      )}
    </div>
  );
}
