from django .urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProdutoViewSet, VendaViewSet, ItemVendaViewSet

router = DefaultRouter()
router.register(r'produtos',ProdutoViewSet)
router.register(r'vendas',VendaViewSet)
router.register(r'itens',ItemVendaViewSet)

urlpatterns = [
    path('',include(router.urls)),
]