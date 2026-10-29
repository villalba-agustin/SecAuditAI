from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), unique=True, nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(128), nullable=False)
    sha256_hash = Column(String(64), index=True, nullable=False)
    extracted_text = Column(Text, nullable=True)
    has_extractable_text = Column(Boolean, default=True, nullable=False)
    extraction_notes = Column(Text, nullable=True)
    status = Column(String(32), default="cargada", nullable=False)  # cargada, analizada, error
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    mappings = relationship("EvidenceMapping", back_populates="evidence", cascade="all, delete-orphan")
    analyses = relationship("AIAnalysis", back_populates="evidence", cascade="all, delete-orphan")


class EvidenceMapping(Base):
    __tablename__ = "evidence_mappings"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(Integer, ForeignKey("evidences.id", ondelete="CASCADE"), nullable=False, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id", ondelete="SET NULL"), nullable=True, index=True)
    control_id = Column(Integer, ForeignKey("annex_controls.id", ondelete="SET NULL"), nullable=True, index=True)
    mapped_by = Column(String(32), default="human", nullable=False)  # human, ai
    reason = Column(Text, nullable=True)
    quote = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    evidence = relationship("Evidence", back_populates="mappings")
    requirement = relationship("Requirement", back_populates="mappings")
    control = relationship("AnnexControl", back_populates="mappings")
