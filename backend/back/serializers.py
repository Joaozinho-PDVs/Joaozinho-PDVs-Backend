from rest_framework import serializers
from .models import Produto, Venda, ItemVenda

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class ItemVendaSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade', 'valor_unitario', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()

class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True)

    class Meta:
        model = Venda
        fields = ['id', 'data', 'valor_total', 'itens']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        venda = Venda.objects.create()
        total = 0

        for item in itens_data:
            produto = item['produto']
            quantidade = item['quantidade']
            valor_unitario = produto.preco

            if produto.estoque < quantidade:
                raise serializers.ValidationError(f"Estoque insuficiente para o produto: {produto.nome}")

            produto.estoque -= quantidade
            produto.save()

            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=quantidade,
                valor_unitario=valor_unitario
            )

            total += valor_unitario * quantidade

        venda.valor_total = total
        venda.save()
        return venda
