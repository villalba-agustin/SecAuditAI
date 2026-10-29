import hashlib
import re
import uuid
from pathlib import Path
from typing import Tuple

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
    "application/octet-stream",  # Often sent for markdown or txt
}

MAGIC_BYTES = {
    ".pdf": [b"%PDF"],
    ".docx": [b"PK\x03\x04"],
}


def sanitize_filename(filename: str) -> str:
    """
    Remove potentially dangerous characters and path traversal sequences.
    Returns only the base filename.
    """
    # Replace backslashes with forward slashes to handle Windows paths uniformly
    clean_name = filename.replace("\\", "/")
    clean_name = Path(clean_name).name
    # Strip path traversal dots
    clean_name = re.sub(r"\.\.+", "", clean_name)
    # Replace dangerous characters with underscore
    clean_name = re.sub(r"[^\w\.\-\_]", "_", clean_name)
    # Remove leading dots or dashes
    clean_name = clean_name.lstrip(".-")
    if not clean_name:
        clean_name = "evidence_file"
    return clean_name


def generate_secure_stored_filename(original_filename: str) -> Tuple[str, str]:
    """
    Generates a secure UUID-prefixed internal storage filename and preserves sanitized extension.
    Returns (secure_stored_name, file_extension).
    """
    clean_original = sanitize_filename(original_filename)
    ext = Path(clean_original).suffix.lower()
    unique_prefix = uuid.uuid4().hex
    secure_name = f"{unique_prefix}_{clean_original}"
    return secure_name, ext


def compute_sha256(content: bytes) -> str:
    """Computes SHA-256 hexadecimal hash of bytes content."""
    hasher = hashlib.sha256()
    hasher.update(content)
    return hasher.hexdigest()


def validate_file_security(
    filename: str,
    content: bytes,
    content_type: str,
    max_size_bytes: int,
) -> Tuple[bool, str]:
    """
    Performs security validation:
    1. Size limit
    2. Extension allowlist
    3. Magic byte signature verification
    """
    # 1. Size check
    if len(content) == 0:
        return False, "El archivo está vacío."

    if len(content) > max_size_bytes:
        mb_limit = max_size_bytes / (1024 * 1024)
        return False, f"El archivo excede el tamaño máximo permitido de {mb_limit:.1f} MB."

    # 2. Extension check
    clean_name = sanitize_filename(filename)
    ext = Path(clean_name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Extensión de archivo no permitida ({ext}). Solo se admiten: {', '.join(sorted(ALLOWED_EXTENSIONS))}."

    # 3. Magic bytes / content inspection
    if ext in MAGIC_BYTES:
        signatures = MAGIC_BYTES[ext]
        if not any(content.startswith(sig) for sig in signatures):
            return False, f"La firma interna del archivo no coincide con un formato {ext} legítimo."
    elif ext in {".txt", ".md"}:
        # Check for null bytes which indicate binary/executable disguise
        if b"\x00" in content[:1024]:
            return False, "El archivo de texto contiene bytes nulos o contenido binario no admitido."

    return True, "Archivo válido"


def is_path_safe(base_dir: Path, target_path: Path) -> bool:
    """
    Verifies that target_path resolves strictly within base_dir,
    preventing directory traversal attacks.
    """
    try:
        resolved_base = base_dir.resolve()
        resolved_target = target_path.resolve()
        return resolved_base in resolved_target.parents or resolved_base == resolved_target
    except Exception:
        return False


def defend_prompt_injection(document_text: str) -> str:
    """
    Encapsulates untrusted evidence text within clear system delimiters
    and neutralizes attempts to break out of delimiters.
    """
    # Sanitize delimiters to avoid breakout
    neutralized = document_text.replace("<<<DOCUMENT_CONTENT>>>", "[DELIMITER_ESCAPED]")
    neutralized = neutralized.replace("<<<END_DOCUMENT_CONTENT>>>", "[DELIMITER_ESCAPED]")
    return f"<<<DOCUMENT_CONTENT>>>\n{neutralized}\n<<<END_DOCUMENT_CONTENT>>>"
