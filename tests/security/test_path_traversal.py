from pathlib import Path

from app.core.security import generate_secure_stored_filename, is_path_safe, sanitize_filename


def test_sanitize_filename_strips_traversal():
    # Arrange: malicious traversal filenames
    payloads = [
        "../../etc/passwd",
        "..\\..\\windows\\system32\\calc.exe",
        "....//....//shadow",
        "nested/path/to/file.pdf",
    ]

    for p in payloads:
        # Act
        clean = sanitize_filename(p)
        # Assert: No slashes, backslashes, or directory markers
        assert "/" not in clean
        assert "\\" not in clean
        assert ".." not in clean


def test_path_safety_checker():
    # Arrange
    base = Path("/home/user/app/data/uploads").resolve()
    safe_target = (base / "safe_file.pdf").resolve()
    traversal_target = (base / ".." / ".." / "etc" / "passwd").resolve()

    # Act & Assert
    assert is_path_safe(base, safe_target) is True
    assert is_path_safe(base, traversal_target) is False


def test_secure_stored_filename_generation():
    # Arrange
    original = "reporte_anual_../../config.pdf"
    # Act
    stored_name, ext = generate_secure_stored_filename(original)
    # Assert
    assert ext == ".pdf"
    assert ".." not in stored_name
    assert "/" not in stored_name
    assert "\\" not in stored_name
    # Must have UUID hex prefix (32 chars)
    assert len(stored_name) > 32
