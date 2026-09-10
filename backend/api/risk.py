from fastapi import APIRouter
from models.schemas import RiskRequest, RiskResponse

router = APIRouter(prefix="/api", tags=["Risk"])

@router.post("/risk", response_model=RiskResponse)
async def evaluate_risk(request: RiskRequest):
    """
    Evaluate risk for a given location and context.
    """
    return RiskResponse(
        risk_score=0, # Placeholder
        risk_level="LOW", # Placeholder
        reasons=["[Placeholder] Risk engine not connected yet."]
    )
