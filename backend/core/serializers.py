from rest_framework import serializers
from .models import Produto, Venda, ItemVenda
from django.contrib.auth.models import User
from rest_framework import serializers
 
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
        fields = ["id","data_venda","itens"]
        
        def create(self,validated_data):
            itens_data = validated_data.pop("itens")
            venda = Venda.objects.create(venda=venda, **validated_data)
            
            for item_data in itens_data:
                ItemVenda.objects.create(venda=venda, **item_data)
                
                return venda 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
        def create(self, validated_data):
            user = User.object.create_user(**validated_data)
            return user