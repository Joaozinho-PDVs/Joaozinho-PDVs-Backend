from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_vencimento = models.DateTimeField()
    codigo = models.CharField(max_length=100, unique=True)
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.produto.nome
    