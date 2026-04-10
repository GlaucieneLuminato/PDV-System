from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProdutoViewSet, VendaViewSet, ItemVendaViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import me, criar_funcionario, dashboard, teste_debug

router = DefaultRouter()
# Rotas dos ViewSets que agora operam com Firestore
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'vendas', VendaViewSet, basename='venda')
router.register(r'itens', ItemVendaViewSet, basename='itemvenda')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Rotas tradicionais
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("me/", me, name="me"),
    path("criar-funcionario/", criar_funcionario, name="criar_funcionario"),
    path("teste/", teste_debug, name="teste"),

    # Inclui todas as rotas do router (API com Firebase)
    path("", include(router.urls)),
]