from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

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
        "tipo": tipo
    })