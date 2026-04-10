from rest_framework import request, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializers import ProdutoSerializer, VendaSerializer, ItemVendaSerializer, UserSerializer
from core.firebase import db
import datetime


# =========================
# PRODUTOS (FIRESTORE)
# =========================
class ProdutoViewSet(viewsets.ViewSet):

    def list(self, request):
        produtos_ref = db.collection("produtos").limit(10).stream()
        produtos = []

        for doc in produtos_ref:
            data = doc.to_dict()
            data["id"] = doc.id
            produtos.append(data)

        return Response(produtos)

    def create(self, request):
        data = request.data

        doc_ref = db.collection("produtos").document()  # cria ID manual
        doc_ref.set(data)  # salva direto

        return Response({
        "message": "Produto criado no Firebase",
        "id": doc_ref.id
    }, status=201)

    def retrieve(self, request, pk=None):
        doc = db.collection("produtos").document(pk).get()

        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return Response(data)

        return Response({"error": "Produto não encontrado"}, status=404)

    def update(self, request, pk=None):
        db.collection("produtos").document(pk).update(request.data)

        return Response({"message": "Produto atualizado"})

    def destroy(self, request, pk=None):
        db.collection("produtos").document(pk).delete()

        return Response({"message": "Produto deletado"})


# =========================
# VENDAS (FIRESTORE)
# =========================
class VendaViewSet(viewsets.ViewSet):

    def list(self, request):
        vendas_ref = db.collection("vendas").stream()
        vendas = []

        for doc in vendas_ref:
            data = doc.to_dict()
            data["id"] = doc.id
            vendas.append(data)

        return Response(vendas)

    def create(self, request):
        data = request.data

        data["data_venda"] = datetime.datetime.now().isoformat()

        doc_ref = db.collection("vendas").add(data)

        return Response({
            "message": "Venda criada",
            "id": doc_ref[1].id
        }, status=201)


# =========================
# ITENS DE VENDA (FIRESTORE)
# =========================
class ItemVendaViewSet(viewsets.ViewSet):

    def list(self, request):
        itens_ref = db.collection("itens_venda").stream()
        itens = []

        for doc in itens_ref:
            data = doc.to_dict()
            data["id"] = doc.id
            itens.append(data)

        return Response(itens)

    def create(self, request):
        data = request.data

        doc_ref = db.collection("itens_venda").add(data)

        return Response({
            "message": "Item criado",
            "id": doc_ref[1].id
        }, status=201)


# =========================
# USERS (continua Django)
# =========================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]