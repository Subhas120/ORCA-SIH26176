"""M3 safety integration with the existing M4 GIS layer.

M3 remains the authoritative deterministic safety decision-maker.

M4 provides:
- coordinate/geofence utilities
- restricted-zone information
- route optimization

M3 provides:
- weather/wave risk
- alert risk
- final deterministic safety decision

This module does not modify or duplicate M4 implementation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, Iterable

from shapely.geometry import Polygon

from agents.risk.risk_engine import RiskEngine, component_risks_from_weather
from geospatial.geo_utils.geo_utils import Coordinate, validate_coordinate
from geospatial.routes.safest_route import safest_route
from geospatial.zones.geofencing import (
    find_containing_zones,
    is_location_restricted,
    load_geojson,
)
from shapely.geometry import shape


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_ZONES_PATH = (
    BASE_DIR / "geospatial" / "zones" / "prototype_zones.geojson"
)


RiskFunction = Callable[[Coordinate], float]


def load_zone_features(
    path: str | Path = DEFAULT_ZONES_PATH,
) -> list[dict[str, Any]]:
    """Load M4 GeoJSON zone features."""
    data = load_geojson(path)
    return list(data.get("features", []))


def load_restricted_polygons(
    path: str | Path = DEFAULT_ZONES_PATH,
) -> list[Polygon]:
    """Load zone geometries for M4's route blocked-cell logic."""
    features = load_zone_features(path)
    return [shape(feature["geometry"]) for feature in features]


def assess_location_safety(
    weather: Dict[str, Any],
    alert: Dict[str, Any] | None,
    coordinate: Coordinate,
    *,
    zone_features: Iterable[dict[str, Any]] | None = None,
    engine: RiskEngine | None = None,
) -> Dict[str, Any]:
    """Calculate deterministic M3 safety using M4 geographic information.

    The M4 geofencing implementation determines whether the coordinate
    lies inside a zone. M3 passes that result to the deterministic
    RiskEngine. No LLM or explanation layer is involved in the decision.
    """
    coordinate = validate_coordinate(coordinate)

    features = list(
        zone_features
        if zone_features is not None
        else load_zone_features()
    )

    restricted = is_location_restricted(
        coordinate,
        features,
    )

    containing_zones = find_containing_zones(
        coordinate,
        features,
    )

    risk_engine = engine or RiskEngine()

    risk = risk_engine.calculate(
        weather,
        alert,
        location_risk=100.0 if restricted else 0.0,
        restricted=restricted,
    )

    risk["location"] = {
        "latitude": coordinate[0],
        "longitude": coordinate[1],
        "restricted": restricted,
        "containing_zones": containing_zones,
        "source": "M4 GIS geofencing",
    }

    return risk


def build_route_risk_functions(
    weather: Dict[str, Any],
    alert: Dict[str, Any] | None = None,
) -> Dict[str, RiskFunction]:
    """Build deterministic risk functions for M4's A* route optimizer.

    The returned functions provide M3 weather/wave/hazard risk values to
    M4's existing safest_route() implementation.

    Prototype weather data is treated as uniform across the route because
    the current M3 weather adapter provides one location-level observation.
    """
    components = component_risks_from_weather(weather)

    weather_risk = float(
        components["wind"] * 0.67
        + components["weather"] * 0.33
    )

    wave_risk = float(components["wave"])

    warning_risk = float(components["warning"])

    def weather_function(_: Coordinate) -> float:
        return weather_risk

    def wave_function(_: Coordinate) -> float:
        return wave_risk

    def hazard_function(_: Coordinate) -> float:
        return warning_risk

    return {
        "weather_risk": weather_function,
        "wave_risk": wave_function,
        "hazard_penalty": hazard_function,
    }


def calculate_safest_route(
    start: Coordinate,
    goal: Coordinate,
    weather: Dict[str, Any],
    alert: Dict[str, Any] | None = None,
    *,
    zone_features: Iterable[dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    """Run M4 A* using deterministic M3 risk inputs.

    Restricted-zone geometry remains controlled by M4 and is passed
    directly to safest_route(), where restricted cells are blocked.
    """
    start = validate_coordinate(start)
    goal = validate_coordinate(goal)

    features = list(
        zone_features
        if zone_features is not None
        else load_zone_features()
    )

    restricted_polygons = [
        shape(feature["geometry"])
        for feature in features
    ]

    risk_functions = build_route_risk_functions(
        weather,
        alert,
    )

    return safest_route(
        start,
        goal,
        restricted_zones=restricted_polygons,
        weather_risk=risk_functions["weather_risk"],
        wave_risk=risk_functions["wave_risk"],
        hazard_penalty=risk_functions["hazard_penalty"],
    )