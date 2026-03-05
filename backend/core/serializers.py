from rest_framework import serializers
from .models import Produto, Venda, ItemVenda
 
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"
        
class ItemVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVenda
        fields = "__all__"
        
class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venda
        fields = "__all__" 