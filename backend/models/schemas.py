from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# ==========================================
# Common Models
# ==========================================

class Location(BaseModel):
    """Basic location representation."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")


# ==========================================
# 1. /api/chat Contracts
# ==========================================

class ChatRequest(BaseModel):
    """Request schema for the main natural language chat endpoint."""
    message: str = Field(..., description="The natural language question from the user")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Optional user latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Optional user longitude")

class ChatResponse(BaseModel):
    """Response schema for the main natural language chat endpoint."""
    response: str = Field(..., description="The natural language answer to the user")
    intent: Optional[str] = Field(None, description="The detected intent of the user's query")
    risk: Optional[str] = Field(None, description="The evaluated risk level, if applicable")
    sources: Optional[List[str]] = Field(None, description="List of data sources used to formulate the answer")


# ==========================================
# 2. /api/weather Contracts
# ==========================================
# GET requests use query parameters (latitude, longitude), so we only define the response schema.

class WeatherObservation(BaseModel):
    """Structured weather observation."""
    parameter: str = Field(..., description="Name of the weather parameter (e.g., wind_speed, rain_probability)")
    value: float = Field(..., description="Value of the parameter")
    unit: str = Field(..., description="Unit of measurement")
    timestamp: datetime = Field(..., description="Time of observation")
    source: str = Field(..., description="Data source (e.g., IMD)")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score of the observation")

class WeatherResponse(BaseModel):
    """Response containing weather data for a location."""
    location: Location
    observations: List[WeatherObservation] = Field(default_factory=list)


# ==========================================
# 3. /api/ocean Contracts
# ==========================================
# GET requests use query parameters, so we only define the response schema.

class MarineObservation(BaseModel):
    """Normalized marine observation, conforming to M2's required standard format."""
    parameter: str = Field(..., description="Name of the marine parameter (e.g., wave_height, SST)")
    value: float = Field(..., description="Value of the parameter")
    unit: str = Field(..., description="Unit of measurement")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timestamp: datetime = Field(..., description="Time of observation")
    source: str = Field(..., description="Data source (e.g., INCOIS)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the observation (required for M2)")

class OceanResponse(BaseModel):
    """Response containing normalized marine data."""
    observations: List[MarineObservation] = Field(default_factory=list)


# ==========================================
# 4. /api/risk Contracts
# ==========================================

class RiskRequest(BaseModel):
    """Request to evaluate risk for a given location and context."""
    location: Location
    activity: Optional[str] = Field(None, description="Activity being evaluated (e.g., fishing, sailing)")
    time: Optional[datetime] = Field(None, description="Time of the intended activity")

class RiskResponse(BaseModel):
    """Response containing the deterministic risk evaluation from M3's engine."""
    risk_score: int = Field(..., ge=0, le=100, description="Calculated risk score (0-100)")
    risk_level: str = Field(..., description="Risk category (LOW, MODERATE, HIGH, EXTREME)")
    reasons: List[str] = Field(default_factory=list, description="Explanations for the risk score/classification")


# ==========================================
# 5. /api/location Contracts
# ==========================================
# GET requests use query parameters, so we only define the response schema.

class LocationResponse(BaseModel):
    """Response containing structured location information."""
    latitude: float
    longitude: float
    name: Optional[str] = Field(None, description="Human readable name of the location")
    type: Optional[str] = Field(None, description="Type of location (e.g., PFZ, restricted_zone, port)")


# ==========================================
# 6. /api/routes Contracts
# ==========================================

class RouteRequest(BaseModel):
    """Request for a safe route from M4's GIS/Route engine."""
    origin: Location
    destination: Location
    constraints: Optional[Dict[str, Any]] = Field(None, description="Additional constraints for routing (e.g., avoid_high_waves)")

class RoutePoint(BaseModel):
    """A single point along a computed route."""
    latitude: float
    longitude: float
    risk_score: Optional[int] = Field(None, ge=0, le=100, description="Risk score at this specific point")

class RouteResponse(BaseModel):
    """Response containing the safest practical route."""
    path: List[RoutePoint] = Field(default_factory=list, description="List of points forming the safest route")
    total_distance: Optional[float] = Field(None, description="Total distance of the route in kilometers")
    estimated_duration: Optional[float] = Field(None, description="Estimated duration to travel the route in hours")


# ==========================================
# 7. /api/alerts Contracts
# ==========================================
# GET requests use query parameters, so we only define the response schema.

class MarineAlert(BaseModel):
    """Structured marine alert."""
    alert_type: str = Field(..., description="Type of alert (e.g., Cyclone, High Wave, Geofence Violation)")
    severity: str = Field(..., description="Severity level of the alert")
    description: str = Field(..., description="Detailed description of the alert condition")
    source: str = Field(..., description="Authoritative source of the alert (e.g., INCOIS, IMD)")
    issued_at: datetime = Field(..., description="When the alert was issued")
    valid_until: Optional[datetime] = Field(None, description="When the alert expires")

class AlertsResponse(BaseModel):
    """Response containing active marine alerts."""
    alerts: List[MarineAlert] = Field(default_factory=list)
