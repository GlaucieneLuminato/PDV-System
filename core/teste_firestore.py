# core/teste_firestore.py

from .firebase import db

def teste_conexao():
    try:
        doc_ref = db.collection("teste").document("doc_teste")
        
        doc_ref.set({
            "mensagem": "Conexão com Firestore OK!",
        })

        doc = doc_ref.get()

        if doc.exists:
            print("✅ Documento criado e lido com sucesso:", doc.to_dict())
        else:
            print("❌ Documento não encontrado.")

    except Exception as e:
        print("❌ Erro ao conectar com Firestore:", str(e))