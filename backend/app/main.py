"""
FastAPI main application entry point.
"""
import logging
import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.types import Scope
from starlette.responses import Response

from app.config import settings
from app.routers import graphics

# Configure logging
log_level = logging.DEBUG if settings.environment == "development" else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class SPAStaticFiles(StaticFiles):
    """
    Custom StaticFiles that serves index.html for SPA routing,
    but doesn't intercept API requests.
    """
    async def get_response(self, path: str, scope: Scope) -> Response:
        # If it's an API request, don't handle it - let it 404
        # so FastAPI's actual API routes can handle it
        if path.startswith('api/'):
            raise RuntimeError("Not a static file")

        try:
            # Try to serve the requested file
            return await super().get_response(path, scope)
        except Exception:
            # If file not found, serve index.html for SPA client-side routing
            # (except for API routes which should 404)
            if not path.startswith('api'):
                index_path = os.path.join(self.directory, 'index.html')
                return FileResponse(index_path)
            raise


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Backend API for Infoviz - Information visualization platform",
    version="1.0.0",
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(graphics.router, prefix="/api", tags=["Graphics"])

# Serve built frontend if available
FRONTEND_DIST = Path(__file__).resolve().parent / "frontend_client"
if FRONTEND_DIST.exists():
    logger.info("Serving frontend assets from %s", FRONTEND_DIST)
    app.mount("/", SPAStaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")
else:
    logger.info("Frontend assets directory not found at %s (skipping mount).", FRONTEND_DIST)

@app.get("/api/ready")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready"}


# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info("=" * 50)
    logger.info("🚀 Infoviz API Starting...")
    logger.info(f"App Name: {settings.app_name}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info("=" * 50)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )
