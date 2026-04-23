from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProdutoViewSet, VendaViewSet, ItemVendaViewSet, UserViewSet
from .views import me, criar_funcionario, teste_debug, teste_firebase

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'vendas', VendaViewSet, basename='venda')
router.register(r'itens', ItemVendaViewSet, basename='itemvenda')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # 🔐 USUÁRIO
    path("me/", me),

    # 👨‍💼 FUNCIONÁRIOS
    path("criar-funcionario/", criar_funcionario),

    # 🧪 TESTES
    path("teste/", teste_debug),
    path("teste-firebase/", teste_firebase),

    # 🔥 VIEWSETS
    path("", include(router.urls)),
]