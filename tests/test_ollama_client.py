import pytest
from agent.ollama_client import OllamaClient

def test_ollama_client_initialization(mock_env_vars):
    """Test l'initialisation du client Ollama."""
    client = OllamaClient()
    assert client.api_url == "http://localhost:11434"
    assert client.model == "mistral"

def test_ollama_client_initialization_with_params():
    """Test l'initialisation du client Ollama avec des paramètres personnalisés."""
    client = OllamaClient(
        api_url="http://custom:11434",
        model="custom-model"
    )
    assert client.api_url == "http://custom:11434"
    assert client.model == "custom-model"

def test_ollama_client_generate(mock_ollama_client):
    """Test la génération de texte."""
    client = OllamaClient()
    response = client.generate("Analyse les logs suivants pour détecter des menaces")
    
    assert response["response"] == "Analyse de sécurité effectuée"
    assert "context" in response

def test_ollama_client_generate_with_options(mock_ollama_client):
    """Test la génération de texte avec des options."""
    client = OllamaClient()
    response = client.generate(
        "Analyse les logs suivants pour détecter des menaces",
        temperature=0.7,
        max_tokens=100
    )
    
    assert response["response"] == "Analyse de sécurité effectuée"
    assert "context" in response

def test_ollama_client_generate_error_handling(mock_ollama_client):
    """Test la gestion des erreurs lors de la génération."""
    mock_ollama_client.generate.side_effect = Exception("Generation error")
    client = OllamaClient()
    
    with pytest.raises(Exception) as exc_info:
        client.generate("Test prompt")
    
    assert str(exc_info.value) == "Generation error"

def test_ollama_client_analyze_logs(mock_ollama_client):
    """Test l'analyse de logs."""
    client = OllamaClient()
    logs = [
        "2024-01-01 12:00:00 Failed login attempt from 192.168.1.100",
        "2024-01-01 12:00:01 Failed login attempt from 192.168.1.100",
        "2024-01-01 12:00:02 Failed login attempt from 192.168.1.100"
    ]
    
    analysis = client.analyze_logs(logs)
    
    assert isinstance(analysis, dict)
    assert "threats" in analysis
    assert "recommendations" in analysis

def test_ollama_client_analyze_logs_empty(mock_ollama_client):
    """Test l'analyse de logs vides."""
    client = OllamaClient()
    
    with pytest.raises(ValueError) as exc_info:
        client.analyze_logs([])
    
    assert "No logs provided" in str(exc_info.value)

def test_ollama_client_analyze_logs_error_handling(mock_ollama_client):
    """Test la gestion des erreurs lors de l'analyse de logs."""
    mock_ollama_client.generate.side_effect = Exception("Analysis error")
    client = OllamaClient()
    
    with pytest.raises(Exception) as exc_info:
        client.analyze_logs(["Test log"])
    
    assert str(exc_info.value) == "Analysis error"

def test_ollama_client_analyze_alert(mock_ollama_client):
    """Test l'analyse d'une alerte."""
    client = OllamaClient()
    alert = {
        "title": "Tentative d'intrusion détectée",
        "description": "Plusieurs tentatives de connexion SSH échouées",
        "severity": "high",
        "source": "ssh"
    }
    
    analysis = client.analyze_alert(alert)
    
    assert isinstance(analysis, dict)
    assert "risk_level" in analysis
    assert "recommendations" in analysis

def test_ollama_client_analyze_alert_invalid(mock_ollama_client):
    """Test l'analyse d'une alerte invalide."""
    client = OllamaClient()
    
    with pytest.raises(ValueError) as exc_info:
        client.analyze_alert({})
    
    assert "Invalid alert" in str(exc_info.value)

def test_ollama_client_analyze_alert_error_handling(mock_ollama_client):
    """Test la gestion des erreurs lors de l'analyse d'une alerte."""
    mock_ollama_client.generate.side_effect = Exception("Analysis error")
    client = OllamaClient()
    
    with pytest.raises(Exception) as exc_info:
        client.analyze_alert({
            "title": "Test alert",
            "description": "Test description",
            "severity": "high"
        })
    
    assert str(exc_info.value) == "Analysis error"

def test_ollama_client_generate_recommendation(mock_ollama_client):
    """Test la génération de recommandations."""
    client = OllamaClient()
    threat = {
        "type": "intrusion",
        "severity": "high",
        "source": "ssh",
        "details": "Multiple failed login attempts"
    }
    
    recommendation = client.generate_recommendation(threat)
    
    assert isinstance(recommendation, dict)
    assert "action" in recommendation
    assert "priority" in recommendation

def test_ollama_client_generate_recommendation_invalid(mock_ollama_client):
    """Test la génération de recommandations pour une menace invalide."""
    client = OllamaClient()
    
    with pytest.raises(ValueError) as exc_info:
        client.generate_recommendation({})
    
    assert "Invalid threat" in str(exc_info.value)

def test_ollama_client_generate_recommendation_error_handling(mock_ollama_client):
    """Test la gestion des erreurs lors de la génération de recommandations."""
    mock_ollama_client.generate.side_effect = Exception("Generation error")
    client = OllamaClient()
    
    with pytest.raises(Exception) as exc_info:
        client.generate_recommendation({
            "type": "intrusion",
            "severity": "high"
        })
    
    assert str(exc_info.value) == "Generation error" 