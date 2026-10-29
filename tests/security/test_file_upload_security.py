from app.core.security import validate_file_security


def test_reject_executable_disguised_as_pdf():
    # Arrange: File named exploit.pdf but starting with ELF binary signature
    elf_header = b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 100
    # Act
    is_valid, msg = validate_file_security("exploit.pdf", elf_header, "application/pdf", 1024 * 1024)
    # Assert
    assert is_valid is False
    assert "firma interna" in msg.lower()


def test_reject_null_byte_in_text():
    # Arrange: text file containing null byte (binary evasion)
    poisoned_text = b"Texto aparente\x00eval('malicious')"
    # Act
    is_valid, msg = validate_file_security("nota.txt", poisoned_text, "text/plain", 1024 * 1024)
    # Assert
    assert is_valid is False
    assert "bytes nulos" in msg.lower()


def test_reject_php_and_jsp_extensions():
    # Arrange
    files = [("shell.php", b"<?php phpinfo(); ?>"), ("cmd.jsp", b"<% Runtime.getRuntime(); %>")]
    for name, content in files:
        # Act
        is_valid, msg = validate_file_security(name, content, "application/octet-stream", 1024 * 1024)
        # Assert
        assert is_valid is False
        assert "no permitida" in msg.lower()


def test_server_error_handler_suppresses_traceback(client):
    # Act: Request non-existent route or invalid param that triggers error
    response = client.get("/requirements/INVALID_NON_EXISTENT_CODE_XYZ")
    # Assert: 404 cleanly returned without exposing Python tracebacks
    assert response.status_code == 404
    assert "Traceback (most recent call last)" not in response.text
