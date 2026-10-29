from app.core.security import validate_file_security


def test_validate_valid_pdf_file():
    # Arrange
    content = b"%PDF-1.4 valid content"
    # Act
    is_valid, msg = validate_file_security("reporte.pdf", content, "application/pdf", 1024 * 1024)
    # Assert
    assert is_valid is True


def test_validate_valid_docx_file():
    # Arrange
    content = b"PK\x03\x04 valid docx zip content"
    # Act
    is_valid, msg = validate_file_security("politica.docx", content, "application/vnd.openxmlformats", 1024 * 1024)
    # Assert
    assert is_valid is True


def test_reject_unsupported_extension():
    # Arrange
    content = b"malicious binary or script"
    # Act
    is_valid, msg = validate_file_security("script.sh", content, "text/x-sh", 1024 * 1024)
    # Assert
    assert is_valid is False
    assert "no permitida" in msg


def test_reject_oversized_file():
    # Arrange
    limit = 1000  # 1000 bytes
    oversized = b"A" * 1500
    # Act
    is_valid, msg = validate_file_security("large.txt", oversized, "text/plain", limit)
    # Assert
    assert is_valid is False
    assert "excede el tamaño" in msg


def test_reject_fake_pdf_magic_bytes():
    # Arrange: Extension is .pdf but content is arbitrary non-PDF bytes
    fake_pdf = b"MZ\x90\x00 (Windows executable disguise)"
    # Act
    is_valid, msg = validate_file_security("spoofed.pdf", fake_pdf, "application/pdf", 1024 * 1024)
    # Assert
    assert is_valid is False
    assert "firma interna" in msg.lower()


def test_reject_empty_file():
    # Arrange
    empty = b""
    # Act
    is_valid, msg = validate_file_security("vacio.txt", empty, "text/plain", 1024 * 1024)
    # Assert
    assert is_valid is False
    assert "está vacío" in msg
