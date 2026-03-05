from rest_framework import viewsets
from .models import Produto, Venda, ItemVenda
from .serializers import ProdutoSerializer, VendaSerializer, ItemVendaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer
    
class ItemVendaViewSet(viewsets.ModelViewSet):
    queryset = ItemVenda.objects.all()
    serializer_class = ItemVendaSerializer