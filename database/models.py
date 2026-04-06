from pydantic import BaseModel
from sqlalchemy import JSON, Column, Integer, String

from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashedPassword = Column(String)
    points = Column(Integer, default=0)
    currentPoints = Column(Integer, default=0)
    weeklyGoalPercent = Column(Integer, default=0)
    history = Column(JSON, default=list)


class historyModel(BaseModel):
    title: str
    description: str
    timestamp: str
    logo: str
    points: int
   