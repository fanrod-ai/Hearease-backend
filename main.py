from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_db

app = FastAPI(title="HearEase AI Backend", version="1.0.0")

# Enable secure communication between your Lovable frontend and this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the cloud database attachment
db = get_db()

@app.get("/")
def home():
    db_status = "Connected" if db is not None else "Disconnected"
    return {
        "status": "Online",
        "database_connection": db_status,
        "message": "Welcome to the HearEase Accessibility & AI Engine API",
        "supported_languages": ["English", "Kinyarwanda", "Français"]
    }