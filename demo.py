from agents.weather.weather_agent import WeatherAgent
from agents.risk.risk_engine import RiskEngine, component_risks_from_weather
from data.sample_data import WEATHER


def main():
    weather = WeatherAgent().get(
        WEATHER,
        timestamp="2026-09-10T21:00:00",
        source="DEMO-WEATHER"
    )

    components = component_risks_from_weather(weather)

    risk = RiskEngine().evaluate(
        components=components,
        weather=weather,
        restricted=False,
        evidence=[
            {
                "source": weather["source"],
                "timestamp": weather["timestamp"],
                "parameter": "wind_speed",
                "value": weather["wind_speed"],
                "unit": "km/h"
            },
            {
                "source": weather["source"],
                "timestamp": weather["timestamp"],
                "parameter": "wave_height",
                "value": weather["wave_height"],
                "unit": "m"
            },
            {
                "source": weather["source"],
                "timestamp": weather["timestamp"],
                "parameter": "visibility",
                "value": weather["visibility"],
                "unit": "km"
            }
        ],
        location={
            "latitude": 9.9312,
            "longitude": 76.2673
        }
    )

    print()
    print("=== ORCA M3 WEATHER AGENT ===")
    print("Weather:", weather)

    print()
    print("=== ORCA M3 DETERMINISTIC RISK ENGINE ===")
    print("Risk score:", risk["risk_score"])
    print("Risk level:", risk["risk_level"])
    print("Confidence:", risk["confidence"])

    print()
    print("Reasons:")
    for reason in risk["reasons"]:
        print("-", reason)

    print()
    print("Evidence:")
    for item in risk["evidence"]:
        print("-", item)

    print()
    print("M3 DEMO SUCCESS")


if __name__ == "__main__":
    main()