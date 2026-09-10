from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api", tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main natural language chat endpoint for ORCA.
    """
    return ChatResponse(
        response="[Placeholder] This is a stub response. NLP integration pending.",
        intent="GENERAL_QUERY",
        risk=None,
        sources=[]
    )
