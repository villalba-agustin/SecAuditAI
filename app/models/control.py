from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class AnnexControl(Base):
    __tablename__ = "annex_controls"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, nullable=False, index=True)
    category = Column(String(64), nullable=False, index=True)  # Organizacional, Personas, Físico, Tecnológico
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    normative_ref = Column(String(128), default="ISO/IEC 27001:2022 Anexo A", nullable=False)

    # Statement of Applicability (SoA)
    is_applicable = Column(Boolean, default=True, nullable=False)
    justification_inclusion = Column(Text, nullable=True)
    justification_exclusion = Column(Text, nullable=True)

    # Implementation
    implementation_status = Column(String(64), default="No iniciado", nullable=False)
    implementation_score = Column(Integer, default=0, nullable=False)  # 0 to 5, or -1 for NA
    implementation_summary = Column(Text, nullable=True)
    responsible = Column(String(128), nullable=True)
    review_date = Column(DateTime, nullable=True)
    human_reviewed = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    mappings = relationship("EvidenceMapping", back_populates="control", cascade="all, delete-orphan")
    proposals = relationship("AIProposal", back_populates="control", cascade="all, delete-orphan")

    def score_label(self) -> str:
        if not self.is_applicable or self.implementation_score == -1:
            return "No aplicable"
        labels = {
            0: "No evaluado",
            1: "No implementado",
            2: "Inicial",
            3: "Parcialmente implementado",
            4: "Mayormente implementado",
            5: "Implementado",
        }
        return labels.get(self.implementation_score, "Desconocido")
