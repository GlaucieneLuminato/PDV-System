from dotenv import load_dotenv
import os

load_dotenv()




import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

cred_json = os.getenv("FIREBASE_CREDENTIALS")

if not cred_json:
    raise ValueError("FIREBASE_CREDENTIALS não encontrado")

cred_dict = json.loads(cred_json)

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

try:
    db.collection("ping").document("init").set({"status": "ok"})
except:
    pass