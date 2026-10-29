from app.models.control import AnnexControl
from app.models.requirement import Requirement
from app.services.compliance_service import (
    calculate_controls_stats,
    calculate_requirements_stats,
    get_dashboard_summary,
)


def test_initial_requirements_compliance_is_zero(db_session):
    # Arrange: All requirements start at score 0
    # Act
    stats = calculate_requirements_stats(db_session)

    # Assert
    assert stats["evaluated_count"] == 0
    assert stats["percentage"] == 0.0
    assert stats["unassessed_count"] == stats["total"]


def test_requirements_compliance_calculation_with_scores(db_session):
    # Arrange: Assign scores to 2 requirements
    r1 = db_session.query(Requirement).filter(Requirement.code == "4.1").first()
    r2 = db_session.query(Requirement).filter(Requirement.code == "5.2").first()
    r1.compliance_score = 3
    r2.compliance_score = 5
    db_session.commit()

    # Act
    stats = calculate_requirements_stats(db_session)

    # Assert: 2 evaluated items, total points = 8, max points = 2 * 5 = 10, pct = 80.0%
    assert stats["evaluated_count"] == 2
    assert stats["total_points"] == 8
    assert stats["max_possible_points"] == 10
    assert stats["percentage"] == 80.0
    assert "8 / 10 pts" in stats["denominator_label"]


def test_not_applicable_excluded_from_breaches_and_denominator(db_session):
    # Arrange: 1 requirement evaluated (level 5), 1 marked NA, rest unassessed (0)
    r1 = db_session.query(Requirement).filter(Requirement.code == "4.1").first()
    r2 = db_session.query(Requirement).filter(Requirement.code == "4.3").first()
    r1.compliance_score = 5
    r2.is_applicable = False
    r2.compliance_score = -1
    r2.na_justification = "Organización unipersonal sin sedes físicas"
    db_session.commit()

    # Act
    stats = calculate_requirements_stats(db_session)

    # Assert: Only 1 evaluated, denominator is 5, percentage is 100.0%, NA count is 1
    assert stats["na_count"] == 1
    assert stats["evaluated_count"] == 1
    assert stats["total_points"] == 5
    assert stats["max_possible_points"] == 5
    assert stats["percentage"] == 100.0


def test_controls_stats_categories_and_progress(db_session):
    # Arrange: Set two controls as implemented (level 5)
    c1 = db_session.query(AnnexControl).filter(AnnexControl.code == "A.5.1").first()
    c2 = db_session.query(AnnexControl).filter(AnnexControl.code == "A.8.5").first()
    c1.implementation_score = 5
    c1.implementation_status = "Implementado"
    c2.implementation_score = 4
    c2.implementation_status = "Implementado"
    db_session.commit()

    # Act
    ctrl_stats = calculate_controls_stats(db_session)

    # Assert
    assert ctrl_stats["total"] == 93
    assert ctrl_stats["implemented_count"] == 2
    assert ctrl_stats["evaluated_count"] == 2
    assert ctrl_stats["total_points"] == 9
    assert ctrl_stats["max_possible_points"] == 10
    assert ctrl_stats["percentage"] == 90.0


def test_dashboard_summary_real_db_reflection(db_session):
    # Arrange & Act
    summary = get_dashboard_summary(db_session)

    # Assert
    assert summary["req_stats"]["total"] == 30
    assert summary["ctrl_stats"]["total"] == 93
    assert "combined_percentage" in summary
    assert "combined_denominator" in summary
    assert isinstance(summary["top_gaps"], list)
