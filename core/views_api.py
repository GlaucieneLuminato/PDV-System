from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer
from core.firebase import get_firestore_db
import datetime


# =========================
# PRODUTOS (FIRESTORE)
# =========================
class ProdutoViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            db = get_firestore_db()
            if not db:
                return Response({"erro": "Firebase indisponível"}, status=500)

            import time
            start = time.time()

            docs = db.collection("produtos").limit(5).stream()

            tempo = time.time() - start

            produtos = []
            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                produtos.append(data)

            return Response({
                "tempo": tempo,
                "dados": produtos
            })

        except Exception as e:
            return Response({"erro": str(e)}, status=500)


    def retrieve(self, request, pk=None):
        try:
            db = get_firestore_db()
            if not db:
                return Response({"erro": "Firebase indisponível"}, status=500)

            doc = db.collection("produtos").document(pk).get()

            if doc.exists:
                data = doc.to_dict()
                data["id"] = doc.id
                return Response(data)

            return Response({"error": "Produto não encontrado"}, status=404)

        except Exception as e:
            return Response({"erro": str(e)}, status=500)


    def update(self, request, pk=None):
        try:
            db = get_firestore_db()
            if not db:
                return Response({"erro": "Firebase indisponível"}, status=500)

            db.collection("produtos").document(pk).update(request.data)
            return Response({"message": "Produto atualizado"})

        except Exception as e:
            return Response({"erro": str(e)}, status=500)


    def destroy(self, request, pk=None):
        try:
            db = get_firestore_db()
            if not db:
                return Response({"erro": "Firebase indisponível"}, status=500)

            db.collection("produtos").document(pk).delete()
            return Response({"message": "Produto deletado"})

        except Exception as e:
            return Response({"erro": str(e)}, status=500)


# =========================
# VENDAS (FIRESTORE)
# =========================
class VendaViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            db = get_firestore_db()
            if not db:
                return Response({"erro": "Firebase indisponível"}, status=500)

            docs = db.collection("vendas").limit(20).stream()
            vendas = []

            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                vendas.append(data)

            return Response(vendas)

        except Exception as e:
            return Response({"erro": str(e)}, status=500)


    def create(self, request):
        try:
            db = get_firestore_db()
            if not db:
                return Response({"erro": "Firebase indisponível"}, status=500)

            data = request.data
            data["data_venda"] = datetime.datetime.now().isoformat()

            doc_ref = db.collection("vendas").document()
            doc_ref.set(data)

            return Response({
                "message": "Venda criada",
                "id": doc_ref.id
            }, status=201)

        except Exception as e:
            return Response({"erro": str(e)}, status=500)


# =========================
# ITENS DE VENDA (FIRESTORE)
# =========================
class ItemVendaViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            db = get_firestore_db()
            if not db:
                return Response({"erro": "Firebase indisponível"}, status=500)

            docs = db.collection("itens_venda").limit(20).stream()
            itens = []

            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                itens.append(data)

            return Response(itens)

        except Exception as e:
            return Response({"erro": str(e)}, status=500)


    def create(self, request):
        try:
            db = get_firestore_db()
            if not db:
                return Response({"erro": "Firebase indisponível"}, status=500)

            data = request.data

            doc_ref = db.collection("itens_venda").document()
            doc_ref.set(data)

            return Response({
                "message": "Item criado",
                "id": doc_ref.id
            }, status=201)

        except Exception as e:
            return Response({"erro": str(e)}, status=500)


# =========================
# USERS (Django)
# =========================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]