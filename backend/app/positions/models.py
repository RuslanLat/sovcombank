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
class Position:
    id: Optional[int]
    position: str


class PositionModel(db):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    position = Column(String, unique=True)
    user_job = relationship("UserJobModel", back_populates="position")
