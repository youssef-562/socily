# 🛡️ Agent de Sécurité IA

<kbd>[<img title="Gabon" alt="Gabon" src="https://cdn.statically.io/gh/hjnilsson/country-flags/master/svg/ga.svg" width="22">](docs/translations/README.ga.md)</kbd>

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-85%25-green)](.coveragerc)

Un agent de sécurité intelligent qui utilise l'IA pour analyser les logs de sécurité, corréler les menaces et automatiser les réponses. Cet outil est conçu pour les équipes de sécurité qui souhaitent améliorer leur capacité de détection et de réponse aux incidents.



<img width="634" alt="image" src="https://github.com/user-attachments/assets/42402779-981b-4b13-a505-66dcbca48791" />




## 🌟 Fonctionnalités Principales

### 🔍 Analyse Intelligente des Logs
- Analyse en temps réel des logs de sécurité
- Détection automatique des patterns suspects
- Corrélation des événements de sécurité
- Classification des menaces avec IA

### 🚨 Gestion Automatisée des Alertes
- Création automatique d'alertes
- Priorisation intelligente des incidents
- Enrichissement des alertes avec contexte
- Intégration avec TheHive

### ⚡ Actions Automatisées
- Blocage automatique d'IPs suspectes
- Scan de fichiers malveillants
- Analyse de domaines suspects
- Notifications (Slack, Email)

## 🛠️ Outils Intégrés

### 🤖 Ollama
- Modèle d'IA local pour l'analyse
- Traitement du langage naturel
- Classification des menaces
- Génération de recommandations

### 📊 Loki
- Collecte centralisée des logs
- Requêtes LogQL puissantes
- Stockage efficace des logs
- Recherche rapide

### 🎯 TheHive
- Gestion des cas de sécurité
- Suivi des investigations
- Collaboration d'équipe
- Workflow d'incident

### ⚙️ Cortex
- Automatisation des actions
- Analyse de fichiers
- Scan d'IPs et domaines
- Intégration avec les outils de sécurité

## 📋 Cas d'Utilisation

### 🔒 SOC (Security Operations Center)
- Surveillance continue des logs
- Détection rapide des incidents
- Automatisation des tâches répétitives
- Réponse aux incidents

### 🏢 Entreprises
- Protection des infrastructures
- Conformité réglementaire
- Gestion des menaces internes
- Surveillance des accès

### 🌐 Fournisseurs de Services
- Sécurité multi-locataires
- Isolation des incidents
- Reporting automatisé
- SLA de sécurité

### 🎓 Éducation et Formation
- Environnement de test
- Démonstration de sécurité
- Formation des analystes
- Simulation d'incidents

## 🚀 Installation Rapide

```bash
# Cloner le repository
git clone https://github.com/votre-org/sec-ia-agent.git
cd sec-ia-agent

# Installer les dépendances
cd agent
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos configurations

# Démarrer l'agent
python main.py
```

## 📚 Documentation

- [Guide d'Installation](docs/INSTALLATION.md)
- [Guide d'Utilisation](docs/USAGE.md)
- [Documentation Technique](docs/DEVELOPMENT.md)
- [Guide de Contribution](docs/CONTRIBUTING.md)

## 🔧 Configuration

### Variables d'Environnement Essentielles
```env
OLLAMA_API_URL=http://localhost:11434
LOKI_API_URL=http://localhost:3100
THEHIVE_API_URL=http://localhost:9000
CORTEX_API_URL=http://localhost:9001
```

## 📊 Métriques et Monitoring

- Métriques Prometheus
- Tableau de bord Grafana
- Alertes de santé
- Logs structurés

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre [guide de contribution](docs/CONTRIBUTING.md) pour commencer.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Ollama](https://ollama.ai/)
- [Loki](https://grafana.com/oss/loki/)
- [TheHive](https://thehive-project.org/)
- [Cortex](https://thehive-project.org/cortex/)
