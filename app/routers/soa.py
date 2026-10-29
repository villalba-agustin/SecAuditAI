from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.control import AnnexControl
from app.services.audit_service import log_audit
from app.services.soa_service import export_soa_csv, export_soa_xlsx, get_soa_data

router = APIRouter(prefix="/soa", tags=["Declaración de Aplicabilidad (SoA)"])


@router.get("", response_class=HTMLResponse)
def get_soa_page(
    request: Request,
    category: Optional[str] = None,
    applicable: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    data = get_soa_data(db)

    # Filter in memory
    filtered = []
    for ctrl, ai_info in data:
        if category and ctrl.category != category:
            continue
        if applicable == "true" and not ctrl.is_applicable:
            continue
        if applicable == "false" and ctrl.is_applicable:
            continue
        if search:
            s = search.lower()
            if s not in ctrl.code.lower() and s not in ctrl.title.lower() and s not in ctrl.description.lower():
                continue
        filtered.append((ctrl, ai_info))

    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request,
        name="soa/list.html",
        context={
            "items": filtered,
            "total_items": len(data),
            "filtered_count": len(filtered),
            "selected_category": category or "",
            "selected_applicable": applicable or "",
            "search_query": search or "",
            "active_page": "soa",
        },
    )


@router.get("/export/xlsx")
def export_xlsx(db: Session = Depends(get_db)):
    xlsx_bytes = export_soa_xlsx(db)
    filename = "Declaracion_de_Aplicabilidad_ISO27001_SecAuditAI.xlsx"
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    csv_text = export_soa_csv(db)
    # Add BOM for Excel UTF-8 compatibility
    csv_bytes = "\ufeff".encode("utf-8") + csv_text.encode("utf-8")
    filename = "Declaracion_de_Aplicabilidad_ISO27001_SecAuditAI.csv"
    return Response(
        content=csv_bytes,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/{code}/quick-update")
def quick_update_soa(
    code: str,
    is_applicable: bool = Form(...),
    justification_inclusion: Optional[str] = Form(None),
    justification_exclusion: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    ctrl = db.query(AnnexControl).filter(AnnexControl.code == code).first()
    if not ctrl:
        raise HTTPException(status_code=404, detail="Control no encontrado")

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
        if ctrl.implementation_score == -1:
            ctrl.implementation_score = 0
            ctrl.implementation_status = "No iniciado"
        ctrl.justification_inclusion = justification_inclusion.strip() if justification_inclusion else None
        ctrl.justification_exclusion = None

    ctrl.human_reviewed = True
    db.commit()

    log_audit(
        db=db,
        action="SOA_DECISION_UPDATED",
        entity_type="CONTROL",
        entity_code=ctrl.code,
        details=f"Decisión de aplicabilidad de {ctrl.code} actualizada a: {'Aplicable' if ctrl.is_applicable else 'Excluido'}.",
        user="Auditor",
    )

    return RedirectResponse(url="/soa", status_code=303)
