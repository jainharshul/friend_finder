# firebase_admin_setup.py
import firebase_admin
from firebase_admin import credentials, firestore

# Replace 'path/to/serviceAccountKey.json' with the actual path to the downloaded JSON file
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
