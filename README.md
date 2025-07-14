# Joaozinho-PDVs-Backend
Backend para o PDV

## Setup

Execute o script `setup.sh` na raiz do projeto.

## Testes

Para executar os testes, execute o comando `python manage.py test`.

## Resumo das Rotas da API
### Produtos

| Método | Endpoint                              | Query Params                                              | Descrição                                                                          |
| ------ | ------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| GET    | `/api/produtos/`                      | `codigo=...`, `codigo__iexact=...`, `nome__icontains=...` | Lista todos os produtos com filtros. `codigo` é tratado de forma case-insensitive. |
| POST   | `/api/produtos/`                      | `{ nome, preco, estoque, codigo, descricao }`             | Cria um novo produto.                                                              |
| GET    | `/api/produtos/{id}/`                 | —                                                         | Detalha um produto específico.                                                     |
| PATCH  | `/api/produtos/{id}/`                 | `{ campo: valor }`                                        | Atualiza parcialmente um produto.                                                  |
| DELETE | `/api/produtos/{id}/`                 | —                                                         | Deleta um produto.                                                                 |
| GET    | `/api/produtos/produtos-sem-estoque/` | —                                                         | Lista produtos com `estoque = 0`.                                                  |

### ItemVenda

| Método | Endpoint                               | Body / Parâmetros | Descrição                                                  |
| ------ | -------------------------------------- | ----------------- | ---------------------------------------------------------- |
| GET    | `/api/itemvenda/`                      | —                 | Lista todos os itens de venda.                             |
| POST   | `/api/itemvenda/`                      | —                 | (Não utilizado diretamente — via `Venda`).                 |
| GET    | `/api/itemvenda/{id}/`                 | —                 | Detalha um item de venda.                                  |
| PATCH  | `/api/itemvenda/{id}/`                 | `{ quantidade }`  | Atualiza a quantidade de um item de venda. Valida estoque. |
| DELETE | `/api/itemvenda/{id}/`                 | —                 | Remove o item de venda.                                    |
| GET    | `/api/itemvenda/por-venda/{venda_id}/` | —                 | Lista itens associados a uma venda específica.             |

### Vendas

| Método | Endpoint                           | Body / Query Params                  | Descrição                                                                     |
| ------ | ---------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------- |
| GET    | `/api/vendas/`                     | —                                    | Lista todas as vendas.                                                        |
| POST   | `/api/vendas/`                     | `{ itens: [{produto, quantidade}] }` | Cria uma nova venda e debita estoque.                                         |
| GET    | `/api/vendas/{id}/`                | —                                    | Detalha uma venda.                                                            |
| GET    | `/api/vendas/receita-total/`       | `?inicio=YYYY-MM-DD&fim=YYYY-MM-DD`  | Calcula a receita total dentro de um intervalo de datas.                      |
| GET    | `/api/vendas/vendas-7-dias/`       | —                                    | Retorna a contagem de vendas por dia nos últimos 7 dias.                      |
| GET    | `/api/vendas/total-vendas-7-dias/` | —                                    | Lista todas as vendas dos últimos 7 dias.                                     |
| GET    | `/api/vendas/relatorio-semanal/`   | —                                    | Relatório de vendas semanais por produto, incluindo quantidade e valor total. |

