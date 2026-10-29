from app.models.control import AnnexControl
from app.models.requirement import Requirement


def test_requirements_catalog_page_and_filtering(client):
    # Act: Request list of clause 4 requirements
    response = client.get("/requirements?clause=4")
    assert response.status_code == 200
    assert "4.1" in response.text
    assert "4.2" in response.text


def test_requirement_detail_and_evaluation_update(client, db_session):
    # Act 1: Get detail page
    detail_resp = client.get("/requirements/4.1")
    assert detail_resp.status_code == 200
    assert "Comprensión de la organización" in detail_resp.text

    # Act 2: Submit evaluation update via POST
    post_resp = client.post(
        "/requirements/4.1/evaluate",
        data={
            "is_applicable": "true",
            "compliance_score": "4",
            "observations": "Evaluación formal con análisis de riesgos climáticos",
            "responsible": "Oficial de Seguridad",
        },
        follow_redirects=True,
    )
    assert post_resp.status_code == 200

    # Assert DB update
    req = db_session.query(Requirement).filter(Requirement.code == "4.1").first()
    assert req.compliance_score == 4
    assert req.responsible == "Oficial de Seguridad"


def test_control_detail_and_evaluation_update(client, db_session):
    # Act 1: Get detail page
    detail_resp = client.get("/controls/A.5.1")
    assert detail_resp.status_code == 200
    assert "Políticas para la seguridad de la información" in detail_resp.text

    # Act 2: Submit evaluation
    post_resp = client.post(
        "/controls/A.5.1/evaluate",
        data={
            "is_applicable": "true",
            "implementation_status": "Implementado",
            "implementation_score": "5",
            "justification_inclusion": "Línea base fundamental de seguridad",
            "implementation_summary": "Políticas aprobadas y publicadas en intranet",
            "responsible": "CISO",
        },
        follow_redirects=True,
    )
    assert post_resp.status_code == 200

    # Assert DB update
    ctrl = db_session.query(AnnexControl).filter(AnnexControl.code == "A.5.1").first()
    assert ctrl.implementation_score == 5
    assert ctrl.implementation_status == "Implementado"
    assert ctrl.human_reviewed is True
