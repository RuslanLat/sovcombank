from dataclasses import dataclass
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Boolean,
    String,
    Float
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db

@dataclass
class ToDoId:
    id: Optional[int]
    user_id: int
    office_id: int
    partner_id: int
    problem_id: str
    queue: int
    message: str
    status: bool = False
    duration: float = 0.0
    length: float = 0.0
    

@dataclass
class ToDo:
    id: Optional[int]
    surname: str
    name: str
    patronymic: str
    city: str
    addresse: str
    lon: float
    lat: float
    partner: str
    partner_city: str
    partner_addresse: str
    partner_lon: float
    partner_lat: float
    problem: str
    queue: int
    status: bool
    message: str
    duration: float
    length: float
    

class ToDoModel(db):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    office_id = Column(ForeignKey("offices.id", ondelete="CASCADE"))
    partner_id = Column(ForeignKey("partners.id", ondelete="CASCADE"))
    problem_id = Column(ForeignKey("problems.id", ondelete="CASCADE"))
    queue = Column(Integer)
    message = Column(String)
    status = Column(Boolean, default=False)
    duration = Column(Float)
    length = Column(Float)
    user = relationship("UserModel", back_populates="todo") #, back_populates="todo"
    partner = relationship("PartnerModel", back_populates="todo") #, back_populates="todo"
    problem = relationship("ProblemModel", back_populates="todo") # , back_populates="todo"
    office = relationship("OfficeModel", back_populates="todo")
