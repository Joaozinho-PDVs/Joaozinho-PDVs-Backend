from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, VendaViewSet, ItemVendaViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'vendas', VendaViewSet)
router.register(r'itemvenda', ItemVendaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
