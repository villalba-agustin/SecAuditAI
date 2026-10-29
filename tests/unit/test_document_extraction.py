from app.services.document_service import (
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_plain_text,
)


def test_extract_text_from_pdf_with_content(sample_pdf_bytes):
    # Arrange & Act
    text, has_text, notes = extract_text_from_pdf(sample_pdf_bytes)

    # Assert
    assert has_text is True
    assert "Politica de Seguridad" in text


def test_extract_text_from_pdf_empty_no_hallucination():
    # Arrange: PDF without text stream
    empty_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
        b"xref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000052 00000 n\n0000000101 00000 n\n"
        b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n178\n%%EOF"
    )

    # Act
    text, has_text, notes = extract_text_from_pdf(empty_pdf)

    # Assert: Must NOT hallucinate text
    assert has_text is False
    assert text == ""
    assert "no contiene capas de texto" in notes.lower()


def test_extract_text_from_docx_with_paragraphs(sample_docx_bytes):
    # Arrange & Act
    text, has_text, notes = extract_text_from_docx(sample_docx_bytes)

    # Assert
    assert has_text is True
    assert "Política de Seguridad de la Información" in text
    assert "alta dirección" in text


def test_extract_text_from_plain_text_utf8():
    # Arrange
    content = "Directiva técnica de control de accesos y contraseñas seguras.".encode("utf-8")

    # Act
    text, has_text, notes = extract_text_from_plain_text(content)

    # Assert
    assert has_text is True
    assert "Directiva técnica" in text
