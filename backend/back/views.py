from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now, timedelta
from django.db.models import Sum, F, Count, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncDate
from .models import Produto, Venda, ItemVenda
from .serializers import ProdutoSerializer, VendaSerializer, ItemVendaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'nome': ['icontains'],
        'codigo': ['exact', 'iexact'],
    }

    def get_queryset(self):
        queryset = Produto.objects.all()
        codigo = self.request.query_params.get('codigo')
        if codigo:
            queryset = queryset.filter(codigo__iexact=codigo)
        return queryset

    @action(detail=False, methods=['get'], url_path='produtos-sem-estoque')
    def produtos_sem_estoque(self, request):
        produtos = Produto.objects.filter(estoque=0)
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)
    
    

class ItemVendaViewSet(viewsets.ModelViewSet):
    queryset = ItemVenda.objects.select_related('venda', 'produto')
    serializer_class = ItemVendaSerializer

    @action(detail=False, methods=['get'], url_path='por-venda/(?P<venda_id>[^/.]+)')
    def por_venda(self, request, venda_id=None):
        itens = self.get_queryset().filter(venda__id=venda_id)
        serializer = self.get_serializer(itens, many=True)
        return Response(serializer.data)

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

    @action(detail=False, methods=['get'], url_path='vendas-7-dias')
    def vendas_7_dias(self, request):
        data_limite = now() - timedelta(days=7)
        quantidade_vendas_por_dia = (
            self.get_queryset()
            .filter(data__gte=data_limite)
            .annotate(dia=TruncDate('data'))
            .values('dia')
            .annotate(quantidade=Count('id'))
            .order_by('dia')
        )
        return Response(quantidade_vendas_por_dia)

    @action(detail=False, methods=['get'], url_path='total-vendas-7-dias')
    def total_vendas_7_dias(self, request):
        data_limite = now() - timedelta(days=7)
        vendas = self.get_queryset().filter(data__gte=data_limite).order_by('-data')
        serializer = self.get_serializer(vendas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='relatorio-semanal')
    def relatorio_semanal(self, request):
        data_limite = now() - timedelta(days=7)

        subtotal_expr = ExpressionWrapper(
            F('itens__quantidade') * F('itens__valor_unitario'),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        )

        relatorio = (
            Venda.objects
            .filter(data__gte=data_limite)
            .values(produto_id=F('itens__produto__id'), produto_nome=F('itens__produto__nome'))
            .annotate(
                quantidade_total=Sum('itens__quantidade'),
                valor_total=Sum(subtotal_expr)
            )
            .order_by('-valor_total')
        )

        return Response(relatorio)
