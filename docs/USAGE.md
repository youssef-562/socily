# Guide d'Utilisation

## Interface API

### Endpoints Principaux

#### Analyse de Logs
```bash
# Analyser les logs des 5 dernières minutes
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"timeframe": 5}'

# Analyser les logs d'une source spécifique
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"timeframe": 5, "source": "firewall"}'
```

#### Gestion des Alertes
```bash
# Créer une alerte
curl -X POST http://localhost:8000/api/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tentative d'intrusion détectée",
    "description": "Plusieurs tentatives de connexion SSH échouées",
    "severity": "high",
    "source": "ssh",
    "tags": ["intrusion", "ssh"]
  }'

# Lister les alertes
curl -X GET http://localhost:8000/api/alerts

# Obtenir une alerte spécifique
curl -X GET http://localhost:8000/api/alerts/{alert_id}
```

#### Actions Automatisées
```bash
# Exécuter une action
curl -X POST http://localhost:8000/api/actions/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action": "block_ip",
    "event": {
      "ip": "192.168.1.100",
      "reason": "Tentative d'intrusion"
    }
  }'
```

### Exemples d'Utilisation

#### Analyse Continue
```python
import requests
import time

def monitor_logs():
    while True:
        response = requests.post(
            "http://localhost:8000/api/analyze",
            json={"timeframe": 5}
        )
        if response.status_code == 200:
            analysis = response.json()
            if analysis["threats"]:
                print(f"Menaces détectées: {analysis['threats']}")
        time.sleep(300)  # Attendre 5 minutes

monitor_logs()
```

#### Gestion des Alertes
```python
import requests

def create_alert(title, description, severity):
    response = requests.post(
        "http://localhost:8000/api/alerts",
        json={
            "title": title,
            "description": description,
            "severity": severity,
            "source": "custom",
            "tags": ["custom"]
        }
    )
    return response.json()

# Exemple d'utilisation
alert = create_alert(
    "Tentative d'intrusion",
    "Détection de scan de ports",
    "high"
)
```

#### Actions Automatisées
```python
import requests

def block_ip(ip, reason):
    response = requests.post(
        "http://localhost:8000/api/actions/execute",
        json={
            "action": "block_ip",
            "event": {
                "ip": ip,
                "reason": reason
            }
        }
    )
    return response.json()

# Exemple d'utilisation
result = block_ip("192.168.1.100", "Tentative d'intrusion")
```

## Intégration avec TheHive

### Création de Cas
```python
from thehive4py.api import TheHiveApi
from thehive4py.models import Case, CaseTask

# Configuration
api = TheHiveApi(
    "http://localhost:9000",
    "votre-clé-api"
)

# Créer un cas
case = Case(
    title="Tentative d'intrusion",
    description="Détection de scan de ports",
    severity=2,
    tags=["intrusion", "scan"]
)

# Ajouter des tâches
tasks = [
    CaseTask(title="Analyser les logs"),
    CaseTask(title="Vérifier les règles de pare-feu")
]

# Créer le cas avec les tâches
api.create_case(case, tasks)
```

### Mise à Jour de Cas
```python
# Mettre à jour un cas
api.update_case(
    case_id="case_id",
    updates={
        "status": "InProgress",
        "description": "Nouvelle description"
    }
)

# Ajouter une tâche
api.create_case_task(
    case_id="case_id",
    task=CaseTask(title="Nouvelle tâche")
)
```

## Intégration avec Cortex

### Exécution d'Actions
```python
from cortex4py.api import Api
from cortex4py.models import Job

# Configuration
api = Api(
    "http://localhost:9001",
    "votre-clé-api"
)

# Exécuter une action
job = api.run_analyzer(
    "block_ip",
    {
        "ip": "192.168.1.100",
        "reason": "Tentative d'intrusion"
    }
)

# Vérifier le statut
status = api.get_job(job.id)
```

## Intégration avec Loki

### Requêtes de Logs
```python
import requests

# Configuration
LOKI_URL = "http://localhost:3100"

# Requête LogQL
query = '{job="security"} |= "error"'

# Exécuter la requête
response = requests.get(
    f"{LOKI_URL}/loki/api/v1/query",
    params={"query": query}
)

# Analyser les résultats
results = response.json()
```

### Streaming de Logs
```python
import requests
import json

# Configuration
LOKI_URL = "http://localhost:3100"

# Requête de streaming
query = '{job="security"}'

# Démarrer le streaming
response = requests.get(
    f"{LOKI_URL}/loki/api/v1/stream",
    params={"query": query},
    stream=True
)

# Traiter les logs en temps réel
for line in response.iter_lines():
    if line:
        log = json.loads(line)
        print(f"Log reçu: {log}")
```

## Monitoring

### Métriques Prometheus
```python
from prometheus_client import start_http_server, Counter, Gauge

# Définir les métriques
security_events = Counter(
    'security_events_total',
    'Nombre total d'événements de sécurité',
    ['severity']
)

alert_processing_time = Gauge(
    'alert_processing_duration_seconds',
    'Temps de traitement des alertes'
)

# Démarrer le serveur de métriques
start_http_server(8000)

# Enregistrer des métriques
security_events.labels(severity='high').inc()
alert_processing_time.set(0.5)
```

### Logs
```python
import logging

# Configuration
logging.basicConfig(
    filename='/var/log/sec-ia-agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Utilisation
logging.info("Démarrage de l'agent")
logging.warning("Tentative d'intrusion détectée")
logging.error("Erreur de connexion à l'API")
```

## Bonnes Pratiques

### Sécurité
1. Utiliser HTTPS pour toutes les communications
2. Implémenter l'authentification pour toutes les API
3. Valider toutes les entrées utilisateur
4. Limiter les taux de requêtes
5. Journaliser toutes les actions importantes

### Performance
1. Utiliser le cache pour les requêtes fréquentes
2. Implémenter la pagination pour les grandes listes
3. Optimiser les requêtes de logs
4. Utiliser des connexions persistantes
5. Mettre en place des timeouts appropriés

### Maintenance
1. Surveiller l'utilisation des ressources
2. Nettoyer régulièrement les logs
3. Mettre à jour les dépendances
4. Sauvegarder les configurations
5. Documenter les changements

## Dépannage

### Problèmes Courants

#### API ne répond pas
1. Vérifier que le service est en cours d'exécution
2. Vérifier les logs pour les erreurs
3. Vérifier la configuration réseau
4. Vérifier les permissions

#### Erreurs d'Authentification
1. Vérifier les clés API
2. Vérifier les tokens JWT
3. Vérifier les permissions
4. Vérifier les logs d'accès

#### Problèmes de Performance
1. Vérifier l'utilisation CPU/RAM
2. Vérifier les requêtes de base de données
3. Vérifier les timeouts
4. Vérifier les logs de performance

### Commandes Utiles

#### Vérifier l'État des Services
```bash
systemctl status sec-ia-agent
systemctl status thehive
systemctl status cortex
systemctl status loki
```

#### Vérifier les Logs
```bash
tail -f /var/log/sec-ia-agent.log
tail -f /var/log/thehive.log
tail -f /var/log/cortex.log
tail -f /var/log/loki.log
```

#### Vérifier les Métriques
```bash
curl http://localhost:8000/metrics
```

#### Vérifier la Configuration
```bash
cat /etc/sec-ia-agent/config.yml
cat /etc/thehive/application.conf
cat /etc/cortex/application.conf
cat /etc/loki/config.yml
``` 