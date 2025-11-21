import uuid
from typing import List, Optional
from .models import Note, NoteCreate

fake_db: List[Note] = []

class NoteService:
    def get_all(self) -> List[Note]:
        return fake_db

    def create(self, note_in: NoteCreate) -> Note:
        new_note = Note(
            id=str(uuid.uuid4()),
            title=note_in.title,
            content=note_in.content
        )
        fake_db.append(new_note)
        return new_note

    def update(self, note_id: str, note_in: NoteCreate) -> Optional[Note]:
        for i, note in enumerate(fake_db):
            if note.id == note_id:
                updated_note = Note(
                    id=note_id,
                    title=note_in.title,
                    content=note_in.content
                )
                fake_db[i] = updated_note
                return updated_note
        return None

    def delete(self, note_id: str) -> bool:
        global fake_db
        initial_len = len(fake_db)
        fake_db = [n for n in fake_db if n.id != note_id]
        return len(fake_db) < initial_len

note_service = NoteService()