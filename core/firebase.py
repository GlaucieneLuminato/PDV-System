from dotenv import load_dotenv
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))


def get_firestore_db():
    try:
        if not firebase_admin._apps:
            cred_json = os.getenv("FIREBASE_CREDENTIALS")

            if not cred_json:
                raise Exception("FIREBASE_CREDENTIALS não encontrado")

            cred_dict = json.loads(cred_json)

            cred = credentials.Certificate(cred_dict)

            firebase_admin.initialize_app(cred)

            print("✅ Firebase inicializado com sucesso")

        return firestore.client()

    except Exception as e:
        print("🔥 ERRO REAL FIREBASE:", repr(e))  # 👈 aqui muda tudo
        return None