from sqlalchemy import Column, String, DateTime, JSON, Integer
from database.connection import Base
from datetime import datetime

class DesignSystem(Base):
    __tablename__ = "design_systems"
    
    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    version: str = Column(String)
    organization_id: str = Column(String)
    tokens: dict = Column(JSON)
    components: list = Column(JSON)
    created_at: datetime = Column(DateTime, default=datetime.now)
    updated_at: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class GeneratedScreen(Base):
    __tablename__ = "generated_screens"
    
    id: str = Column(String, primary_key=True)
    design_system_id: str = Column(String)
    prompt: str = Column(String)
    design_spec: dict = Column(JSON)
    code: str = Column(String)
    tokens_used: list = Column(JSON)
    components_used: list = Column(JSON)
    created_at: datetime = Column(DateTime, default=datetime.now)

class DesignToken(Base):
    __tablename__ = "design_tokens"
    
    id: str = Column(String, primary_key=True)
    design_system_id: str = Column(String)
    name: str = Column(String)
    type: str = Column(String)  # color, typography, spacing
    value: dict = Column(JSON)
    created_at: datetime = Column(DateTime, default=datetime.now)
    updated_at: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
