from app.routers.controls import router as controls_router
from app.routers.dashboard import router as dashboard_router
from app.routers.evidences import router as evidences_router
from app.routers.proposals import router as proposals_router
from app.routers.requirements import router as requirements_router
from app.routers.settings import router as settings_router
from app.routers.soa import router as soa_router

__all__ = [
    "dashboard_router",
    "requirements_router",
    "controls_router",
    "evidences_router",
    "soa_router",
    "proposals_router",
    "settings_router",
]
