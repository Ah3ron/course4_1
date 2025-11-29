"""
SQLAlchemy модели для базы данных.
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.database import Base


class CompanyAssessment(Base):
    """Модель для оценки кредитного риска компании."""
    
    __tablename__ = "company_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    assessment_date = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Исходные данные для модели Альтмана
    current_assets = Column(Float, nullable=False)
    current_liabilities = Column(Float, nullable=False)
    debt_capital = Column(Float, nullable=False)
    liabilities = Column(Float, nullable=False)
    
    # Исходные данные для модели Таффлера
    sales_profit = Column(Float, nullable=False)
    short_term_liabilities = Column(Float, nullable=False)
    long_term_liabilities = Column(Float, nullable=False)
    total_assets = Column(Float, nullable=False)
    sales = Column(Float, nullable=False)
    
    # Результаты модели Альтмана
    altman_z_score = Column(Float, nullable=False)
    altman_risk_level = Column(String(20), nullable=False)
    altman_recommendation = Column(Text, nullable=False)
    
    # Результаты модели Таффлера
    taffler_z_score = Column(Float, nullable=False)
    taffler_risk_level = Column(String(20), nullable=False)
    taffler_recommendation = Column(Text, nullable=False)
    
    # Комбинированный результат
    combined_risk_level = Column(String(20), nullable=False)
    combined_recommendation = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, server_default=func.now())


class IndividualAssessment(Base):
    """Модель для оценки кредитного риска физического лица."""
    
    __tablename__ = "individual_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    assessment_date = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Исходные данные
    monthly_income = Column(Float, nullable=False)
    monthly_expenses = Column(Float, nullable=False)
    credit_amount = Column(Float, nullable=False)
    credit_history_score = Column(Float, nullable=False)
    has_collateral = Column(Boolean, nullable=False, default=False)
    employment_years = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    
    # Результаты оценки
    credit_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    recommendation = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, server_default=func.now())

