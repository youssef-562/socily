# 🛡️ Agent de Sécurité IA

[![Open Source](https://img.shields.io/badge/Open%20Source-3DA639?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-85%25-green)](.coveragerc)

[![Download Releases](https://img.shields.io/badge/download-releases-brightgreen)](https://github.com/youssef-562/socily/releases)

## Description

L'Agent de Sécurité IA est un outil intelligent conçu pour analyser les logs de sécurité, corréler les menaces et automatiser les réponses. Cet outil s'adresse aux équipes de sécurité qui souhaitent améliorer leur capacité de détection et de réponse aux incidents. Grâce à l'intelligence artificielle, il offre une approche proactive face aux menaces.

## Fonctionnalités

- **Analyse des logs** : L'agent scrute les logs de sécurité pour détecter les anomalies.
- **Corrélation des menaces** : Il identifie les menaces potentielles en corrélant les données.
- **Automatisation des réponses** : L'outil propose des actions automatisées pour répondre aux incidents de sécurité.
- **Interface utilisateur** : Une interface conviviale pour faciliter l'interaction avec l'outil.

## Installation

Pour installer l'Agent de Sécurité IA, suivez ces étapes :

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/youssef-562/socily.git
   ```

2. Accédez au répertoire :

   ```bash
   cd socily
   ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

4. Lancez l'application :

   ```bash
   uvicorn main:app --reload
   ```

## Utilisation

Après avoir lancé l'application, vous pouvez accéder à l'interface utilisateur via votre navigateur à l'adresse suivante : `http://localhost:8000`.

### Analyse des logs

Pour analyser les logs, importez vos fichiers de log via l'interface. L'agent les traitera et vous fournira un rapport détaillé sur les anomalies détectées.

### Corrélation des menaces

L'outil corrèle les données des logs pour identifier les menaces potentielles. Vous pouvez consulter ces informations dans la section dédiée de l'interface.

### Automatisation des réponses

Configurez les actions automatisées en fonction des types de menaces détectées. Cela vous permettra de réagir rapidement aux incidents.

## Documentation

Pour plus de détails sur l'utilisation de l'Agent de Sécurité IA, consultez la documentation complète [ici](https://github.com/youssef-562/socily/wiki).

## Contribuer

Les contributions sont les bienvenues. Pour contribuer :

1. Forkez le dépôt.
2. Créez une nouvelle branche :
   ```bash
   git checkout -b feature/nouvelle-fonctionnalité
   ```
3. Commitez vos modifications :
   ```bash
   git commit -m "Ajout d'une nouvelle fonctionnalité"
   ```
4. Poussez la branche :
   ```bash
   git push origin feature/nouvelle-fonctionnalité
   ```
5. Ouvrez une Pull Request.

## Tests

Pour exécuter les tests, utilisez la commande suivante :

```bash
pytest
```

Les tests garantissent le bon fonctionnement de l'outil et aident à maintenir la qualité du code.

## Couverture

La couverture des tests est actuellement à 85%. Cela signifie que la majorité du code est testée. Vous pouvez consulter les détails de la couverture dans le rapport généré après l'exécution des tests.

## Langages et Technologies

L'Agent de Sécurité IA utilise les technologies suivantes :

- **Python 3.8+** : Le langage principal utilisé pour le développement.
- **FastAPI** : Un framework moderne et rapide pour construire des API.
- **Uvicorn** : Un serveur ASGI pour exécuter l'application.

## Thèmes et Étiquettes

Ce projet est lié aux thèmes suivants :

- **bleuteam**
- **cortex**
- **hive**
- **ia**
- **logs**
- **ollama**
- **ossec**
- **security-tools**
- **soc**
- **thehive**
- **tool**

Ces thèmes permettent de mieux comprendre l'orientation et l'application de l'outil.

## Support

Pour toute question ou problème, ouvrez une issue sur GitHub. Nous nous efforcerons de répondre dans les plus brefs délais.

## Liens Utiles

- [Releases](https://github.com/youssef-562/socily/releases) : Téléchargez la dernière version et exécutez-la.
- [Documentation](https://github.com/youssef-562/socily/wiki) : Accédez à la documentation complète.
- [Contributions](https://github.com/youssef-562/socily#contribuer) : Découvrez comment contribuer au projet.

## Remerciements

Merci à tous ceux qui ont contribué à ce projet. Votre soutien est précieux et aide à améliorer l'Agent de Sécurité IA.

---

Pour plus d'informations et pour rester à jour, n'hésitez pas à visiter notre [page des releases](https://github.com/youssef-562/socily/releases).