import unittest

from agents.explanation.explanation_engine import build_explanation
from agents.risk.m4_integration import (
    assess_location_safety,
    build_route_risk_functions,
    calculate_safest_route,
    load_zone_features,
)
from agents.risk.risk_engine import RiskEngine


def base_weather():
    return {
        "wind_speed": 20.0,
        "rain_probability": 20.0,
        "visibility": 10.0,
        "temperature": 28.0,
        "wave_height": 1.0,
        "wave_period": 7.0,
        "warning": False,
        "warning_type": None,
        "warning_severity": None,
        "cyclone": False,
        "storm": False,
        "lightning": False,
        "confidence": 0.95,
        "source": "TEST-WEATHER",
        "timestamp": "2026-09-10T22:00:00",
        "location": "Kochi",
    }


class TestM3M4Integration(unittest.TestCase):

    def test_m4_geofence_reaches_m3_risk_engine(self):
        weather = base_weather()

        risk = assess_location_safety(
            weather,
            None,
            (9.84, 76.25),
        )

        self.assertTrue(risk["location"]["restricted"])
        self.assertIn(
            "Prototype Restricted Zone",
            risk["location"]["containing_zones"],
        )
        self.assertEqual(
            risk["level"],
            "DO NOT ENTER",
        )
        self.assertEqual(
            risk["decision"],
            "DO NOT ENTER",
        )

    def test_safe_location_is_not_restricted(self):
        weather = base_weather()

        risk = assess_location_safety(
            weather,
            None,
            (9.9312, 76.2673),
        )

        self.assertFalse(risk["location"]["restricted"])
        self.assertEqual(
            risk["location"]["containing_zones"],
            [],
        )
        self.assertEqual(
            risk["level"],
            "LOW",
        )

    def test_m3_route_risk_functions_are_callable(self):
        weather = base_weather()

        functions = build_route_risk_functions(
            weather,
            None,
        )

        self.assertIn("weather_risk", functions)
        self.assertIn("wave_risk", functions)
        self.assertIn("hazard_penalty", functions)

        coordinate = (9.9, 76.3)

        for function in functions.values():
            value = function(coordinate)
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 100.0)

    def test_m3_risk_inputs_reach_m4_astar(self):
        weather = base_weather()

        route = calculate_safest_route(
            (9.9312, 76.2673),
            (9.4981, 76.3388),
            weather,
            None,
        )

        self.assertEqual(
            route["status"],
            "success",
        )
        self.assertEqual(
            route["algorithm"],
            "A*",
        )
        self.assertIn(
            "weather_risk",
            route["cost_model"],
        )
        self.assertIn(
            "wave_risk",
            route["cost_model"],
        )
        self.assertIn(
            "hazard_penalty",
            route["cost_model"],
        )

    def test_restricted_zone_geometry_is_preserved_for_routes(self):
        features = load_zone_features()

        restricted = [
            feature
            for feature in features
            if feature.get("properties", {}).get("zone_type")
            == "restricted"
        ]

        self.assertEqual(
            len(restricted),
            1,
        )
        self.assertEqual(
            restricted[0]["properties"]["name"],
            "Prototype Restricted Zone",
        )

    def test_explanation_cannot_downgrade_extreme_risk(self):
        engine = RiskEngine()

        weather = base_weather()
        weather.update({
            "warning": True,
            "cyclone": True,
            "warning_severity": "SEVERE",
        })

        alert = {
            "warning": True,
            "warning_type": "CYCLONE",
            "warning_severity": "SEVERE",
            "confidence": 0.95,
            "source": "TEST-ALERT",
            "timestamp": "2026-09-10T22:00:00",
            "location": "Kochi",
        }

        risk = engine.calculate(
            weather,
            alert,
        )

        explanation = build_explanation(
            risk,
            [],
        )

        self.assertEqual(
            risk["level"],
            "EXTREME",
        )
        self.assertEqual(
            risk["decision"],
            "UNSAFE",
        )
        self.assertEqual(
            explanation["risk_level"],
            "EXTREME",
        )
        self.assertEqual(
            explanation["risk_score"],
            risk["score"],
        )


if __name__ == "__main__":
    unittest.main()