import pytest
from fastapi.testclient import TestClient
from agent.main import app

@pytest.fixture
def client():
    """Fixture pour le client de test FastAPI."""
    return TestClient(app)

def test_health_check(client):
    """Test du endpoint de vérification de santé."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_logs(client, mock_loki_client, mock_ollama_client):
    """Test de l'analyse de logs."""
    response = client.post(
        "/api/analyze",
        json={"timeframe": 5}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "threats" in data
    assert "recommendations" in data
    assert "statistics" in data

def test_analyze_logs_with_source(client, mock_loki_client, mock_ollama_client):
    """Test de l'analyse de logs avec une source spécifique."""
    response = client.post(
        "/api/analyze",
        json={
            "timeframe": 5,
            "source": "ssh"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "threats" in data
    assert "recommendations" in data

def test_analyze_logs_invalid_timeframe(client):
    """Test de l'analyse de logs avec un timeframe invalide."""
    response = client.post(
        "/api/analyze",
        json={"timeframe": -1}
    )
    
    assert response.status_code == 400
    assert "timeframe must be positive" in response.json()["detail"]

def test_create_alert(client, mock_ollama_client):
    """Test de la création d'une alerte."""
    response = client.post(
        "/api/alerts",
        json={
            "title": "Tentative d'intrusion détectée",
            "description": "Plusieurs tentatives de connexion SSH échouées",
            "severity": "high",
            "source": "ssh",
            "tags": ["intrusion", "ssh"]
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Tentative d'intrusion détectée"
    assert data["severity"] == "high"

def test_create_alert_invalid_severity(client):
    """Test de la création d'une alerte avec une sévérité invalide."""
    response = client.post(
        "/api/alerts",
        json={
            "title": "Test alert",
            "description": "Test description",
            "severity": "invalid",
            "source": "test"
        }
    )
    
    assert response.status_code == 400
    assert "severity" in response.json()["detail"]

def test_get_alerts(client):
    """Test de la récupération des alertes."""
    response = client.get("/api/alerts")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_alert(client):
    """Test de la récupération d'une alerte spécifique."""
    # D'abord créer une alerte
    create_response = client.post(
        "/api/alerts",
        json={
            "title": "Test alert",
            "description": "Test description",
            "severity": "high",
            "source": "test"
        }
    )
    alert_id = create_response.json()["id"]
    
    # Ensuite récupérer l'alerte
    response = client.get(f"/api/alerts/{alert_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == alert_id
    assert data["title"] == "Test alert"

def test_get_alert_not_found(client):
    """Test de la récupération d'une alerte inexistante."""
    response = client.get("/api/alerts/invalid-id")
    
    assert response.status_code == 404
    assert "Alert not found" in response.json()["detail"]

def test_execute_action(client, mock_cortex_client):
    """Test de l'exécution d'une action."""
    response = client.post(
        "/api/actions/execute",
        json={
            "action": "block_ip",
            "event": {
                "ip": "192.168.1.100",
                "reason": "Tentative d'intrusion"
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert "status" in data

def test_execute_action_invalid(client):
    """Test de l'exécution d'une action invalide."""
    response = client.post(
        "/api/actions/execute",
        json={
            "action": "invalid_action",
            "event": {}
        }
    )
    
    assert response.status_code == 400
    assert "Invalid action" in response.json()["detail"]

def test_get_action_status(client, mock_cortex_client):
    """Test de la récupération du statut d'une action."""
    # D'abord exécuter une action
    execute_response = client.post(
        "/api/actions/execute",
        json={
            "action": "block_ip",
            "event": {
                "ip": "192.168.1.100",
                "reason": "Test"
            }
        }
    )
    job_id = execute_response.json()["job_id"]
    
    # Ensuite récupérer le statut
    response = client.get(f"/api/actions/{job_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "result" in data

def test_get_action_status_not_found(client):
    """Test de la récupération du statut d'une action inexistante."""
    response = client.get("/api/actions/invalid-id")
    
    assert response.status_code == 404
    assert "Action not found" in response.json()["detail"]

def test_metrics_endpoint(client):
    """Test du endpoint des métriques."""
    response = client.get("/metrics")
    
    assert response.status_code == 200
    assert "security_events_total" in response.text
    assert "alert_processing_duration_seconds" in response.text

def test_cors_headers(client):
    """Test des en-têtes CORS."""
    response = client.options("/api/health")
    
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers 