from firebase_admin import firestore
from firebase_admin_setup import db

class User:
    def __init__(self, user_id, event_ids, friend_ids, pfp, username, password):
        self.user_id = user_id
        self.event_ids = event_ids
        self.friend_ids = friend_ids
        self.pfp = pfp
        self.username = username
        self.password = password

    @staticmethod
    def from_dict(source):
        return User(
            source.get('userId'),
            source.get('eventIds', []),
            source.get('friendIds', []),
            source.get('pfp'),
            source.get('username'),
            source.get('password')
        )

    def to_dict(self):
        return {
            'userId': self.user_id,
            'eventIds': self.event_ids,
            'friendIds': self.friend_ids,
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


class Event:
    def __init__(self, event_id, location, title, date, time, users_invited, users_attending):
        self.event_id = event_id
        self.location = location
        self.title = title
        self.date = date
        self.time = time
        self.users_invited = users_invited
        self.users_attending = users_attending

    @staticmethod
    def from_dict(source):
        return Event(
            source.get('eventId'),
            source.get('location'),
            source.get('title'),
            source.get('date'),
            source.get('time'),
            source.get('usersInvited', []),
            source.get('usersAttending', [])
        )

    def to_dict(self):
        return {
            'eventId': self.event_id,
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


class ETA:
    def __init__(self, user_id, time, distance, event_id):
        self.user_id = user_id
        self.time = time
        self.distance = distance
        self.event_id = event_id

    @staticmethod
    def from_dict(source):
        return ETA(
            source.get('userId'),
            source.get('time'),
            source.get('distance'),
            source.get('eventId')
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