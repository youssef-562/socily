# Guide de Contribution

## Comment Contribuer

### 1. Fork et Clone
1. Fork le repository sur GitHub
2. Clone votre fork localement
```bash
git clone https://github.com/votre-username/sec-ia-agent.git
cd sec-ia-agent
```

### 2. Configuration de l'Environnement de Développement
1. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

2. Installer les dépendances de développement
```bash
pip install -r requirements-dev.txt
```

3. Installer les hooks de pre-commit
```bash
pre-commit install
```

### 3. Créer une Branche
```bash
git checkout -b feature/nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug
```

### 4. Développement

#### Structure du Code
```
sec-ia-agent/
├── agent/
│   ├── __init__.py
│   ├── main.py
│   ├── cortex_client.py
│   ├── loki_client.py
│   └── ollama_client.py
├── tests/
│   ├── __init__.py
│   ├── test_cortex_client.py
│   ├── test_loki_client.py
│   └── test_ollama_client.py
├── docs/
│   ├── README.md
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   └── CONTRIBUTING.md
└── requirements.txt
```

#### Standards de Code
1. Suivre PEP 8
2. Utiliser des docstrings
3. Écrire des tests unitaires
4. Documenter les changements

#### Exemple de Docstring
```python
def analyze_logs(timeframe: int, source: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyse les logs pour détecter des menaces de sécurité.

    Args:
        timeframe (int): Période d'analyse en minutes
        source (Optional[str]): Source de logs spécifique

    Returns:
        Dict[str, Any]: Résultat de l'analyse contenant:
            - threats: Liste des menaces détectées
            - recommendations: Liste des recommandations
            - statistics: Statistiques d'analyse

    Raises:
        ValueError: Si timeframe est négatif
        ConnectionError: Si la connexion à Loki échoue
    """
```

#### Tests
```python
# tests/test_loki_client.py
import pytest
from agent.loki_client import LokiClient

def test_loki_client_initialization():
    client = LokiClient("http://localhost:3100")
    assert client.base_url == "http://localhost:3100"

def test_loki_client_query():
    client = LokiClient("http://localhost:3100")
    result = client.query('{job="security"}')
    assert isinstance(result, dict)
```

### 5. Commit et Push
```bash
# Ajouter les fichiers modifiés
git add .

# Créer un commit
git commit -m "feat: ajout de la fonctionnalité X"

# Pousser les changements
git push origin feature/nouvelle-fonctionnalite
```

### 6. Pull Request
1. Aller sur GitHub
2. Cliquer sur "New Pull Request"
3. Sélectionner votre branche
4. Remplir le template de PR
5. Soumettre la PR

## Standards de Code

### Python
- PEP 8
- Type hints
- Docstrings
- Tests unitaires
- Gestion des erreurs

### Git
- Conventional Commits
- Branches feature/fix
- Pull Requests
- Code Review

### Documentation
- Markdown
- Exemples de code
- Mise à jour du CHANGELOG
- Documentation API

## Processus de Review

### 1. Vérifications Automatiques
- Tests unitaires
- Linting
- Type checking
- Coverage

### 2. Review de Code
- Architecture
- Performance
- Sécurité
- Tests
- Documentation

### 3. Approbation
- 2 approbations minimum
- Tests passés
- Documentation à jour
- Pas de conflits

## Bonnes Pratiques

### Développement
1. Écrire des tests avant le code (TDD)
2. Documenter les changements
3. Utiliser des branches feature
4. Faire des commits atomiques
5. Maintenir la couverture de tests

### Code Review
1. Vérifier la qualité du code
2. Tester les changements
3. Vérifier la documentation
4. Suggérer des améliorations
5. Valider les tests

### Documentation
1. Mettre à jour le README
2. Documenter les API
3. Ajouter des exemples
4. Mettre à jour le CHANGELOG
5. Vérifier la cohérence

## Gestion des Issues

### Types d'Issues
- Bug
- Feature
- Documentation
- Enhancement
- Question

### Template d'Issue
```markdown
## Description

## Comportement Attendu

## Comportement Actuel

## Étapes pour Reproduire
1.
2.
3.

## Environnement
- OS:
- Python:
- Version:

## Informations Supplémentaires
```

## Release Process

### 1. Préparation
1. Mettre à jour la version
2. Mettre à jour le CHANGELOG
3. Vérifier les dépendances
4. Tester la release

### 2. Release
1. Créer un tag
2. Générer les assets
3. Publier sur PyPI
4. Mettre à jour la documentation

### 3. Post-Release
1. Vérifier l'installation
2. Surveiller les erreurs
3. Répondre aux feedbacks
4. Planifier la prochaine release

## Support

### Canaux de Communication
- Issues GitHub
- Discussions GitHub
- Slack
- Email

### Documentation
- README
- Wiki
- Exemples
- Tutoriels

### Ressources
- Code source
- Documentation
- Tests
- Exemples 