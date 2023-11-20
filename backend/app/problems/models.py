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
class Problem:
    id: Optional[int]
    problem_type: int
    problem: str
    priority: str
    lead_time: str
    condition_one: str
    condition_two: str
    rank: str


class ProblemModel(db):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True)
    problem_type = Column(Integer, unique=True)
    problem = Column(String, unique=True)
    priority = Column(String)
    lead_time = Column(String)
    condition_one = Column(String)
    condition_two = Column(String)
    rank = Column(String)
    todo = relationship("ToDoModel", back_populates="problem")