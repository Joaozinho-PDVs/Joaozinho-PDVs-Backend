from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from django.db.models import Sum, F
from .models import Produto, Venda
from .serializers import ProdutoSerializer, VendaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all().prefetch_related('itens', 'itens__produto')
    serializer_class = VendaSerializer

    @action(detail=False, methods=['get'], url_path='receita-total')
    def receita_total(self, request):
        vendas = Venda.objects.all()

        inicio = request.query_params.get('inicio')
        fim = request.query_params.get('fim')

        if inicio:
            vendas = vendas.filter(data__gte=inicio)
        if fim:
            vendas = vendas.filter(data__lte=fim)

        total = vendas.aggregate(receita_total=Sum('valor_total'))

        return Response({
            "receita_total": total['receita_total'] or 0.00
        })

    @action(detail=False, methods=['get'], url_path='ultimos-7-dias')
    def ultimos_7_dias(self, request):
        data_limite = now() - timedelta(days=7)
        vendas = self.get_queryset().filter(data__gte=data_limite).order_by('-data')
        serializer = self.get_serializer(vendas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='relatorio-semanal')
    def relatorio_semanal(self, request):
        data_limite = now() - timedelta(days=7)
        relatorio = (
            Venda.objects
            .filter(data__gte=data_limite)
            .values(produto_id=F('itens__produto__id'), produto_nome=F('itens__produto__nome'))
            .annotate(
                quantidade_total=Sum('itens__quantidade'),
                valor_total=Sum(F('itens__quantidade') * F('itens__valor_unitario'))
            )
            .order_by('-valor_total')
        )

        return Response(relatorio)
