from fastapi import APIRouter, Query
from models.schemas import WeatherResponse, Location

router = APIRouter(prefix="/api", tags=["Weather"])

@router.get("/weather", response_model=WeatherResponse)
async def get_weather(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude")
):
    """
    Retrieve structured weather information for a specific location.
    """
    return WeatherResponse(
        location=Location(latitude=latitude, longitude=longitude),
        observations=[] # Placeholder
    )
