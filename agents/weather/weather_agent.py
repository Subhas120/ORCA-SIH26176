from dataclasses import dataclass, asdict
from copy import deepcopy
from typing import Any, Dict, Optional


@dataclass
class WeatherData:
    wind_speed: float
    wind_direction: Optional[float]
    rain_probability: float
    visibility: float
    temperature: float
    wave_height: float
    wave_period: float
    storm: bool
    cyclone: bool
    lightning: bool
    warning: bool
    warning_type: Optional[str]
    warning_severity: Optional[str]
    timestamp: str
    source: str
    confidence: float


REQUIRED = (
    "wind_speed", "rain_probability", "visibility", "temperature",
    "wave_height", "wave_period", "warning"
)


class WeatherAgent:
    """Normalizes weather/marine inputs into one stable M3 contract.

    Real API adapters should call get() with their response converted to the fields below.
    The agent can fall back to the last cached observation when a source is unavailable.
    """

    def __init__(self):
        self._cache: Optional[Dict[str, Any]] = None

    def get(self, observation: Optional[Dict[str, Any]], *,
            source_available: bool = True,
            timestamp: str = "2026-09-02T10:00:00",
            source: str = "DEMO") -> Dict[str, Any]:
        if source_available and observation:
            data = self._normalize(observation, timestamp, source, confidence=0.95)
            self._cache = deepcopy(data)
            return data

        if self._cache:
            cached = deepcopy(self._cache)
            cached["confidence"] = min(float(cached["confidence"]), 0.60)
            cached["source_status"] = "cached"
            return cached

        raise RuntimeError(
            "Reliable weather data is unavailable and no cached observation exists."
        )

    def _normalize(self, raw: Dict[str, Any], timestamp: str,
                   source: str, confidence: float) -> Dict[str, Any]:
        missing = [k for k in REQUIRED if k not in raw]
        if missing:
            raise ValueError(f"Missing weather fields: {missing}")

        result = {
            "wind_speed": float(raw["wind_speed"]),
            "wind_direction": raw.get("wind_direction"),
            "rain_probability": float(raw["rain_probability"]),
            "visibility": float(raw["visibility"]),
            "temperature": float(raw["temperature"]),
            "wave_height": float(raw["wave_height"]),
            "wave_period": float(raw["wave_period"]),
            "storm": bool(raw.get("storm", False)),
            "cyclone": bool(raw.get("cyclone", False)),
            "lightning": bool(raw.get("lightning", False)),
            "warning": bool(raw["warning"]),
            "warning_type": raw.get("warning_type"),
            "warning_severity": raw.get("warning_severity"),
            "timestamp": timestamp,
            "source": source,
            "confidence": confidence,
            "source_status": "live",
        }
        return result
