from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, nullable=False, index=True)
    clause_number = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    normative_ref = Column(String(128), nullable=False, default="ISO/IEC 27001:2022")

    # Internal Scale: 0 (No evaluado), 1 (No implementado), 2 (Inicial), 3 (Parcial),
    # 4 (Mayormente), 5 (Implementado), -1 (No aplicable)
    compliance_score = Column(Integer, default=0, nullable=False)
    is_applicable = Column(Boolean, default=True, nullable=False)
    na_justification = Column(Text, nullable=True)
    observations = Column(Text, nullable=True)
    responsible = Column(String(128), nullable=True)
    review_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    mappings = relationship("EvidenceMapping", back_populates="requirement", cascade="all, delete-orphan")
    proposals = relationship("AIProposal", back_populates="requirement", cascade="all, delete-orphan")

    def score_label(self) -> str:
        if not self.is_applicable or self.compliance_score == -1:
            return "No aplicable"
        labels = {
            0: "No evaluado",
            1: "No implementado",
            2: "Inicial",
            3: "Parcialmente implementado",
            4: "Mayormente implementado",
            5: "Implementado",
        }
        return labels.get(self.compliance_score, "Desconocido")
