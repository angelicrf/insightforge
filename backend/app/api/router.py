"""Main API router for the application."""

from fastapi import APIRouter

from app.api.routes import assistant, integrations, pardot, tables, tickets, users
from app.api.routes.neoondb import neon
api_router = APIRouter()

# Include resource-specific routers
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["Integrations"])
api_router.include_router(pardot.router, prefix="/pardot", tags=["Pardot"])
api_router.include_router(neon.router, prefix="/neon", tags=["NeonDB"])
api_router.include_router(tables.router, tags=["Tables"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])