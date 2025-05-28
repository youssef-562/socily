from database import SessionLocal, init_db
from models import Action, Alert, LogAnalysis, ActionType, ActionStatus
from datetime import datetime, timedelta
import json

def create_test_data():
    db = SessionLocal()
    try:
        # Créer des actions de test
        actions = [
            Action(
                type=ActionType.BLOCK_IP,
                status=ActionStatus.COMPLETED,
                parameters={"ip": "192.168.1.100", "reason": "Tentative de brute force"},
                result={"blocked": True},
                created_at=datetime.utcnow() - timedelta(hours=2)
            ),
            Action(
                type=ActionType.SCAN_IP,
                status=ActionStatus.IN_PROGRESS,
                parameters={"ip": "10.0.0.1"},
                created_at=datetime.utcnow() - timedelta(hours=1)
            ),
            Action(
                type=ActionType.ALERT_SLACK,
                status=ActionStatus.COMPLETED,
                parameters={"message": "Détection d'une activité suspecte"},
                result={"sent": True},
                created_at=datetime.utcnow() - timedelta(minutes=30)
            )
        ]
        db.add_all(actions)

        # Créer des alertes de test
        alerts = [
            Alert(
                title="Tentative de brute force détectée",
                description="Plusieurs tentatives de connexion échouées",
                severity="high",
                source="firewall",
                status="open",
                tags=["brute-force", "ssh"],
                artifacts={"ip": "192.168.1.100"},
                created_at=datetime.utcnow() - timedelta(hours=2)
            ),
            Alert(
                title="Port scan détecté",
                description="Scan de ports sur le serveur web",
                severity="medium",
                source="ids",
                status="investigating",
                tags=["port-scan", "reconnaissance"],
                artifacts={"ip": "10.0.0.1"},
                created_at=datetime.utcnow() - timedelta(hours=1)
            )
        ]
        db.add_all(alerts)

        # Créer des analyses de test
        analyses = [
            LogAnalysis(
                source="firewall",
                timeframe=60,
                threats_detected=[
                    {"type": "brute-force", "severity": "high"},
                    {"type": "port-scan", "severity": "medium"}
                ],
                recommendations=[
                    "Renforcer la politique de mots de passe",
                    "Mettre en place un système de détection d'intrusion"
                ],
                statistics={
                    "total_events": 1000,
                    "suspicious_events": 50,
                    "blocked_events": 30
                },
                created_at=datetime.utcnow() - timedelta(hours=2)
            ),
            LogAnalysis(
                source="ids",
                timeframe=30,
                threats_detected=[
                    {"type": "malware", "severity": "critical"},
                    {"type": "data-exfiltration", "severity": "high"}
                ],
                recommendations=[
                    "Mettre à jour les signatures antivirus",
                    "Renforcer la surveillance des transferts de données"
                ],
                statistics={
                    "total_events": 500,
                    "suspicious_events": 20,
                    "blocked_events": 15
                },
                created_at=datetime.utcnow() - timedelta(hours=1)
            )
        ]
        db.add_all(analyses)

        db.commit()
        print("Données de test créées avec succès !")
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la création des données de test : {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    init_db()
    print("Création des données de test...")
    create_test_data() 