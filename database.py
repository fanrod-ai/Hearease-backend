import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Your fully authorized, production-ready MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://HearEase293:HearEase293@cluster1.agnla3x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

try:
    # Initialize the MongoDB client connection
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Target our primary project database
    db = client.HearEase
    
    # Ping the deployment to verify a successful connection
    client.admin.command('ping')
    print("✨ Successfully connected to MongoDB Atlas Cloud Database!")
    
except ConnectionFailure:
    print("❌ Failed to connect to MongoDB Atlas. Verify your password, URI string, or IP whitelist access.")
    db = None

def get_db():
    """Helper function to fetch our database instance across other API modules"""
    return db