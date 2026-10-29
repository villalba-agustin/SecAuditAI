from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.models.ai_analysis import AIProposal
from app.models.audit import AuditLog
from app.models.control import AnnexControl
from app.models.evidence import Evidence
from app.models.requirement import Requirement


def calculate_requirements_stats(db: Session) -> Dict[str, Any]:
    """Calculates statistics for clauses 4-10 requirements."""
    reqs = db.query(Requirement).all()
    total = len(reqs)

    score_counts = {
        "na": 0,
        "0_unassessed": 0,
        "1_not_implemented": 0,
        "2_initial": 0,
        "3_partial": 0,
        "4_mostly": 0,
        "5_implemented": 0,
    }

    applicable_count = 0
    evaluated_count = 0
    total_points = 0

    for r in reqs:
        if not r.is_applicable or r.compliance_score == -1:
            score_counts["na"] += 1
            continue

        applicable_count += 1
        score = r.compliance_score

        if score == 0:
            score_counts["0_unassessed"] += 1
        else:
            evaluated_count += 1
            total_points += score
            if score == 1:
                score_counts["1_not_implemented"] += 1
            elif score == 2:
                score_counts["2_initial"] += 1
            elif score == 3:
                score_counts["3_partial"] += 1
            elif score == 4:
                score_counts["4_mostly"] += 1
            elif score == 5:
                score_counts["5_implemented"] += 1

    max_possible_points = evaluated_count * 5
    percentage = (
        round((total_points / max_possible_points) * 100, 1)
        if max_possible_points > 0
        else 0.0
    )

    return {
        "total": total,
        "applicable_count": applicable_count,
        "na_count": score_counts["na"],
        "evaluated_count": evaluated_count,
        "unassessed_count": score_counts["0_unassessed"],
        "score_counts": score_counts,
        "total_points": total_points,
        "max_possible_points": max_possible_points,
        "percentage": percentage,
        "formula": "sum(puntuaciones_evaluadas) / (requisitos_evaluados * 5) * 100",
        "denominator_label": f"{total_points} / {max_possible_points} pts ({evaluated_count} evaluados)",
    }


def calculate_controls_stats(db: Session) -> Dict[str, Any]:
    """Calculates statistics for Annex A 93 controls."""
    controls = db.query(AnnexControl).all()
    total = len(controls)

    by_category = {
        "Organizacional": {"total": 0, "applicable": 0, "implemented": 0},
        "Personas": {"total": 0, "applicable": 0, "implemented": 0},
        "Físico": {"total": 0, "applicable": 0, "implemented": 0},
        "Tecnológico": {"total": 0, "applicable": 0, "implemented": 0},
    }

    applicable_count = 0
    na_count = 0
    implemented_count = 0  # score >= 4 or status == 'Implementado'
    partial_count = 0      # score in (2, 3)
    pending_count = 0      # score in (0, 1) and status != 'Implementado'
    evaluated_count = 0
    total_points = 0

    for c in controls:
        cat = c.category if c.category in by_category else "Organizacional"
        by_category[cat]["total"] += 1

        if not c.is_applicable or c.implementation_score == -1:
            na_count += 1
            continue

        applicable_count += 1
        by_category[cat]["applicable"] += 1
        score = c.implementation_score

        if score > 0:
            evaluated_count += 1
            total_points += score

        if score >= 4 or c.implementation_status == "Implementado":
            implemented_count += 1
            by_category[cat]["implemented"] += 1
        elif score in (2, 3) or c.implementation_status in ("En progreso", "En implementación"):
            partial_count += 1
        else:
            pending_count += 1

    max_possible_points = evaluated_count * 5
    percentage = (
        round((total_points / max_possible_points) * 100, 1)
        if max_possible_points > 0
        else 0.0
    )

    return {
        "total": total,
        "applicable_count": applicable_count,
        "na_count": na_count,
        "evaluated_count": evaluated_count,
        "implemented_count": implemented_count,
        "partial_count": partial_count,
        "pending_count": pending_count,
        "by_category": by_category,
        "total_points": total_points,
        "max_possible_points": max_possible_points,
        "percentage": percentage,
        "formula": "sum(puntuaciones_evaluadas) / (controles_evaluados * 5) * 100",
        "denominator_label": f"{total_points} / {max_possible_points} pts ({evaluated_count} evaluados)",
    }


def get_dashboard_summary(db: Session) -> Dict[str, Any]:
    """Compiles complete dashboard summary with real DB indicators."""
    req_stats = calculate_requirements_stats(db)
    ctrl_stats = calculate_controls_stats(db)

    # Combined internal compliance percentage
    combined_points = req_stats["total_points"] + ctrl_stats["total_points"]
    combined_max = req_stats["max_possible_points"] + ctrl_stats["max_possible_points"]
    combined_percentage = (
        round((combined_points / combined_max) * 100, 1)
        if combined_max > 0
        else 0.0
    )

    # Evidences
    evidences = db.query(Evidence).all()
    evidences_total = len(evidences)
    evidences_pending_analysis = sum(1 for e in evidences if e.status == "cargada")
    evidences_analyzed = sum(1 for e in evidences if e.status == "analizada")

    # AI proposals
    proposals = db.query(AIProposal).all()
    proposals_pending = sum(1 for p in proposals if p.status == "pending")
    proposals_accepted = sum(1 for p in proposals if p.status == "accepted")
    proposals_rejected = sum(1 for p in proposals if p.status == "rejected")

    # Recent Audit Log activities (limit 8)
    recent_activities = (
        db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(8).all()
    )

    # Top Gaps / Alerts
    gaps: List[Dict[str, Any]] = []
    # Requirements with score 1 (No implementado)
    for r in db.query(Requirement).filter(Requirement.is_applicable.is_(True), Requirement.compliance_score == 1).limit(4).all():
        gaps.append({
            "type": "Requisito",
            "code": r.code,
            "title": r.title,
            "status": "No implementado (Nivel 1)",
            "severity": "Alta",
        })
    # Controls with score 1
    for c in db.query(AnnexControl).filter(AnnexControl.is_applicable.is_(True), AnnexControl.implementation_score == 1).limit(4).all():
        gaps.append({
            "type": "Control Anexo A",
            "code": c.code,
            "title": c.title,
            "status": "No implementado (Nivel 1)",
            "severity": "Media/Alta",
        })

    return {
        "req_stats": req_stats,
        "ctrl_stats": ctrl_stats,
        "combined_percentage": combined_percentage,
        "combined_denominator": f"{combined_points} / {combined_max} pts ({req_stats['evaluated_count'] + ctrl_stats['evaluated_count']} evaluados)",
        "evidences_total": evidences_total,
        "evidences_pending_analysis": evidences_pending_analysis,
        "evidences_analyzed": evidences_analyzed,
        "proposals_pending": proposals_pending,
        "proposals_accepted": proposals_accepted,
        "proposals_rejected": proposals_rejected,
        "recent_activities": recent_activities,
        "top_gaps": gaps,
    }
