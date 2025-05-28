# Documentation Technique

## Architecture Technique

### Composants Principaux

1. **Backend FastAPI (`main.py`)**
   - Gestion des routes API
   - Middleware d'authentification
   - Gestion des erreurs
   - Validation des données

2. **Client Ollama (`ollama_client.py`)**
   - Interface avec le modèle d'IA local
   - Gestion des prompts
   - Analyse des réponses
   - Cache des résultats

3. **Client Loki (`loki_client.py`)**
   - Collecte des logs
   - Requêtes LogQL
   - Filtrage des données
   - Agrégation des résultats

4. **Client TheHive (`thehive_client.py`)**
   - Création d'alertes
   - Gestion des cas
   - Mise à jour des statuts
   - Recherche d'incidents

5. **Client Cortex (`cortex_client.py`)**
   - Exécution d'actions
   - Gestion des jobs
   - Récupération des rapports
   - Monitoring des tâches

## API Documentation

### Endpoints

#### Analyse
```python
@app.post("/api/analyze")
async def analyze_logs(
    timeframe: int = 5,  # minutes
    source: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyse les logs récents.
    
    Args:
        timeframe: Période d'analyse en minutes
        source: Source de logs spécifique (optionnel)
    
    Returns:
        Dict contenant l'analyse et les recommandations
    """
```

#### Alertes
```python
@app.post("/api/alerts")
async def create_alert(
    alert: AlertCreate
) -> Dict[str, Any]:
    """
    Crée une nouvelle alerte.
    
    Args:
        alert: Données de l'alerte
    
    Returns:
        Dict contenant les détails de l'alerte créée
    """
```

#### Actions
```python
@app.post("/api/actions/execute")
async def execute_action(
    action: str,
    event: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Exécute une action de réponse.
    
    Args:
        action: Type d'action à exécuter
        event: Données de l'événement
    
    Returns:
        Dict contenant le résultat de l'action
    """
```

## Modèles de Données

### Alert
```python
class Alert(BaseModel):
    id: str
    title: str
    description: str
    severity: str
    status: str
    created_at: datetime
    updated_at: datetime
    source: str
    tags: List[str]
    artifacts: List[Dict[str, Any]]
```

### Action
```python
class Action(BaseModel):
    type: str
    parameters: Dict[str, Any]
    status: str
    result: Optional[Dict[str, Any]]
    created_at: datetime
    completed_at: Optional[datetime]
```

## Configuration

### Variables d'Environnement

```env
# Ollama
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Loki
LOKI_API_URL=http://localhost:3100
LOKI_TIMEOUT=30

# TheHive
THEHIVE_API_URL=http://localhost:9000
THEHIVE_API_KEY=your-api-key

# Cortex
CORTEX_API_URL=http://localhost:9001
CORTEX_API_KEY=your-api-key

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
```

### Configuration Promtail

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: security
          __path__: /var/log/*.log
```

## Tests

### Tests Unitaires
```bash
pytest tests/unit/
```

### Tests d'Intégration
```bash
pytest tests/integration/
```

### Tests de Performance
```bash
locust -f tests/performance/locustfile.py
```

## Déploiement

### Docker
```bash
docker build -t sec-ia-agent .
docker run -p 8000:8000 sec-ia-agent
```

### Docker Compose
```bash
docker-compose up -d
```

## Monitoring

### Métriques Prometheus
- `security_events_total`
- `alert_processing_duration_seconds`
- `action_execution_duration_seconds`
- `api_request_duration_seconds`

### Logs
- Format: JSON
- Niveaux: INFO, WARNING, ERROR
- Rotation: quotidienne
- Rétention: 30 jours

## Sécurité

### Authentification
- JWT avec expiration
- Refresh tokens
- Rate limiting
- CORS configuré

### Validation
- Schémas Pydantic
- Sanitization des entrées
- Validation des types
- Gestion des erreurs

## Maintenance

### Nettoyage
```bash
# Nettoyer les logs
find /var/log -name "*.log" -mtime +30 -delete

# Nettoyer les métriques
curl -X POST http://localhost:9090/api/v1/admin/tsdb/clean_tombstones
```

### Backup
```bash
# Backup de la base de données
pg_dump -U postgres thehive > backup.sql

# Backup des configurations
tar -czf configs.tar.gz /etc/sec-ia-agent/
``` 