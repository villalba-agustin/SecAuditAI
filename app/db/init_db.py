import logging

from sqlalchemy.orm import Session

from app.db.seed_data import ANNEX_CONTROLS_DATA, REQUIREMENTS_DATA
from app.db.session import Base, SessionLocal, engine
from app.models.audit import AuditLog
from app.models.control import AnnexControl
from app.models.requirement import Requirement

logger = logging.getLogger(__name__)


def init_db(db: Session = None) -> None:
    """
    Idempotent database initialization:
    1. Creates all tables if they do not exist.
    2. Seeds clauses 4-10 requirements if empty.
    3. Seeds Annex A 93 controls if empty.
    """
    Base.metadata.create_all(bind=engine)

    close_session_at_end = False
    if db is None:
        db = SessionLocal()
        close_session_at_end = True

    try:
        # Check requirements
        existing_req_count = db.query(Requirement).count()
        if existing_req_count == 0:
            logger.info("Precargando cláusulas 4 a 10 de ISO/IEC 27001:2022...")
            for item in REQUIREMENTS_DATA:
                req = Requirement(
                    code=item["code"],
                    clause_number=item["clause_number"],
                    title=item["title"],
                    description=item["description"],
                    normative_ref=item["normative_ref"],
                    compliance_score=0,
                    is_applicable=True,
                )
                db.add(req)
            db.commit()

            audit = AuditLog(
                action="INITIAL_SEED_REQUIREMENTS",
                entity_type="SYSTEM",
                entity_code="CLAUSES_4_10",
                details=f"Precarga exitosa de {len(REQUIREMENTS_DATA)} requisitos normativos.",
                user_identifier="Sistema",
            )
            db.add(audit)
            db.commit()
            logger.info(f"{len(REQUIREMENTS_DATA)} requisitos precargados.")

        # Check annex controls
        existing_ctrl_count = db.query(AnnexControl).count()
        if existing_ctrl_count == 0:
            logger.info("Precargando los 93 controles del Anexo A de ISO/IEC 27001:2022...")
            for item in ANNEX_CONTROLS_DATA:
                ctrl = AnnexControl(
                    code=item["code"],
                    category=item["category"],
                    title=item["title"],
                    description=item["description"],
                    is_applicable=True,
                    justification_inclusion="Control establecido como aplicable en la línea base de seguridad de la organización.",
                    implementation_status="No iniciado",
                    implementation_score=0,
                )
                db.add(ctrl)
            db.commit()

            audit = AuditLog(
                action="INITIAL_SEED_CONTROLS",
                entity_type="SYSTEM",
                entity_code="ANNEX_A",
                details=f"Precarga exitosa de {len(ANNEX_CONTROLS_DATA)} controles del Anexo A.",
                user_identifier="Sistema",
            )
            db.add(audit)
            db.commit()
            logger.info(f"{len(ANNEX_CONTROLS_DATA)} controles de Anexo A precargados.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error inicializando la base de datos: {e}")
        raise
    finally:
        if close_session_at_end:
            db.close()


if __name__ == "__main__":
    init_db()
