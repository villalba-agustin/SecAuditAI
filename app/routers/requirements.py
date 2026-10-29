from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_analysis import AIProposal
from app.models.assessment import Assessment
from app.models.audit import AuditLog
from app.models.evidence import EvidenceMapping
from app.models.requirement import Requirement
from app.services.audit_service import log_audit

router = APIRouter(prefix="/requirements", tags=["Requisitos"])


@router.get("", response_class=HTMLResponse)
def list_requirements_page(
    request: Request,
    clause: Optional[int] = None,
    score: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Requirement)

    if clause is not None:
        query = query.filter(Requirement.clause_number == clause)
    if score is not None:
        query = query.filter(Requirement.compliance_score == score)
    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(
            (Requirement.code.ilike(search_fmt))
            | (Requirement.title.ilike(search_fmt))
            | (Requirement.description.ilike(search_fmt))
        )

    # Sort numerically by clause and subclause
    def sort_key(r: Requirement):
        parts = r.code.split(".")
        return [int(p) if p.isdigit() else p for p in parts]

    reqs = sorted(query.all(), key=sort_key)
    templates = request.app.state.templates

    return templates.TemplateResponse(
        request=request,
        name="requirements/list.html",
        context={
            "requirements": reqs,
            "active_page": "requirements",
            "selected_clause": clause,
            "selected_score": score,
            "search_query": search or "",
        },
    )


@router.get("/{code}", response_class=HTMLResponse)
def requirement_detail_page(code: str, request: Request, db: Session = Depends(get_db)):
    req = db.query(Requirement).filter(Requirement.code == code).first()
    if not req:
        raise HTTPException(status_code=404, detail="Requisito no encontrado")

    # Mapped evidences
    mappings = (
        db.query(EvidenceMapping)
        .filter(EvidenceMapping.requirement_id == req.id)
        .all()
    )

    # AI proposals
    proposals = (
        db.query(AIProposal)
        .filter(AIProposal.requirement_id == req.id)
        .order_by(AIProposal.created_at.desc())
        .all()
    )

    # Assessment history
    assessments = (
        db.query(Assessment)
        .filter(Assessment.entity_type == "requirement", Assessment.entity_id == req.id)
        .order_by(Assessment.created_at.desc())
        .all()
    )

    # Audit history
    audit_logs = (
        db.query(AuditLog)
        .filter(AuditLog.entity_code == req.code)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )

    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request,
        name="requirements/detail.html",
        context={
            "req": req,
            "mappings": mappings,
            "proposals": proposals,
            "assessments": assessments,
            "audit_logs": audit_logs,
            "active_page": "requirements",
        },
    )


@router.post("/{code}/evaluate")
def evaluate_requirement(
    code: str,
    compliance_score: int = Form(...),
    is_applicable: bool = Form(True),
    na_justification: Optional[str] = Form(None),
    observations: Optional[str] = Form(None),
    responsible: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    req = db.query(Requirement).filter(Requirement.code == code).first()
    if not req:
        raise HTTPException(status_code=404, detail="Requisito no encontrado")

    previous_score = req.compliance_score

    # Validation: if not applicable, justification is required
    if not is_applicable:
        if not na_justification or not na_justification.strip():
            raise HTTPException(
                status_code=400,
                detail="La justificación es obligatoria para requisitos declarados como No aplicables.",
            )
        req.compliance_score = -1
        req.is_applicable = False
        req.na_justification = na_justification.strip()
    else:
        req.is_applicable = True
        req.compliance_score = compliance_score
        req.na_justification = None

    req.observations = observations.strip() if observations else None
    req.responsible = responsible.strip() if responsible else None

    # Record Assessment
    assessment = Assessment(
        entity_type="requirement",
        entity_id=req.id,
        entity_code=req.code,
        previous_score=previous_score,
        new_score=req.compliance_score,
        justification=observations or "Actualización de evaluación humana",
        evaluated_by=responsible or "Auditor",
    )
    db.add(assessment)
    db.commit()

    # Log to audit
    log_audit(
        db=db,
        action="REQUIREMENT_EVALUATION_UPDATED",
        entity_type="REQUIREMENT",
        entity_code=req.code,
        details=f"Evaluación del requisito {req.code} modificada de nivel {previous_score} a {req.compliance_score}.",
        user=responsible or "Auditor",
    )

    return RedirectResponse(url=f"/requirements/{code}", status_code=303)
