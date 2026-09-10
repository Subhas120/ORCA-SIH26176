from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
