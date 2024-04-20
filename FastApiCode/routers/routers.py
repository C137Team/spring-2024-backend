from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random
from models.models import UserProfile, db
#from fastapi.responses import FileResponse


router = APIRouter()


@router.post("/login")
def login(email: str):
    # Process user authentication
    return {"message": f"Logged in as {email}"}

@router.post("/profile")
def create_profile(user_profile: UserProfile):
    db.append(user_profile)
    return {"message": "User profile created successfully"}

@router.post("/agree_meeting/{username}")
def agree_meeting(username: str):
    for profile in db:
        if profile.username == username:
            profile.agreed_meeting = True
            return {"message": f"{username} agreed to the meeting"}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/select_meeting")
def select_meeting():
    # Filter users who agreed to the meeting
    meeting_candidates = [profile for profile in db if profile.agreed_meeting]

    if len(meeting_candidates) < 2:
        return {"message": "Not enough participants for a meeting."}

    # Randomly select two participants for the meeting
    meeting_participants = random.sample(meeting_candidates, 2)

    return {
        "message": "Meeting scheduled successfully",
        "participants": [participant.username for participant in meeting_participants]
    }

@router.post("/schedule_meeting/{username}")
def schedule_meeting(username: str, duration: str, meeting_type: str):
    for profile in db:
        if profile.username == username:
            profile.meeting_type = meeting_type
            return {"message": f"{username} scheduled a {duration} minute {meeting_type} meeting"}
    raise HTTPException(status_code=404, detail="User not found")
