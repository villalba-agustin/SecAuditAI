from app.models.ai_analysis import AIAnalysis, AIProposal
from app.models.control import AnnexControl
from app.models.evidence import Evidence


def test_proposal_accept_workflow(client, db_session):
    # Arrange: Control at score 0, evidence and AIProposal with suggested_score = 4
    ctrl = db_session.query(AnnexControl).filter(AnnexControl.code == "A.5.1").first()
    ctrl.implementation_score = 0
    ctrl.human_reviewed = False

    evidence = Evidence(
        original_filename="doc.txt",
        stored_filename="uuid_doc.txt",
        file_path="/tmp/doc.txt",
        file_size=100,
        mime_type="text/plain",
        sha256_hash="dummyhash",
        extracted_text="Texto",
        status="analizada",
    )
    db_session.add(evidence)
    db_session.commit()

    analysis = AIAnalysis(
        evidence_id=evidence.id,
        model_name="test-model",
        summary="Resumen de prueba",
    )
    db_session.add(analysis)
    db_session.commit()

    proposal = AIProposal(
        analysis_id=analysis.id,
        control_id=ctrl.id,
        target_type="control",
        suggested_score=4,
        confidence=0.9,
        rationale="Políticas estructuradas detectadas",
        status="pending",
    )
    db_session.add(proposal)
    db_session.commit()

    # Act: Accept proposal
    resp = client.post(
        f"/proposals/{proposal.id}/review",
        data={
            "action": "accept",
            "reviewer_name": "Auditor Principal",
            "reviewer_notes": "Conforme con la propuesta",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    # Assert: Proposal is accepted and control score is updated to 4
    updated_prop = db_session.query(AIProposal).filter(AIProposal.id == proposal.id).first()
    assert updated_prop.status == "accepted"

    updated_ctrl = db_session.query(AnnexControl).filter(AnnexControl.id == ctrl.id).first()
    assert updated_ctrl.implementation_score == 4
    assert updated_ctrl.human_reviewed is True


def test_proposal_reject_workflow(client, db_session):
    # Arrange: Control at score 2, proposal suggests 5
    ctrl = db_session.query(AnnexControl).filter(AnnexControl.code == "A.6.1").first()
    ctrl.implementation_score = 2

    evidence = Evidence(
        original_filename="doc2.txt",
        stored_filename="uuid_doc2.txt",
        file_path="/tmp/doc2.txt",
        file_size=100,
        mime_type="text/plain",
        sha256_hash="dummyhash2",
        status="analizada",
    )
    db_session.add(evidence)
    db_session.commit()

    analysis = AIAnalysis(evidence_id=evidence.id, model_name="test-model", summary="Resumen")
    db_session.add(analysis)
    db_session.commit()

    proposal = AIProposal(
        analysis_id=analysis.id,
        control_id=ctrl.id,
        target_type="control",
        suggested_score=5,
        confidence=0.7,
        rationale="Sugerencia",
        status="pending",
    )
    db_session.add(proposal)
    db_session.commit()

    # Act: Reject proposal
    resp = client.post(
        f"/proposals/{proposal.id}/review",
        data={
            "action": "reject",
            "reviewer_name": "Auditor Principal",
            "reviewer_notes": "No se acredita nivel 5",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    # Assert: Proposal status is rejected, but control score remains unchanged at 2
    updated_prop = db_session.query(AIProposal).filter(AIProposal.id == proposal.id).first()
    assert updated_prop.status == "rejected"

    updated_ctrl = db_session.query(AnnexControl).filter(AnnexControl.id == ctrl.id).first()
    assert updated_ctrl.implementation_score == 2
