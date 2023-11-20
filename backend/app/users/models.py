from dataclasses import dataclass
from hashlib import sha256
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
class UserLogin:
    id: Optional[int]
    login: str
    password: Optional[str] = None

    def is_password_valid(self, password: str) -> bool:
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["UserLogin"]:
        return cls(id=session["user"]["id"], login=session["user"]["login"])


@dataclass
class User:
    id: Optional[int]
    surname: str
    name: str
    patronymic: str
    



class UserLoginModel(db):
    __tablename__ = "user_logins"
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    user = relationship("UserModel", back_populates="user_login")


class UserModel(db):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_login_id = Column(ForeignKey("user_logins.id", ondelete="CASCADE"))
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    user_login = relationship(UserLoginModel, back_populates="user")
    user_job = relationship("UserJobModel", back_populates="user")
    todo = relationship("ToDoModel", back_populates="user")