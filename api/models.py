from sqlalchemy import Column, String, Text
from pydantic import BaseModel, ConfigDict
from .database import Base
import uuid

class NoteTable(Base):
    __tablename__ = "notes" 

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    content = Column(Text)

class NoteInput(BaseModel):
    title: str
    content: str

class NoteOutput(NoteInput):
    id: str

    model_config = ConfigDict(from_attributes=True)