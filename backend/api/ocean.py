from fastapi import APIRouter, Query
from models.schemas import OceanResponse

router = APIRouter(prefix="/api", tags=["Ocean"])

@router.get("/ocean", response_model=OceanResponse)
async def get_ocean(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude")
):
    """
    Retrieve normalized marine observations for a specific location.
    """
    return OceanResponse(observations=[]) # Placeholder
