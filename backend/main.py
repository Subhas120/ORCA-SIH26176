from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat import router as chat_router
from api.weather import router as weather_router
from api.ocean import router as ocean_router
from api.risk import router as risk_router
from api.location import router as location_router
from api.routes import router as routes_router
from api.alerts import router as alerts_router

# Initialize FastAPI application
app = FastAPI(
    title="ORCA Backend",
    description="Backend for ORCA-SIH26176",
    version="1.0.0"
)

# Configure CORS so the future React frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routers
app.include_router(chat_router)
app.include_router(weather_router)
app.include_router(ocean_router)
app.include_router(risk_router)
app.include_router(location_router)
app.include_router(routes_router)
app.include_router(alerts_router)

@app.get("/")
async def read_root():
    """
    Root endpoint.
    """
    return {"message": "ORCA Backend Running"}

@app.get("/health")
async def read_health():
    """
    Health check endpoint to verify backend status.
    """
    return {"status": "healthy"}
