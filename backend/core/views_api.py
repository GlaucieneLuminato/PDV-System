from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.db.models import Sum 
from django.utils import timezone
from .models import Produto, Venda, ItemVenda
from .serializers import ProdutoSerializer, VendaSerializer, ItemVendaSerializer

@api_view(["GET"])
def dashboard(request):
    hoje = timezone.now().date()
    
    vendas_hoje = Venda.objects.filter(data_venda__date=hoje).count()
    
    itens_vendidos = ItemVenda.objects.filter(
        venda__data_venda__date=hoje
    ).aggregate(total=Sum("quantidade"))["total"] or 0
    
    total_vendido = ItemVenda.objects.filter(
        venda__data_venda__date=hoje
    ).aggregate(total=Sum("preco_unitario"))["total"] or 0
    
    return Response({
        "vendas_hoje": vendas_hoje,
        "itens_vendidos": itens_vendidos,
        "total_vendido": total_vendido
    })

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.filter(status=True)
    serializer_class = ProdutoSerializer
    
class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all().order_by("-data_venda")
    serializer_class = VendaSerializer
    
class ItemVendaViewSet(viewsets.ModelViewSet):
    queryset = ItemVenda.objects.all()
    serializer_class = ItemVendaSerializer