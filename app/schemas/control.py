from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ControlBase(BaseModel):
    code: str
    category: str
    title: str
    description: str
    is_applicable: bool
    justification_inclusion: Optional[str] = None
    justification_exclusion: Optional[str] = None
    implementation_status: str
    implementation_score: int
    implementation_summary: Optional[str] = None
    responsible: Optional[str] = None
    human_reviewed: bool


class ControlUpdate(BaseModel):
    is_applicable: bool = Field(True, description="Indica si el control es aplicable en el SGSI")
    justification_inclusion: Optional[str] = Field(None, description="Justificación técnica de inclusión en SoA")
    justification_exclusion: Optional[str] = Field(None, description="Justificación obligatoria si el control es excluido")
    implementation_status: str = Field("No iniciado", description="Estado de implementación")
    implementation_score: int = Field(0, ge=-1, le=5, description="Nivel de madurez interna 0 a 5 o -1")
    implementation_summary: Optional[str] = Field(None, description="Resumen de cómo se implementa")
    responsible: Optional[str] = Field(None, description="Responsable del control")


class ControlResponse(ControlBase):
    id: int
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
