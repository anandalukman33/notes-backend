from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import List
from . import models, database, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(root_path="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.UserTable).filter(models.UserTable.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@app.post("/register", status_code=201)
def register(user: models.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.UserTable).filter(models.UserTable.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.UserTable(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login", response_model=models.Token)
def login(user: models.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.UserTable).filter(models.UserTable.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = auth.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/notes", response_model=List[models.NoteOutput])
def get_notes(
    db: Session = Depends(database.get_db), 
    current_user: models.UserTable = Depends(get_current_user)
):
    return db.query(models.NoteTable).filter(models.NoteTable.owner_id == current_user.id).all()

@app.post("/notes", response_model=models.NoteOutput)
def create_note(
    note: models.NoteInput, 
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user)
):
    new_note = models.NoteTable(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/notes/{note_id}", response_model=models.NoteOutput)
def update_note(
    note_id: str, 
    note: models.NoteInput, 
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user)
):
    db_note = db.query(models.NoteTable).filter(
        models.NoteTable.id == note_id,
        models.NoteTable.owner_id == current_user.id
    ).first()
    
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found or access denied")
    
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}")
def delete_note(
    note_id: str, 
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user)
):
    db_note = db.query(models.NoteTable).filter(
        models.NoteTable.id == note_id,
        models.NoteTable.owner_id == current_user.id
    ).first()
    
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(db_note)
    db.commit()
    return {"message": "Deleted"}


@app.get("/schedules", response_model=List[models.ScheduleOutput])
def get_schedules(
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user)
):
    return db.query(models.ScheduleTable).filter(models.ScheduleTable.owner_id == current_user.id).all()

@app.post("/schedules", response_model=models.ScheduleOutput)
def create_schedule(
    schedule: models.ScheduleInput,
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user)
):
    new_schedule = models.ScheduleTable(
        title=schedule.title,
        alarm_time=schedule.alarm_time,
        owner_id=current_user.id
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

@app.delete("/schedules/{schedule_id}")
def delete_schedule(
    schedule_id: str,
    db: Session = Depends(database.get_db),
    current_user: models.UserTable = Depends(get_current_user)
):
    db_schedule = db.query(models.ScheduleTable).filter(
        models.ScheduleTable.id == schedule_id, 
        models.ScheduleTable.owner_id == current_user.id
    ).first()
    
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
        
    db.delete(db_schedule)
    db.commit()
    return {"message": "Deleted"}