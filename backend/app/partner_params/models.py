from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class PartnerParamId:
    id: Optional[int]
    created_at: datetime
    partner_id: int
    delivered: bool
    num_days: int
    num_applications: int
    num_cards: int
    


@dataclass
class PartnerParam:
    id: Optional[int]
    created_at: datetime
    partner: str
    city: str
    addresse: str
    data_connect: str
    delivered: bool
    num_days: int
    num_applications: int
    num_cards: int


class PartnerParamModel(db):
    __tablename__ = "partner_params"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    partner_id = Column(ForeignKey("partners.id", ondelete="CASCADE"))
    delivered = Column(Boolean)
    num_days = Column(Integer)
    num_applications = Column(Integer)
    num_cards = Column(Integer)
    partner = relationship("PartnerModel", back_populates="partner_param")

