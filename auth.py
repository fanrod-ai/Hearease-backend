import jwt
import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from bson import ObjectId
import bcrypt
from database import get_db

# Create an APIRouter so main.py can import these routes easily
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Secret key to sign our JWT tokens (keep this secret!)
SECRET_KEY = "HearEase_Super_Secret_Access_Token_Key_2026"
ALGORITHM = "HS256"

# Fetch our MongoDB database instance
db = get_db()

# Define data shapes using Pydantic
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str:
    """Encrypts a plain text password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against an encrypted hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    """Generates a secure login token valid for 24 hours"""
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(user_data: UserRegister):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection is unavailable.")
    
    # Check if user email already exists in MongoDB
    existing_user = db.users.find_one({"email": user_data.email.lower()})
    if existing_user:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    
    # Securely encrypt password and structure user profile document
    new_user = {
        "name": user_data.name,
        "email": user_data.email.lower(),
        "password_hash": hash_password(user_data.password),
        "preferred_language": "English", # Default language setting
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    # Insert user profile straight into our MongoDB 'users' collection
    result = db.users.insert_one(new_user)
    
    # Create an automatic access token for immediate login after sign up
    token = create_access_token({"user_id": str(result.inserted_id), "email": user_data.email})
    
    return {
        "message": "Account created successfully!",
        "access_token": token,
        "token_type": "bearer",
        "user": {"name": user_data.name, "email": user_data.email}
    }


@router.post("/login")
def login(credentials: UserLogin):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection is unavailable.")
    
    # Look for the user profile inside our 'users' collection
    user = db.users.find_one({"email": credentials.email.lower()})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password credentials.")
    
    # Check if the typed password matches the encrypted database hash
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid email or password credentials.")
    
    # Generate secure sign-in token
    token = create_access_token({"user_id": str(user["_id"]), "email": user["email"]})
    
    return {
        "message": "Login successful!",
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
    }