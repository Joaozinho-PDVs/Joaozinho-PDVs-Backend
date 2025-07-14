from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Produto, Venda, ItemVenda

class APITestSuite(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.produto = Produto.objects.create(
            nome="Mouse",
            preco=50.00,
            estoque=10,
            codigo="mouse-001",
            descricao="Mouse sem fio"
        )
        self.produto2 = Produto.objects.create(
            nome="Teclado",
            preco=100.00,
            estoque=5,
            codigo="teclado-001",
            descricao="Teclado mecânico"
        )
        self.produto3 = Produto.objects.create(
            nome="Teclado", preco=150, estoque=10, codigo="TEC123", descricao="Teclado mecânico"
        )
        self.produto4 = Produto.objects.create(
            nome="Mouse", preco=50, estoque=5, codigo="MOU456", descricao="Mouse ótico"
        )

    def test_criar_produto(self):
        url = reverse('produto-list')
        data = {
            "nome": "Monitor",
            "preco": 600.00,
            "estoque": 15,
            "codigo": "monitor-001",
            "descricao": "Monitor LED 24"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listar_produtos(self):
        response = self.client.get(reverse('produto-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filtrar_por_nome(self):
        url = reverse('produto-list') + '?nome__icontains=mouse'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_produto(self):
        url = reverse('produto-detail', args=[self.produto.id])
        response = self.client.patch(url, {"estoque": 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque, 20)

    def test_deletar_produto(self):
        url = reverse('produto-detail', args=[self.produto.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_criar_venda(self):
        url = reverse('venda-list')
        data = {
            "itens": [
                {"produto": self.produto.id, "quantidade": 2}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["valor_total"], "100.00")

    def test_listar_vendas(self):
        self.test_criar_venda()
        response = self.client.get(reverse('venda-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receita_total(self):
        self.test_criar_venda()
        response = self.client.get(reverse('venda-receita-total'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("receita_total", response.data)

    def test_vendas_7_dias(self):
        self.test_criar_venda()
        response = self.client.get(reverse('venda-vendas-7-dias'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_relatorio_semanal(self):
        self.test_criar_venda()
        response = self.client.get(reverse('venda-relatorio-semanal'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_criar_e_atualizar_itemvenda(self):
        self.test_criar_venda()
        item = ItemVenda.objects.first()
        url = reverse('itemvenda-detail', args=[item.id])
        response = self.client.patch(url, {"quantidade": 4}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 4)

    def test_deletar_itemvenda(self):
        self.test_criar_venda()
        item = ItemVenda.objects.first()
        url = reverse('itemvenda-detail', args=[item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_venda_com_estoque_insuficiente(self):
        url = reverse('venda-list')
        data = {
            "itens": [
                {"produto": self.produto.id, "quantidade": 999}  # maior que o estoque
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Estoque insuficiente", str(response.data))

    def test_criar_venda_com_produto_inexistente(self):
        url = reverse('venda-list')
        data = {
            "itens": [
                {"produto": 9999, "quantidade": 1}  # ID inexistente
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_itemvenda_invalido(self):
        self.test_criar_venda()
        item = ItemVenda.objects.first()
        url = reverse('itemvenda-detail', args=[item.id])
        response = self.client.patch(url, {"quantidade": -5}, format='json')  # Quantidade negativa
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_produto_inexistente(self):
        url = reverse('produto-detail', args=[9999])  # ID inexistente
        response = self.client.patch(url, {"estoque": 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_produto_inexistente(self):
        url = reverse('produto-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deletar_itemvenda_inexistente(self):
        url = reverse('itemvenda-detail', args=[9999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_venda_com_item_sem_produto(self):
        url = reverse('venda-list')
        data = {
            "itens": [
                {"quantidade": 1}  # Produto omitido
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_criar_produto_invalido(self):
        data = {"nome": "", "preco": -10, "estoque": -5, "codigo": "", "descricao": ""}
        response = self.client.post('/api/produtos/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtrar_produtos_por_codigo(self):
        response = self.client.get('/api/produtos/?codigo=TEC123')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['codigo'], "TEC123")

    def test_venda_com_produto_inexistente(self):
        data = {
            "itens": [
                {"produto": 999, "quantidade": 1}
            ]
        }
        response = self.client.post('/api/vendas/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_criar_venda_com_estoque_exato(self):
        data = {
            "itens": [
                {"produto": self.produto4.id, "quantidade": 5}
            ]
        }
        response = self.client.post('/api/vendas/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.produto4.refresh_from_db()
        self.assertEqual(self.produto4.estoque, 0)

    def test_itemvenda_subtotal_calculado(self):
        venda = Venda.objects.create()
        item = ItemVenda.objects.create(
            venda=venda, produto=self.produto3, quantidade=3, valor_unitario=150
        )
        self.assertEqual(item.subtotal(), 450)

    def test_patch_produto_valido(self):
        response = self.client.patch(f'/api/produtos/{self.produto3.id}/', {"estoque": 99})
        self.assertEqual(response.status_code, 200)
        self.produto3.refresh_from_db()
        self.assertEqual(self.produto3.estoque, 99)

    def test_endpoint_produtos_sem_estoque(self):
        self.produto4.estoque = 0
        self.produto4.save()
        response = self.client.get('/api/produtos/produtos-sem-estoque/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], self.produto4.id)

    def test_receita_total_periodo_vazia(self):
        response = self.client.get('/api/vendas/receita-total/?inicio=2022-01-01&fim=2022-01-02')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['receita_total'], 0.00)

    def test_produto_search_case_insensitive(self):
        response = self.client.get('/api/produtos/?codigo__iexact=tec123')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['codigo'], "TEC123")

    def test_venda_total_vendas_7_dias(self):
        self.test_criar_venda()
        response = self.client.get('/api/vendas/total-vendas-7-dias/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_relatorio_semanal_ordenado(self):
        self.test_criar_venda()
        response = self.client.get('/api/vendas/relatorio-semanal/')
        self.assertEqual(response.status_code, 200)
        valores = [float(v["valor_total"]) for v in response.data]
        self.assertEqual(valores, sorted(valores, reverse=True))

    def test_filtro_produto_por_codigo_inexistente(self):
        response = self.client.get('/api/produtos/?codigo=invalido999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_listar_itemvenda_por_venda(self):
        self.test_criar_venda()
        venda_id = Venda.objects.first().id
        response = self.client.get(f'/api/itemvenda/por-venda/{venda_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
    def test_criar_produto_com_codigo_repetido(self):
        data = {
            "nome": "Mouse Gamer",
            "preco": 70,
            "estoque": 5,
            "codigo": "mouse-001",  # já existe
            "descricao": "Mouse com RGB"
        }
        response = self.client.post(reverse('produto-list'), data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_criar_produto_sem_nome(self):
        data = {
            "nome": "",
            "preco": 50,
            "estoque": 10,
            "codigo": "novo001",
            "descricao": "Sem nome"
        }
        response = self.client.post(reverse('produto-list'), data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_listar_produto_vazio(self):
        Produto.objects.all().delete()
        response = self.client.get(reverse('produto-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_filtro_por_nome_inexistente(self):
        response = self.client.get(reverse('produto-list') + '?nome__icontains=xxxxxxx')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_patch_codigo_produto(self):
        url = reverse('produto-detail', args=[self.produto.id])
        response = self.client.patch(url, {"codigo": "novo-codigo"})
        self.assertEqual(response.status_code, 200)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.codigo, "novo-codigo")

    def test_patch_nome_produto(self):
        url = reverse('produto-detail', args=[self.produto.id])
        response = self.client.patch(url, {"nome": "Novo Nome"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["nome"], "Novo Nome")

    def test_patch_preco_produto(self):
        url = reverse('produto-detail', args=[self.produto.id])
        response = self.client.patch(url, {"preco": 123.45})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["preco"], "123.45")

    def test_patch_descricao_produto(self):
        url = reverse('produto-detail', args=[self.produto.id])
        response = self.client.patch(url, {"descricao": "Nova descrição"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nova descrição", response.data["descricao"])

    def test_listar_produtos_ordenados_nome(self):
        response = self.client.get(reverse('produto-list') + '?ordering=nome')
        self.assertEqual(response.status_code, 200)

    def test_filtrar_codigo_case_sensitive(self):
        response = self.client.get(reverse('produto-list') + '?codigo=MOU456')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['codigo'], "MOU456")

    def test_buscar_produto_por_id(self):
        url = reverse('produto-detail', args=[self.produto2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.produto2.id)

    def test_atualizar_produto_inteiro(self):
        url = reverse('produto-detail', args=[self.produto2.id])
        data = {
            "nome": "Produto Atualizado",
            "preco": 199.99,
            "estoque": 25,
            "codigo": "atualizado-001",
            "descricao": "Produto atualizado totalmente"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["codigo"], "atualizado-001")

    def test_atualizar_produto_preco_negativo(self):
        url = reverse('produto-detail', args=[self.produto2.id])
        response = self.client.patch(url, {"preco": -1})
        self.assertEqual(response.status_code, 400)

    def test_atualizar_produto_estoque_negativo(self):
        url = reverse('produto-detail', args=[self.produto2.id])
        response = self.client.patch(url, {"estoque": -5})
        self.assertEqual(response.status_code, 400)

    def test_atualizar_produto_nome_vazio(self):
        url = reverse('produto-detail', args=[self.produto2.id])
        response = self.client.patch(url, {"nome": ""})
        self.assertEqual(response.status_code, 400)

    def test_filtrar_produtos_por_codigo_parcial(self):
        response = self.client.get('/api/produtos/?codigo__icontains=TEC')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_produto_descricao_max_length(self):
        long_desc = "x" * 501  # excedendo limite
        response = self.client.post(reverse('produto-list'), {
            "nome": "Desc Test",
            "preco": 10,
            "estoque": 1,
            "codigo": "desc-001",
            "descricao": long_desc
        })
        self.assertEqual(response.status_code, 400)

    def test_criar_produto_limite_min_estoque_zero(self):
        response = self.client.post(reverse('produto-list'), {
            "nome": "Zero Estoque",
            "preco": 30,
            "estoque": 0,
            "codigo": "zero-001",
            "descricao": "Estoque inicial zero"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_produto_codigo_unico_case_insensitive(self):
        response = self.client.post(reverse('produto-list'), {
            "nome": "Novo Produto",
            "preco": 25,
            "estoque": 10,
            "codigo": "tec123",  # já existe em maiúsculo
            "descricao": "Código já usado"
        }, format='json')
        self.assertEqual(response.status_code, 400)
