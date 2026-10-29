from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.session import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(64), nullable=False, index=True)
    entity_type = Column(String(32), nullable=False)
    entity_code = Column(String(32), nullable=True)
    details = Column(Text, nullable=False)
    user_identifier = Column(String(128), default="Auditor", nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
