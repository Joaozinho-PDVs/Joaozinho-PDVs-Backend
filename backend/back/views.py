from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from back.models import Produto, Venda
from django.http import HttpResponse
# Create your views here.
def cadastrar_produto(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        preco = request.POST['preco']
        estoque = request.POST['estoque']
        codigo = request.POST['codigo']
        descricao = request.POST['descricao']
        produto = request.POST['produto']
        produto = produto.save()
        return HttpResponse('Cadastro realizado com sucesso')
    #return HttpResponse('Cadastro não realizado. Utilize o metodo POST')
    return render(request, 'cadastrar_produto.html')

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        nome = request.POST['nome']
        preco = request.POST['preco']
        estoque = request.POST['estoque']
        codigo = request.POST['codigo']
        descricao = request.POST['descricao']
        produto.nome = nome
        produto.preco = preco
        produto.estoque = estoque
        produto.codigo = codigo
        produto.descricao = descricao
        produto.save()
        return HttpResponse('Editado com sucesso')
    #return HttpResponse('Modificação não realizada. Utilize o metodo POST')
    return render(request, 'editar_produto.html', {'produto':produto})

def ler_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    #return HttpResponse({'produto':produto})
    return render(request, 'ler_produto.html', {'produto':produto})

def cadastrar_venda(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade'))
        produto = get_object_or_404(Produto, id=produto_id)
        if produto.estoque >= quantidade:
            Venda.objects.create(produto=produto, quantidade=quantidade)
            produto.estoque -= quantidade
            produto.save()
            return HttpResponse('Venda realizada com sucesso')
        return HttpResponse('Estoque insuficiente')
    return render(request, 'cadastrar_venda.html')