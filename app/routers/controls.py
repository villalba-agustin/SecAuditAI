from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_analysis import AIProposal
from app.models.assessment import Assessment
from app.models.audit import AuditLog
from app.models.control import AnnexControl
from app.models.evidence import EvidenceMapping
from app.services.audit_service import log_audit

router = APIRouter(prefix="/controls", tags=["Controles Anexo A"])


@router.get("", response_class=HTMLResponse)
def list_controls_page(
    request: Request,
    category: Optional[str] = None,
    score: Optional[int] = None,
    status: Optional[str] = None,
    applicable: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(AnnexControl)

    if category:
        query = query.filter(AnnexControl.category == category)
    if score is not None:
        query = query.filter(AnnexControl.implementation_score == score)
    if status:
        query = query.filter(AnnexControl.implementation_status == status)
    if applicable == "true":
        query = query.filter(AnnexControl.is_applicable.is_(True))
    elif applicable == "false":
        query = query.filter(AnnexControl.is_applicable.is_(False))

    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(
            (AnnexControl.code.ilike(search_fmt))
            | (AnnexControl.title.ilike(search_fmt))
            | (AnnexControl.description.ilike(search_fmt))
        )

    # Sort numerically by code
    def sort_key(c: AnnexControl):
        parts = c.code.replace("A.", "").split(".")
        return [int(p) if p.isdigit() else p for p in parts]

    controls = sorted(query.all(), key=sort_key)
    templates = request.app.state.templates

    return templates.TemplateResponse(
        request=request,
        name="controls/list.html",
        context={
            "controls": controls,
            "active_page": "controls",
            "selected_category": category or "",
            "selected_score": score,
            "selected_status": status or "",
            "selected_applicable": applicable or "",
            "search_query": search or "",
        },
    )


@router.get("/{code}", response_class=HTMLResponse)
def control_detail_page(code: str, request: Request, db: Session = Depends(get_db)):
    ctrl = db.query(AnnexControl).filter(AnnexControl.code == code).first()
    if not ctrl:
        raise HTTPException(status_code=404, detail="Control no encontrado")

    # Mapped evidences
    mappings = (
        db.query(EvidenceMapping)
        .filter(EvidenceMapping.control_id == ctrl.id)
        .all()
    )

    # AI proposals
    proposals = (
        db.query(AIProposal)
        .filter(AIProposal.control_id == ctrl.id)
        .order_by(AIProposal.created_at.desc())
        .all()
    )

    # Assessment history
    assessments = (
        db.query(Assessment)
        .filter(Assessment.entity_type == "control", Assessment.entity_id == ctrl.id)
        .order_by(Assessment.created_at.desc())
        .all()
    )

    # Audit history
    audit_logs = (
        db.query(AuditLog)
        .filter(AuditLog.entity_code == ctrl.code)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )

    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request,
        name="controls/detail.html",
        context={
            "ctrl": ctrl,
            "mappings": mappings,
            "proposals": proposals,
            "assessments": assessments,
            "audit_logs": audit_logs,
            "active_page": "controls",
        },
    )


@router.post("/{code}/evaluate")
def evaluate_control(
    code: str,
    is_applicable: bool = Form(True),
    justification_inclusion: Optional[str] = Form(None),
    justification_exclusion: Optional[str] = Form(None),
    implementation_status: str = Form("No iniciado"),
    implementation_score: int = Form(0),
    implementation_summary: Optional[str] = Form(None),
    responsible: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    ctrl = db.query(AnnexControl).filter(AnnexControl.code == code).first()
    if not ctrl:
        raise HTTPException(status_code=404, detail="Control no encontrado")

    previous_score = ctrl.implementation_score

    # Validation: exclusion justification mandatory if not applicable
    if not is_applicable:
        if not justification_exclusion or not justification_exclusion.strip():
            raise HTTPException(
                status_code=400,
                detail="La justificación de exclusión es obligatoria para controles No aplicables.",
            )
        ctrl.is_applicable = False
        ctrl.implementation_score = -1
        ctrl.implementation_status = "No aplicable"
        ctrl.justification_exclusion = justification_exclusion.strip()
    else:
        ctrl.is_applicable = True
        ctrl.implementation_score = implementation_score
        ctrl.implementation_status = implementation_status
        ctrl.justification_inclusion = (
            justification_inclusion.strip() if justification_inclusion else None
        )
        ctrl.justification_exclusion = None

    ctrl.implementation_summary = (
        implementation_summary.strip() if implementation_summary else None
    )
    ctrl.responsible = responsible.strip() if responsible else None
    ctrl.human_reviewed = True

    # Record Assessment
    assessment = Assessment(
        entity_type="control",
        entity_id=ctrl.id,
        entity_code=ctrl.code,
        previous_score=previous_score,
        new_score=ctrl.implementation_score,
        justification=implementation_summary or "Actualización de evaluación humana de control",
        evaluated_by=responsible or "Auditor",
    )
    db.add(assessment)
    db.commit()

    # Log to audit
    log_audit(
        db=db,
        action="CONTROL_EVALUATION_UPDATED",
        entity_type="CONTROL",
        entity_code=ctrl.code,
        details=f"Evaluación del control {ctrl.code} actualizada. Puntuación: {ctrl.implementation_score}, Estado: {ctrl.implementation_status}.",
        user=responsible or "Auditor",
    )

    return RedirectResponse(url=f"/controls/{code}", status_code=303)
