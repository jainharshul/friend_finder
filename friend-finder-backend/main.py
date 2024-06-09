# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import User, Event, ETA

app = FastAPI()

class UserRequest(BaseModel):
    userId: str
    eventIds: list
    friendIds: list
    pfp: str
    username: str
    password: str

class EventRequest(BaseModel):
    eventId: str
    location: str
    title: str
    date: str
    time: str
    usersInvited: list
    usersAttending: list

class ETARequest(BaseModel):
    userId: str
    time: str
    distance: float
    eventId: str

@app.post("/users")
async def create_user(user_request: UserRequest):
    user = User(
        user_id=user_request.userId,
        event_ids=user_request.eventIds,
        friend_ids=user_request.friendIds,
        pfp=user_request.pfp,
        username=user_request.username,
        password=user_request.password
    )
    user.save()
    return user.to_dict()

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = User.get(user_id)
    if user:
        return user.to_dict()
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/events")
async def create_event(event_request: EventRequest):
    event = Event(
        event_id=event_request.eventId,
        location=event_request.location,
        title=event_request.title,
        date=event_request.date,
        time=event_request.time,
        users_invited=event_request.usersInvited,
        users_attending=event_request.usersAttending
    )
    event.save()
    return event.to_dict()

@app.get("/events/{event_id}")
async def get_event(event_id: str):
    event = Event.get(event_id)
    if event:
        return event.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Event not found")

@app.post("/etas")
async def create_eta(eta_request: ETARequest):
    eta = ETA(
        user_id=eta_request.userId,
        time=eta_request.time,
        distance=eta_request.distance,
        event_id=eta_request.eventId
    )
    eta.save()
    return eta.to_dict()

@app.get("/etas/{eta_id}")
async def get_eta(eta_id: str):
    eta = ETA.get(eta_id)
    if eta:
        return eta.to_dict()
    else:
        raise HTTPException(status_code=404, detail="ETA not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
