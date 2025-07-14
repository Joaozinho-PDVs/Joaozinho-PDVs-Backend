from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=100, unique=True)
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Venda(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Venda #{self.id}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.valor_unitario
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.venda.valor_total = sum(item.subtotal() for item in self.venda.itens.all())
        self.venda.save()
