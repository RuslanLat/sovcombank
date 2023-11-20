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
class UserJobId:
    id: Optional[int]
    user_id: int
    office_id: int
    position_id: int
    rank_id: int
    

@dataclass
class UserJob:
    id: Optional[int]
    surname: str
    name: str
    patronymic: str
    position: str
    rank: str
    city: str
    addresse: str
    lon: float
    lat: float
    

class UserJobModel(db):
    __tablename__ = "user_jobs"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    office_id = Column(ForeignKey("offices.id", ondelete="CASCADE"))
    position_id = Column(ForeignKey("positions.id", ondelete="CASCADE"))
    rank_id = Column(ForeignKey("ranks.id", ondelete="CASCADE"))
    user = relationship("UserModel", back_populates="user_job")
    office = relationship("OfficeModel", back_populates="user_job")
    rank = relationship("RankModel", back_populates="user_job")
    position = relationship("PositionModel", back_populates="user_job")
