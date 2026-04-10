# core/serializers.py
from rest_framework import serializers
from .models import Produto, Venda, ItemVenda
from django.contrib.auth.models import User

# -------------------- PRODUTO --------------------
class ProdutoSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    nome = serializers.CharField()
    sku = serializers.CharField()
    categoria = serializers.CharField(default="Eletrônicos")
    preco_custo = serializers.FloatField(default=0)
    preco = serializers.FloatField()
    estoque = serializers.IntegerField(default=0)
    status = serializers.BooleanField(default=True)

    def create(self, validated_data):
        produto = Produto(**validated_data)
        produto.salvar()
        return produto

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.salvar()
        return instance


# -------------------- ITEM VENDA --------------------
class ItemVendaSerializer(serializers.Serializer):
    produto = ProdutoSerializer()
    quantidade = serializers.IntegerField()
    preco_unitario = serializers.FloatField(required=False)

    def create(self, validated_data):
        produto_data = validated_data.pop("produto")
        produto = Produto(**produto_data)
        item = ItemVenda(produto=produto, **validated_data)
        return item


# -------------------- VENDA --------------------
class VendaSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    data_venda = serializers.DateTimeField(required=False)
    itens = ItemVendaSerializer(many=True)

    def create(self, validated_data):
        itens_data = validated_data.pop("itens")
        venda = Venda(**validated_data)
        for item_data in itens_data:
            produto_data = item_data.pop("produto")
            produto = Produto(**produto_data)
            item = ItemVenda(produto=produto, **item_data)
            venda.adicionar_item(item)
        venda.salvar()
        return venda


# -------------------- USER --------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user