from dataclasses import dataclass
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db



@dataclass
class OfficeId:
    id: Optional[int]
    addresse_id: int


@dataclass
class Office:
    id: Optional[int]
    city: str
    addresse: str
    lat: float
    lon: float
    

class OfficeModel(db):
    __tablename__ = "offices"
    id = Column(Integer, primary_key=True)
    addresse_id = Column(ForeignKey("addresses.id", ondelete="CASCADE"))
    user_job = relationship("UserJobModel", back_populates="office")
    addresse = relationship("AddresseModel", back_populates="office")
    todo = relationship("ToDoModel", back_populates="office")