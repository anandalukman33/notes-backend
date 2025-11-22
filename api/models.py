from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from .database import Base
from datetime import datetime
import uuid

class ScheduleTable(Base):
    __tablename__ = "schedules"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    alarm_time = Column(String)
    owner_id = Column(String, ForeignKey("users.id"))
    
    owner = relationship("UserTable")

class UserTable(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    notes = relationship("NoteTable", back_populates="owner")

class NoteTable(Base):
    __tablename__ = "notes"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    content = Column(Text)
    owner_id = Column(String, ForeignKey("users.id"))
    
    owner = relationship("UserTable", back_populates="notes")

class ScheduleInput(BaseModel):
    title: str
    alarm_time: str

class ScheduleOutput(ScheduleInput):
    id: str
    owner_id: str
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class NoteInput(BaseModel):
    title: str
    content: str

class NoteOutput(NoteInput):
    id: str
    owner_id: str
    model_config = ConfigDict(from_attributes=True)