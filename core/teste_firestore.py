# core/teste_firestore.py
from .firebase import db
from core.teste_firestore import teste_conexao
teste_conexao()

def teste_conexao():
    try:
        # Vamos criar um documento de teste na coleção "teste"
        doc_ref = db.collection("teste").document("doc_teste")
        doc_ref.set({
            "mensagem": "Conexão com Firestore OK!",
        })
        
        # Ler o documento de volta
        doc = doc_ref.get()
        if doc.exists:
            print("✅ Documento criado e lido com sucesso:", doc.to_dict())
        else:
            print("❌ Documento não encontrado.")
    except Exception as e:
        print("❌ Erro ao conectar com Firestore:", e)

if __name__ == "__main__":
    teste_conexao()