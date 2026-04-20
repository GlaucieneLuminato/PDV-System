from dotenv import load_dotenv
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()


def get_firestore_db():
    try:
        # Evita reinicializar o Firebase várias vezes
        if not firebase_admin._apps:
            cred_json = os.getenv("FIREBASE_CREDENTIALS")

            if not cred_json:
                raise Exception("FIREBASE_CREDENTIALS não encontrado no ambiente")

            # 🔥 Corrige problema de quebra de linha
            cred_json = cred_json.replace('\\n', '\n')

            cred_dict = json.loads(cred_json)

            cred = credentials.Certificate(cred_dict)

            firebase_admin.initialize_app(cred)

        return firestore.client()

    except Exception as e:
        print("🔥 ERRO FIREBASE:", str(e))
        return None