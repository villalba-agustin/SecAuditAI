import io
from pathlib import Path
from typing import Tuple

import docx
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    compute_sha256,
    generate_secure_stored_filename,
    is_path_safe,
    validate_file_security,
)
from app.models.evidence import Evidence
from app.services.audit_service import log_audit


def extract_text_from_pdf(content: bytes) -> Tuple[str, bool, str]:
    """
    Extracts text from PDF bytes using pypdf.
    Returns (extracted_text, has_text, notes).
    """
    try:
        reader = PdfReader(io.BytesIO(content))
        text_parts = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(f"--- Página {i+1} ---\n{page_text.strip()}")

        extracted = "\n\n".join(text_parts).strip()
        if not extracted:
            return (
                "",
                False,
                "El archivo PDF fue procesado correctamente pero no contiene capas de texto digital extraíble (documento escaneado o solo imágenes).",
            )
        return extracted, True, f"Texto extraído con éxito ({len(reader.pages)} páginas)."
    except Exception as e:
        return "", False, f"Error durante la extracción de texto del PDF: {str(e)}"


def extract_text_from_docx(content: bytes) -> Tuple[str, bool, str]:
    """
    Extracts text from DOCX bytes using python-docx.
    Returns (extracted_text, has_text, notes).
    """
    try:
        doc = docx.Document(io.BytesIO(content))
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        # Also extract table text if present
        table_texts = []
        for table in doc.tables:
            for row in table.rows:
                row_str = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_str:
                    table_texts.append(row_str)

        all_text = []
        if paragraphs:
            all_text.extend(paragraphs)
        if table_texts:
            all_text.append("\n[Tablas en documento]:\n" + "\n".join(table_texts))

        extracted = "\n\n".join(all_text).strip()
        if not extracted:
            return "", False, "El archivo DOCX no contiene texto ni párrafos legibles."
        return extracted, True, f"Texto extraído con éxito ({len(paragraphs)} párrafos)."
    except Exception as e:
        return "", False, f"Error durante la extracción de texto del DOCX: {str(e)}"


def extract_text_from_plain_text(content: bytes) -> Tuple[str, bool, str]:
    """Extracts text from TXT or Markdown bytes."""
    try:
        text = content.decode("utf-8")
        return text.strip(), True, "Texto plano decodificado en UTF-8 con éxito."
    except UnicodeDecodeError:
        try:
            text = content.decode("latin-1")
            return text.strip(), True, "Texto plano decodificado en Latin-1 con éxito."
        except Exception as e:
            return "", False, f"Error decodificando texto: {str(e)}"


def process_and_save_evidence(
    filename: str,
    content: bytes,
    mime_type: str,
    db: Session,
    user: str = "Auditor",
) -> Evidence:
    """
    Validates, saves to disk safely, extracts text, and creates DB record.
    Raises ValueError on validation failure.
    """
    # 1. AppSec Validation
    is_valid, reason = validate_file_security(
        filename=filename,
        content=content,
        content_type=mime_type,
        max_size_bytes=settings.max_upload_size_bytes,
    )
    if not is_valid:
        raise ValueError(reason)

    # 2. Secure stored filename & path traversal check
    stored_name, ext = generate_secure_stored_filename(filename)
    upload_dir = settings.resolved_upload_dir
    target_path = upload_dir / stored_name

    if not is_path_safe(upload_dir, target_path):
        raise ValueError("Violación de seguridad de ruta detectada (Path Traversal attempt).")

    # 3. Write file bytes to disk
    with open(target_path, "wb") as f:
        f.write(content)

    # 4. Compute Hash
    sha256 = compute_sha256(content)

    # 5. Extract text based on extension
    if ext == ".pdf":
        extracted_text, has_text, notes = extract_text_from_pdf(content)
    elif ext == ".docx":
        extracted_text, has_text, notes = extract_text_from_docx(content)
    elif ext in {".txt", ".md"}:
        extracted_text, has_text, notes = extract_text_from_plain_text(content)
    else:
        extracted_text, has_text, notes = "", False, f"Formato {ext} no procesable para texto."

    # 6. Create Evidence Record
    evidence = Evidence(
        original_filename=Path(filename).name,
        stored_filename=stored_name,
        file_path=str(target_path),
        file_size=len(content),
        mime_type=mime_type or "application/octet-stream",
        sha256_hash=sha256,
        extracted_text=extracted_text,
        has_extractable_text=has_text,
        extraction_notes=notes,
        status="cargada",
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    # 7. Audit log
    log_audit(
        db=db,
        action="EVIDENCE_UPLOADED",
        entity_type="EVIDENCE",
        entity_code=f"EVID-{evidence.id}",
        details=f"Carga de evidencia '{evidence.original_filename}' (SHA-256: {sha256[:12]}..., {len(content)} bytes).",
        user=user,
    )

    return evidence
