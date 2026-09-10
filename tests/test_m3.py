import unittest

from agents.weather.weather_agent import WeatherAgent, handle_weather
from agents.alert.alert_agent import handle_alert
from agents.risk.risk_engine import (
    RiskEngine,
    component_risks_from_weather,
)
from agents.common.agent_contract import AgentRequest, AgentResponse


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
    }


class TestM3(unittest.TestCase):

    def test_weather_agent_contract(self):
        agent = WeatherAgent()

        result = agent.get(
            base_weather(),
            source_available=True,
            timestamp="2026-09-10T22:00:00",
            source="TEST-WEATHER",
        )

        self.assertIn("wind_speed", result)
        self.assertIn("rain_probability", result)
        self.assertIn("visibility", result)
        self.assertIn("wave_height", result)
        self.assertIn("warning", result)

        self.assertEqual(result["source"], "TEST-WEATHER")
        self.assertEqual(result["confidence"], 0.95)

    def test_weather_agent_returns_agent_response(self):
        request = AgentRequest(
            query="Is it safe to fish?",
            location="Kochi",
        )

        result = handle_weather(request)

        self.assertIsInstance(result, AgentResponse)
        self.assertEqual(result.agent, "weather")
        self.assertEqual(result.status, "success")
        self.assertIsNotNone(result.data)
        self.assertIsNotNone(result.source)
        self.assertIsNotNone(result.timestamp)
        self.assertIsNotNone(result.location)
        self.assertIsNotNone(result.confidence)

    def test_alert_agent_returns_agent_response(self):
        request = AgentRequest(
            query="Are there marine warnings?",
            location="Kochi",
        )

        result = handle_alert(request)

        self.assertIsInstance(result, AgentResponse)
        self.assertEqual(result.agent, "alert")
        self.assertEqual(result.status, "success")
        self.assertIsNotNone(result.data)
        self.assertIsNotNone(result.source)
        self.assertIsNotNone(result.timestamp)
        self.assertIsNotNone(result.location)
        self.assertIsNotNone(result.confidence)

    def test_risk_bands(self):
        engine = RiskEngine()

        self.assertEqual(engine.classify(0), "LOW")
        self.assertEqual(engine.classify(25), "LOW")

        self.assertEqual(engine.classify(26), "MODERATE")
        self.assertEqual(engine.classify(50), "MODERATE")

        self.assertEqual(engine.classify(51), "HIGH")
        self.assertEqual(engine.classify(79), "HIGH")

        self.assertEqual(engine.classify(80), "EXTREME")
        self.assertEqual(engine.classify(100), "EXTREME")

    def test_normal_risk_calculation(self):
        engine = RiskEngine()

        weather = base_weather()

        risk = engine.calculate(weather)

        self.assertIn("score", risk)
        self.assertIn("level", risk)
        self.assertIn("decision", risk)
        self.assertIn("reasons", risk)
        self.assertIn("evidence", risk)
        self.assertIn("confidence", risk)

        self.assertGreaterEqual(risk["score"], 0)
        self.assertLessEqual(risk["score"], 100)

        self.assertEqual(risk["level"], "LOW")
        self.assertEqual(risk["decision"], "LOW RISK")

    def test_cyclone_override_forces_extreme(self):
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

        self.assertEqual(risk["level"], "EXTREME")
        self.assertEqual(risk["decision"], "UNSAFE")

        self.assertIn(
            "Severe cyclone warning",
            risk["reasons"],
        )

    def test_high_wave_override(self):
        engine = RiskEngine()

        weather = base_weather()
        weather["wave_height"] = 3.5

        risk = engine.calculate(weather)

        self.assertIn(
            risk["level"],
            ["HIGH", "EXTREME"],
        )

        self.assertTrue(
            any(
                "Dangerously high wave height" in reason
                for reason in risk["reasons"]
            )
        )

    def test_restricted_override(self):
        engine = RiskEngine()

        weather = base_weather()

        risk = engine.calculate(
            weather,
            restricted=True,
        )

        self.assertEqual(
            risk["level"],
            "DO NOT ENTER",
        )

        self.assertEqual(
            risk["decision"],
            "DO NOT ENTER",
        )

        self.assertIn(
            "Location is inside a restricted marine zone",
            risk["reasons"],
        )

    def test_component_risks(self):
        weather = base_weather()

        components = component_risks_from_weather(weather)

        self.assertIn("wave", components)
        self.assertIn("warning", components)
        self.assertIn("wind", components)
        self.assertIn("weather", components)
        self.assertIn("sea_state", components)
        self.assertIn("location", components)

        for value in components.values():
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 100)


if __name__ == "__main__":
    unittest.main()