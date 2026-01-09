"""
FastAPI application entry point.
Mechanical Assistant - CAD part generation from natural language.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.parts import router as parts_router
from app.api.v1.interpret import router as interpret_router

# Create FastAPI app
app = FastAPI(
    title="Mechanical Assistant",
    description="Generate CAD parts from natural language descriptions",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(parts_router)
app.include_router(interpret_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Mechanical Assistant API",
        "version": "0.1.0",
        "description": "Generate CAD parts from natural language descriptions",
        "endpoints": {
            "interpret": "/api/v1/interpret - Convert natural language to structured intent",
            "parts": "/api/v1/parts - Generate STEP files from CAD specifications",
            "docs": "/docs - Interactive API documentation",
            "redoc": "/redoc - Alternative API documentation"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "mechanical-assistant"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
