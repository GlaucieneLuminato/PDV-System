from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated



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
    return Response({"msg":"ok"})
         
        
# Create your views here.
