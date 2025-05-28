from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import json

from .database import get_db
from .models import Action, Alert, LogAnalysis, ActionType, ActionStatus

app = FastAPI(title="SOCily Dashboard API")

@app.get("/api/actions")
async def get_actions(
    db: Session = Depends(get_db),
    action_type: Optional[ActionType] = None,
    status: Optional[ActionStatus] = None,
    limit: int = 100
):
    """Récupère la liste des actions avec filtres optionnels."""
    query = db.query(Action)
    
    if action_type:
        query = query.filter(Action.type == action_type)
    if status:
        query = query.filter(Action.status == status)
        
    actions = query.order_by(Action.created_at.desc()).limit(limit).all()
    return actions

@app.get("/api/actions/stats")
async def get_action_stats(db: Session = Depends(get_db)):
    """Récupère les statistiques des actions."""
    # Actions par type
    actions_by_type = db.query(
        Action.type, 
        db.func.count(Action.id)
    ).group_by(Action.type).all()
    
    # Actions par statut
    actions_by_status = db.query(
        Action.status,
        db.func.count(Action.id)
    ).group_by(Action.status).all()
    
    # Actions par jour
    actions_by_day = db.query(
        db.func.date(Action.created_at),
        db.func.count(Action.id)
    ).group_by(db.func.date(Action.created_at)).all()
    
    return {
        "by_type": dict(actions_by_type),
        "by_status": dict(actions_by_status),
        "by_day": dict(actions_by_day)
    }

@app.get("/api/alerts")
async def get_alerts(
    db: Session = Depends(get_db),
    severity: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 100
):
    """Récupère la liste des alertes avec filtres optionnels."""
    query = db.query(Alert)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    if source:
        query = query.filter(Alert.source == source)
        
    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
    return alerts

@app.get("/api/alerts/stats")
async def get_alert_stats(db: Session = Depends(get_db)):
    """Récupère les statistiques des alertes."""
    # Alertes par sévérité
    alerts_by_severity = db.query(
        Alert.severity,
        db.func.count(Alert.id)
    ).group_by(Alert.severity).all()
    
    # Alertes par source
    alerts_by_source = db.query(
        Alert.source,
        db.func.count(Alert.id)
    ).group_by(Alert.source).all()
    
    # Alertes par jour
    alerts_by_day = db.query(
        db.func.date(Alert.created_at),
        db.func.count(Alert.id)
    ).group_by(db.func.date(Alert.created_at)).all()
    
    return {
        "by_severity": dict(alerts_by_severity),
        "by_source": dict(alerts_by_source),
        "by_day": dict(alerts_by_day)
    }

@app.get("/api/analyses")
async def get_analyses(
    db: Session = Depends(get_db),
    source: Optional[str] = None,
    limit: int = 100
):
    """Récupère la liste des analyses de logs."""
    query = db.query(LogAnalysis)
    
    if source:
        query = query.filter(LogAnalysis.source == source)
        
    analyses = query.order_by(LogAnalysis.created_at.desc()).limit(limit).all()
    return analyses

@app.get("/api/analyses/stats")
async def get_analysis_stats(db: Session = Depends(get_db)):
    """Récupère les statistiques des analyses."""
    # Analyses par source
    analyses_by_source = db.query(
        LogAnalysis.source,
        db.func.count(LogAnalysis.id)
    ).group_by(LogAnalysis.source).all()
    
    # Menaces détectées
    all_threats = []
    analyses = db.query(LogAnalysis).all()
    for analysis in analyses:
        if analysis.threats_detected:
            all_threats.extend(analysis.threats_detected)
    
    threats_by_type = {}
    for threat in all_threats:
        threat_type = threat.get("type", "unknown")
        threats_by_type[threat_type] = threats_by_type.get(threat_type, 0) + 1
    
    return {
        "by_source": dict(analyses_by_source),
        "threats_by_type": threats_by_type
    }

@app.get("/api/dashboard/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Récupère un résumé des données pour le dashboard."""
    # Actions récentes
    recent_actions = db.query(Action).order_by(
        Action.created_at.desc()
    ).limit(5).all()
    
    # Alertes récentes
    recent_alerts = db.query(Alert).order_by(
        Alert.created_at.desc()
    ).limit(5).all()
    
    # Statistiques globales
    total_actions = db.query(Action).count()
    total_alerts = db.query(Alert).count()
    total_analyses = db.query(LogAnalysis).count()
    
    # Actions en cours
    pending_actions = db.query(Action).filter(
        Action.status.in_([ActionStatus.PENDING, ActionStatus.IN_PROGRESS])
    ).count()
    
    return {
        "recent_actions": recent_actions,
        "recent_alerts": recent_alerts,
        "total_actions": total_actions,
        "total_alerts": total_alerts,
        "total_analyses": total_analyses,
        "pending_actions": pending_actions
    } 