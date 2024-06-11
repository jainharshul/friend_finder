from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from firebase_admin import firestore
from firebase_admin_setup import db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    user_id: str
    event_ids: List[str] = []
    friend_ids: List[str] = []
    friend_requests: List[str] = []
    pfp: str
    username: str
    password: str

    @staticmethod
    def from_dict(source):
        return User(
            user_id=source.get('userId'),
            event_ids=source.get('eventIds', []),
            friend_ids=source.get('friendIds', []),
            friend_requests=source.get('friendRequests', []),
            pfp=source.get('pfp'),
            username=source.get('username'),
            password=source.get('password')
        )

    def to_dict(self):
        return {
            'userId': self.user_id,
            'eventIds': self.event_ids,
            'friendIds': self.friend_ids,
            'friendRequests': self.friend_requests,
            'pfp': self.pfp,
            'username': self.username,
            'password': self.password
        }

    def save(self):
        db.collection('users').document(self.user_id).set(self.to_dict())

    @staticmethod
    def get(user_id):
        doc = db.collection('users').document(user_id).get()
        if doc.exists:
            return User.from_dict(doc.to_dict())
        else:
            return None

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4())

class Event(BaseModel):
    event_id: str
    user_id: str
    location: str
    title: str
    date: str
    time: str
    users_invited: List[str] = []
    users_attending: List[str] = []

    @staticmethod
    def from_dict(source):
        return Event(
            event_id=source.get('eventId'),
            user_id=source.get('userId'),
            location=source.get('location'),
            title=source.get('title'),
            date=source.get('date'),
            time=source.get('time'),
            users_invited=source.get('usersInvited', []),
            users_attending=source.get('usersAttending', [])
        )

    def to_dict(self):
        return {
            'eventId': self.event_id,
            'userId': self.user_id,
            'location': self.location,
            'title': self.title,
            'date': self.date,
            'time': self.time,
            'usersInvited': self.users_invited,
            'usersAttending': self.users_attending
        }

    def save(self):
        db.collection('events').document(self.event_id).set(self.to_dict())

    @staticmethod
    def get(event_id):
        doc = db.collection('events').document(event_id).get()
        if doc.exists:
            return Event.from_dict(doc.to_dict())
        else:
            return None

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4())

class ETA(BaseModel):
    user_id: str
    time: str
    distance: float
    event_id: str

    @staticmethod
    def from_dict(source):
        return ETA(
            user_id=source.get('userId'),
            time=source.get('time'),
            distance=source.get('distance'),
            event_id=source.get('eventId')
        )

    def to_dict(self):
        return {
            'userId': self.user_id,
            'time': self.time,
            'distance': self.distance,
            'eventId': self.event_id
        }

    def save(self):
        db.collection('etas').add(self.to_dict())

    @staticmethod
    def get(eta_id):
        doc = db.collection('etas').document(eta_id).get()
        if doc.exists:
            return ETA.from_dict(doc.to_dict())
        else:
            return None
