from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.get("/notes", response_model=List[models.NoteOutput])
def get_notes(db: Session = Depends(database.get_db)):
    return db.query(models.NoteTable).all()

@app.post("/notes", response_model=models.NoteOutput)
def create_note(note: models.NoteInput, db: Session = Depends(database.get_db)):
    new_note = models.NoteTable(
        title=note.title,
        content=note.content
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/notes/{note_id}", response_model=models.NoteOutput)
def update_note(note_id: str, note: models.NoteInput, db: Session = Depends(database.get_db)):
    db_note = db.query(models.NoteTable).filter(models.NoteTable.id == note_id).first()
    
    if not db_note:
        raise HTTPException(status_code=404, detail="Catatan tidak ditemukan")
    
    db_note.title = note.title
    db_note.content = note.content
    
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: str, db: Session = Depends(database.get_db)):
    db_note = db.query(models.NoteTable).filter(models.NoteTable.id == note_id).first()
    
    if not db_note:
        raise HTTPException(status_code=404, detail="Catatan tidak ditemukan")
    
    db.delete(db_note)
    db.commit()
    return {"message": "Berhasil dihapus"}