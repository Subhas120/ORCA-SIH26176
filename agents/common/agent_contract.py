from dataclasses import dataclass, field
from typing import Any, Optional


VALID_STATUSES = {
    "success",
    "error",
    "unavailable",
}


@dataclass
class AgentRequest:
    query: str
    location: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    activity: Optional[str] = None

    def __post_init__(self):
        if not self.query or not self.query.strip():
            raise ValueError("query cannot be empty")


@dataclass
class AgentResponse:
    agent: str
    status: str
    data: dict[str, Any] = field(default_factory=dict)
    source: Optional[str] = None
    timestamp: Optional[str] = None
    location: Optional[str] = None
    confidence: Optional[float] = None
    error: Optional[str] = None

    def __post_init__(self):

        if not self.agent or not self.agent.strip():
            raise ValueError("agent cannot be empty")

        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status: {self.status}"
            )

        if self.confidence is not None:

            if not isinstance(
                self.confidence,
                (int, float),
            ):
                raise ValueError(
                    "confidence must be a number"
                )

            if not 0.0 <= self.confidence <= 1.0:
                raise ValueError(
                    "confidence must be between 0.0 and 1.0"
                )

        if self.status in {
            "error",
            "unavailable",
        }:

            if not self.error or not self.error.strip():
                raise ValueError(
                    "error is required when status is error or unavailable"
                )
