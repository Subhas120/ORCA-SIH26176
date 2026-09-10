from typing import Any, Dict, List


class RiskEngine:
    """
    ORCA M3 Deterministic Safety/Risk Engine.

    IMPORTANT:
    This engine makes the final safety decision.

    AI/LLM components may explain the result,
    but they must never lower or override this decision.
    """

    WEIGHTS = {
        "wave": 0.25,
        "warning": 0.25,
        "wind": 0.20,
        "weather": 0.10,
        "sea_state": 0.10,
        "location": 0.10,
    }

    RISK_BANDS = {
        "LOW": (0, 25),
        "MODERATE": (26, 50),
        "HIGH": (51, 79),
        "EXTREME": (80, 100),
    }

    def __init__(
        self,
        dangerous_wave_m: float = 3.0,
    ):
        self.dangerous_wave_m = dangerous_wave_m

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 100.0,
    ) -> float:
        return max(
            minimum,
            min(maximum, float(value)),
        )

    def classify(self, score: float) -> str:
        score = self._clamp(score)

        if score <= 25:
            return "LOW"

        if score <= 50:
            return "MODERATE"

        if score <= 79:
            return "HIGH"

        return "EXTREME"

    def _wave_risk(
        self,
        wave_height: float,
    ) -> float:
        """
        Prototype normalization:
        0 m = 0 risk
        4 m or above = 100 risk
        """
        return self._clamp(
            (float(wave_height) / 4.0) * 100.0
        )

    def _wind_risk(
        self,
        wind_speed: float,
    ) -> float:
        """
        Prototype normalization:
        0 km/h = 0 risk
        60 km/h or above = 100 risk
        """
        return self._clamp(
            (float(wind_speed) / 60.0) * 100.0
        )

    def _weather_risk(
        self,
        rain_probability: float,
        visibility: float,
    ) -> float:
        """
        Combines rain probability and visibility.

        Prototype assumptions:
        rain contributes 50%
        visibility contributes 50%
        """

        rain_risk = self._clamp(
            float(rain_probability)
        )

        visibility_risk = self._clamp(
            (10.0 - float(visibility)) * 10.0
        )

        return (
            rain_risk * 0.5
            + visibility_risk * 0.5
        )

    def _warning_risk(
        self,
        warning: bool,
        severity: Any = None,
    ) -> float:

        if not warning:
            return 0.0

        severity_text = str(
            severity or ""
        ).upper()

        if severity_text == "EXTREME":
            return 100.0

        if severity_text == "SEVERE":
            return 100.0

        if severity_text == "HIGH":
            return 90.0

        if severity_text == "MODERATE":
            return 60.0

        return 100.0

    def calculate(
        self,
        weather: Dict[str, Any],
        alert: Dict[str, Any] | None = None,
        *,
        sea_state_risk: float = 0.0,
        location_risk: float = 0.0,
        restricted: bool = False,
    ) -> Dict[str, Any]:
        """
        Calculate deterministic ORCA safety risk.

        Returns:
            score
            level
            reasons
            evidence
            confidence
            decision
        """

        alert = alert or {}

        wave_height = float(
            weather.get("wave_height", 0.0)
        )

        wind_speed = float(
            weather.get("wind_speed", 0.0)
        )

        rain_probability = float(
            weather.get("rain_probability", 0.0)
        )

        visibility = float(
            weather.get("visibility", 10.0)
        )

        warning = bool(
            alert.get(
                "warning",
                weather.get("warning", False),
            )
        )

        warning_severity = alert.get(
            "warning_severity",
            weather.get("warning_severity"),
        )

        wave_component = self._wave_risk(
            wave_height
        )

        warning_component = self._warning_risk(
            warning,
            warning_severity,
        )

        wind_component = self._wind_risk(
            wind_speed
        )

        weather_component = self._weather_risk(
            rain_probability,
            visibility,
        )

        sea_component = self._clamp(
            sea_state_risk
        )

        location_component = self._clamp(
            location_risk
        )

        score = (
            wave_component
            * self.WEIGHTS["wave"]
            + warning_component
            * self.WEIGHTS["warning"]
            + wind_component
            * self.WEIGHTS["wind"]
            + weather_component
            * self.WEIGHTS["weather"]
            + sea_component
            * self.WEIGHTS["sea_state"]
            + location_component
            * self.WEIGHTS["location"]
        )

        score = round(
            self._clamp(score),
            2,
        )

        level = self.classify(score)

        reasons: List[str] = []

        # -------------------------------------------------
        # SAFETY OVERRIDE 1: SEVERE CYCLONE
        # -------------------------------------------------

        cyclone = bool(
            weather.get("cyclone", False)
        )

        storm = bool(
            weather.get("storm", False)
        )

        if (
            cyclone
            and warning
            and str(
                warning_severity or ""
            ).upper()
            in {"SEVERE", "EXTREME"}
        ):
            level = "EXTREME"

            reasons.append(
                "Severe cyclone warning"
            )

        # -------------------------------------------------
        # SAFETY OVERRIDE 2: DANGEROUS WAVE
        # -------------------------------------------------

        if wave_height >= self.dangerous_wave_m:

            if level == "LOW":
                level = "HIGH"

            elif level == "MODERATE":
                level = "HIGH"

            reasons.append(
                f"Dangerously high wave height: "
                f"{wave_height:.1f} m"
            )

        # -------------------------------------------------
        # SAFETY OVERRIDE 3: RESTRICTED ZONE
        # -------------------------------------------------

        if restricted:

            level = "DO NOT ENTER"

            reasons.append(
                "Location is inside a restricted marine zone"
            )

        # -------------------------------------------------
        # ADDITIONAL EXPLANATION REASONS
        # -------------------------------------------------

        if warning:
            reasons.append(
                "Official marine warning is active"
            )

        if wind_speed >= 40:
            reasons.append(
                f"High wind speed: "
                f"{wind_speed:.1f} km/h"
            )

        if rain_probability >= 70:
            reasons.append(
                f"High rain probability: "
                f"{rain_probability:.1f}%"
            )

        if visibility <= 3:
            reasons.append(
                f"Poor visibility: "
                f"{visibility:.1f} km"
            )

        if storm and not cyclone:
            reasons.append(
                "Storm condition reported"
            )

        if not reasons:
            reasons.append(
                "No major risk factor exceeded "
                "the prototype trigger levels"
            )

        # -------------------------------------------------
        # CONFIDENCE
        # -------------------------------------------------

        confidence_values = []

        if weather.get("confidence") is not None:
            confidence_values.append(
                float(weather["confidence"])
            )

        if alert.get("confidence") is not None:
            confidence_values.append(
                float(alert["confidence"])
            )

        if confidence_values:
            confidence = min(
                confidence_values
            )
        else:
            confidence = 0.0

        # -------------------------------------------------
        # EVIDENCE
        # -------------------------------------------------

        evidence = []

        if weather.get("source"):
            evidence.append({
                "source": weather.get("source"),
                "timestamp": weather.get("timestamp"),
                "location": weather.get("location"),
                "parameter": "wind_speed",
                "value": wind_speed,
                "unit": "km/h",
            })

            evidence.append({
                "source": weather.get("source"),
                "timestamp": weather.get("timestamp"),
                "location": weather.get("location"),
                "parameter": "wave_height",
                "value": wave_height,
                "unit": "m",
            })

        if warning:
            evidence.append({
                "source": alert.get(
                    "source",
                    "UNKNOWN",
                ),
                "timestamp": alert.get(
                    "timestamp"
                ),
                "location": alert.get(
                    "location"
                ),
                "parameter": "official_warning",
                "value": warning,
                "unit": None,
            })

        # -------------------------------------------------
        # FINAL DECISION
        # -------------------------------------------------

        if level == "DO NOT ENTER":
            decision = "DO NOT ENTER"

        elif level == "EXTREME":
            decision = "UNSAFE"

        elif level == "HIGH":
            decision = "HIGH RISK"

        elif level == "MODERATE":
            decision = "CAUTION"

        else:
            decision = "LOW RISK"

        return {
            "score": score,
            "level": level,
            "decision": decision,
            "reasons": reasons,
            "evidence": evidence,
            "confidence": confidence,
            "components": {
                "wave": round(
                    wave_component,
                    2,
                ),
                "warning": round(
                    warning_component,
                    2,
                ),
                "wind": round(
                    wind_component,
                    2,
                ),
                "weather": round(
                    weather_component,
                    2,
                ),
                "sea_state": round(
                    sea_component,
                    2,
                ),
                "location": round(
                    location_component,
                    2,
                ),
            },
            "weights": self.WEIGHTS.copy(),
        }


