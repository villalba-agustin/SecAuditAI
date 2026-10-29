from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.services.ollama_service import check_ollama_status, load_skill_definition

router = APIRouter(prefix="/settings", tags=["Configuración"])


@router.get("/ollama", response_class=HTMLResponse)
def get_ollama_settings_page(request: Request):
    status = check_ollama_status()
    skill_meta, skill_body = load_skill_definition()
    templates = request.app.state.templates

    return templates.TemplateResponse(
        request=request,
        name="settings/ollama.html",
        context={
            "status": status,
            "skill_meta": skill_meta,
            "skill_body": skill_body,
            "config": settings,
            "active_page": "settings",
        },
    )


@router.get("/api/ollama/status")
def get_ollama_status_api():
    return check_ollama_status()
