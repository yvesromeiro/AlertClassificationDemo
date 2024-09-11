import uuid

from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Boolean, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PGUUID

@dataclass
class BaseClassification:
    db_name: str
    owner_email: str
    manager_email: str
    classification: str

@dataclass
class UserInformation:
    row_id: int
    user_id: str
    user_state: str
    user_manager: str

Base = declarative_base()

class ClassificationModel(Base):
    __tablename__ = 'data_classification'

    id = Column(PGUUID, primary_key=True, default=uuid.uuid4)
    db_name = Column(String)
    owner_email = Column(String)
    manager_email = Column(String)
    classification = Column(String)

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(PGUUID, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    birthdate = Column(String)
    document = Column(String)
    gender = Column(String)
    telephone = Column(String)
    is_active = Column(Boolean)
    yearly_income = Column(Integer)

class MarketingCampaign(Base):
    __tablename__ = 'marketing_campaigns'

    id = Column(String, primary_key=True)
    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    channel = Column(String)
    budget = Column(Float)
    target_audience = Column(String)