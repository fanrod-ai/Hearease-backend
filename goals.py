import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from database import get_db

router = APIRouter(prefix="/goals", tags=["Accessible Goal Planner"])
db = get_db()

# Data schema for creating an accessible goal milestone
class GoalCreate(BaseModel):
    user_id: str
    title: str
    target_date: str
    sensory_alert: str # Options: "Visual Flash", "Haptic Vibration", "Audio Tone", "None"
    category: str = "General" # e.g., "Speech", "Learning", "Daily Task"

@router.post("/create")
def create_goal(goal: GoalCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection is offline.")
    
    new_goal = {
        "user_id": goal.user_id,
        "title": goal.title,
        "target_date": goal.target_date,
        "sensory_alert": goal.sensory_alert,
        "category": goal.category,
        "completed": False,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    # MongoDB creates the 'goals' collection implicitly on the fly!
    result = db.goals.insert_one(new_goal)
    return {"message": "Goal milestone locked into your tracker!", "goal_id": str(result.inserted_id)}

@router.get("/user/{user_id}")
def get_user_goals(user_id: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection is offline.")
    
    cursor = db.goals.find({"user_id": user_id})
    goals_list = []
    
    for goal in cursor:
        goals_list.append({
            "id": str(goal["_id"]),
            "title": goal["title"],
            "target_date": goal["target_date"],
            "sensory_alert": goal["sensory_alert"],
            "category": goal["category"],
            "completed": goal["completed"],
            "created_at": goal["created_at"]
        })
        
    return goals_list

@router.put("/complete/{goal_id}")
def complete_goal(goal_id: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection is offline.")
    
    # Toggle the goal completion checkbox status in MongoDB
    result = db.goals.update_one(
        {"_id": ObjectId(goal_id)},
        {"$set": {"completed": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Target milestone variant not found.")
        
    return {"message": "Milestone successfully checked off! Triggering positive accessibility feedback."}