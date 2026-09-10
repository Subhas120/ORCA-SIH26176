from fastapi import APIRouter
from models.schemas import RouteRequest, RouteResponse

router = APIRouter(prefix="/api", tags=["Routes"])

@router.post("/routes", response_model=RouteResponse)
async def calculate_route(request: RouteRequest):
    """
    Calculate the safest route from origin to destination.
    """
    return RouteResponse(
        path=[], # Placeholder
        total_distance=0.0,
        estimated_duration=0.0
    )
