from django .urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProdutoViewSet, VendaViewSet, ItemVendaViewSet
from django.urls import path
from .views_api import dashboard

router = DefaultRouter()
router.register(r'produtos',ProdutoViewSet)
router.register(r'vendas',VendaViewSet)
router.register(r'itens',ItemVendaViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path("dashboard/", dashboard, name="dashboard"), 
]