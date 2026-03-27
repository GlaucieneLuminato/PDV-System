from django.shortcuts import render
from django.contrib.auth.models import authenticate
from rest_framework.response import Response 
from rest_framework.decorators import api_view

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        return Response ({
            'tipo': user.tipo,
            'username': user.username
        })
    return Response ({'erro': 'Credenciais inválidos'}, status=400)

@api_view(['POST'])
def criar_funcionario(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = Usuario.object.create_user(
        username = username,
        password = password,
        tipo = 'funcionario'
    )
    
    return Response({'msg':'Funcionário criado'})
# Create your views here.
