import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

if not firebase_admin._apps:
    cred_json = os.environ.get("FIREBASE_CREDENTIALS")

    if not cred_json:
        raise ValueError("FIREBASE_CREDENTIALS não encontrado")

    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)

    firebase_admin.initialize_app(cred)

db = firestore.client()