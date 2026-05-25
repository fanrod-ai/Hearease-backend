import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Read the connection string directly from Render's environment
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("❌ Critical Error: MONGO_URI environment variable is missing from system!")
    db = None
else:
    try:
        # Initialize connection with a standard timeout
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client.HearEase
        
        # Test connection
        client.admin.command('ping')
        print("✨ Successfully connected to MongoDB Atlas Cloud Database!")
    except ConnectionFailure:
        print("❌ Failed to connect to MongoDB Atlas. Check your string credentials.")
        db = None

def get_db():
    return db