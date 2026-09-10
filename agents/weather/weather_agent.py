from dataclasses import dataclass
from copy import deepcopy
from typing import Any, Dict, Optional

from agents.common.agent_contract import AgentResponse


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
    "wind_speed",
    "rain_probability",
    "visibility",
    "temperature",
    "wave_height",
    "wave_period",
    "warning",
)


class WeatherAgent:
    """
    ORCA M3 Weather Agent.

    Normalizes weather/marine observations into a stable contract.

    Real API adapters can provide observations to get().
    If a source becomes unavailable, the last cached observation
    can be returned with reduced confidence.

    This prototype uses mock/demo data until a real weather source
    is connected.
    """

    def __init__(self):
        self._cache: Optional[Dict[str, Any]] = None

    def get(
        self,
        observation: Optional[Dict[str, Any]],
        *,
        source_available: bool = True,
        timestamp: str = "2026-09-10T22:00:00",
        source: str = "DEMO-WEATHER",
    ) -> Dict[str, Any]:

        # Live/source data available
        if source_available and observation:

            data = self._normalize(
                observation,
                timestamp,
                source,
                confidence=0.95,
            )

            self._cache = deepcopy(data)

            return data

        # Fallback to cached observation
        if self._cache:

            cached = deepcopy(self._cache)

            cached["confidence"] = min(
                float(cached["confidence"]),
                0.60,
            )

            cached["source_status"] = "cached"

            return cached

        # No live data and no cache
        raise RuntimeError(
            "Reliable weather data is unavailable and "
            "no cached observation exists."
        )

    def _normalize(
        self,
        raw: Dict[str, Any],
        timestamp: str,
        source: str,
        confidence: float,
    ) -> Dict[str, Any]:

        missing = [
            field
            for field in REQUIRED
            if field not in raw
        ]

        if missing:
            raise ValueError(
                f"Missing weather fields: {missing}"
            )

        result = {
            "wind_speed": float(
                raw["wind_speed"]
            ),

            "wind_direction": (
                None
                if raw.get("wind_direction") is None
                else float(raw["wind_direction"])
            ),

            "rain_probability": float(
                raw["rain_probability"]
            ),

            "visibility": float(
                raw["visibility"]
            ),

            "temperature": float(
                raw["temperature"]
            ),

            "wave_height": float(
                raw["wave_height"]
            ),

            "wave_period": float(
                raw["wave_period"]
            ),

            "storm": bool(
                raw.get("storm", False)
            ),

            "cyclone": bool(
                raw.get("cyclone", False)
            ),

            "lightning": bool(
                raw.get("lightning", False)
            ),

            "warning": bool(
                raw["warning"]
            ),

            "warning_type": raw.get(
                "warning_type"
            ),

            "warning_severity": raw.get(
                "warning_severity"
            ),

            "timestamp": timestamp,

            "source": source,

            "confidence": confidence,

            "source_status": "live",
        }

        return result


def handle_weather(request) -> AgentResponse:
    """
    M1-compatible Weather Agent handler.

    M1 sends an AgentRequest.
    M3 returns an AgentResponse.

    The deterministic Risk Engine will consume the weather
    data later. This function itself does NOT make a safety
    decision.
    """

    try:

        agent = WeatherAgent()

        # -------------------------------------------------
        # MOCK / DEMO WEATHER DATA
        # -------------------------------------------------
        #
        # This is clearly labelled demo data.
        # It must NOT be presented as live weather.
        #
        observation = {

            "wind_speed": 22.0,

            "wind_direction": 250.0,

            "rain_probability": 30.0,

            "visibility": 8.0,

            "temperature": 28.0,

            "wave_height": 1.2,

            "wave_period": 7.0,

            "storm": False,

            "cyclone": False,

            "lightning": False,

            "warning": False,

            "warning_type": None,

            "warning_severity": None,
        }

        data = agent.get(
            observation,
            source_available=True,
            timestamp="2026-09-10T22:00:00",
            source="DEMO-WEATHER",
        )

        return AgentResponse(
            agent="weather",

            status="success",

            data=data,

            source=data["source"],

            timestamp=data["timestamp"],

            location=request.location,

            confidence=data["confidence"],
        )

    except Exception as exc:

        return AgentResponse(
            agent="weather",

            status="unavailable",

            data={},

            source="DEMO-WEATHER",

            timestamp=None,

            location=request.location,

            confidence=0.0,

            error=str(exc),
        )


if __name__ == "__main__":

    print("=== ORCA M3 WEATHER AGENT ===")

    class DemoRequest:
        location = "Kochi"

    response = handle_weather(
        DemoRequest()
    )

    print(response)