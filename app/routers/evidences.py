from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_analysis import AIAnalysis
from app.models.control import AnnexControl
from app.models.evidence import Evidence, EvidenceMapping
from app.models.requirement import Requirement
from app.services.document_service import process_and_save_evidence
from app.services.ollama_service import analyze_evidence_with_ollama

router = APIRouter(prefix="/evidences", tags=["Evidencias"])


@router.get("", response_class=HTMLResponse)
def list_evidences_page(request: Request, db: Session = Depends(get_db)):
    evidences = db.query(Evidence).order_by(Evidence.created_at.desc()).all()
    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request,
        name="evidences/list.html",
        context={"evidences": evidences, "active_page": "evidences"},
    )


@router.get("/upload", response_class=HTMLResponse)
def upload_evidence_page(
    request: Request,
    target_req: Optional[str] = None,
    target_ctrl: Optional[str] = None,
    db: Session = Depends(get_db),
):
    requirements = db.query(Requirement).order_by(Requirement.code).all()
    controls = db.query(AnnexControl).order_by(AnnexControl.code).all()
    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request,
        name="evidences/upload.html",
        context={
            "requirements": requirements,
            "controls": controls,
            "target_req": target_req or "",
            "target_ctrl": target_ctrl or "",
            "active_page": "evidences",
        },
    )


@router.post("/upload")
async def upload_evidence(
    file: UploadFile = File(...),
    target_req_code: Optional[str] = Form(None),
    target_ctrl_code: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    auto_analyze: bool = Form(False),
    db: Session = Depends(get_db),
):
    content = await file.read()
    try:
        evidence = process_and_save_evidence(
            filename=file.filename or "evidence.bin",
            content=content,
            mime_type=file.content_type or "application/octet-stream",
            db=db,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Link manually if user selected a target requirement
    if target_req_code:
        req = db.query(Requirement).filter(Requirement.code == target_req_code).first()
        if req:
            mapping = EvidenceMapping(
                evidence_id=evidence.id,
                requirement_id=req.id,
                mapped_by="human",
                reason=notes or f"Vinculación manual con requisito {req.code}",
            )
            db.add(mapping)

    # Link manually if user selected a target control
    if target_ctrl_code:
        ctrl = db.query(AnnexControl).filter(AnnexControl.code == target_ctrl_code).first()
        if ctrl:
            mapping = EvidenceMapping(
                evidence_id=evidence.id,
                control_id=ctrl.id,
                mapped_by="human",
                reason=notes or f"Vinculación manual con control {ctrl.code}",
            )
            db.add(mapping)

    db.commit()

    if auto_analyze and evidence.has_extractable_text:
        try:
            analyze_evidence_with_ollama(
                evidence=evidence,
                db=db,
                target_control_code=target_ctrl_code,
                target_requirement_code=target_req_code,
            )
        except Exception:
            pass  # Analysis failure shouldn't abort upload

    return RedirectResponse(url=f"/evidences/{evidence.id}", status_code=303)


@router.get("/{evidence_id}", response_class=HTMLResponse)
def evidence_detail_page(evidence_id: int, request: Request, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")

    mappings = (
        db.query(EvidenceMapping)
        .filter(EvidenceMapping.evidence_id == evidence.id)
        .all()
    )

    analyses = (
        db.query(AIAnalysis)
        .filter(AIAnalysis.evidence_id == evidence.id)
        .order_by(AIAnalysis.created_at.desc())
        .all()
    )

    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request,
        name="evidences/detail.html",
        context={
            "evidence": evidence,
            "mappings": mappings,
            "analyses": analyses,
            "active_page": "evidences",
        },
    )


@router.post("/{evidence_id}/analyze")
def trigger_analysis(
    evidence_id: int,
    force_mock: bool = Form(False),
    db: Session = Depends(get_db),
):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")

    try:
        analyze_evidence_with_ollama(
            evidence=evidence,
            db=db,
            force_mock=force_mock,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis IA: {str(e)}")

    return RedirectResponse(url=f"/evidences/{evidence_id}", status_code=303)


@router.get("/{evidence_id}/download")
def download_evidence(evidence_id: int, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")

    file_path = Path(evidence.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo físico no encontrado en el servidor")

    return FileResponse(
        path=file_path,
        filename=evidence.original_filename,
        media_type=evidence.mime_type,
    )
