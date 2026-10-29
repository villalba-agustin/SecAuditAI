import pytest
from pydantic import ValidationError

from app.schemas.ai_analysis import AIAnalysisOutput, RelatedControlItem


def test_valid_ai_analysis_output_parsing():
    # Arrange
    raw_data = {
        "summary": "Documento formal de políticas de acceso y autenticación.",
        "related_clauses": [
            {
                "clause_id": "5.2",
                "reason": "Define compromisos de la dirección.",
                "quote": "La dirección aprueba la política.",
                "suggested_level": 3,
                "confidence": 0.9,
            }
        ],
        "related_controls": [
            {
                "control_id": "A.5.15",
                "reason": "Regula el control de accesos.",
                "quote": "Principio de menor privilegio.",
                "suggested_level": 4,
                "confidence": 0.85,
            }
        ],
        "strengths": ["Documentación formal", "Aprobación de la dirección"],
        "gaps": ["Falta evidencia de pruebas periódicas"],
        "recommended_actions": ["Ejecutar revisión de accesos"],
        "missing_information": ["Registros históricos de revocación"],
    }

    # Act
    parsed = AIAnalysisOutput.model_validate(raw_data)

    # Assert
    assert parsed.summary.startswith("Documento formal")
    assert len(parsed.related_clauses) == 1
    assert parsed.related_clauses[0].suggested_level == 3
    assert len(parsed.related_controls) == 1
    assert parsed.related_controls[0].control_id == "A.5.15"


def test_control_id_normalization():
    # Arrange & Act: prefix 'A.' is automatically ensured if omitted
    item = RelatedControlItem(
        control_id="5.1",
        reason="Mapeo organizacional",
        quote="Cita",
        suggested_level=3,
        confidence=0.8,
    )

    # Assert
    assert item.control_id == "A.5.1"


def test_validation_error_on_invalid_level():
    # Arrange: level 6 is out of range 1-5
    with pytest.raises(ValidationError):
        RelatedControlItem(
            control_id="A.5.1",
            reason="Mapeo",
            quote="Cita",
            suggested_level=6,
            confidence=0.8,
        )


def test_validation_error_on_invalid_confidence():
    # Arrange: confidence 1.5 is out of range 0.0-1.0
    with pytest.raises(ValidationError):
        RelatedControlItem(
            control_id="A.5.1",
            reason="Mapeo",
            quote="Cita",
            suggested_level=3,
            confidence=1.5,
        )
