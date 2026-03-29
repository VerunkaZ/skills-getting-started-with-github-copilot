"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Strategy sessions, casual play, and tournament prep",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["morgan@mergington.edu"]
    },
    "Programming Class": {
        "description": "Hands-on coding lessons in Python and web development",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["sam@mergington.edu"]
    },
    "Gym Class": {
        "description": "Fitness training, sports drills, and conditioning",
        "schedule": "Wednesdays and Fridays, 2:30 PM - 4:00 PM",
        "max_participants": 25,
        "participants": ["jessica@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team practice, drills, and friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Lap swimming, water workouts, and swim technique training",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["nina@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and mixed-media workshops",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["lisa@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, improvisation, and stage performance practice",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["jordan@mergington.edu"]
    },
    "Debate Society": {
        "description": "Research, argument practice, and competitive debate events",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["maria@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "STEM challenges, experiments, and competition prep",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 14,
        "participants": ["dylan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    if len(activity["participants"]) < activity["max_participants"]:
        activity["participants"].append(email)
        return {"message": f"Signed up {email} for {activity_name}"}
    else:
        raise HTTPException(status_code=400, detail="Activity is full") 