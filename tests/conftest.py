import pytest
from typing import Dict, Any
from unittest.mock import Mock, patch

@pytest.fixture
def mock_loki_client():
    """Fixture pour simuler un client Loki."""
    with patch('agent.loki_client.LokiClient') as mock:
        client = mock.return_value
        client.query.return_value = {
            "status": "success",
            "data": {
                "resultType": "streams",
                "result": [
                    {
                        "stream": {"job": "security"},
                        "values": [
                            ["1234567890", "log entry 1"],
                            ["1234567891", "log entry 2"]
                        ]
                    }
                ]
            }
        }
        yield client

@pytest.fixture
def mock_cortex_client():
    """Fixture pour simuler un client Cortex."""
    with patch('agent.cortex_client.Api') as mock:
        client = mock.return_value
        client.run_analyzer.return_value = Mock(
            id="job123",
            status="Success",
            report={
                "summary": "Analysis complete",
                "artifacts": []
            }
        )
        yield client

@pytest.fixture
def mock_ollama_client():
    """Fixture pour simuler un client Ollama."""
    with patch('agent.ollama_client.OllamaClient') as mock:
        client = mock.return_value
        client.generate.return_value = {
            "response": "Analyse de sécurité effectuée",
            "context": []
        }
        yield client

@pytest.fixture
def sample_log_entry() -> Dict[str, Any]:
    """Fixture pour un exemple d'entrée de log."""
    return {
        "timestamp": "2024-01-01T12:00:00Z",
        "level": "WARNING",
        "message": "Tentative de connexion SSH échouée",
        "source": "ssh",
        "ip": "192.168.1.100",
        "user": "root"
    }

@pytest.fixture
def sample_alert() -> Dict[str, Any]:
    """Fixture pour un exemple d'alerte."""
    return {
        "title": "Tentative d'intrusion détectée",
        "description": "Plusieurs tentatives de connexion SSH échouées",
        "severity": "high",
        "source": "ssh",
        "tags": ["intrusion", "ssh"],
        "artifacts": [
            {
                "type": "ip",
                "value": "192.168.1.100"
            }
        ]
    }

@pytest.fixture
def sample_action() -> Dict[str, Any]:
    """Fixture pour un exemple d'action."""
    return {
        "type": "block_ip",
        "parameters": {
            "ip": "192.168.1.100",
            "reason": "Tentative d'intrusion"
        }
    }

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Fixture pour simuler les variables d'environnement."""
    env_vars = {
        "OLLAMA_API_URL": "http://localhost:11434",
        "OLLAMA_MODEL": "mistral",
        "LOKI_API_URL": "http://localhost:3100",
        "LOKI_TIMEOUT": "30",
        "THEHIVE_API_URL": "http://localhost:9000",
        "THEHIVE_API_KEY": "test-key",
        "CORTEX_API_URL": "http://localhost:9001",
        "CORTEX_API_KEY": "test-key",
        "API_HOST": "0.0.0.0",
        "API_PORT": "8000",
        "API_DEBUG": "false"
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars

@pytest.fixture
def mock_http_response():
    """Fixture pour simuler une réponse HTTP."""
    return Mock(
        status_code=200,
        json=lambda: {
            "status": "success",
            "data": {
                "result": "test result"
            }
        }
    )

@pytest.fixture
def mock_logger():
    """Fixture pour simuler un logger."""
    with patch('logging.getLogger') as mock:
        logger = mock.return_value
        logger.info = Mock()
        logger.warning = Mock()
        logger.error = Mock()
        logger.debug = Mock()
        yield logger

@pytest.fixture
def mock_metrics():
    """Fixture pour simuler les métriques Prometheus."""
    with patch('prometheus_client.Counter') as mock_counter, \
         patch('prometheus_client.Gauge') as mock_gauge:
        counter = mock_counter.return_value
        gauge = mock_gauge.return_value
        counter.labels.return_value.inc = Mock()
        gauge.set = Mock()
        yield {
            'counter': counter,
            'gauge': gauge
        } 