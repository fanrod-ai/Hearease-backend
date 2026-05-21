from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HearEase AI Backend", version="1.0.0")

# Allow your Lovable frontend to talk to this backend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # We can restrict this to your Lovable URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "Online",
        "message": "Welcome to the HearEase Accessibility & AI Engine API",
        "supported_languages": ["English", "Kinyarwanda", "Français"]
    }