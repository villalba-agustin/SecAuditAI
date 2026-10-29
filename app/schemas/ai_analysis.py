from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class RelatedClauseItem(BaseModel):
    clause_id: str = Field(..., description="Identificador de la cláusula o subcláusula (ej. '4.1', '5.2', '6.1.2')")
    reason: str = Field(..., description="Fundamento técnico del mapeo")
    quote: Optional[str] = Field(None, description="Fragmento textual del documento que sustenta el hallazgo")
    suggested_level: int = Field(..., ge=1, le=5, description="Nivel de madurez sugerido (1 a 5)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza estimado (0.0 a 1.0)")


class RelatedControlItem(BaseModel):
    control_id: str = Field(..., description="Identificador del control del Anexo A (ej. 'A.5.1', 'A.8.24')")
    reason: str = Field(..., description="Fundamento técnico del mapeo")
    quote: Optional[str] = Field(None, description="Fragmento textual del documento que sustenta el hallazgo")
    suggested_level: int = Field(..., ge=1, le=5, description="Nivel de madurez sugerido (1 a 5)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza estimado (0.0 a 1.0)")

    @field_validator("control_id")
    @classmethod
    def normalize_control_id(cls, v: str) -> str:
        v = v.strip()
        if not v.upper().startswith("A.") and any(v.startswith(prefix) for prefix in ["5.", "6.", "7.", "8."]):
            v = f"A.{v}"
        return v


class AIAnalysisOutput(BaseModel):
    """
    Estructura estricta para la respuesta JSON generada por Ollama
    conforme a la Skill iso27001-evidence-review.
    """
    summary: str = Field(..., description="Resumen ejecutivo del documento analizado")
    related_clauses: List[RelatedClauseItem] = Field(default_factory=list, description="Requisitos normativos relacionados")
    related_controls: List[RelatedControlItem] = Field(default_factory=list, description="Controles del Anexo A relacionados")
    strengths: List[str] = Field(default_factory=list, description="Fortalezas detectadas en la evidencia")
    gaps: List[str] = Field(default_factory=list, description="Brechas u omisiones frente a la norma")
    recommended_actions: List[str] = Field(default_factory=list, description="Acciones de mejora recomendadas")
    missing_information: List[str] = Field(default_factory=list, description="Evidencias faltantes para evaluación definitiva")


class ProposalReviewRequest(BaseModel):
    action: str = Field(..., pattern="^(accept|reject|modify)$", description="Acción: accept, reject o modify")
    modified_score: Optional[int] = Field(None, ge=1, le=5, description="Nuevo nivel si se seleccionó 'modify'")
    reviewer_notes: Optional[str] = Field(None, description="Observaciones o justificación del revisor")
