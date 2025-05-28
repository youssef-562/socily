import pytest
from datetime import datetime
from agent.cortex_client import CortexClient

def test_cortex_client_initialization(mock_env_vars):
    """Test l'initialisation du client Cortex."""
    client = CortexClient()
    assert client.api_url == "http://localhost:9001"
    assert client.api_key == "test-key"

def test_cortex_client_initialization_with_params():
    """Test l'initialisation du client Cortex avec des paramètres personnalisés."""
    client = CortexClient(
        api_url="http://custom:9001",
        api_key="custom-key"
    )
    assert client.api_url == "http://custom:9001"
    assert client.api_key == "custom-key"

def test_cortex_client_run_analyzer(mock_cortex_client):
    """Test l'exécution d'un analyseur."""
    client = CortexClient()
    result = client.run_analyzer(
        "block_ip",
        {
            "ip": "192.168.1.100",
            "reason": "Tentative d'intrusion"
        }
    )
    
    assert result.id == "job123"
    assert result.status == "Success"
    assert "summary" in result.report
    assert "artifacts" in result.report

def test_cortex_client_run_analyzer_with_timeout(mock_cortex_client):
    """Test l'exécution d'un analyseur avec un timeout."""
    client = CortexClient()
    result = client.run_analyzer(
        "block_ip",
        {
            "ip": "192.168.1.100",
            "reason": "Tentative d'intrusion"
        },
        timeout=60
    )
    
    assert result.id == "job123"
    assert result.status == "Success"

def test_cortex_client_run_analyzer_error_handling(mock_cortex_client):
    """Test la gestion des erreurs lors de l'exécution d'un analyseur."""
    mock_cortex_client.run_analyzer.side_effect = Exception("Analyzer error")
    client = CortexClient()
    
    with pytest.raises(Exception) as exc_info:
        client.run_analyzer("block_ip", {"ip": "192.168.1.100"})
    
    assert str(exc_info.value) == "Analyzer error"

def test_cortex_client_get_job(mock_cortex_client):
    """Test la récupération d'un job."""
    client = CortexClient()
    job = client.get_job("job123")
    
    assert job.id == "job123"
    assert job.status == "Success"
    assert "summary" in job.report

def test_cortex_client_get_job_error_handling(mock_cortex_client):
    """Test la gestion des erreurs lors de la récupération d'un job."""
    mock_cortex_client.get_job.side_effect = Exception("Job not found")
    client = CortexClient()
    
    with pytest.raises(Exception) as exc_info:
        client.get_job("invalid_id")
    
    assert str(exc_info.value) == "Job not found"

def test_cortex_client_wait_for_job(mock_cortex_client):
    """Test l'attente de la fin d'un job."""
    client = CortexClient()
    job = client.wait_for_job("job123", timeout=30)
    
    assert job.id == "job123"
    assert job.status == "Success"

def test_cortex_client_wait_for_job_timeout(mock_cortex_client):
    """Test le timeout lors de l'attente d'un job."""
    mock_cortex_client.get_job.return_value = Mock(
        id="job123",
        status="InProgress"
    )
    client = CortexClient()
    
    with pytest.raises(TimeoutError) as exc_info:
        client.wait_for_job("job123", timeout=1)
    
    assert "Job timeout" in str(exc_info.value)

def test_cortex_client_get_analyzers(mock_cortex_client):
    """Test la récupération de la liste des analyseurs."""
    mock_cortex_client.get_analyzers.return_value = [
        {"name": "block_ip", "description": "Block IP address"},
        {"name": "scan_file", "description": "Scan file for malware"}
    ]
    client = CortexClient()
    analyzers = client.get_analyzers()
    
    assert len(analyzers) == 2
    assert analyzers[0]["name"] == "block_ip"
    assert analyzers[1]["name"] == "scan_file"

def test_cortex_client_get_analyzers_error_handling(mock_cortex_client):
    """Test la gestion des erreurs lors de la récupération des analyseurs."""
    mock_cortex_client.get_analyzers.side_effect = Exception("API error")
    client = CortexClient()
    
    with pytest.raises(Exception) as exc_info:
        client.get_analyzers()
    
    assert str(exc_info.value) == "API error"

def test_cortex_client_validate_analyzer(mock_cortex_client):
    """Test la validation d'un analyseur."""
    client = CortexClient()
    is_valid = client.validate_analyzer("block_ip")
    assert is_valid is True

def test_cortex_client_validate_analyzer_invalid(mock_cortex_client):
    """Test la validation d'un analyseur invalide."""
    mock_cortex_client.get_analyzers.return_value = [
        {"name": "scan_file", "description": "Scan file for malware"}
    ]
    client = CortexClient()
    is_valid = client.validate_analyzer("invalid_analyzer")
    assert is_valid is False

def test_cortex_client_validate_parameters(mock_cortex_client):
    """Test la validation des paramètres d'un analyseur."""
    client = CortexClient()
    is_valid = client.validate_parameters(
        "block_ip",
        {
            "ip": "192.168.1.100",
            "reason": "Tentative d'intrusion"
        }
    )
    assert is_valid is True

def test_cortex_client_validate_parameters_invalid(mock_cortex_client):
    """Test la validation de paramètres invalides."""
    client = CortexClient()
    is_valid = client.validate_parameters(
        "block_ip",
        {
            "invalid": "parameter"
        }
    )
    assert is_valid is False 