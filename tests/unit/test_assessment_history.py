from app.models.assessment import Assessment
from app.models.audit import AuditLog
from app.models.requirement import Requirement
from app.services.audit_service import log_audit


def test_assessment_history_preservation_on_score_update(db_session):
    # Arrange: Requirement starts at score 0
    req = db_session.query(Requirement).filter(Requirement.code == "5.2").first()
    assert req.compliance_score == 0

    # Act 1: Initial evaluation to Level 2
    assessment1 = Assessment(
        entity_type="requirement",
        entity_id=req.id,
        entity_code=req.code,
        previous_score=0,
        new_score=2,
        justification="Evaluación preliminar inicial",
        evaluated_by="Auditor Junior",
    )
    req.compliance_score = 2
    db_session.add(assessment1)
    db_session.commit()

    # Act 2: Subsequent evaluation to Level 4 with evidence
    assessment2 = Assessment(
        entity_type="requirement",
        entity_id=req.id,
        entity_code=req.code,
        previous_score=2,
        new_score=4,
        justification="Evidencia aprobada por comité",
        evaluated_by="Auditor Senior",
    )
    req.compliance_score = 4
    db_session.add(assessment2)
    db_session.commit()

    # Assert: Current score is 4, but both assessments are preserved in history
    updated_req = db_session.query(Requirement).filter(Requirement.code == "5.2").first()
    assert updated_req.compliance_score == 4

    history = (
        db_session.query(Assessment)
        .filter(Assessment.entity_type == "requirement", Assessment.entity_id == req.id)
        .order_by(Assessment.created_at.asc())
        .all()
    )
    assert len(history) == 2
    assert history[0].previous_score == 0
    assert history[0].new_score == 2
    assert history[0].evaluated_by == "Auditor Junior"
    assert history[1].previous_score == 2
    assert history[1].new_score == 4
    assert history[1].evaluated_by == "Auditor Senior"


def test_audit_log_traceability(db_session):
    # Arrange & Act
    entry = log_audit(
        db=db_session,
        action="TEST_ACTION",
        entity_type="TEST_ENTITY",
        entity_code="TEST-001",
        details="Acción de prueba de auditoría",
        user="Auditor Test",
    )

    # Assert
    saved = db_session.query(AuditLog).filter(AuditLog.id == entry.id).first()
    assert saved is not None
    assert saved.action == "TEST_ACTION"
    assert saved.user_identifier == "Auditor Test"
    assert "Acción de prueba" in saved.details
