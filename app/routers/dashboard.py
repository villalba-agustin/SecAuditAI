from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.compliance_service import get_dashboard_summary

router = APIRouter(tags=["Dashboard"])


@router.get("/", response_class=HTMLResponse)
def get_dashboard_page(request: Request, db: Session = Depends(get_db)):
    summary = get_dashboard_summary(db)
    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"summary": summary, "active_page": "dashboard"},
    )


@router.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)
