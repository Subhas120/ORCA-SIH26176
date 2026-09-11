import React, { useState } from 'react';
import Header from '../components/Header';
import TripSituation, { SUPPORTED_LOCATIONS, getTomorrowDate } from '../components/TripSituation';
import ChatPanel from '../components/ChatPanel';
import RiskCard from '../components/RiskCard';
import MarineMap from '../maps/MarineMap';
import MarineConditions from '../components/MarineConditions';
import EvidencePanel from '../components/EvidencePanel';

export default function Dashboard() {
  const defaultLocation = SUPPORTED_LOCATIONS[0];

  const [situation, setSituation] = useState({
    location: defaultLocation.name,
    center: defaultLocation.center,
    userPosition: defaultLocation.userPosition,
    coordsText: defaultLocation.coordsText,
    date: getTomorrowDate(),
    time: '06:00',
    activity: 'Fishing',
    vesselType: 'Small Fishing Boat',
    duration: '4 hours',
    crewSize: 4,
    preferredZone: 'Suitable Zone'
  });

  const handleApplySituation = (updatedSituation) => {
    setSituation(updatedSituation);
  };

  return (
    <div className="orca-dashboard-root">
      <div className="dashboard-content-wrapper">
        {/* Navigation & Header */}
        <Header location={situation.location} />

        {/* Trip & Situation Scenario Inputs (Top of Dashboard) */}
        <TripSituation
          currentSituation={situation}
          onApplySituation={handleApplySituation}
        />

        <main className="dashboard-main-grid">
          {/* Row 1: Chat / AI Panel & Safety Risk Command Card */}
          <section className="dashboard-row top-command-row">
            <ChatPanel situation={situation} />
            <RiskCard situation={situation} />
          </section>

          {/* Row 2: Centerpiece Interactive Marine Map */}
          <section className="dashboard-row map-centerpiece-row">
            <MarineMap
              locationName={situation.location}
              mapCenter={situation.center}
              userPosition={situation.userPosition}
              coordsText={situation.coordsText}
            />
          </section>

          {/* Row 3: Marine Conditions & Evidence Sources */}
          <section className="dashboard-row bottom-intelligence-row">
            <MarineConditions />
            <EvidencePanel />
          </section>
        </main>

        <footer className="orca-dashboard-footer">
          <div className="footer-left">
            <span>ORCA SIH-26176 • Marine Safety Intelligence & Decision Support</span>
          </div>
          <div className="footer-right">
            <span className="footer-tag">M6 UI v2.1</span>
            <span className="footer-mode">Interactive Scenario Mode</span>
          </div>
        </footer>
      </div>
    </div>
  );
}
