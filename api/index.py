from fastapi import FastAPI, HTTPException, status
from typing import List
from .models import Note, NoteCreate
from .service import note_service

app = FastAPI(title="Notes API 2025", docs_url="/docs", redoc_url=None)

@app.get("/notes", response_model=List[Note])
def read_notes():
    return note_service.get_all()

@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate):
    return note_service.create(note)

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: str, note: NoteCreate):
    updated = note_service.update(note_id, note)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str):
    success = note_service.delete(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return