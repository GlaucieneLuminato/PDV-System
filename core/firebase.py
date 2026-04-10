# core/firebase.py
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Caminho da chave JSON do Firebase (você vai colocar dentro da pasta core/firebase)
cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
cred = credentials.Certificate(cred_path)

# Inicializa o Firebase
firebase_admin.initialize_app(cred)

# Cria o cliente para o Firestore
db = firestore.client()