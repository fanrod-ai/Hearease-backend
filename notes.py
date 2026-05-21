import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from bson import ObjectId
from database import get_db

router = APIRouter(prefix="/notes", tags=["Secure Notes Vault"])
db = get_db()

# Data validation model for creating a note
class NoteCreate(BaseModel):
    user_id: str
    title: str       # This will receive the encrypted string from your frontend
    content: str     # This will receive the encrypted string from your frontend
    category: str = "General"
    pin_locked: bool = False

@router.post("/save")
def save_note(note: NoteCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection is offline.")
    
    new_note = {
        "user_id": note.user_id,
        "title": note.title,
        "content": note.content,
        "category": note.category,
        "pin_locked": note.pin_locked,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    # MongoDB will automatically spin up the 'secret_notes' collection on first insertion!
    result = db.secret_notes.insert_one(new_note)
    return {"message": "Note locked securely inside the vault!", "note_id": str(result.inserted_id)}

@router.get("/user/{user_id}")
def get_user_notes(user_id: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection is offline.")
    
    # Pull all documents belonging strictly to the requested user ID
    cursor = db.secret_notes.find({"user_id": user_id})
    notes_list = []
    
    for note in cursor:
        notes_list.append({
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"],
            "category": note["category"],
            "pin_locked": note["pin_locked"],
            "created_at": note["created_at"]
        })
        
    return notes_list

@router.delete("/delete/{note_id}")
def delete_note(note_id: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection is offline.")
    
    # Delete the target document matching the distinct MongoDB unique ID
    result = db.secret_notes.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note variant not found.")
        
    return {"message": "Note permanently erased from vault."}