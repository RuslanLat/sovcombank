from dataclasses import dataclass
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class PartnerId:
    id: Optional[int]
    partner: str
    data_connect: str
    addresse_id: int


@dataclass
class Partner:
    id: Optional[int]
    partner: str
    data_connect: str
    city: str
    addresse: str
    lat: float
    lon: float
    


class PartnerModel(db):
    __tablename__ = "partners"
    id = Column(Integer, primary_key=True)
    partner = Column(String, unique=True)
    data_connect = Column(String)
    addresse_id = Column(ForeignKey("addresses.id", ondelete="CASCADE"))
    addresse = relationship("AddresseModel", back_populates="partner")
    partner_param = relationship("PartnerParamModel", back_populates="partner")
    todo = relationship("ToDoModel", back_populates="partner")