from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequirementBase(BaseModel):
    code: str
    clause_number: int
    title: str
    description: str
    normative_ref: str
    compliance_score: int
    is_applicable: bool
    na_justification: Optional[str] = None
    observations: Optional[str] = None
    responsible: Optional[str] = None


class RequirementUpdate(BaseModel):
    compliance_score: int = Field(..., ge=-1, le=5, description="-1 para No aplicable, 0 a 5 para la escala interna")
    is_applicable: bool = Field(True, description="Indica si el requisito es aplicable")
    na_justification: Optional[str] = Field(None, description="Justificación obligatoria si es No aplicable")
    observations: Optional[str] = Field(None, description="Observaciones y comentarios del auditor")
    responsible: Optional[str] = Field(None, description="Responsable asignado")


class RequirementResponse(RequirementBase):
    id: int
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
