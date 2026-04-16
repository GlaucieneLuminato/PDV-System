from dotenv import load_dotenv
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()


def get_firestore_db():
    try:
        if not firebase_admin._apps:
            cred_json = os.getenv("FIREBASE_CREDENTIALS")

            if not cred_json:
                raise ValueError("FIREBASE_CREDENTIALS não encontrado")

            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)

            firebase_admin.initialize_app(cred)

        return firestore.client()

    except Exception as e:
        print("Erro ao conectar com Firebase:", e)
        return None