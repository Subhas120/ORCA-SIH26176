from fastapi import APIRouter, Query
from models.schemas import AlertsResponse
from typing import Optional

router = APIRouter(prefix="/api", tags=["Alerts"])

@router.get("/alerts", response_model=AlertsResponse)
async def get_alerts(
    latitude: Optional[float] = Query(None, ge=-90, le=90, description="Optional latitude"),
    longitude: Optional[float] = Query(None, ge=-180, le=180, description="Optional longitude")
):
    """
    Retrieve structured marine alerts for a specific location or globally.
    """
    return AlertsResponse(alerts=[]) # Placeholder
