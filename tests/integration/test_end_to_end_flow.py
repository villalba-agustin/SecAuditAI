from app.models.ai_analysis import AIProposal
from app.models.audit import AuditLog
from app.models.control import AnnexControl
from app.models.evidence import Evidence
from app.models.requirement import Requirement


def test_complete_end_to_end_audit_flow(client, db_session):
    """
    Simulates complete user flow:
    1. Uploads real-world policy evidence document.
    2. Runs AI analysis using declarative Skill instructions.
    3. Verifies persistence of AI findings, strengths, gaps and proposals.
    4. Navigates to Proposals review inbox.
    5. Auditor accepts proposal for control A.5.15 (Access Control).
    6. Confirms human decision is recorded and reflected in SoA.
    7. Verifies AuditLog entry exists.
    """
    # Step 1: Upload Evidence
    policy_text = (
        b"# Politica de Accesos y Autenticacion\n"
        b"La organizacion formaliza el control de acceso logico.\n"
        b"Es mandatorio el uso de autenticacion multifactor (MFA).\n"
        b"Los privilegios se revisan trimestralmente.\n"
        b"Evaluacion del contexto organizacional y resiliencia climatica (Enmienda 1:2024).\n"
    )
    files = {"file": ("politica_acceso_integral.md", policy_text, "text/markdown")}
    upload_resp = client.post(
        "/evidences/upload",
        files=files,
        data={"notes": "Carga integral de prueba E2E", "auto_analyze": "false"},
        follow_redirects=False,
    )
    assert upload_resp.status_code == 303
    evidence_id = int(upload_resp.headers["location"].split("/")[-1])

    # Step 2: Trigger AI Analysis (forced mock or local)
    analyze_resp = client.post(
        f"/evidences/{evidence_id}/analyze",
        data={"force_mock": "true"},
        follow_redirects=True,
    )
    assert analyze_resp.status_code == 200

    # Step 3: Verify Persistence
    evidence = db_session.query(Evidence).filter(Evidence.id == evidence_id).first()
    assert evidence.status == "analizada"
    assert len(evidence.analyses) >= 1
    analysis = evidence.analyses[0]
    assert len(analysis.get_strengths()) > 0

    proposals = db_session.query(AIProposal).filter(AIProposal.analysis_id == analysis.id).all()
    assert len(proposals) >= 1

    # Find proposal for A.5.15 (Access Control) or A.8.5
    access_proposal = next(
        (p for p in proposals if p.control and p.control.code in ["A.5.15", "A.8.5"]),
        proposals[0],
    )

    # Step 4: Auditor Reviews and Accepts Proposal
    review_resp = client.post(
        f"/proposals/{access_proposal.id}/review",
        data={
            "action": "accept",
            "reviewer_name": "Auditor Jefe E2E",
            "reviewer_notes": "Aprobado tras cotejar el texto de la politica.",
        },
        follow_redirects=True,
    )
    assert review_resp.status_code == 200

    # Step 5: Check Target Control Updated
    if access_proposal.target_type == "control":
        ctrl = db_session.query(AnnexControl).filter(AnnexControl.id == access_proposal.control_id).first()
        assert ctrl.implementation_score == access_proposal.suggested_score
        assert ctrl.human_reviewed is True
    else:
        req = db_session.query(Requirement).filter(Requirement.id == access_proposal.requirement_id).first()
        assert req.compliance_score == access_proposal.suggested_score

    # Step 6: Verify AuditLog record exists
    audit_entry = (
        db_session.query(AuditLog)
        .filter(AuditLog.action == "PROPOSAL_ACCEPT")
        .order_by(AuditLog.timestamp.desc())
        .first()
    )
    assert audit_entry is not None
    assert audit_entry.user_identifier == "Auditor Jefe E2E"
