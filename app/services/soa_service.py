import csv
import io
from datetime import datetime
from typing import List, Tuple

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from sqlalchemy.orm import Session

from app.models.ai_analysis import AIProposal
from app.models.control import AnnexControl


def get_soa_data(db: Session) -> List[Tuple[AnnexControl, str]]:
    """
    Fetches all Annex A controls sorted by code, along with pending AI proposal summary.
    """
    controls = db.query(AnnexControl).all()

    # Sort numerically by category and control number
    def sort_key(c: AnnexControl):
        parts = c.code.replace("A.", "").split(".")
        return [int(p) if p.isdigit() else p for p in parts]

    sorted_controls = sorted(controls, key=sort_key)

    result = []
    for ctrl in sorted_controls:
        # Check pending AI proposal
        pending_proposal = (
            db.query(AIProposal)
            .filter(AIProposal.control_id == ctrl.id, AIProposal.status == "pending")
            .first()
        )
        ai_info = (
            f"Sugerido: Nivel {pending_proposal.suggested_score} ({int(pending_proposal.confidence * 100)}% conf.)"
            if pending_proposal
            else "Sin propuestas pendientes"
        )
        result.append((ctrl, ai_info))

    return result


def export_soa_xlsx(db: Session) -> bytes:
    """
    Generates a professionally formatted Excel spreadsheet of the Statement of Applicability.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Declaración de Aplicabilidad"

    # Ensure grid lines are visible
    ws.views.sheetView[0].showGridLines = True

    # Palette
    NAVY_FILL = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    HEADER_FILL = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    WHITE_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    TITLE_FONT = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    SUBTITLE_FONT = Font(name="Calibri", size=10, italic=True, color="E2E8F0")
    REGULAR_FONT = Font(name="Calibri", size=10)

    thin_border_side = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(
        top=thin_border_side,
        bottom=thin_border_side,
        left=thin_border_side,
        right=thin_border_side,
    )

    # Title block
    ws.merge_cells("A1:N1")
    title_cell = ws["A1"]
    title_cell.value = "DECLARACIÓN DE APLICABILIDAD (SoA) - ISO/IEC 27001:2022"
    title_cell.font = TITLE_FONT
    title_cell.fill = NAVY_FILL
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 35

    ws.merge_cells("A2:N2")
    sub_cell = ws["A2"]
    sub_cell.value = f"Generado automáticamente por SecAuditAI el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Total: 93 Controles Anexo A"
    sub_cell.font = SUBTITLE_FONT
    sub_cell.fill = NAVY_FILL
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 20

    # Headers
    headers = [
        "Código",
        "Categoría",
        "Título del Control",
        "Descripción Breve",
        "¿Aplicable?",
        "Justificación de Inclusión",
        "Justificación de Exclusión",
        "Estado de Implementación",
        "Nivel de Madurez",
        "Resumen de Implementación",
        "Revisión Humana",
        "Responsable",
        "Propuestas IA",
        "Última Revisión",
    ]

    ws.append([])  # Blank row 3
    ws.row_dimensions[3].height = 10

    ws.append(headers)
    ws.row_dimensions[4].height = 28

    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=4, column=col_idx)
        cell.font = WHITE_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = cell_border

    # Data rows
    data = get_soa_data(db)
    current_row = 5

    for ctrl, ai_info in data:
        is_app_str = "Sí" if ctrl.is_applicable else "No"
        human_rev_str = "Confirmado" if ctrl.human_reviewed else "Pendiente"
        rev_date_str = ctrl.updated_at.strftime("%d/%m/%Y") if ctrl.updated_at else "-"

        row_values = [
            ctrl.code,
            ctrl.category,
            ctrl.title,
            ctrl.description,
            is_app_str,
            ctrl.justification_inclusion or "-",
            ctrl.justification_exclusion or "-",
            ctrl.implementation_status,
            f"{ctrl.implementation_score} - {ctrl.score_label()}",
            ctrl.implementation_summary or "-",
            human_rev_str,
            ctrl.responsible or "No asignado",
            ai_info,
            rev_date_str,
        ]
        ws.append(row_values)
        ws.row_dimensions[current_row].height = 22

        fill_to_use = ZEBRA_FILL if current_row % 2 == 0 else PatternFill(fill_type=None)

        for col_idx in range(1, len(row_values) + 1):
            cell = ws.cell(row=current_row, column=col_idx)
            cell.font = REGULAR_FONT
            cell.border = cell_border
            if fill_to_use.fill_type:
                cell.fill = fill_to_use

            # Centering for short codes and states
            if col_idx in [1, 2, 5, 8, 9, 11, 14]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

        current_row += 1

    # Column widths
    col_widths = {
        1: 12,   # Código
        2: 16,   # Categoría
        3: 32,   # Título
        4: 45,   # Descripción
        5: 14,   # Aplicable
        6: 30,   # Just. Inclusión
        7: 30,   # Just. Exclusión
        8: 22,   # Estado
        9: 24,   # Nivel
        10: 35,  # Resumen
        11: 18,  # Revisión Humana
        12: 20,  # Responsable
        13: 28,  # Propuestas IA
        14: 16,  # Última revisión
    }

    for col_idx, width in col_widths.items():
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width

    # Save to buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def export_soa_csv(db: Session) -> str:
    """
    Generates a CSV text string of the Statement of Applicability with UTF-8 encoding.
    """
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)

    headers = [
        "Identificador",
        "Categoría",
        "Título del Control",
        "Descripción",
        "Es Aplicable",
        "Justificación de Inclusión",
        "Justificación de Exclusión",
        "Estado de Implementación",
        "Nivel de Madurez (0-5)",
        "Etiqueta de Madurez",
        "Resumen de Implementación",
        "Revisión Humana Confirmada",
        "Responsable",
        "Propuestas IA Pendientes",
        "Fecha de Actualización",
    ]
    writer.writerow(headers)

    data = get_soa_data(db)
    for ctrl, ai_info in data:
        writer.writerow([
            ctrl.code,
            ctrl.category,
            ctrl.title,
            ctrl.description,
            "SÍ" if ctrl.is_applicable else "NO",
            ctrl.justification_inclusion or "",
            ctrl.justification_exclusion or "",
            ctrl.implementation_status,
            ctrl.implementation_score,
            ctrl.score_label(),
            ctrl.implementation_summary or "",
            "SÍ" if ctrl.human_reviewed else "NO",
            ctrl.responsible or "",
            ai_info,
            ctrl.updated_at.strftime("%Y-%m-%d %H:%M:%S") if ctrl.updated_at else "",
        ])

    return output.getvalue()
