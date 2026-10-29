def test_health_check_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "SecAuditAI"


def test_dashboard_page_renders_successfully(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Tablero General de Cumplimiento ISO/IEC 27001:2022" in response.text
    assert "Cumplimiento Interno Estimado" in response.text


def test_settings_ollama_page_renders(client):
    response = client.get("/settings/ollama")
    assert response.status_code == 200
    assert "Configuración y Estado de Ollama Local" in response.text
    assert "Skill Declarativa Cargada" in response.text
