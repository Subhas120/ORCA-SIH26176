import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon, Polyline, Tooltip, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Custom SVG-based radar pulse marker for user location
const userIcon = L.divIcon({
  className: 'custom-marine-user-marker',
  html: `
    <div class="user-pulse-container">
      <div class="user-center-dot"></div>
      <div class="user-pulse-ring"></div>
    </div>
  `,
  iconSize: [28, 28],
  iconAnchor: [14, 14],
  popupAnchor: [0, -14]
});

// Map recentering controller hook component
function RecenterController({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center && Array.isArray(center)) {
      map.setView(center, 11, { animate: true });
    }
  }, [center, map]);
  return null;
}

export default function MarineMap({
  locationName = 'Kochi, Kerala',
  mapCenter = [9.95, 76.21],
  userPosition = [9.9312, 76.2673],
  coordsText = "09°55'N | 76°12'E"
}) {
  const [lat, lng] = mapCenter;

  // Generate dynamic demo zones positioned around the chosen port
  const suitableZoneCoords = [
    [lat + 0.045, lng + 0.025],
    [lat + 0.045, lng + 0.075],
    [lat - 0.040, lng + 0.075],
    [lat - 0.040, lng + 0.030]
  ];

  const moderateRiskZoneCoords = [
    [lat + 0.075, lng - 0.050],
    [lat + 0.075, lng + 0.025],
    [lat - 0.070, lng + 0.030],
    [lat - 0.070, lng - 0.050]
  ];

  const highRiskZoneCoords = [
    [lat + 0.110, lng - 0.150],
    [lat + 0.110, lng - 0.050],
    [lat - 0.110, lng - 0.050],
    [lat - 0.110, lng - 0.150]
  ];

  const restrictedZoneCoords = [
    [lat + 0.015, lng - 0.005],
    [lat + 0.035, lng - 0.005],
    [lat + 0.035, lng + 0.018],
    [lat + 0.015, lng + 0.018]
  ];

  const routeCoords = [
    userPosition,
    [lat - 0.0020, lng + 0.0420],
    [lat + 0.0120, lng + 0.0280],
    [lat + 0.0100, lng - 0.0150],
    [lat + 0.0280, lng - 0.0350]
  ];

  return (
    <div className="panel-card marine-map-panel">
      <div className="map-card-header">
        <div className="map-title-group">
          <div className="panel-title-with-icon">
            <span className="icon-badge blue">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon>
                <line x1="9" y1="3" x2="9" y2="18"></line>
                <line x1="15" y1="6" x2="15" y2="21"></line>
              </svg>
            </span>
            <h3>INTERACTIVE MARINE MAP</h3>
          </div>
          <span className="map-demo-badge">DEMO MARINE ZONES</span>
        </div>
        <div className="map-meta-tags">
          <span className="coordinate-tag">COORDS: {coordsText}</span>
          <span className="layer-tag">Port: {locationName}</span>
        </div>
      </div>

      <div className="map-viewport-wrapper">
        <MapContainer
          center={mapCenter}
          zoom={11}
          scrollWheelZoom={false}
          className="leaflet-marine-canvas"
          attributionControl={true}
        >
          <RecenterController center={mapCenter} />

          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Suitable Zone (Green) */}
          <Polygon
            positions={suitableZoneCoords}
            pathOptions={{
              color: '#10b981',
              fillColor: '#10b981',
              fillOpacity: 0.22,
              weight: 2,
              dashArray: '4, 4'
            }}
          >
            <Tooltip sticky>Suitable Zone ({locationName})</Tooltip>
            <Popup>
              <div className="map-popup-content">
                <strong className="text-safe">SUITABLE ZONE</strong>
                <p>Inner coastal & harbor shelf off {locationName}. Swell &lt; 0.8m. Safe for standard small craft operations.</p>
                <span className="mock-note">[Demo Safety Classification]</span>
              </div>
            </Popup>
          </Polygon>

          {/* Moderate Risk Zone (Yellow/Amber) */}
          <Polygon
            positions={moderateRiskZoneCoords}
            pathOptions={{
              color: '#f59e0b',
              fillColor: '#f59e0b',
              fillOpacity: 0.25,
              weight: 2
            }}
          >
            <Tooltip sticky>Moderate Risk Zone</Tooltip>
            <Popup>
              <div className="map-popup-content">
                <strong className="text-warning">MODERATE RISK ZONE</strong>
                <p>Intermediate shelf. Wind gusts ~22 km/h, wave swell ~1.2m. Requires elevated navigation vigilance.</p>
                <span className="mock-note">[Demo Safety Classification]</span>
              </div>
            </Popup>
          </Polygon>

          {/* High Risk Zone (Red) */}
          <Polygon
            positions={highRiskZoneCoords}
            pathOptions={{
              color: '#ef4444',
              fillColor: '#ef4444',
              fillOpacity: 0.25,
              weight: 2
            }}
          >
            <Tooltip sticky>High Risk Zone</Tooltip>
            <Popup>
              <div className="map-popup-content">
                <strong className="text-danger">HIGH RISK ZONE</strong>
                <p>Deep water offshore channel. Unpredictable chop & strong currents. Small crafts strongly advised to avoid.</p>
                <span className="mock-note">[Demo Safety Classification]</span>
              </div>
            </Popup>
          </Polygon>

          {/* Restricted Zone (Slate/Navy) */}
          <Polygon
            positions={restrictedZoneCoords}
            pathOptions={{
              color: '#94a3b8',
              fillColor: '#475569',
              fillOpacity: 0.45,
              weight: 2,
              dashArray: '6, 6'
            }}
          >
            <Tooltip sticky>Restricted Zone (Naval / Port Corridor)</Tooltip>
            <Popup>
              <div className="map-popup-content">
                <strong className="text-muted">RESTRICTED ZONE</strong>
                <p>Commercial navigation channel & naval perimeter. Civilian navigation prohibited without clearance.</p>
                <span className="mock-note">[Demo Safety Classification]</span>
              </div>
            </Popup>
          </Polygon>

          {/* Recommended Route (Cyan Line) */}
          <Polyline
            positions={routeCoords}
            pathOptions={{
              color: '#06b6d4',
              weight: 4,
              opacity: 0.9,
              dashArray: '8, 6'
            }}
          >
            <Tooltip sticky>Recommended Route</Tooltip>
            <Popup>
              <div className="map-popup-content">
                <strong className="text-cyan">RECOMMENDED TRANSIT ROUTE</strong>
                <p>Optimized waypoint corridor out of {locationName} navigating through suitable zone fairway.</p>
                <span className="mock-note">[Demo Waypoint Calculation]</span>
              </div>
            </Popup>
          </Polyline>

          {/* User Location Marker */}
          <Marker position={userPosition} icon={userIcon}>
            <Tooltip permanent direction="top" offset={[0, -10]}>
              Current Position ({locationName})
            </Tooltip>
            <Popup>
              <div className="map-popup-content">
                <strong className="text-primary-accent">USER LOCATION</strong>
                <p>{locationName} Marine Base Station</p>
                <p className="coords-text">Lat: {userPosition[0].toFixed(4)}°, Lon: {userPosition[1].toFixed(4)}°</p>
              </div>
            </Popup>
          </Marker>
        </MapContainer>

        {/* Floating Overlay: Marine Conditions (Mock observation data kept separated from inputs) */}
        <div className="map-floating-overlay conditions-overlay">
          <div className="overlay-header">
            <span className="pulse-cyan-dot"></span>
            <h4>MARINE CONDITIONS</h4>
          </div>
          <div className="overlay-grid">
            <div className="overlay-metric">
              <span className="metric-label">Wind</span>
              <span className="metric-value">22 <small>km/h</small></span>
            </div>
            <div className="overlay-metric">
              <span className="metric-label">Wave</span>
              <span className="metric-value">1.2 <small>m</small></span>
            </div>
            <div className="overlay-metric">
              <span className="metric-label">Visibility</span>
              <span className="metric-value">8.5 <small>km</small></span>
            </div>
            <div className="overlay-metric">
              <span className="metric-label">Sea State</span>
              <span className="metric-value text-warning">Moderate</span>
            </div>
          </div>
          <div className="overlay-footer">Station Observation Feed [Demo]</div>
        </div>

        {/* Floating Overlay: Route Status */}
        <div className="map-floating-overlay route-overlay">
          <div className="overlay-header">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" strokeWidth="2.5">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <h4>ROUTE STATUS</h4>
          </div>
          <div className="route-status-content">
            <div className="route-status-badge">
              <span className="check-dot">✓</span>
              <span>Recommended route available</span>
            </div>
            <div className="route-risk-line">
              <span>Fairway Risk:</span>
              <strong className="text-warning">Moderate</strong>
            </div>
          </div>
        </div>

        {/* Interactive Map Legend */}
        <div className="map-legend-dock">
          <div className="legend-title">MAP LAYERS</div>
          <div className="legend-items">
            <div className="legend-item">
              <span className="legend-symbol user-sym">●</span>
              <span>User Location</span>
            </div>
            <div className="legend-item">
              <span className="legend-symbol suitable-sym">■</span>
              <span>Suitable Zone</span>
            </div>
            <div className="legend-item">
              <span className="legend-symbol moderate-sym">■</span>
              <span>Moderate Risk</span>
            </div>
            <div className="legend-item">
              <span className="legend-symbol high-sym">■</span>
              <span>High Risk</span>
            </div>
            <div className="legend-item">
              <span className="legend-symbol restricted-sym">■</span>
              <span>Restricted</span>
            </div>
            <div className="legend-item">
              <span className="legend-symbol route-sym">━</span>
              <span>Recommended Route</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
