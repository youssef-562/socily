# Guide d'Installation

## Prérequis

### Système
- Système d'exploitation : Linux (Ubuntu 20.04+ recommandé)
- RAM : 8 Go minimum (16 Go recommandé)
- CPU : 4 cœurs minimum
- Stockage : 50 Go d'espace libre

### Logiciels
- Python 3.8+
- Docker 20.10+
- Docker Compose 2.0+
- Git

## Installation

### 1. Cloner le Repository
```bash
git clone https://github.com/votre-org/sec-ia-agent.git
cd sec-ia-agent
```

### 2. Configuration de l'Environnement

#### Créer le fichier .env
```bash
cp .env.example .env
```

#### Éditer les variables d'environnement
```env
# Ollama
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Loki
LOKI_API_URL=http://localhost:3100
LOKI_TIMEOUT=30

# TheHive
THEHIVE_API_URL=http://localhost:9000
THEHIVE_API_KEY=votre-clé-api

# Cortex
CORTEX_API_URL=http://localhost:9001
CORTEX_API_KEY=votre-clé-api

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
```

### 3. Installation des Dépendances

#### Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

#### Installer les dépendances Python
```bash
pip install -r requirements.txt
```

### 4. Configuration des Services

#### TheHive
1. Télécharger TheHive 4.1
```bash
wget https://download.thehive-project.org/TheHive-4.1.21.zip
unzip TheHive-4.1.21.zip
```

2. Configurer la base de données
```bash
sudo -u postgres psql
CREATE DATABASE thehive;
CREATE USER thehive WITH PASSWORD 'votre-mot-de-passe';
GRANT ALL PRIVILEGES ON DATABASE thehive TO thehive;
```

3. Configurer TheHive
```bash
cp application.conf.example application.conf
# Éditer application.conf avec vos paramètres
```

#### Cortex
1. Télécharger Cortex 3.1
```bash
wget https://download.thehive-project.org/cortex/Cortex-3.1.21.zip
unzip Cortex-3.1.21.zip
```

2. Configurer la base de données
```bash
sudo -u postgres psql
CREATE DATABASE cortex;
CREATE USER cortex WITH PASSWORD 'votre-mot-de-passe';
GRANT ALL PRIVILEGES ON DATABASE cortex TO cortex;
```

3. Configurer Cortex
```bash
cp application.conf.example application.conf
# Éditer application.conf avec vos paramètres
```

#### Loki
1. Créer le fichier de configuration Promtail
```yaml
# /etc/promtail/config.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: security
          __path__: /var/log/*.log
```

2. Configurer Loki
```yaml
# /etc/loki/config.yml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
    final_sleep: 0s
  chunk_idle_period: 5m
  chunk_retain_period: 30s
```

### 5. Démarrage des Services

#### TheHive
```bash
cd TheHive-4.1.21
./bin/thehive
```

#### Cortex
```bash
cd Cortex-3.1.21
./bin/cortex
```

#### Loki
```bash
# Démarrer Promtail
promtail -config.file /etc/promtail/config.yml

# Démarrer Loki
loki -config.file /etc/loki/config.yml
```

#### Ollama
```bash
# Installer Ollama
curl https://ollama.ai/install.sh | sh

# Télécharger le modèle
ollama pull mistral
```

#### Agent de Sécurité
```bash
# Démarrer l'agent
python main.py
```

### 6. Vérification de l'Installation

#### Tester l'API
```bash
curl http://localhost:8000/api/health
```

#### Vérifier les Logs
```bash
tail -f /var/log/sec-ia-agent.log
```

#### Vérifier les Métriques
```bash
curl http://localhost:8000/metrics
```

## Dépannage

### Problèmes Courants

#### TheHive ne démarre pas
1. Vérifier les logs
```bash
tail -f /var/log/thehive.log
```

2. Vérifier la base de données
```bash
sudo -u postgres psql -d thehive -c "\dt"
```

#### Cortex ne démarre pas
1. Vérifier les logs
```bash
tail -f /var/log/cortex.log
```

2. Vérifier la base de données
```bash
sudo -u postgres psql -d cortex -c "\dt"
```

#### Loki ne reçoit pas de logs
1. Vérifier Promtail
```bash
systemctl status promtail
```

2. Vérifier les permissions
```bash
ls -l /var/log/
```

#### Ollama ne répond pas
1. Vérifier le service
```bash
systemctl status ollama
```

2. Vérifier le modèle
```bash
ollama list
```

### Logs et Diagnostics

#### Logs de l'Agent
```bash
tail -f /var/log/sec-ia-agent.log
```

#### Métriques Prometheus
```bash
curl http://localhost:8000/metrics
```

#### État des Services
```bash
systemctl status thehive cortex promtail loki ollama
```

## Mise à Jour

### Mise à Jour de l'Agent
```bash
git pull
pip install -r requirements.txt
systemctl restart sec-ia-agent
```

### Mise à Jour des Services
```bash
# TheHive
wget https://download.thehive-project.org/TheHive-4.1.22.zip
unzip TheHive-4.1.22.zip
systemctl restart thehive

# Cortex
wget https://download.thehive-project.org/cortex/Cortex-3.1.22.zip
unzip Cortex-3.1.22.zip
systemctl restart cortex

# Loki
wget https://github.com/grafana/loki/releases/download/v2.9.0/loki-linux-amd64.zip
unzip loki-linux-amd64.zip
systemctl restart loki
```

## Désinstallation

### Supprimer l'Agent
```bash
systemctl stop sec-ia-agent
systemctl disable sec-ia-agent
rm -rf /opt/sec-ia-agent
```

### Supprimer les Services
```bash
# TheHive
systemctl stop thehive
systemctl disable thehive
rm -rf /opt/thehive

# Cortex
systemctl stop cortex
systemctl disable cortex
rm -rf /opt/cortex

# Loki
systemctl stop loki promtail
systemctl disable loki promtail
rm -rf /opt/loki
```

### Nettoyer la Base de Données
```bash
sudo -u postgres psql
DROP DATABASE thehive;
DROP DATABASE cortex;
DROP USER thehive;
DROP USER cortex;
``` 