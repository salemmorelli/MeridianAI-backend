# ml-backend/models.py
from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Session(Base):
    __tablename__ = "sessions"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(String, nullable=False, index=True)
    symptom     = Column(String, nullable=False)
    region      = Column(String, nullable=False)
    point_code  = Column(String, nullable=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

class Feedback(Base):
    __tablename__ = "feedback"

    id                 = Column(Integer, primary_key=True, index=True)
    session_id         = Column(String, nullable=False, index=True)
    symptom            = Column(String, nullable=False)
    region             = Column(String, nullable=False)
    selected_meridian  = Column(String, nullable=True)
    duration_minutes   = Column(Integer, nullable=False)
    recommended_point  = Column(String, nullable=False)
    helped             = Column(Boolean, nullable=False)
    created_at         = Column(DateTime(timezone=True), server_default=func.now())

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id               = Column(Integer, primary_key=True, index=True)
    version          = Column(String, nullable=False)
    roc_auc          = Column(Float, nullable=True)
    training_samples = Column(Integer, nullable=True)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())