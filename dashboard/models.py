from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class ActionType(enum.Enum):
    BLOCK_IP = "block_ip"
    SCAN_IP = "scan_ip"
    SCAN_DOMAIN = "scan_domain"
    SCAN_FILE = "scan_file"
    ALERT_SLACK = "alert_slack"
    ALERT_EMAIL = "alert_email"

class ActionStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ActionType))
    status = Column(Enum(ActionStatus), default=ActionStatus.PENDING)
    parameters = Column(JSON)
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    error_message = Column(String, nullable=True)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    severity = Column(String)
    source = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(JSON)
    artifacts = Column(JSON)

class LogAnalysis(Base):
    __tablename__ = "log_analyses"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    timeframe = Column(Integer)  # en minutes
    threats_detected = Column(JSON)
    recommendations = Column(JSON)
    statistics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow) 