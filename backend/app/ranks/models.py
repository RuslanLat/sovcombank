from dataclasses import dataclass
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db



@dataclass
class Rank:
    id: Optional[int]
    rank: str


class RankModel(db):
    __tablename__ = "ranks"
    id = Column(Integer, primary_key=True)
    rank = Column(String, unique=True)
    user_job = relationship("UserJobModel", back_populates="rank")
