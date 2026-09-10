from agents.risk.risk_engine import RiskEngine, component_risks_from_weather
from agents.weather.weather_agent import WeatherAgent


def base_weather():
    return {
        "wind_speed": 22, "rain_probability": 30, "visibility": 8,
        "temperature": 28, "wave_height": 1.2, "wave_period": 7,
        "warning": False
    }


def test_weather_contract_and_cache():
    agent = WeatherAgent()
    live = agent.get(base_weather(), timestamp="t1", source="test")
    assert live["wave_height"] == 1.2
    assert live["timestamp"] == "t1"

    cached = agent.get(None, source_available=False)
    assert cached["source_status"] == "cached"
    assert cached["confidence"] <= 0.60


def test_risk_bands():
    assert RiskEngine.classify(0) == "LOW"
    assert RiskEngine.classify(25) == "LOW"
    assert RiskEngine.classify(26) == "MODERATE"
    assert RiskEngine.classify(50) == "MODERATE"
    assert RiskEngine.classify(51) == "HIGH"
    assert RiskEngine.classify(79) == "HIGH"
    assert RiskEngine.classify(80) == "EXTREME"


def test_cyclone_override_forces_extreme():
    weather = base_weather()
    weather.update({
        "warning": True,
        "cyclone": True,
        "warning_severity": "SEVERE"
    })
    risk = RiskEngine().evaluate(
        components=component_risks_from_weather(weather),
        weather=weather
    )
    assert risk["risk_level"] == "EXTREME"


def test_restricted_override():
    weather = base_weather()
    risk = RiskEngine().evaluate(
        components=component_risks_from_weather(weather),
        weather=weather,
        restricted=True
    )
    assert risk["risk_level"] == "DO NOT ENTER"
