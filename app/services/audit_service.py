from sqlalchemy.orm import Session

from app.models.audit import AuditLog


def log_audit(
    db: Session,
    action: str,
    entity_type: str,
    entity_code: str | None,
    details: str,
    user: str = "Auditor",
) -> AuditLog:
    """Records an audit log entry for traceability."""
    audit_entry = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_code=entity_code,
        details=details,
        user_identifier=user,
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    return audit_entry
