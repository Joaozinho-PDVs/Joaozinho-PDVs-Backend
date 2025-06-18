#Detalhamento de Ações de Cada Estória de Usuário
1. Venda no Caixa

    Modelo: A estória de "Venda no Caixa" interage diretamente com os modelos Produto e Venda. Quando uma venda é realizada, uma nova entrada é criada no modelo Venda, associando um produto específico e a quantidade vendida.

    Serializador: Para criar uma venda, você utiliza o VendaSerializer, que valida e serializa os dados da venda.

    ViewSet: O VendaViewSet gerencia as operações relacionadas às vendas. Ele permite que você faça um POST para criar uma nova venda (registro da transação de venda) e também GET para listar todas as vendas.

    Endpoint: O endpoint relevante para a venda no caixa é /api/vendas/, onde a transação da venda é registrada.

    Ação: Quando uma venda ocorre, o sistema cria uma venda e diminui a quantidade do produto no estoque. Isso é feito ao criar um Venda e ajustar o Produto.estoque.

2. Conferir Receita e Movimento da Loja

    Modelo: A consulta de vendas realizadas interage com o modelo Venda. Ele armazena todas as transações e pode ser utilizado para gerar relatórios de receita.

    Serializador: O VendaSerializer será usado para serializar os dados das vendas quando o usuário quiser ver os detalhes de cada venda, como a quantidade vendida e o preço do produto.

    ViewSet: O VendaViewSet é responsável por fornecer uma listagem das vendas registradas na loja, o que permite ao usuário conferir a receita e o movimento da loja.

    Endpoint: O endpoint relevante é /api/vendas/ (GET), onde todas as vendas podem ser consultadas.

    Ação: O usuário pode fazer uma requisição GET para /api/vendas/ para listar todas as vendas realizadas. O sistema pode calcular a receita total somando os preços dos produtos vendidos e as quantidades associadas.

3. Verificar e Repor Estoque

    Modelo: O modelo Produto contém o campo estoque, que registra a quantidade de unidades de cada produto disponível.

    Serializador: O ProdutoSerializer é utilizado para serializar os dados do produto, incluindo a quantidade de estoque. O usuário pode consultar o estoque e fazer atualizações (reposições) de estoque através desse serializador.

    ViewSet: O ProdutoViewSet gerencia as operações sobre o produto. O método GET permite visualizar o estoque atual, enquanto o PATCH/PUT permite atualizar a quantidade de estoque.

    Endpoint: O endpoint para verificar o estoque é /api/produtos/ (GET) e para atualizar o estoque é o mesmo endpoint usando o método PATCH/PUT.

    Ação: O usuário pode consultar o estoque de produtos usando o método GET (/api/produtos/ ou /api/produtos/{id}/) e atualizar a quantidade de estoque usando PATCH ou PUT.

4. Adicionando Itens ao Estoque

    Modelo: Para adicionar itens ao estoque, o modelo Produto precisa ser atualizado para refletir o novo valor do estoque.

    Serializador: O ProdutoSerializer é utilizado para validar os dados ao atualizar o produto. O campo estoque pode ser atualizado para refletir o aumento na quantidade de unidades de um produto.

    ViewSet: O ProdutoViewSet gerencia as operações sobre os produtos. O método PATCH ou PUT é utilizado para atualizar o estoque de um produto existente.

    Endpoint: O endpoint relevante é /api/produtos/ (POST/PUT/PATCH) para criar ou atualizar um produto com o novo valor de estoque.

    Ação: O sistema usa PATCH ou PUT para aumentar a quantidade de estoque de um produto. O usuário pode adicionar mais unidades de um produto existente através da API.