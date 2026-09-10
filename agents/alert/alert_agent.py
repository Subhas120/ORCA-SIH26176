from typing import Any, Dict, Optional

from agents.common.agent_contract import AgentResponse


class AlertAgent:
    """
    ORCA M3 Alert Agent.

    Handles official marine warnings and alerts.

    This prototype uses clearly labelled demo data.
    Real official alert APIs can be connected later.

    IMPORTANT:
    The Alert Agent reports warnings.
    It does NOT calculate or lower risk.
    The deterministic Risk Engine makes the final safety decision.
    """

    def __init__(self):
        self._cache: Optional[Dict[str, Any]] = None

    def get(
        self,
        observation: Optional[Dict[str, Any]],
        *,
        source_available: bool = True,
        timestamp: str = "2026-09-10T22:00:00",
        source: str = "DEMO-ALERT",
        location: Optional[str] = None,
    ) -> Dict[str, Any]:

        if source_available and observation is not None:

            data = {
                "warning": bool(
                    observation.get("warning", False)
                ),
                "warning_type": observation.get(
                    "warning_type"
                ),
                "warning_severity": observation.get(
                    "warning_severity"
                ),
                "message": observation.get(
                    "message"
                ),
                "timestamp": timestamp,
                "source": source,
                "location": location,
                "confidence": 0.95,
                "source_status": "live",
            }

            self._cache = dict(data)

            return data

        if self._cache:

            cached = dict(self._cache)

            cached["confidence"] = min(
                float(cached["confidence"]),
                0.60,
            )

            cached["source_status"] = "cached"

            return cached

        raise RuntimeError(
            "Reliable alert data is unavailable "
            "and no cached alert exists."
        )


def handle_alert(request) -> AgentResponse:
    """
    M1-compatible Alert Agent handler.

    Returns an AgentResponse using the common M1 contract.
    """

    try:

        agent = AlertAgent()

        # -------------------------------------------------
        # MOCK / DEMO OFFICIAL ALERT DATA
        # -------------------------------------------------
        #
        # Currently there is no active warning.
        # This is demo data and NOT a live official alert.
        #
        observation = {
            "warning": False,
            "warning_type": None,
            "warning_severity": None,
            "message": None,
        }

        data = agent.get(
            observation,
            source_available=True,
            timestamp="2026-09-10T22:00:00",
            source="DEMO-ALERT",
            location=request.location,
        )

        return AgentResponse(
            agent="alert",
            status="success",
            data=data,
            source=data["source"],
            timestamp=data["timestamp"],
            location=data["location"],
            confidence=data["confidence"],
        )

    except Exception as exc:

        return AgentResponse(
            agent="alert",
            status="unavailable",
            data={},
            source="DEMO-ALERT",
            timestamp=None,
            location=request.location,
            confidence=0.0,
            error=str(exc),
        )


if __name__ == "__main__":

    print("=== ORCA M3 ALERT AGENT ===")

    class DemoRequest:
        location = "Kochi"

    response = handle_alert(
        DemoRequest()
    )

    print(response)