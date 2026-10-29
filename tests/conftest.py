import io

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.init_db import init_db
from app.db.session import Base, get_db
from app.main import app

# In-memory SQLite database engine for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Initializes tables and seeds normative catalog in memory once for test session."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    init_db(db=db)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """Provides a transactional database session rolled back after each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """FastAPI TestClient with overridden database session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_pdf_bytes():
    """Generates valid PDF bytes in memory with extractable text."""
    from pypdf import PdfReader, PdfWriter
    raw_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        b"4 0 obj\n<< /Length 55 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Politica de Seguridad) Tj\nET\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\nxref\n0 6\n0000000000 65535 f \n"
        b"0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000244 00000 n \n0000000350 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n424\n%%EOF"
    )
    reader = PdfReader(io.BytesIO(raw_pdf))
    writer = PdfWriter()
    writer.add_page(reader.pages[0])
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


@pytest.fixture
def sample_docx_bytes():
    """Generates valid DOCX bytes in memory using python-docx."""
    import docx
    doc = docx.Document()
    doc.add_heading("Política de Seguridad de la Información", level=1)
    doc.add_paragraph("La alta dirección aprueba los lineamientos de control de accesos y respaldos.")
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()
