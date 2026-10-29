import json
from datetime import datetime, timezone
from typing import List

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(Integer, ForeignKey("evidences.id", ondelete="CASCADE"), nullable=False, index=True)
    model_name = Column(String(64), nullable=False)
    raw_prompt = Column(Text, nullable=True)
    raw_response = Column(Text, nullable=True)
    summary = Column(Text, nullable=False)
    strengths_json = Column(Text, default="[]", nullable=False)
    gaps_json = Column(Text, default="[]", nullable=False)
    recommendations_json = Column(Text, default="[]", nullable=False)
    missing_info_json = Column(Text, default="[]", nullable=False)
    status = Column(String(32), default="completado", nullable=False)  # completado, error, simulado
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    evidence = relationship("Evidence", back_populates="analyses")
    proposals = relationship("AIProposal", back_populates="analysis", cascade="all, delete-orphan")

    def get_strengths(self) -> List[str]:
        try:
            return json.loads(self.strengths_json)
        except Exception:
            return []

    def get_gaps(self) -> List[str]:
        try:
            return json.loads(self.gaps_json)
        except Exception:
            return []

    def get_recommendations(self) -> List[str]:
        try:
            return json.loads(self.recommendations_json)
        except Exception:
            return []

    def get_missing_info(self) -> List[str]:
        try:
            return json.loads(self.missing_info_json)
        except Exception:
            return []


class AIProposal(Base):
    __tablename__ = "ai_proposals"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("ai_analyses.id", ondelete="CASCADE"), nullable=False, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id", ondelete="CASCADE"), nullable=True, index=True)
    control_id = Column(Integer, ForeignKey("annex_controls.id", ondelete="CASCADE"), nullable=True, index=True)
    target_type = Column(String(32), nullable=False)  # "requirement" or "control"
    suggested_score = Column(Integer, nullable=False)  # 1 to 5
    confidence = Column(Float, default=0.8, nullable=False)  # 0.0 to 1.0
    rationale = Column(Text, nullable=False)
    quote = Column(Text, nullable=True)
    status = Column(String(32), default="pending", nullable=False)  # pending, accepted, rejected, modified
    reviewer_notes = Column(Text, nullable=True)
    reviewed_by = Column(String(128), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    analysis = relationship("AIAnalysis", back_populates="proposals")
    requirement = relationship("Requirement", back_populates="proposals")
    control = relationship("AnnexControl", back_populates="proposals")
