from fastapi import APIRouter, Query
from models.schemas import LocationResponse

router = APIRouter(prefix="/api", tags=["Location"])

@router.get("/location", response_model=LocationResponse)
async def get_location(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude")
):
    """
    Retrieve structured location information (e.g., nearest PFZ, restricted zones).
    """
    return LocationResponse(
        latitude=latitude,
        longitude=longitude,
        name="[Placeholder] Unknown Location",
        type="[Placeholder] UNKNOWN"
    )
