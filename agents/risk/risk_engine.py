from typing import Any, Dict, List, Optional


class RiskEngine:
    """Deterministic, explainable M3 risk engine.

    Prototype weights from the project plan:
      wave 25%, official warning 25%, wind 20%,
      rain/visibility 10%, sea state/current 10%, location/zones 10%.

    Inputs are expected as normalized 0..100 component risks.
    """

    WEIGHTS = {
        "wave": 0.25,
        "warning": 0.25,
        "wind": 0.20,
        "weather": 0.10,
        "sea_state": 0.10,
        "location": 0.10,
    }

    def __init__(self,
                 dangerous_wave_m: float = 3.0,
                 dangerous_wave_floor: str = "HIGH"):
        self.dangerous_wave_m = dangerous_wave_m
        self.dangerous_wave_floor = dangerous_wave_floor

    @staticmethod
    def classify(score: float) -> str:
        if score <= 25:
            return "LOW"
        if score <= 50:
            return "MODERATE"
        if score <= 79:
            return "HIGH"
        return "EXTREME"

    @staticmethod
    def _clamp(x: float) -> float:
        return max(0.0, min(100.0, float(x)))

    def score(self, components: Dict[str, float]) -> float:
        return round(sum(
            self._clamp(components.get(k, 0.0)) * w
            for k, w in self.WEIGHTS.items()
        ), 2)

    def evaluate(self, *,
                 components: Dict[str, float],
                 weather: Dict[str, Any],
                 restricted: bool = False,
                 evidence: Optional[List[Dict[str, Any]]] = None,
                 location: Optional[Dict[str, float]] = None) -> Dict[str, Any]:

        raw_score = self.score(components)
        level = self.classify(raw_score)
        reasons: List[str] = []

        # Non-negotiable safety overrides.
        severe_cyclone = (
            bool(weather.get("cyclone")) and
            str(weather.get("warning_severity", "")).upper() in {"SEVERE", "EXTREME"}
        )
        official_severe = (
            bool(weather.get("warning")) and
            str(weather.get("warning_severity", "")).upper() in {"SEVERE", "EXTREME"}
        )

        if severe_cyclone or official_severe:
            level = "EXTREME"
            reasons.append("Severe official marine/cyclone warning is active")

        if float(weather.get("wave_height", 0)) >= self.dangerous_wave_m:
            if self.dangerous_wave_floor == "EXTREME":
                level = "EXTREME"
            elif level not in {"EXTREME"}:
                level = "HIGH"
            reasons.append("Dangerously high wave conditions")

        if restricted:
            level = "DO NOT ENTER"
            reasons.append("Location is inside a restricted marine zone")

        # Evidence-driven reasons for the weighted result.
        if components.get("wave", 0) >= 50:
            reasons.append("Elevated wave conditions")
        if components.get("wind", 0) >= 50:
            reasons.append("Strong wind")
        if components.get("weather", 0) >= 50:
            reasons.append("Rain/visibility conditions increase risk")
        if components.get("sea_state", 0) >= 50:
            reasons.append("Unfavorable sea state/current")
        if components.get("location", 0) >= 50 and not restricted:
            reasons.append("Location/zone conditions increase risk")

        if not reasons:
            reasons.append("No major risk factor exceeded the prototype trigger levels")

        return {
            "risk_score": raw_score,
            "risk_level": level,
            "reasons": reasons,
            "evidence": evidence or [],
            "location": location,
            "confidence": self._confidence(weather),
        }

    @staticmethod
    def _confidence(weather: Dict[str, Any]) -> str:
        c = float(weather.get("confidence", 0))
        if c >= 0.85:
            return "HIGH"
        if c >= 0.60:
            return "MEDIUM"
        return "LOW"


def component_risks_from_weather(weather: Dict[str, Any],
                                  location_risk: float = 0.0,
                                  sea_state_risk: float = 0.0) -> Dict[str, float]:
    """Simple transparent prototype normalization.

    These thresholds are engineering assumptions for a prototype, not scientific truth.
    Tune them with domain experts/historical incident data.
    """

    # Wave: 0 at 0m, 100 at 4m+.
    wave = min(100.0, max(0.0, float(weather["wave_height"]) / 4.0 * 100.0))

    # Wind: 0 at 0, 100 at 60 km/h+.
    wind = min(100.0, max(0.0, float(weather["wind_speed"]) / 60.0 * 100.0))

    # Weather combines rain probability and poor visibility.
    rain = float(weather["rain_probability"])
    visibility = float(weather["visibility"])
    visibility_risk = min(100.0, max(0.0, (10.0 - visibility) / 10.0 * 100.0))
    weather_risk = 0.6 * rain + 0.4 * visibility_risk

    warning = 100.0 if weather.get("warning") else 0.0

    return {
        "wave": wave,
        "warning": warning,
        "wind": wind,
        "weather": weather_risk,
        "sea_state": sea_state_risk,
        "location": location_risk,
    }
