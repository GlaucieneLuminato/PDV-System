from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse

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
        "username": request.user.username,
        "is_staff": request.user.is_staff, 
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







def teste_debug(request):
    return HttpResponse("🔥 DJANGO TÁ RESPONDENDO 🔥")