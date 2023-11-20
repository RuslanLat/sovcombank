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
class Product:
    id: Optional[int]
    product: str
    description: str


class ProductModel(db):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    product = Column(String, unique=True)
    description = Column(String)
    #todo = relationship("ToDoModel", back_populates="product")