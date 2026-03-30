from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


@api_view(['POST'])
def criar_funcionario(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = User.objects.create_user(
        username = username,
        password = password,
       
    )
    
    user.is_staff = True
    user.save()
    
    return Response({'msg':'Funcionário criado'})

@api_view(['GET'])
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
        "tipo": tipo
    })
    
    @api_view(["GET"])
    @permission_classes([IsAuthenticated])
    def me(request): 
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser
        })
# Create your views here.
