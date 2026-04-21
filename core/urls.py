from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProdutoViewSet, VendaViewSet, ItemVendaViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import me, criar_funcionario, dashboard, teste_debug, teste_firebase

# Router (API REST)
router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'vendas', VendaViewSet, basename='venda')
router.register(r'itens', ItemVendaViewSet, basename='itemvenda')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # 🔐 AUTENTICAÇÃO
   
    path("me/", me, name="me"),

    # 🧪 TESTES
    path("teste/", teste_debug, name="teste"),
    path("teste-firebase/", teste_firebase, name="teste_firebase"),

    # 👨‍💼 FUNCIONÁRIOS
    path("criar-funcionario/", criar_funcionario, name="criar_funcionario"),

 

    # 📊 FRONT (HTML)
    path("dashboard/", dashboard, name="dashboard"),

    # 🔥 API REST (ViewSets)
    path("", include(router.urls)),
]