def component_risks_from_weather(
    weather: Dict[str, Any],
) -> Dict[str, float]:
    """
    Convenience function for M3 integrations.
    """

    engine = RiskEngine()

    return {
        "wave": engine._wave_risk(
            weather.get("wave_height", 0.0)
        ),

        "warning": engine._warning_risk(
            weather.get("warning", False),
            weather.get("warning_severity"),
        ),

        "wind": engine._wind_risk(
            weather.get("wind_speed", 0.0)
        ),

        "weather": engine._weather_risk(
            weather.get(
                "rain_probability",
                0.0,
            ),
            weather.get(
                "visibility",
                10.0,
            ),
        ),

        "sea_state": 0.0,

        "location": 0.0,
    }


if __name__ == "__main__":

    print("=== ORCA M3 RISK ENGINE ===")

    weather = {
        "wind_speed": 22.0,
        "rain_probability": 30.0,
        "visibility": 8.0,
        "wave_height": 1.2,
        "wave_period": 7.0,
        "warning": False,
        "cyclone": False,
        "storm": False,
        "confidence": 0.95,
        "source": "DEMO-WEATHER",
        "timestamp": "2026-09-10T22:00:00",
        "location": "Kochi",
    }

    alert = {
        "warning": False,
        "warning_type": None,
        "warning_severity": None,
        "confidence": 0.95,
        "source": "DEMO-ALERT",
        "timestamp": "2026-09-10T22:00:00",
        "location": "Kochi",
    }

    engine = RiskEngine()

    risk = engine.calculate(
        weather,
        alert,
    )

    print("Risk score:", risk["score"])
    print("Risk level:", risk["level"])
    print("Decision:", risk["decision"])

    print("Reasons:")

    for reason in risk["reasons"]:
        print("-", reason)