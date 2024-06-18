import base64
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models import User, Event, ETA
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Optional
from firebase_admin import firestore
from firebase_admin_setup import db

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class UserRequest(BaseModel):
    eventIds: List[str]
    friendIds: List[str]
    pfp: str
    username: str
    password: str

class EventRequest(BaseModel):
    eventId: str
    location: str
    title: str
    date: str
    time: str
    usersInvited: List[str]
    usersAttending: List[str]

class EventUpdateRequest(BaseModel):
    location: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    usersInvited: Optional[List[str]] = None
    usersAttending: Optional[List[str]] = None

class ETARequest(BaseModel):
    userId: str
    time: str
    distance: float
    eventId: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class FriendRequest(BaseModel):
    friend_username: str

class FriendResponse(BaseModel):
    friend_username: str
    accept: bool

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.collection('users').where('username', '==', token_data.username).stream()
    user = next(user, None)
    if user is None:
        raise credentials_exception
    return User.from_dict(user.to_dict())


'''
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    users = db.collection('users').where('username', '==', form_data.username).stream()
    user = next(users, None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    user_data = User.from_dict(user.to_dict())
    if not user_data.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    '''
@app.post("/token", response_model=Token)
async def login_for_access_token():
    form_data = OAuth2PasswordRequestForm(username="string", password="string")
    users = db.collection('users').where('username', '==', form_data.username).stream()
    user = next(users, None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    user_data = User.from_dict(user.to_dict())
    if not user_data.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=Token)
async def register(user_request: UserRequest):
    existing_user = db.collection('users').where('username', '==', user_request.username).stream()
    if any(existing_user):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    user = User(
        user_id=User.generate_unique_id(),
        event_ids=user_request.eventIds,
        friend_ids=user_request.friendIds,
        pfp=user_request.pfp,
        username=user_request.username,
        password=User.hash_password(user_request.password)
    )
    user.save()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/events", response_model=Event)
async def create_event(event_request: EventRequest, current_user: User = Depends(get_current_user)):
    event_id = Event.generate_unique_id()
    event = Event(
        event_id=event_id,
        user_id=current_user.user_id,
        location=event_request.location,
        title=event_request.title,
        date=event_request.date,
        time=event_request.time,
        users_invited=event_request.usersInvited,
        users_attending=event_request.usersAttending
    )
    event.save()
    
    # Update user's eventIds
    current_user.event_ids.append(event_id)
    current_user.save()

    return event

@app.delete("/events/{event_id}")
async def delete_event(event_id: str, current_user: User = Depends(get_current_user)):
    event = Event.get(event_id)
    if event:
        db.collection('events').document(event_id).delete()
        # Update user's eventIds
        current_user.event_ids.remove(event_id)
        current_user.save()
        return {"message": "Event deleted"}
    else:
        raise HTTPException(status_code=404, detail="Event not found")

@app.put("/events/{event_id}")
async def edit_event(event_id: str, event_update: EventUpdateRequest, current_user: User = Depends(get_current_user)):
    event = Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    updated_data = event.to_dict()
    if event_update.location is not None:
        updated_data["location"] = event_update.location
    if event_update.title is not None:
        updated_data["title"] = event_update.title
    if event_update.date is not None:
        updated_data["date"] = event_update.date
    if event_update.time is not None:
        updated_data["time"] = event_update.time
    if event_update.usersInvited is not None:
        updated_data["usersInvited"] = event_update.usersInvited
    if event_update.usersAttending is not None:
        updated_data["usersAttending"] = event_update.usersAttending
    
    db.collection('events').document(event_id).update(updated_data)
    return {"message": "Event updated"}

@app.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: str):
    event = Event.get(event_id)
    if event:
        return event
    else:
        raise HTTPException(status_code=404, detail="Event not found")

@app.post("/friend/request", response_model=dict)
async def send_friend_request(friend_request: FriendRequest, current_user: User = Depends(get_current_user)):
    friend_user = db.collection('users').where('username', '==', friend_request.friend_username).stream()
    friend_user = next(friend_user, None)
    if not friend_user:
        raise HTTPException(status_code=404, detail="Friend not found")
    
    friend_data = User.from_dict(friend_user.to_dict())
    if current_user.user_id in friend_data.friend_requests or current_user.user_id in friend_data.friend_ids:
        raise HTTPException(status_code=400, detail="Friend request already sent or already friends")

    friend_data.friend_requests.append(current_user.user_id)
    friend_data.save()

    return {"message": "Friend request sent"}

@app.get("/friend/requests", response_model=List[str])
async def get_friend_requests(current_user: User = Depends(get_current_user)):
    return current_user.friend_requests

@app.post("/friend/response", response_model=dict)
async def respond_to_friend_request(friend_response: FriendResponse, current_user: User = Depends(get_current_user)):
    # Debugging: Print current user's friend requests
    print(f"Current user ({current_user.username}) friend requests: {current_user.friend_requests}")

    friend_user = db.collection('users').where('username', '==', friend_response.friend_username).stream()
    friend_user = next(friend_user, None)
    if not friend_user:
        raise HTTPException(status_code=404, detail="Friend not found")
    
    friend_data = User.from_dict(friend_user.to_dict())
    print(f"Found friend user: {friend_data.username}, Friend requests: {friend_data.friend_requests}")

    if friend_data.user_id not in current_user.friend_requests:
        raise HTTPException(status_code=400, detail="No friend request found from this user")

    if friend_response.accept:
        current_user.friend_ids.append(friend_data.user_id)
        friend_data.friend_ids.append(current_user.user_id)
    current_user.friend_requests.remove(friend_data.user_id)
    current_user.save()
    friend_data.save()

    return {"message": "Friend request handled"}

@app.get("/user/events", response_model=List[str])
async def get_user_events(current_user: User = Depends(get_current_user)):
    return current_user.event_ids


@app.post("/profile/picture", response_model=dict)
async def add_profile_picture(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    file_content = await file.read()
    file_base64 = base64.b64encode(file_content).decode('utf-8')
    
    current_user.pfp = file_base64
    current_user.save()

    return {"message": "Profile picture added"}

@app.delete("/profile/picture", response_model=dict)
async def delete_profile_picture(current_user: User = Depends(get_current_user)):
    if not current_user.pfp:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    
    current_user.pfp = ""
    current_user.save()

    return {"message": "Profile picture deleted"}

@app.put("/profile/picture", response_model=dict)
async def edit_profile_picture(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if not current_user.pfp:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    
    file_content = await file.read()
    file_base64 = base64.b64encode(file_content).decode('utf-8')
    
    current_user.pfp = file_base64
    current_user.save()

    return {"message": "Profile picture updated"}

@app.get("/profile/picture", response_model=dict)
async def get_profile_picture(current_user: User = Depends(get_current_user)):
    if not current_user.pfp:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    
    return JSONResponse(content={"profile_picture": current_user.pfp})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
