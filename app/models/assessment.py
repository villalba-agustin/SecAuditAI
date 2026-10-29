from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.session import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(32), nullable=False, index=True)  # requirement or control
    entity_id = Column(Integer, nullable=False, index=True)
    entity_code = Column(String(32), nullable=False)
    previous_score = Column(Integer, nullable=False)
    new_score = Column(Integer, nullable=False)
    justification = Column(Text, nullable=False)
    evaluated_by = Column(String(128), default="Auditor", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
