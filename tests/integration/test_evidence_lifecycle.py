from app.models.evidence import Evidence


def test_upload_valid_evidence_txt(client, db_session):
    # Arrange
    file_content = b"Politica formal de control de accesos e identificacion segura."
    files = {"file": ("politica_acceso.txt", file_content, "text/plain")}
    data = {
        "notes": "Documento subido en test de integracion",
        "auto_analyze": "false",
    }

    # Act
    response = client.post("/evidences/upload", files=files, data=data, follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert "politica_acceso.txt" in response.text

    # Verify DB record
    evidence = (
        db_session.query(Evidence)
        .filter(Evidence.original_filename == "politica_acceso.txt")
        .first()
    )
    assert evidence is not None
    assert evidence.has_extractable_text is True
    assert "control de accesos" in evidence.extracted_text


def test_upload_invalid_extension_rejected(client):
    # Arrange: executable script
    file_content = b"#!/bin/bash\necho Exploit"
    files = {"file": ("malicious.sh", file_content, "application/x-sh")}

    # Act
    response = client.post("/evidences/upload", files=files, data={})

    # Assert
    assert response.status_code == 400
    assert "no permitida" in response.text


def test_download_evidence_file(client, db_session):
    # Arrange: Upload a file first
    file_content = b"Contenido para test de descarga"
    files = {"file": ("descarga_test.txt", file_content, "text/plain")}
    client.post("/evidences/upload", files=files, data={})

    evidence = db_session.query(Evidence).filter(Evidence.original_filename == "descarga_test.txt").first()
    assert evidence is not None

    # Act
    download_resp = client.get(f"/evidences/{evidence.id}/download")

    # Assert
    assert download_resp.status_code == 200
    assert download_resp.content == file_content
