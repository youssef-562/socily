import pytest
from datetime import datetime, timedelta
from agent.loki_client import LokiClient

def test_loki_client_initialization(mock_env_vars):
    """Test l'initialisation du client Loki."""
    client = LokiClient()
    assert client.base_url == "http://localhost:3100"
    assert client.timeout == 30

def test_loki_client_initialization_with_params():
    """Test l'initialisation du client Loki avec des paramètres personnalisés."""
    client = LokiClient(
        base_url="http://custom:3100",
        timeout=60
    )
    assert client.base_url == "http://custom:3100"
    assert client.timeout == 60

def test_loki_client_query(mock_loki_client):
    """Test la requête de logs."""
    client = LokiClient()
    result = client.query('{job="security"}')
    
    assert result["status"] == "success"
    assert "data" in result
    assert "result" in result["data"]
    assert len(result["data"]["result"]) > 0

def test_loki_client_query_with_timeframe(mock_loki_client):
    """Test la requête de logs avec un intervalle de temps."""
    client = LokiClient()
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=5)
    
    result = client.query(
        '{job="security"}',
        start_time=start_time,
        end_time=end_time
    )
    
    assert result["status"] == "success"
    assert "data" in result
    assert "result" in result["data"]

def test_loki_client_query_with_limit(mock_loki_client):
    """Test la requête de logs avec une limite."""
    client = LokiClient()
    result = client.query('{job="security"}', limit=10)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "result" in result["data"]

def test_loki_client_query_error_handling(mock_loki_client):
    """Test la gestion des erreurs lors d'une requête."""
    mock_loki_client.query.side_effect = Exception("Connection error")
    client = LokiClient()
    
    with pytest.raises(Exception) as exc_info:
        client.query('{job="security"}')
    
    assert str(exc_info.value) == "Connection error"

def test_loki_client_stream(mock_loki_client):
    """Test le streaming de logs."""
    client = LokiClient()
    logs = list(client.stream('{job="security"}'))
    
    assert len(logs) > 0
    assert all(isinstance(log, dict) for log in logs)

def test_loki_client_stream_with_timeframe(mock_loki_client):
    """Test le streaming de logs avec un intervalle de temps."""
    client = LokiClient()
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=5)
    
    logs = list(client.stream(
        '{job="security"}',
        start_time=start_time,
        end_time=end_time
    ))
    
    assert len(logs) > 0
    assert all(isinstance(log, dict) for log in logs)

def test_loki_client_stream_error_handling(mock_loki_client):
    """Test la gestion des erreurs lors du streaming."""
    mock_loki_client.stream.side_effect = Exception("Stream error")
    client = LokiClient()
    
    with pytest.raises(Exception) as exc_info:
        list(client.stream('{job="security"}'))
    
    assert str(exc_info.value) == "Stream error"

def test_loki_client_parse_log_entry(sample_log_entry):
    """Test le parsing d'une entrée de log."""
    client = LokiClient()
    parsed = client._parse_log_entry(sample_log_entry)
    
    assert isinstance(parsed, dict)
    assert "timestamp" in parsed
    assert "level" in parsed
    assert "message" in parsed
    assert "source" in parsed

def test_loki_client_parse_log_entry_invalid():
    """Test le parsing d'une entrée de log invalide."""
    client = LokiClient()
    invalid_entry = {"invalid": "entry"}
    
    with pytest.raises(ValueError) as exc_info:
        client._parse_log_entry(invalid_entry)
    
    assert "Invalid log entry" in str(exc_info.value)

def test_loki_client_build_query():
    """Test la construction d'une requête LogQL."""
    client = LokiClient()
    query = client._build_query(
        job="security",
        level="ERROR",
        source="ssh",
        message="failed"
    )
    
    assert query == '{job="security", level="ERROR", source="ssh"} |= "failed"'

def test_loki_client_build_query_minimal():
    """Test la construction d'une requête LogQL minimale."""
    client = LokiClient()
    query = client._build_query(job="security")
    
    assert query == '{job="security"}'

def test_loki_client_build_query_empty():
    """Test la construction d'une requête LogQL vide."""
    client = LokiClient()
    
    with pytest.raises(ValueError) as exc_info:
        client._build_query()
    
    assert "At least one filter is required" in str(exc_info.value) 