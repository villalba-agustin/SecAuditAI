from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_analysis import AIProposal
from app.models.assessment import Assessment
from app.models.control import AnnexControl
from app.models.requirement import Requirement
from app.services.audit_service import log_audit

router = APIRouter(prefix="/proposals", tags=["Revisión de Propuestas de IA"])


@router.get("", response_class=HTMLResponse)
def list_proposals_page(
    request: Request,
    status: Optional[str] = "pending",
    target_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(AIProposal)
    if status and status != "all":
        query = query.filter(AIProposal.status == status)
    if target_type:
        query = query.filter(AIProposal.target_type == target_type)

    proposals = query.order_by(AIProposal.created_at.desc()).all()
    templates = request.app.state.templates

    return templates.TemplateResponse(
        request=request,
        name="proposals/list.html",
        context={
            "proposals": proposals,
            "selected_status": status or "all",
            "selected_target_type": target_type or "",
            "active_page": "proposals",
        },
    )


@router.post("/{proposal_id}/review")
def review_proposal(
    proposal_id: int,
    action: str = Form(..., pattern="^(accept|reject|modify)$"),
    modified_score: Optional[int] = Form(None),
    reviewer_notes: Optional[str] = Form(None),
    reviewer_name: str = Form("Auditor"),
    db: Session = Depends(get_db),
):
    proposal = db.query(AIProposal).filter(AIProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")

    now = datetime.now(timezone.utc)
    proposal.reviewed_at = now
    proposal.reviewed_by = reviewer_name
    proposal.reviewer_notes = reviewer_notes

    target_code = ""
    target_entity_type = proposal.target_type

    if proposal.target_type == "requirement":
        req = db.query(Requirement).filter(Requirement.id == proposal.requirement_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Requisito asociado no encontrado")
        target_code = req.code
        prev_score = req.compliance_score

        if action == "accept":
            proposal.status = "accepted"
            req.compliance_score = proposal.suggested_score
            db.add(Assessment(
                entity_type="requirement",
                entity_id=req.id,
                entity_code=req.code,
                previous_score=prev_score,
                new_score=proposal.suggested_score,
                justification=f"Propuesta de IA aceptada (análisis {proposal.analysis_id}). {reviewer_notes or ''}".strip(),
                evaluated_by=reviewer_name,
            ))
        elif action == "modify":
            if modified_score is None:
                raise HTTPException(status_code=400, detail="Debe especificar un nivel para la acción 'modify'")
            proposal.status = "modified"
            req.compliance_score = modified_score
            db.add(Assessment(
                entity_type="requirement",
                entity_id=req.id,
                entity_code=req.code,
                previous_score=prev_score,
                new_score=modified_score,
                justification=f"Propuesta de IA modificada por auditor a nivel {modified_score}. {reviewer_notes or ''}".strip(),
                evaluated_by=reviewer_name,
            ))
        elif action == "reject":
            proposal.status = "rejected"

    elif proposal.target_type == "control":
        ctrl = db.query(AnnexControl).filter(AnnexControl.id == proposal.control_id).first()
        if not ctrl:
            raise HTTPException(status_code=404, detail="Control asociado no encontrado")
        target_code = ctrl.code
        prev_score = ctrl.implementation_score

        if action == "accept":
            proposal.status = "accepted"
            ctrl.implementation_score = proposal.suggested_score
            ctrl.human_reviewed = True
            if ctrl.implementation_status == "No iniciado" and proposal.suggested_score >= 2:
                ctrl.implementation_status = "En progreso" if proposal.suggested_score < 4 else "Implementado"

            db.add(Assessment(
                entity_type="control",
                entity_id=ctrl.id,
                entity_code=ctrl.code,
                previous_score=prev_score,
                new_score=proposal.suggested_score,
                justification=f"Propuesta de IA aceptada (análisis {proposal.analysis_id}). {reviewer_notes or ''}".strip(),
                evaluated_by=reviewer_name,
            ))
        elif action == "modify":
            if modified_score is None:
                raise HTTPException(status_code=400, detail="Debe especificar un nivel para la acción 'modify'")
            proposal.status = "modified"
            ctrl.implementation_score = modified_score
            ctrl.human_reviewed = True
            db.add(Assessment(
                entity_type="control",
                entity_id=ctrl.id,
                entity_code=ctrl.code,
                previous_score=prev_score,
                new_score=modified_score,
                justification=f"Propuesta de IA modificada por auditor a nivel {modified_score}. {reviewer_notes or ''}".strip(),
                evaluated_by=reviewer_name,
            ))
        elif action == "reject":
            proposal.status = "rejected"

    db.commit()

    log_audit(
        db=db,
        action=f"PROPOSAL_{action.upper()}",
        entity_type=target_entity_type.upper(),
        entity_code=target_code,
        details=f"Propuesta #{proposal.id} para {target_code} marcada como '{proposal.status}'. {reviewer_notes or ''}".strip(),
        user=reviewer_name,
    )

    return RedirectResponse(url="/proposals", status_code=303)
