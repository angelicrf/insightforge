"""Main application entrypoint for the InsightForge API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.api.router import api_router
from app.config.settings import settings
from app.middleware.logging_middleware import LoggingMiddleware

# Configure structured logging for production-ready logs
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

log = structlog.get_logger()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Enterprise Multi-Agent AI Support Automation Platform"
)

# Add middleware
app.add_middleware(LoggingMiddleware)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add the root health check endpoint directly to the app
@app.get("/", tags=["Health Check"])
async def root_health_check():
    """A simple health check endpoint to confirm the API is running."""
    return {"status": "ok", "message": f"Welcome to {settings.PROJECT_NAME}"}


# Include the main API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Backward compatibility for clients using a historical typo in the prefix.
app.include_router(api_router, prefix="/api/vi")