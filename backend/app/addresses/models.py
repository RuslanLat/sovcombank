from dataclasses import dataclass
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class Addresse:
    id: Optional[int]
    city: str
    addresse: str
    lat: float
    lon: float
    

class AddresseModel(db):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    city = Column(String)
    addresse = Column(String, unique=True)
    lat = Column(Float)
    lon = Column(Float)    
    office = relationship("OfficeModel", back_populates="addresse")
    partner = relationship("PartnerModel", back_populates="addresse")
