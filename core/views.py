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
        return Response({"erro": str(e)}, status=500)


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


# 🔒 PROTEGIDO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_funcionario(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"erro": "Username e senha são obrigatórios"}, status=400)

        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.is_staff = True
        user.save()

        return Response({"msg": "Funcionário criado com sucesso"})

    except Exception as e:
        return Response({"erro": str(e)}, status=500)


# ===================== DASHBOARD E TESTES =====================
def dashboard(request):
    return render(request, "dashboard.html")


def teste_debug(request):
    return HttpResponse("🔥 DJANGO TÁ RESPONDENDO 🔥")