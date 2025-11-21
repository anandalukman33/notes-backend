from pydantic import BaseModel, Field
from typing import Optional
import uuid

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, description="Judul catatan")
    content: str = Field(..., description="Isi catatan")

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: str

    class Config:
        from_attributes = True