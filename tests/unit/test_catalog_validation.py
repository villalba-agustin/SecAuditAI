from collections import Counter

from app.models.control import AnnexControl
from app.models.requirement import Requirement


def test_annex_a_total_controls_is_93(db_session):
    # Arrange & Act
    controls = db_session.query(AnnexControl).all()

    # Assert
    assert len(controls) == 93, f"Se esperaban exactamente 93 controles de Anexo A, pero hay {len(controls)}"


def test_annex_a_categories_distribution(db_session):
    # Arrange & Act
    controls = db_session.query(AnnexControl).all()
    categories = Counter(c.category for c in controls)

    # Assert
    assert categories["Organizacional"] == 37, f"Esperado 37 controles organizacionales, obtenido {categories['Organizacional']}"
    assert categories["Personas"] == 8, f"Esperado 8 controles de personas, obtenido {categories['Personas']}"
    assert categories["Físico"] == 14, f"Esperado 14 controles físicos, obtenido {categories['Físico']}"
    assert categories["Tecnológico"] == 34, f"Esperado 34 controles tecnológicos, obtenido {categories['Tecnológico']}"


def test_annex_a_unique_codes(db_session):
    # Arrange & Act
    controls = db_session.query(AnnexControl).all()
    codes = [c.code for c in controls]

    # Assert
    assert len(codes) == len(set(codes)), "Existen códigos duplicados en el Anexo A"
    assert "A.5.1" in codes
    assert "A.5.37" in codes
    assert "A.6.1" in codes
    assert "A.6.8" in codes
    assert "A.7.1" in codes
    assert "A.7.14" in codes
    assert "A.8.1" in codes
    assert "A.8.34" in codes


def test_clauses_4_to_10_requirements_loaded(db_session):
    # Arrange & Act
    requirements = db_session.query(Requirement).all()
    clause_numbers = {r.clause_number for r in requirements}

    # Assert: All clauses from 4 to 10 must be represented
    for c_num in range(4, 11):
        assert c_num in clause_numbers, f"Cláusula {c_num} no está presente en los requisitos precargados"

    # Amendment 1:2024 verification
    req_4_1 = db_session.query(Requirement).filter(Requirement.code == "4.1").first()
    assert req_4_1 is not None
    assert "cambio climático" in req_4_1.description.lower(), "4.1 debe contener la referencia de la Enmienda 1:2024"

    req_4_2 = db_session.query(Requirement).filter(Requirement.code == "4.2").first()
    assert req_4_2 is not None
    assert "cambio climático" in req_4_2.description.lower(), "4.2 debe contener la referencia de la Enmienda 1:2024"
