from rest_framework import serializers
from .models import Produto, Venda, ItemVenda

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
    
    def validate_preco(self, value):
        if value < 0:
            raise serializers.ValidationError("Preco negativo")
        return value
    
    def validate_estoque(self, value):
        if value < 0:
            raise serializers.ValidationError("Estoque negativo")
        return value
    
    def validate_codigo(self, value):
        produto_id = self.instance.id if self.instance else None
        if Produto.objects.filter(codigo__iexact=value).exclude(id=produto_id).exists():
            raise serializers.ValidationError("Código já existe")
        return value

class ItemVendaSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ItemVenda
        fields = ['id', 'produto', 'quantidade', 'valor_unitario', 'subtotal']
        read_only_fields = ['subtotal', 'valor_unitario']
    def get_subtotal(self, obj):
        return obj.quantidade * obj.valor_unitario

    def update(self, instance, validated_data):
        nova_quantidade = validated_data.get('quantidade', instance.quantidade)

        if nova_quantidade < 0:
            raise serializers.ValidationError("Quantidade negativa")

        produto = validated_data.get('produto', instance.produto)
        diferenca = nova_quantidade - instance.quantidade
        estoque_disponivel = produto.estoque - diferenca

        if diferenca > 0 and estoque_disponivel < diferenca:
            raise serializers.ValidationError(f"Estoque insuficiente para o produto: {produto.nome}")
        
        produto.estoque -= diferenca
        produto.save()

        instance.quantidade = nova_quantidade
        instance.produto = produto
        instance.save()

        return instance

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
