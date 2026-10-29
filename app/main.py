from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.db.init_db import init_db
from app.routers import (
    controls_router,
    dashboard_router,
    evidences_router,
    proposals_router,
    requirements_router,
    settings_router,
    soa_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed data idempotently
    init_db()
    # Ensure upload directory exists
    settings.resolved_upload_dir
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema de evaluación, documentación y gestión de ISO/IEC 27001:2022 con IA local.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# Static and Templates configuration
BASE_PATH = Path(__file__).resolve().parent
templates_dir = BASE_PATH / "templates"
static_dir = BASE_PATH / "static"

templates = Jinja2Templates(directory=str(templates_dir))
app.state.templates = templates

# Mount static folder
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include Routers
app.include_router(dashboard_router)
app.include_router(requirements_router)
app.include_router(controls_router)
app.include_router(evidences_router)
app.include_router(soa_router)
app.include_router(proposals_router)
app.include_router(settings_router)


@app.get("/health", tags=["Salud"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "ollama_configured": settings.OLLAMA_MODEL,
    }


# Secure error handler - avoid leaking internal stack traces
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # If API request, return JSON
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=500,
            content={"detail": "Ocurrió un error interno en el servidor."},
        )
    # If web request, render friendly error page
    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Error en SecAuditAI</title>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body class="bg-dark text-light">
            <div class="container py-5 text-center">
                <div class="card p-5 mx-auto" style="max-width: 600px;">
                    <h2 class="text-danger mb-3">Aviso del Sistema</h2>
                    <p class="mb-4">Se produjo una situación imprevista al procesar la solicitud. Los detalles han sido registrados de forma segura.</p>
                    <a href="/" class="btn btn-primary">Volver al Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        """,
        status_code=500,
    )
