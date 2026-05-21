from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_db
import auth
import notes # 1. Import our fresh notes file

app = FastAPI(title="HearEase AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = get_db()

# Mount our modular component sub-routers onto the main engine
app.include_router(auth.router)
app.include_router(notes.router) # 2. Register the notes paths

@app.get("/")
def home():
    db_status = "Connected" if db is not None else "Disconnected"
    return {
        "status": "Online",
        "database_connection": db_status,
        "message": "Welcome to the HearEase Accessibility & AI Engine API"
    }