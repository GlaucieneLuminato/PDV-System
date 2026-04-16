# core/views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from .firebase import get_firestore_db


# ===================== TESTE FIREBASE =====================
@api_view(["GET"])
def teste_firebase(request):
    try:
        db = get_firestore_db()
        if not db:
            return Response({"erro": "Firebase indisponível"}, status=500)

        db.collection("teste").document("1").set({"ok": True})
        return Response({"status": "Firebase OK"})

    except Exception as e:
        return Response({"erro": str(e)})


# ===================== AUTENTICAÇÃO E PERFIL =====================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    if user.is_superuser:
        tipo = "admin"
    elif user.is_staff:
        tipo = "funcionario"
    else:
        tipo = "usuario"

    return Response({
        "username": user.username,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "tipo": tipo
    })


@api_view(['POST'])
def criar_funcionario(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.create_user(
        username=username,
        password=password
    )

    user.is_staff = True
    user.save()

    return Response({"msg": "Funcionário criado com sucesso"})


# ===================== PRODUTOS =====================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_produtos(request):
    try:
        db = get_firestore_db()
        if not db:
            return Response({"erro": "Firebase indisponível"}, status=500)

        produtos_ref = db.collection('produtos')
        produtos_docs = produtos_ref.stream()

        produtos = []
        for doc in produtos_docs:
            p = doc.to_dict()
            p['id'] = doc.id
            produtos.append(p)

        return Response(produtos)

    except Exception as e:
        return Response({"erro": str(e)}, status=500)


@api_view(['POST'])

def criar_produto(request):
    try:
        db = get_firestore_db()
        if not db:
            return Response({"erro": "Firebase indisponível"}, status=500)

        dados = request.data

        produto_ref = db.collection('produtos').document()
        produto_ref.set({
            'nome': dados.get('nome'),
            'sku': dados.get('sku'),
            'categoria': dados.get('categoria', 'Eletrônicos'),
            'preco_custo': float(dados.get('preco_custo', 0)),
            'preco': float(dados.get('preco')),
            'estoque': int(dados.get('estoque', 0)),
            'status': True
        })

        return Response({"msg": "Produto criado com sucesso"})

    except Exception as e:
        return Response({"erro": str(e)}, status=500)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def atualizar_produto(request, produto_id):
    try:
        db = get_firestore_db()
        if not db:
            return Response({"erro": "Firebase indisponível"}, status=500)

        dados = request.data

        produto_ref = db.collection('produtos').document(produto_id)
        produto_ref.update({
            'nome': dados.get('nome'),
            'sku': dados.get('sku'),
            'categoria': dados.get('categoria', 'Eletrônicos'),
            'preco_custo': float(dados.get('preco_custo', 0)),
            'preco': float(dados.get('preco')),
            'estoque': int(dados.get('estoque', 0)),
            'status': dados.get('status', True)
        })

        return Response({"msg": "Produto atualizado com sucesso"})

    except Exception as e:
        return Response({"erro": str(e)}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletar_produto(request, produto_id):
    try:
        db = get_firestore_db()
        if not db:
            return Response({"erro": "Firebase indisponível"}, status=500)

        produto_ref = db.collection('produtos').document(produto_id)
        produto_ref.delete()

        return Response({"msg": "Produto deletado com sucesso"})

    except Exception as e:
        return Response({"erro": str(e)}, status=500)


# ===================== DASHBOARD E TESTES =====================
def dashboard(request):
    return render(request, "dashboard.html")


def teste_debug(request):
    return HttpResponse("🔥 DJANGO TÁ RESPONDENDO 🔥")